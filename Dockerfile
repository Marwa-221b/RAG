
FROM python:3.11-slim


WORKDIR /app


RUN apt-get update && apt-get install -y \
    build-essential \ #needed to compile Python packages that have C++ components(faais)
    libpoppler-cpp-dev \
    poppler-utils \ #handling PDFs
    && rm -rf /var/lib/apt/lists/* #cleanp

 
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


COPY . .

EXPOSE 8000

COPY docker/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]