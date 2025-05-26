readme: |
  # 🚀 Başlangıç

  ## 1. Bu repoyu klonlayın

  ```bash
  git clone https://github.com/kullanici-adi/flask-blog.git
  cd flask-blog
2. Docker image oluşturun

docker build -t flask-blog .

3. Uygulamayı çalıştırın


docker run -d -p 5000:5000 --name blog-app flask-blog

Uygulamaya erişmek için tarayıcınızdan:

http://localhost:5000

🛠 Temel Docker Komutları

Komut	Açıklama
docker build -t isim .	Image oluşturur
docker images	Mevcut image'ları listeler
docker run -p 5000:5000 image_adi	Container başlatır
docker ps	Çalışan container'ları gösterir
docker stop container_id	Container'ı durdurur
docker rm container_id	Container'ı siler
docker rmi image_adi	Image'ı siler










