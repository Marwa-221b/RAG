#!/bin/bash
set -e

# If command is streamlit, run it directly without waiting for Ollama
if [[ "$1" == "streamlit" ]]; then
    echo "Starting Streamlit GUI..."
    exec "$@"
fi

# Otherwise, this is the API container - wait for Ollama
echo "Starting RAG API..."
echo "Waiting for Ollama service..."
until curl -s http://ollama:11434/api/tags > /dev/null 2>&1; do
    echo "Ollama not ready yet, retrying in 3 seconds..."
    sleep 3
done

echo "Ollama is ready!"
MODEL=${OLLAMA_MODEL:-llama3.2}
echo "Ensuring model '$MODEL' is available..."
curl -s -X POST http://ollama:11434/api/pull \
    -H "Content-Type: application/json" \
    -d "{\"name\": \"$MODEL\"}"

echo "Starting FastAPI..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload