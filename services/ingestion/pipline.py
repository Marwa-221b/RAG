import os
import re
import pdfplumber
import docx
from bs4 import BeautifulSoup
from arabic_reshaper import reshape
from bidi.algorithm import get_display

class DataIngestionPipeline:
    def __init__(self):

        self.arabic_diacritics = re.compile(r"""ّ|َ|ً|ُ|ٌ|ِ|ٍ|ْ|ـ""")

    #  Loaders 

    def _load_pdf(self, path):
        text = ""
        with pdfplumber.open(path) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ""
        return text

    def _load_docx(self, path):
        doc = docx.Document(path)
        return "\n".join([p.text for p in doc.paragraphs])

    def _load_html(self, path):
        with open(path, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f, 'html.parser')
            return soup.get_text()

    def _load_txt(self, path):
        with open(path, "r", encoding="utf-8") as f:
            return f.read()


    def _fix_arabic_rtl(self, text):
      
        return get_display(reshape(text))

    def _clean_and_normalize(self, text):
   
        text = self._fix_arabic_rtl(text)
        
        text = re.sub(self.arabic_diacritics, '', text)
        
    
        text = re.sub("[إأآا]", "ا", text)
        text = re.sub("ى", "ي", text)
        text = re.sub("ة", "ه", text)
        
      
        text = re.sub(r'\s+', ' ', text)
        return text.strip()

    

    def process_file(self, path):
       
        if not os.path.exists(path):
            return None

        ext = path.split('.')[-1].lower()
        
       
        try:
            if ext == "pdf":
                raw_text = self._load_pdf(path)
            elif ext == "docx":
                raw_text = self._load_docx(path)
            elif ext == "html":
                raw_text = self._load_html(path)
            elif ext == "txt":
                raw_text = self._load_txt(path)
            else:
                return None 

            processed_content = self._clean_and_normalize(raw_text)

            return {
                "content": processed_content,
                "metadata": {
                    "source": os.path.basename(path),
                    "file_type": ext,
                    "char_count": len(processed_content)
                }
            }
        except Exception as e:
            print(f"Error processing {path}: {str(e)}")
            return None

# if we try the pipeline 3ala folder 
    def run_on_folder(self, folder_path):
      
        documents = []
        if not os.path.exists(folder_path):
            return documents

        for file_name in os.listdir(folder_path):
            full_path = os.path.join(folder_path, file_name)
            if os.path.isfile(full_path):
                result = self.process_file(full_path)
                if result:
                    documents.append(result)
        
        return documents

# 3alashan ataked mn el run momken tmsa7oh
if __name__ == "__main__":
    pipeline = DataIngestionPipeline()
  
    data_folder = "data" 
    
    final_docs = pipeline.run_on_folder(data_folder)
    
    print(f"Total documents processed: {len(final_docs)}")
    if final_docs:
        print("\n--- Sample Output (First Doc) ---")
        print(f"Source: {final_docs[1]['metadata']['source']}")
        print(f"Content (Snippet): {final_docs[1]['content'][:200]}...")