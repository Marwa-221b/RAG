# RAG API Documentation

**Base URL:** `http://your-api-domain:port`  
**API Version:** `1.0.0`  
**Authentication:** Bearer token (JWT) required for `/config`, `/ingest`, and `/query` endpoints.  
**Data Format:** JSON for all requests and responses except `/auth/login`, which uses form data.

---

# Authentication & User Management

## `POST /auth/register`

Create a new user account.

### Request Body (JSON)

| Field | Type | Required | Description |
|---|---|---|---|
| `username` | string | Yes | Unique username |
| `email` | string | Yes | Email address |
| `password` | string | Yes | Plain-text password |

### Response — `200 OK`

```json
{
  "message": "User created successfully"
}
```

### Response — `400 Bad Request`

```json
{
  "detail": "Username already registered"
}
```

---

## `POST /auth/login`

Authenticate and obtain a JWT access token using OAuth2 password flow.

### Request Body

| Field | Type | Required |
|---|---|---|
| `username` | string | Yes |
| `password` | string | Yes |

### Response — `200 OK`

```json
{
  "access_token": "string",
  "token_type": "bearer"
}
```

### Response — `401 Unauthorized`

```json
{
  "detail": "Incorrect username or password"
}
```

---

# System Configuration

All endpoints under `/config` require a valid Bearer token.

## `GET /config`

Retrieve the current system configuration.

### Headers

```text
Authorization: Bearer <token>
```

### Response — `200 OK`

```json
{
  "config": {
    "chunk_size": "integer",
    "chunk_overlap": "integer",
    "top_k": "integer",
    "embedding_model": "string",
    "temperature": "float",
    "max_length": "integer",
    "vector_db_path": "string",
    "data_directory": "string",
    "llm_model": "string",
    "retrieval_strategy": "string"
  },
  "service": "RAG API",
  "version": "1.0.0"
}
```

---

## `PUT /config`

Partially update the system configuration. All fields are optional.

### Headers

```text
Authorization: Bearer <token>
```

### Request Body (JSON)

| Field | Type | Constraints |
|---|---|---|
| `chunk_size` | integer | Positive integer |
| `chunk_overlap` | integer | Must be less than `chunk_size` |
| `top_k` | integer | Positive integer |
| `embedding_model` | string | Any model name |
| `temperature` | float | Between 0 and 2 inclusive |
| `llm_model` | string | Any model name |
| `retrieval_strategy` | string | One of `similarity`, `mmr`, `hybrid` |

### Response — `200 OK`

```json
{
  "message": "Configuration updated successfully",
  "config": {
    "chunk_size": 200,
    "chunk_overlap": 20,
    "top_k": 5,
    "embedding_model": "sentence-transformers/all-MiniLM-L6-v2",
    "temperature": 0.1,
    "max_length": 512,
    "vector_db_path": "path/to/vector_store",
    "data_directory": "path/to/data",
    "llm_model": "mock",
    "retrieval_strategy": "similarity"
  }
}
```

### Response — `400 Bad Request`

```json
{
  "detail": "error description"
}
```

Possible errors include:
- `chunk_overlap` larger than `chunk_size`
- Invalid `temperature` value
- Unsupported `retrieval_strategy`

---

# Health & Monitoring

These endpoints do not require authentication.

## `GET /health/live`

Liveness probe endpoint.

### Response — `200 OK`

```json
{
  "status": "alive",
  "timestamp": "ISO datetime string"
}
```

---

## `GET /metrics`

Retrieve service health and metadata.

### Response — `200 OK`

```json
{
  "status": "healthy",
  "timestamp": "ISO datetime string",
  "service": "RAG API"
}
```

---

# Document Ingestion

## `POST /ingest` *(Protected)*

Process documents from a folder and build or update the vector store.

### Headers

```text
Authorization: Bearer <token>
```

### Request Body (JSON)

| Field | Type | Required | Description |
|---|---|---|---|
| `folder_path` | string | Yes | Absolute path to the documents folder |

### Response — `200 OK`

```json
{
  "documents": [],
  "total_processed": 0
}
```

### Response — `404 Not Found`

```json
{
  "detail": "No documents found or processed in the specified folder"
}
```

---

# Query & Answer

## `POST /query` *(Protected)*

Send a natural language query and receive an answer with source chunks.

### Headers

```text
Authorization: Bearer <token>
```

### Request Body (JSON)

| Field | Type | Required | Description |
|---|---|---|---|
| `query` | string | Yes | User’s question |

### Response — `200 OK`

```json
{
  "answer": "string",
  "sources": [
    {
      "chunk": "string",
      "source": "string"
    }
  ]
}
```

---

# Authentication Usage

For protected endpoints (`/config`, `/ingest`, `/query`), include the JWT token in the request header.

```text
Authorization: Bearer <access_token>
```

The token is obtained from `/auth/login` and expires after the configured duration (default: 15 minutes).

---

# Environment Variables

| Variable | Description |
|---|---|
| `SECRET_KEY` | Secret key used for JWT generation |
| `ALGORITHM` | JWT algorithm (example: `HS256`) |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Token lifetime in minutes |

These variables should be defined in a `.env` file or system environment.

---

# Endpoints Summary

| Method | Endpoint | Authentication | Description |
|---|---|---|---|
| `POST` | `/auth/register` | No | Register a new user |
| `POST` | `/auth/login` | No | Obtain access token |
| `GET` | `/config` | Yes | View current configuration |
| `PUT` | `/config` | Yes | Update configuration partially |
| `GET` | `/health/live` | No | Liveness probe |
| `GET` | `/metrics` | No | Service health information |
| `POST` | `/ingest` | Yes | Ingest documents from folder |
| `POST` | `/query` | Yes | Ask questions and retrieve answers |
