FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Only needed if tkinter is indirectly used in API logic
RUN apt-get update && apt-get install -y \
    tk \
    libx11-6 \
    && rm -rf /var/lib/apt/lists/*

COPY . .

EXPOSE 8080

CMD ["python", "main.py"]
