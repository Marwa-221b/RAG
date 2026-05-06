# API Documentation for Team Members

## Authentication
All endpoints require Bearer token from /auth/login

## For Member 1 (Data Pipeline)
- POST /ingest - Receive folder path for processing
- Expected output format: JSON with document content

## Configuration
- GET /config - Get current settings
- PUT /config - Update settings (chunk_size, top_k, temperature, etc.)

## Health Checks
- GET /health - For Docker monitoring