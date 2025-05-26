# Temel Python imajını kullan
FROM python:3.10-slim

# Çalışma dizinini belirle
WORKDIR /app

# Gereken dosyaları container'a kopyala
COPY requirements.txt .
COPY app.py .
COPY flag.txt .
COPY static ./static

# Gerekli Python kütüphanelerini yükle
RUN pip install --no-cache-dir -r requirements.txt

# Flask portu
EXPOSE 5000

# Uygulamayı çalıştır
CMD ["python", "app.py"]
