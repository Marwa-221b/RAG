# streamlit_app.py
import streamlit as st
import requests
import json
import os
from datetime import datetime

# Configuration
API_URL = "http://127.0.0.1:8001"

# Page configuration
st.set_page_config(
    page_title="Askara",
    page_icon="/home/marwaahmed/rag-project/RAG/GUI/logo_rag.png",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 1rem;
        background: linear-gradient(135deg, #D35400 0%, #E67E22 100%);
        border-radius: 10px;
        margin-bottom: 2rem;
        color: white;
        box-shadow: 0 4px 15px rgba(211, 84, 0, 0.3);
    }
    .success-box {
        background-color: #fef5e7;
        padding: 1rem;
        border-radius: 5px;
        border-left: 5px solid #E67E22;
        margin: 1rem 0;
    }
    .info-box {
        background-color: #fdf2e9;
        padding: 1rem;
        border-radius: 5px;
        border-left: 5px solid #D35400;
        margin: 1rem 0;
    }
    .warning-box {
        background-color: #fae5d3;
        padding: 1rem;
        border-radius: 5px;
        border-left: 5px solid #A04000;
        margin: 1rem 0;
    }
    .stButton > button {
        background-color: #E67E22;
        color: white;
    }
    .stButton > button:hover {
        background-color: #D35400;
    }
    [data-testid="stMetricValue"] {
        color: #E67E22;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Session state initialization
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'token' not in st.session_state:
    st.session_state.token = None
if 'username' not in st.session_state:
    st.session_state.username = None
if 'page' not in st.session_state:
    st.session_state.page = "Login"
if 'system_config' not in st.session_state:
    st.session_state.system_config = None

# ==================== API HELPER FUNCTIONS ====================

def register_user(username, email, password):
    try:
        response = requests.post(
            f"{API_URL}/auth/register",
            json={"username": username, "email": email, "password": password}
        )
        if response.status_code == 200:
            return True, response.json().get("message", "User created successfully")
        else:
            return False, response.json().get("detail", "Registration failed")
    except Exception as e:
        return False, f"Connection error: {str(e)}"

def login_user(username, password):
    try:
        response = requests.post(
            f"{API_URL}/auth/login",
            data={"username": username, "password": password}
        )
        if response.status_code == 200:
            token = response.json()["access_token"]
            return True, token
        else:
            return False, response.json().get("detail", "Login failed")
    except Exception as e:
        return False, f"Connection error: {str(e)}"

def get_config(token):
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{API_URL}/config", headers=headers)
        if response.status_code == 200:
            return True, response.json()
        else:
            return False, response.json().get("detail", "Failed to get config")
    except Exception as e:
        return False, f"Connection error: {str(e)}"

def update_config(token, updates):
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.put(f"{API_URL}/config", json=updates, headers=headers)
        if response.status_code == 200:
            return True, response.json()
        else:
            return False, response.json().get("detail", "Failed to update config")
    except Exception as e:
        return False, f"Connection error: {str(e)}"

def query_documents(question, token):
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.post(
            f"{API_URL}/query",
            json={"query": question},
            headers=headers
        )
        if response.status_code == 200:
            return True, response.json()
        else:
            return False, response.json().get("detail", "Query failed")
    except Exception as e:
        return False, f"Connection error: {str(e)}"

def ingest_documents(folder_path, token):
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.post(
            f"{API_URL}/ingest",
            json={"folder_path": folder_path},
            headers=headers
        )
        if response.status_code == 200:
            return True, response.json()
        else:
            return False, response.json().get("detail", "Ingestion failed")
    except Exception as e:
        return False, f"Connection error: {str(e)}"

def get_health():
    try:
        response = requests.get(f"{API_URL}/health/live")
        if response.status_code == 200:
            return True, response.json()
        return False, "Health check failed"
    except Exception as e:
        return False, str(e)

def get_metrics(token):
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{API_URL}/metrics", headers=headers)
        if response.status_code == 200:
            return True, response.json()
        return False, "Failed to get metrics"
    except Exception as e:
        return False, str(e)

def get_documents_list(folder_path):
    try:
        if not os.path.exists(folder_path):
            return False, f"Folder not found: {folder_path}"
        
        files = []
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            if os.path.isfile(file_path):
                file_stat = os.stat(file_path)
                files.append({
                    "filename": filename,
                    "file_type": filename.split('.')[-1] if '.' in filename else 'unknown',
                    "size_bytes": file_stat.st_size,
                    "size_kb": round(file_stat.st_size / 1024, 2),
                    "size_mb": round(file_stat.st_size / (1024 * 1024), 2),
                })
        files.sort(key=lambda x: x['filename'])
        return True, files
    except Exception as e:
        return False, str(e)

def delete_file(file_path):
    try:
        os.remove(file_path)
        return True, "File deleted successfully"
    except Exception as e:
        return False, f"Error deleting file: {str(e)}"

# ==================== UI PAGES ====================

def login_page():
    st.markdown('<div class="main-header"><h1>🔐 Welcome to RAG System</h1><p>Document Q&A System</p></div>', unsafe_allow_html=True)
    
    # Show health status
    health_ok, health_info = get_health()
    if health_ok:
        st.success(f"✅ API Status: {health_info.get('status', 'healthy')}")
    else:
        st.error("❌ API is not responding. Make sure the server is running.")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("### Login")
        
        username = st.text_input("Username", key="login_username")
        password = st.text_input("Password", type="password", key="login_password")
        
        col_login, col_register = st.columns(2)
        
        with col_login:
            if st.button("🔑 Login", use_container_width=True):
                if username and password:
                    with st.spinner("Logging in..."):
                        success, result = login_user(username, password)
                        if success:
                            st.session_state.authenticated = True
                            st.session_state.token = result
                            st.session_state.username = username
                            # Load config after login
                            config_success, config_data = get_config(result)
                            if config_success:
                                st.session_state.system_config = config_data.get('config', {})
                            st.success(f"Welcome back, {username}!")
                            st.rerun()
                        else:
                            st.error(f"Login failed: {result}")
                else:
                    st.warning("Please enter username and password")
        
        with col_register:
            if st.button("📝 Create Account", use_container_width=True):
                st.session_state.page = "Register"
                st.rerun()

def register_page():
    st.markdown('<div class="main-header"><h1>📝 Create New Account</h1></div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("### Registration Form")
        
        username = st.text_input("Username", key="reg_username")
        email = st.text_input("Email", key="reg_email")
        password = st.text_input("Password", type="password", key="reg_password")
        confirm_password = st.text_input("Confirm Password", type="password", key="reg_confirm")
        
        if st.button("📝 Register", use_container_width=True):
            if not username or not email or not password:
                st.warning("Please fill all fields")
            elif password != confirm_password:
                st.error("Passwords do not match")
            elif len(password) < 4:
                st.error("Password must be at least 4 characters")
            else:
                with st.spinner("Creating account..."):
                    success, message = register_user(username, email, password)
                    if success:
                        st.success("✅ Account created successfully!")
                        st.info("Please login with your credentials")
                    #     if st.button("Go to Login"):
                    #         st.session_state.page = "Login"
                    #         st.rerun()
                    # else:
                    #     st.error(f"Registration failed: {message}")
        
        if st.button("← Back to Login", use_container_width=True):
            st.session_state.page = "Login"
            st.rerun()

def main_app():
    """Main application after login"""
    
    # Sidebar
    with st.sidebar:
        st.markdown(f"### 👋 Welcome, **{st.session_state.username}**!")
        
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.authenticated = False
            st.session_state.token = None
            st.session_state.username = None
            st.session_state.system_config = None
            st.rerun()
        
        st.divider()
        
        # Navigation
        st.markdown("### 📍 Navigation")
        selected = st.radio(
            "Choose Action",
            options=["📄 Ingest Documents", "💬 Ask Query", "📚 Document Library", "⚙️ Configuration", "📊 Metrics"],
            index=0
        )
        
        st.divider()
        
        # System Info
        st.markdown("### ℹ️ System Info")
        if st.session_state.system_config:
            st.info(
                f"**API:** {API_URL}\n\n"
                f"**User:** {st.session_state.username}\n\n"
                f"**Chunk Size:** {st.session_state.system_config.get('chunk_size', 'N/A')}\n\n"
                f"**Top K:** {st.session_state.system_config.get('top_k', 'N/A')}\n\n"
                f"**LLM:** {st.session_state.system_config.get('llm_model', 'N/A')}"
            )
    
    # Main content
    if "Ingest" in selected:
        ingest_page()
    elif "Ask" in selected:
        query_page()
    elif "Library" in selected:
        library_page()
    elif "Configuration" in selected:
        config_page()
    else:
        metrics_page()

def ingest_page():
    st.markdown('<div class="main-header"><h1>📥 Ingest Documents</h1></div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### 📂 Document Source")
        default_path = "/home/marwaahmed/rag-project/RAG/data/orgin_doc"
        folder_path = st.text_input("Folder Path", value=default_path)
        
        st.markdown("#### Supported Formats:")
        st.caption("📄 PDF | 📝 TXT | 📰 DOCX | 🌐 HTML")
        
        if st.button("🚀 Start Ingestion", type="primary", use_container_width=True):
            if folder_path:
                with st.spinner("Processing documents..."):
                    success, result = ingest_documents(folder_path, st.session_state.token)
                    if success:
                        st.success(f"✅ Ingestion Successful! Processed {result.get('total_processed', 0)} documents")
                        
                        # Display results
                        st.markdown("### 📊 Results")
                        st.metric("Total Processed", result.get('total_processed', 0))
                        
                        if result.get('documents'):
                            st.markdown("### 📄 Processed Documents")
                            for doc in result['documents'][:5]:
                                st.write(f"- {doc.get('metadata', {}).get('source', 'Unknown')}")
                    else:
                        st.error(f"Ingestion failed: {result}")
            else:
                st.warning("Please enter a folder path")
    
    with col2:
        st.markdown("### 💡 Tips")
        st.info("""
        **Best Practices:**
        - Use the default folder path
        - Supported: PDF, TXT, DOCX, HTML
        - Arabic text is automatically processed
        - Adjust chunking in Configuration page
        """)

def query_page():
    st.markdown('<div class="main-header"><h1>💬 Ask Questions</h1></div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col2:
        st.markdown("### ⚙️ Settings")
        top_k = st.slider("Top K (sources to retrieve)", 1, 10, 
                          st.session_state.system_config.get('top_k', 5))
        
        st.markdown("### 💡 Examples")
        examples = ["What is RAG?", "Summarize the project objectives", "What are the main challenges?"]
        for ex in examples:
            if st.button(f"🔍 {ex}", use_container_width=True):
                st.session_state.example_query = ex
                st.rerun()
    
    with col1:
        st.markdown("### 📝 Your Question")
        default_query = st.session_state.get('example_query', '')
        question = st.text_area("Enter your question:", value=default_query, height=150)
        
        if 'example_query' in st.session_state:
            del st.session_state.example_query
        
        if st.button("🔍 Get Answer", type="primary", use_container_width=True):
            if question:
                with st.spinner("🤔 Thinking..."):
                    success, result = query_documents(question, st.session_state.token)
                    if success:
                        st.markdown("### ✨ Answer")
                        st.success(result.get("answer", "No answer generated"))
                        
                        if result.get('sources'):
                            st.markdown("### 📚 Sources")
                            for source in result['sources']:
                                if isinstance(source, dict):
                                    st.write(f"- {source.get('metadata', {}).get('source', 'Unknown')}")
                    else:
                        st.error(f"Query failed: {result}")
            else:
                st.warning("Please enter a question")

def library_page():
    st.markdown('<div class="main-header"><h1>📚 Document Library</h1></div>', unsafe_allow_html=True)
    
    default_path = "/home/marwaahmed/rag-project/RAG/data/orgin_doc"
    folder_path = st.text_input("📁 Data Folder Path", value=default_path)
    
    col1, col2 = st.columns([1, 4])
    with col1:
        refresh = st.button("🔄 Refresh", use_container_width=True)
    
    if refresh or 'cached_files' not in st.session_state:
        with st.spinner("Loading..."):
            success, files = get_documents_list(folder_path)
            if success:
                st.session_state.cached_files = files
            else:
                st.error(f"Error: {files}")
                st.session_state.cached_files = []
    
    if st.session_state.get('cached_files'):
        files = st.session_state.cached_files
        total_size_mb = sum(f.get('size_mb', 0) for f in files)
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Documents", len(files))
        col2.metric("Total Size", f"{total_size_mb:.2f} MB")
        
        search = st.text_input("🔍 Filter", placeholder="Search by filename...")
        
        filtered = [f for f in files if search.lower() in f['filename'].lower()] if search else files
        
        for file in filtered:
            col1, col2, col3, col4 = st.columns([4, 2, 2, 1])
            col1.write(f"📄 {file['filename']}")
            col2.write(f"Type: {file['file_type'].upper()}")
            col3.write(f"Size: {file['size_kb']:.1f} KB")
            if col4.button("🗑️", key=f"del_{file['filename']}"):
                file_path = os.path.join(folder_path, file['filename'])
                success, msg = delete_file(file_path)
                if success:
                    st.success(f"Deleted {file['filename']}")
                    st.rerun()
                else:
                    st.error(msg)
    else:
        st.info("No documents found")

def config_page():
    st.markdown('<div class="main-header"><h1>⚙️ System Configuration</h1></div>', unsafe_allow_html=True)
    
    if not st.session_state.system_config:
        success, config_data = get_config(st.session_state.token)
        if success:
            st.session_state.system_config = config_data.get('config', {})
    
    config = st.session_state.system_config
    
    st.markdown("### Current Configuration")
    
    col1, col2 = st.columns(2)
    
    with col1:
        chunk_size = st.number_input("Chunk Size", value=config.get('chunk_size', 500), step=50)
        chunk_overlap = st.number_input("Chunk Overlap", value=config.get('chunk_overlap', 50), step=10)
        top_k = st.number_input("Top K", value=config.get('top_k', 5), step=1)
    
    with col2:
        temperature = st.slider("Temperature", 0.0, 2.0, config.get('temperature', 0.7), 0.1)
        llm_model = st.selectbox("LLM Model", ["mock", "ollama", "openai", "gemini"], 
                                  index=["mock", "ollama", "openai", "gemini"].index(config.get('llm_model', 'mock')))
        retrieval_strategy = st.selectbox("Retrieval Strategy", ["similarity", "mmr", "hybrid"],
                                           index=["similarity", "mmr", "hybrid"].index(config.get('retrieval_strategy', 'similarity')))
    
    if st.button("💾 Save Configuration", type="primary", use_container_width=True):
        updates = {
            "chunk_size": chunk_size,
            "chunk_overlap": chunk_overlap,
            "top_k": top_k,
            "temperature": temperature,
            "llm_model": llm_model,
            "retrieval_strategy": retrieval_strategy
        }
        success, result = update_config(st.session_state.token, updates)
        if success:
            st.success("Configuration saved successfully!")
            st.session_state.system_config = result.get('config', {})
            st.rerun()
        else:
            st.error(f"Failed to save: {result}")

def metrics_page():
    st.markdown('<div class="main-header"><h1>📊 System Metrics</h1></div>', unsafe_allow_html=True)
    
    with st.spinner("Loading metrics..."):
        success, metrics = get_metrics(st.session_state.token)
        
        if success:
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Documents", metrics.get('total_documents', 0))
            with col2:
                st.metric("Total Size", f"{metrics.get('total_size_mb', 0)} MB")
            with col3:
                st.metric("Query Count", metrics.get('query_count', 0))
            with col4:
                st.metric("Avg Response", f"{metrics.get('avg_response_time_ms', 0)} ms")
            
            st.markdown("### File Types")
            file_types = metrics.get('file_types', {})
            if file_types:
                for ft, count in file_types.items():
                    st.write(f"- {ft.upper()}: {count} files")
        else:
            st.warning(f"Metrics endpoint not fully implemented: {metrics}")

# ==================== MAIN ====================

def main():
    if not st.session_state.authenticated:
        if st.session_state.page == "Register":
            register_page()
        else:
            login_page()
    else:
        main_app()

if __name__ == "__main__":
    main()