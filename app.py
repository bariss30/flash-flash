from flask import Flask, render_template_string, request, redirect, url_for
import re
import urllib.parse

app = Flask(__name__)

BLACKLIST_COMMANDS = ["ls", "dir", "rm", "popen","cat","less","<",">"," :" ]

def is_command_blacklisted(command_str):
    
    cmd = command_str.strip().split(' ')[0].lower()
    return cmd in BLACKLIST_COMMANDS

def check_popen_commands(user_input):
   
    
    matches = re.findall(r"popen\(['\"](.*?)['\"]\)", user_input)
    for cmd in matches:
        if is_command_blacklisted(cmd):
            return False
    return True

def temizle_input(girdi):
    # Sadece <, >, : karakterlerini kaldır
    return re.sub(r'[<>:]', '', girdi)


# Main blog page
@app.route("/")
def home():
    # Blog homepage with navbar and featured articles
    template = '''
    <!DOCTYPE html>
    <html lang="tr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Yavuzlar Blog - Siber Güvenlik Platformu</title>
          <style>
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                margin: 0;
                padding: 0;
                background-color: #f4f4f4;
                color: #333;
                line-height: 1.6;
            }
            .container {
                width: 85%;
                margin: auto;
                overflow: hidden;
            }
            header {
                background: #35424a;
                color: #ffffff;
                padding-top: 20px;
                min-height: 70px;
                border-bottom: #e8491d 3px solid;
            }
            header a {
                color: #ffffff;
                text-decoration: none;
                text-transform: uppercase;
                font-size: 16px;
            }
            header ul {
                padding: 0;
                margin: 0;
                list-style: none;
                overflow: hidden;
            }
            header li {
                float: left;
                display: inline;
                padding: 0 20px 0 20px;
            }
            header #branding {
                float: left;
            }
            header #branding h1 {
                margin: 0;
            }
            header nav {
                float: right;
                margin-top: 10px;
            }
            header .highlight, header .current a {
                color: #e8491d;
                font-weight: bold;
            }
            header a:hover {
                color: #cccccc;
                font-weight: bold;
            }
            #showcase {
                min-height: 400px;
                background: url('/static/logo.png') no-repeat center;
                background-size: cover;
                text-align: center;
                color: #ffffff;
            }
            #showcase h1 {
                margin-top: 100px;
                font-size: 55px;
                margin-bottom: 10px;
                text-shadow: 2px 2px 5px #000;
            }
            #showcase p {
                font-size: 20px;
                text-shadow: 1px 1px 3px #000;
            }
            .blog-container {
                margin-top: 30px;
                display: flex;
                flex-direction: column;
                gap: 20px;
                padding-left: 20px; /* Left spacing for all cards */
                align-items: center; /* Center cards horizontally */
            }
            .blog-card {
                background: #fff;
                padding: 15px;
            
                border-radius: 5px;
                box-shadow: 0 5px 15px rgba(0,0,0,0.1);
                transition: transform 0.3s;
                width: 100%; /* Ensure cards don't stretch too wide */
                max-width: 600px; /* Limit card width for centering */
                margin-left:600px;
            }
            .blog-card:hover {
                transform: translateY(-5px);
            }
            .blog-card img {
                width: 100%;
                height: 180px;
                object-fit: cover;
                border-radius: 5px;
            }
            .blog-card h3 {
                margin-top: 15px;
                color: #35424a;
            }
            .blog-card p {
                color: #666;
            }
            .blog-card .btn {
                display: inline-block;
                background: #e8491d;
                color: #fff;
                padding: 10px 15px;
                border: none;
                border-radius: 5px;
                text-decoration: none;
                margin-top: 10px;
                cursor: pointer;
            }
            footer {
                background: #35424a;
                color: #ffffff;
                text-align: center;
                padding: 20px;
                margin-top: 30px;
            }
        </style>
    </head>
    <body>
        <header>
            <div class="container">
                <div id="branding">
                    <h1><span class="highlight">Yavuzlar</span> Blog</h1>
                </div>
                <nav>
                    <ul>
                        <li class="current"><a href="/">Anasayfa</a></li>
                        <li><a href="/blog">Makaleler</a></li>
                        <li><a href="/egitim">Eğitimler</a></li>
                        <li><a href="/hakkimizda">Hakkımızda</a></li>
                        <li><a href="/iletisim">İletişim</a></li>
                    </ul>
                </nav>
            </div>
        </header>

        <section id="showcase">
            <div class="container">
                <h1>Siber Güvenlikte Lider Platform</h1>
                <p>Yavuzlar ile siber güvenlik dünyasındaki en güncel bilgilere erişin ve kendinizi geliştirin.</p>
            </div>
        </section>

    
                <div class="blog-card">
                    <img src="/static/images/blog/1.jpg" alt="Siber Saldırılar">
                    <h3>2025'in En Yaygın Siber Saldırıları</h3>
                    <p>Bu yıl en çok karşılaşılan siber saldırı türleri ve korunma yöntemleri</p>
                    <a href="/blog/2025-siber-saldirilari" class="btn">Devamını Oku</a>
                </div>
                <div class="blog-card">
                    <img src="/static/images/blog/2.jpg" alt="CTF Eğitimi">
                    <h3>CTF Yarışmaları İçin Hazırlık</h3>
                    <p>Capture The Flag yarışmalarında başarılı olmak için ipuçları</p>
                    <a href="/blog/ctf-egitimi" class="btn">Devamını Oku</a>
                </div>
                <div class="blog-card">
                    <img src="/static/images/blog/3.jpg" alt="Penetrasyon Testi">
                    <h3>Penetrasyon Testi Metodolojileri</h3>
                    <p>Profesyonel pentest süreçlerinde kullanılan metodolojiler ve araçlar</p>
                    <a href="/blog/pentest-metodolojileri" class="btn">Devamını Oku</a>
                </div>
                <div class="blog-card">
                    <img src="/static/images/blog/4.jpg" alt="Zero Day">
                    <h3>Zero Day Açıkları ve Etkileri</h3>
                    <p>Sıfır gün açıklarının tespit edilmesi ve potansiyel etkilerinin analizi</p>
                    <a href="/blog/zero-day-aciklari" class="btn">Devamını Oku</a>
                </div>
                <div class="blog-card">
                    <img src="/static/images/blog/5.jpg" alt="Red Team">
                    <h3>Red Team Operasyonları</h3>
                    <p>Kırmızı takım operasyonlarının planlanması ve yürütülmesi hakkında</p>
                    <a href="/blog/red-team-operasyonlari" class="btn">Devamını Oku</a>
                </div>
            </div>
        </div>

        <footer>
            <p>Yavuzlar Blog &copy; 2025</p>
        </footer>
    </body>
    </html>
    '''
    return template

# Blog details page - example
@app.route("/blog/<article_name>")
def blog_detail(article_name):
    # Example blog article page
    template = f'''
    <!DOCTYPE html>
    <html lang="tr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Yavuzlar Blog - {article_name.replace('-', ' ').title()}</title>
        <style>
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                margin: 0;
                padding: 0;
                background-color: #f4f4f4;
                color: #333;
                line-height: 1.6;
            }}
            .container {{
                width: 85%;
                margin: auto;
                overflow: hidden;
            }}
            header {{
                background: #35424a;
                color: #ffffff;
                padding-top: 20px;
                min-height: 70px;
                border-bottom: #e8491d 3px solid;
            }}
            header a {{
                color: #ffffff;
                text-decoration: none;
                text-transform: uppercase;
                font-size: 16px;
            }}
            header ul {{
                padding: 0;
                margin: 0;
                list-style: none;
                overflow: hidden;
            }}
            header li {{
                float: left;
                display: inline;
                padding: 0 20px 0 20px;
            }}
            header #branding {{
                float: left;
            }}
            header #branding h1 {{
                margin: 0;
            }}
            header nav {{
                float: right;
                margin-top: 10px;
            }}
            header .highlight, header .current a {{
                color: #e8491d;
                font-weight: bold;
            }}
            header a:hover {{
                color: #cccccc;
                font-weight: bold;
            }}
            .article {{
                background: white;
                padding: 30px;
                margin-top: 30px;
                border-radius: 5px;
                box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            }}
            .article img {{
                width: 100%;
                max-height: 400px;
                object-fit: cover;
                border-radius: 5px;
                margin-bottom: 20px;
            }}
            footer {{
                background: #35424a;
                color: #ffffff;
                text-align: center;
                padding: 20px;
                margin-top: 30px;
            }}
        </style>
    </head>
    <body>
        <header>
            <div class="container">
                <div id="branding">
                    <h1><span class="highlight">Yavuzlar</span> Blog</h1>
                </div>
                <nav>
                    <ul>
                        <li><a href="/">Anasayfa</a></li>
                        <li class="current"><a href="/blog">Makaleler</a></li>
                        <li><a href="/egitim">Eğitimler</a></li>
                        <li><a href="/hakkimizda">Hakkımızda</a></li>
                        <li><a href="/iletisim">İletişim</a></li>
                    </ul>
                </nav>
            </div>
        </header>

        <div class="container">
            <div class="article">
                <img src="/static/images/blog/1.jpg" alt="Siber Saldırılar">
                <h1>Yavuzlar</h1>
                <p>Bu makale henüz hazırlanmaktadır. Yakında burada olacak!</p>
                <p>Siber güvenlik dünyasındaki en güncel bilgileri sizlerle paylaşmaya devam edeceğiz. Takipte kalın!</p>
                <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam quis risus eget urna mollis ornare vel eu leo. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Nullam id dolor id nibh ultricies vehicula ut id elit.</p>
                <p>Etiam porta sem malesuada magna mollis euismod. Cras mattis consectetur purus sit amet fermentum. Aenean lacinia bibendum nulla sed consectetur. Donec id elit non mi porta gravida at eget metus. Vestibulum id ligula porta felis euismod semper.</p>
            </div>
        </div>

        <footer>
            <p>Yavuzlar Blog &copy; 2025</p>
        </footer>
    </body>
    </html>
    '''
    return template



@app.route("/greeting/")
def greetinginf():

    template = '''
    <!DOCTYPE html>
    <html lang="tr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Yavuzlar Blog - </title>
        <style>
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                margin: 0;
                padding: 0;
                background-color: #f4f4f4;
                color: #333;
                line-height: 1.6;
            }
            .container {
                width: 85%;
                margin: auto;
                overflow: hidden;
                padding: 20px;
            }
            header {
                background: #35424a;
                color: #ffffff;
                padding-top: 20px;
                min-height: 70px;
                border-bottom: #e8491d 3px solid;
            }
            header a {
                color: #ffffff;
                text-decoration: none;
                text-transform: uppercase;
                font-size: 16px;
            }
            header #branding {
                float: left;
            }
            header #branding h1 {
                margin: 0;
            }
            .message-box {
                background: white;
                padding: 20px;
                margin-top: 30px;
                border-radius: 5px;
                box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            }
            footer {
                background: #35424a;
                color: #ffffff;
                text-align: center;
                padding: 20px;
                margin-top: 30px;
                position: fixed;
                bottom: 0;
                width: 100%;
            }
        </style>
    </head>
    <body>
        <header>
            <div class="container">
                <div id="branding">
                    <h1><span class="highlight">Yavuzlar</span> Blog</h1>
                </div>
            </div>
        </header>

        <div class="container">
            <div class="message-box">
               <!-- 
                    QnVyYXPEsSBzYWRlY2UgYmHFn2xhbmfEscOnLi4uCkfDtnLDvG5tZXllbiBrYXDEsWxhciwgc2Vzc2l6IGFkxLFtbGFybGEgYcOnxLFsxLFyLgpCYXplbiBVUkwnbGVyIGbEsXPEsWxkYXIsIGRpa2thdGxpIGRpbmxlLgpCaXIgaXN0ZWssIGJpciB5b2zigKYgYmVsa2kgYmlyIGVr4oCmCkJpciBzbGFzaCBhcmTEsW5kYW4gZ2VsZW4ga2VsaW1lbGVyIGJhemVuIHPEsXJsYXLEsSB0YcWfxLFyLgpTZXNzaXogYmlyIMOnYcSfcsSxIHZhciwgYW1hIGR1eW1hayBpw6dpbiBkaWtrYXQgZ2VyZWsu
                -->
            

                <div class="user-message">
                
                </div>
            </div>
        </div>

        <footer>
            <p>Yavuzlar Blog &copy; 2025</p>
        </footer>
    </body>
    </html>
    '''
    return render_template_string(template)



@app.route("/greeting/<path:user_input>")
def greeting(user_input):
    decoded_input = urllib.parse.unquote(user_input)
    
    if not check_popen_commands(decoded_input):
        return "Hata: Yasaklı komut içeriği var!", 403

    temiz_input = temizle_input(decoded_input)

    template = '''
    <!DOCTYPE html>
    <html lang="tr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Yavuzlar Blog - </title>
        <style>
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                margin: 0;
                padding: 0;
                background-color: #f4f4f4;
                color: #333;
                line-height: 1.6;
            }
            .container {
                width: 85%;
                margin: auto;
                overflow: hidden;
                padding: 20px;
            }
            header {
                background: #35424a;
                color: #ffffff;
                padding-top: 20px;
                min-height: 70px;
                border-bottom: #e8491d 3px solid;
            }
            header a {
                color: #ffffff;
                text-decoration: none;
                text-transform: uppercase;
                font-size: 16px;
            }
            header #branding {
                float: left;
            }
            header #branding h1 {
                margin: 0;
            }
            .message-box {
                background: white;
                padding: 20px;
                margin-top: 30px;
                border-radius: 5px;
                box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            }
            footer {
                background: #35424a;
                color: #ffffff;
                text-align: center;
                padding: 20px;
                margin-top: 30px;
                position: fixed;
                bottom: 0;
                width: 100%;
            }
        </style>
    </head>
    <body>
        <header>
            <div class="container">
                <div id="branding">
                    <h1><span class="highlight">Yavuzlar</span> Blog</h1>
                </div>
            </div>
        </header>

        <div class="container">
            <div class="message-box">
                <!-- 
                    ZGl6aW4gdGFyYW1hc8SxID8=
                -->
                <div class="user-message">
                    ''' + temiz_input + '''
                </div>
            </div>
        </div>

        <footer>
            <p>Yavuzlar Blog &copy; 2025</p>
        </footer>
    </body>
    </html>
    '''
    return render_template_string(template)


# About Us page
@app.route("/hakkimizda")
def about():
    template = '''
    <!DOCTYPE html>
    <html lang="tr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Yavuzlar Blog - Hakkımızda</title>
        <style>
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                margin: 0;
                padding: 0;
                background-color: #f4f4f4;
                color: #333;
                line-height: 1.6;
            }
            .container {
                width: 85%;
                margin: auto;
                overflow: hidden;
            }
            header {
                background: #35424a;
                color: #ffffff;
                padding-top: 20px;
                min-height: 70px;
                border-bottom: #e8491d 3px solid;
            }
            header a {
                color: #ffffff;
                text-decoration: none;
                text-transform: uppercase;
                font-size: 16px;
            }
            header ul {
                padding: 0;
                margin: 0;
                list-style: none;
                overflow: hidden;
            }
            header li {
                float: left;
                display: inline;
                padding: 0 20px 0 20px;
            }
            header #branding {
                float: left;
            }
            header #branding h1 {
                margin: 0;
            }
            header nav {
                float: right;
                margin-top: 10px;
            }
            header .highlight, header .current a {
                color: #e8491d;
                font-weight: bold;
            }
            header a:hover {
                color: #cccccc;
                font-weight: bold;
            }
            .about {
                background: white;
                padding: 30px;
                margin-top: 30px;
                border-radius: 5px;
                box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            }
            .team {
                display: grid;
                grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
                gap: 20px;
                margin-top: 30px;
            }
            .team-member {
                background: #f9f9f9;
                padding: 15px;
                border-radius: 5px;
                text-align: center;
            }
            .team-member img {
                width: 150px;
                height: 150px;
                border-radius: 50%;
                object-fit: cover;
            }
            footer {
                background: #35424a;
                color: #ffffff;
                text-align: center;
                padding: 20px;
                margin-top: 30px;
            }
        </style>
    </head>
    <body>
        <header>
            <div class="container">
                <div id="branding">
                    <h1><span class="highlight">Yavuzlar</span> Blog</h1>
                </div>
                <nav>
                    <ul>
                        <li><a href="/">Anasayfa</a></li>
                        <li><a href="/blog">Makaleler</a></li>
                        <li><a href="/egitim">Eğitimler</a></li>
                        <li class="current"><a href="/hakkimizda">Hakkımızda</a></li>
                        <li><a href="/iletisim">İletişim</a></li>
                    </ul>
                </nav>
            </div>
        </header>

        <div class="container">
            <div class="about">
                <h1>Hakkımızda</h1>
                <p>Yavuzlar Blog, siber güvenlik alanında bilgi paylaşımı yapmak ve farkındalık oluşturmak amacıyla 2025 yılında kurulmuştur. Türkiye'nin önde gelen siber güvenlik uzmanları tarafından hazırlanan içeriklerle sizlere en güncel bilgileri sunmayı hedefliyoruz.</p>
                
                <p>Misyonumuz, siber güvenlik alanında eğitim ve farkındalık çalışmaları yaparak toplumun dijital okuryazarlık seviyesini yükseltmek ve güvenlik kültürünü yaygınlaştırmaktır. Vizyonumuz ise, Türkiye'nin siber güvenlik alanında uluslararası düzeyde söz sahibi olmasına katkıda bulunmaktır.</p>
                
             
                
                <h2>İlkelerimiz</h2>
                <ul>
                    <li>Bilgi paylaşımında etik kurallara uygunluk</li>
                    <li>Doğru ve güncel bilginin aktarılması</li>
                    <li>Toplum yararına hizmet etme</li>
                    <li>Sürekli öğrenme ve gelişme</li>
                </ul>
            </div>
        </div>

        <footer>
            <p>Yavuzlar Blog &copy; 2025</p>
        </footer>
    </body>
    </html>
    '''
    return template

# Contact page with hidden hint
@app.route("/iletisim")
def contact():
    template = '''
    <!DOCTYPE html>
    <html lang="tr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Yavuzlar Blog - İletişim</title>
        <style>
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                margin: 0;
                padding: 0;
                background-color: #f4f4f4;
                color: #333;
                line-height: 1.6;
            }
            .container {
                width: 85%;
                margin: auto;
                overflow: hidden;
            }
            header {
                background: #35424a;
                color: #ffffff;
                padding-top: 20px;
                min-height: 70px;
                border-bottom: #e8491d 3px solid;
            }
            header a {
                color: #ffffff;
                text-decoration: none;
                text-transform: uppercase;
                font-size: 16px;
            }
            header ul {
                padding: 0;
                margin: 0;
                list-style: none;
                overflow: hidden;
            }
            header li {
                float: left;
                display: inline;
                padding: 0 20px 0 20px;
            }
            header #branding {
                float: left;
            }
            header #branding h1 {
                margin: 0;
            }
            header nav {
                float: right;
                margin-top: 10px;
            }
            header .highlight, header .current a {
                color: #e8491d;
                font-weight: bold;
            }
            header a:hover {
                color: #cccccc;
                font-weight: bold;
            }
            .contact {
                background: white;
                padding: 30px;
                margin-top: 30px;
                border-radius: 5px;
                box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            }
            .contact-form {
                margin-top: 20px;
            }
            .form-group {
                margin-bottom: 15px;
            }
            .form-group label {
                display: block;
                margin-bottom: 5px;
            }
            .form-group input, .form-group textarea {
                width: 100%;
                padding: 10px;
                border: 1px solid #ddd;
                border-radius: 5px;
            }
            .form-group textarea {
                height: 150px;
            }
            .btn {
                display: inline-block;
                background: #e8491d;
                color: #fff;
                padding: 10px 20px;
                border: none;
                border-radius: 5px;
                cursor: pointer;
            }
            .contact-info {
                margin-top: 30px;
                display: flex;
                justify-content: space-between;
                flex-wrap: wrap;
            }
            .contact-item {
                flex: 1;
                min-width: 250px;
                padding: 15px;
                margin: 10px;
                background: #f9f9f9;
                border-radius: 5px;
            }
            footer {
                background: #35424a;
                color: #ffffff;
                text-align: center;
                padding: 20px;
                margin-top: 30px;
            }
            .hidden-hint {
                color: transparent;
                font-size: 1px;
                position: absolute;
            }
        </style>
    </head>
    <body>
        <header>
            <div class="container">
                <div id="branding">
                    <h1><span class="highlight">Yavuzlar</span> Blog</h1>
                </div>
                <nav>
                    <ul>
                        <li><a href="/">Anasayfa</a></li>
                        <li><a href="/blog">Makaleler</a></li>
                        <li><a href="/egitim">Eğitimler</a></li>
                        <li><a href="/hakkimizda">Hakkımızda</a></li>
                        <li class="current"><a href="/iletisim">İletişim</a></li>
                    </ul>
                </nav>
            </div>
        </header>

        <div class="container">
            <div class="contact">
                <h1>İletişim</h1>
                <p>Bize ulaşmak için aşağıdaki formu kullanabilirsiniz. En kısa sürede size geri dönüş yapacağız.</p>
                
                <!-- Hidden hint for CTF players -->
                <div class="hidden-hint">
                    İpucu: Gizli endpoint'i bulmak için greeting/ yolunu deneyin. Template injection zafiyeti için {{ 7*7 }} gibi ifadeler kullanılabilir.
                </div>
                
                <div class="contact-form">
                    <form action="#" method="post">
                        <div class="form-group">
                            <label for="name">Ad Soyad</label>
                            <input type="text" id="name" name="name" placeholder="Adınız ve soyadınız">
                        </div>
                        <div class="form-group">
                            <label for="email">E-posta</label>
                            <input type="email" id="email" name="email" placeholder="E-posta adresiniz">
                        </div>
                        <div class="form-group">
                            <label for="subject">Konu</label>
                            <input type="text" id="subject" name="subject" placeholder="Mesajınızın konusu">
                        </div>
                        <div class="form-group">
                            <label for="message">Mesaj</label>
                            <textarea id="message" name="message" placeholder="Mesajınız"></textarea>
                        </div>
                        <button type="submit" class="btn">Gönder</button>
                    </form>
                </div>
                
                <div class="contact-info">
                    <div class="contact-item">
                        <h3>Adres</h3>
                        <p>Siber Güvenlik Caddesi No: 123</p>
                        <p>Yazılım Mahallesi</p>
                        <p>Ankara, Türkiye</p>
                    </div>
                    <div class="contact-item">
                        <h3>İletişim Bilgileri</h3>
                        <p>Email: info@yavuzlarblog.com</p>
                        <p>Telefon: +90 (312) 123 4567</p>
                    </div>
                    <div class="contact-item">
                        <h3>Çalışma Saatleri</h3>
                        <p>Pazartesi - Cuma: 09:00 - 18:00</p>
                        <p>Cumartesi: 10:00 - 14:00</p>
                        <p>Pazar: Kapalı</p>
                    </div>
                </div>
            </div>
        </div>

        <footer>
            <p>Yavuzlar Blog &copy; 2025</p>
        </footer>
    </body>
    </html>
    '''
    return template

# Training page
@app.route("/egitim")
def training():
    template = '''
    <!DOCTYPE html>
    <html lang="tr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Yavuzlar Blog - Eğitimler</title>
        <style>
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                margin: 0;
                padding: 0;
                background-color: #f4f4f4;
                color: #333;
                line-height: 1.6;
            }
            .container {
                width: 85%;
                margin: auto;
                overflow: hidden;
            }
            header {
                background: #35424a;
                color: #ffffff;
                padding-top: 20px;
                min-height: 70px;
                border-bottom: #e8491d 3px solid;
            }
            header a {
                color: #ffffff;
                text-decoration: none;
                text-transform: uppercase;
                font-size: 16px;
            }
            header ul {
                padding: 0;
                margin: 0;
                list-style: none;
                overflow: hidden;
            }
            header li {
                float: left;
                display: inline;
                padding: 0 20px 0 20px;
            }
            header #branding {
                float: left;
            }
            header #branding h1 {
                margin: 0;
            }
            header nav {
                float: right;
                margin-top: 10px;
            }
            header .highlight, header .current a {
                color: #e8491d;
                font-weight: bold;
            }
            header a:hover {
                color: #cccccc;
                font-weight: bold;
            }
            .training {
                background: white;
                padding: 30px;
                margin-top: 30px;
                border-radius: 5px;
                box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            }
            .courses {
                display: grid;
                grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
                gap: 20px;
                margin-top: 30px;
            }
            .course {
                background: #f9f9f9;
                padding: 20px;
                border-radius: 5px;
                box-shadow: 0 3px 10px rgba(0,0,0,0.1);
            }
            .course h3 {
                color: #35424a;
                margin-top: 0;
            }
            .course .price {
                font-weight: bold;
                color: #e8491d;
                font-size: 1.2em;
                margin: 10px 0;
            }
            .course .btn {
                display: inline-block;
                background: #e8491d;
                color: #fff;
                padding: 10px 15px;
                border: none;
                border-radius: 5px;
                text-decoration: none;
                margin-top: 10px;
                cursor: pointer;
            }
            footer {
                background: #35424a;
                color: #ffffff;
                text-align: center;
                padding: 20px;
                margin-top: 30px;
            }
            .comment {
                display: none;
            }
        </style>
    </head>
    <body>
        <header>
            <div class="container">
                <div id="branding">
                    <h1><span class="highlight">Yavuzlar</span> Blog</h1>
                </div>
                <nav>
                    <ul>
                        <li><a href="/">Anasayfa</a></li>
                        <li><a href="/blog">Makaleler</a></li>
                        <li class="current"><a href="/egitim">Eğitimler</a></li>
                        <li><a href="/hakkimizda">Hakkımızda</a></li>
                        <li><a href="/iletisim">İletişim</a></li>
                    </ul>
                </nav>
            </div>
        </header>

        <div class="container">
            <div class="training">
                <h1>Eğitimlerimiz</h1>
                <p>Siber güvenlik alanında kendini geliştirmek isteyenler için uzman eğitmenlerimiz tarafından hazırlanan eğitimlerimize göz atın.</p>
                
               
                <!-- 
                    ZGl6aW4gdGFyYW1hc8SxID8=
                -->
                
                <div class="courses">
                    <div class="course">
                        <h3>Temel Siber Güvenlik</h3>
                        <p>Siber güvenlik dünyasına giriş yapmak isteyenler için temel kavramlar ve uygulamalar.</p>
                        
                        <p><strong>Süre:</strong> 4 Hafta</p>
                        <a href="/" class="btn">Detaylar</a>
                    </div>
                    <div class="course">
                        <h3>Web Uygulama Güvenliği</h3>
                        <p>Web uygulamalarında güvenlik açıklarını tespit etme ve önleme teknikleri.</p>
                        
                        <p><strong>Süre:</strong> 6 Hafta</p>
                        <a href="/" class="btn">Detaylar</a>
                    </div>
                    <div class="course">
                        <h3>Ağ Güvenliği</h3>
                        <p>Ağ sistemlerinde güvenlik açıklarını tespit etme ve önleme teknikleri.</p>
                        
                        <p><strong>Süre:</strong> 8 Hafta</p>
                        <a href="/" class="btn">Detaylar</a>
                    </div>
                    <div class="course">
                        <h3>SSTI & Template Injection</h3>
                        <p>Template Injection zafiyetlerini anlama, tespit etme ve önleme teknikleri.</p>
                        
                        <p><strong>Süre:</strong> 3 Hafta</p>
                        <a href="/" class="btn">Detaylar</a>
                    </div>
                    <div class="course">
                        <h3>Red Team Operasyonları</h3>
                        <p>Profesyonel red team operasyonları planlama ve yürütme eğitimi.</p>
                        
                        <p><strong>Süre:</strong> 10 Hafta</p>
                        <a href="/" class="btn">Detaylar</a>
                    </div>
                    <div class="course">
                        <h3>CTF Hazırlık</h3>
                        <p>Capture The Flag yarışmalarına hazırlık ve CTF zorlukları çözme teknikleri.</p>
                        
                        <p><strong>Süre:</strong> 5 Hafta</p>
                        <a href="/  " class="btn">Detaylar</a>
                    </div>
                </div>
            </div>
        </div>

        <footer>
            <p>Yavuzlar Blog &copy; 2025</p>
        </footer>
    </body>
    </html>
    '''
    return template

# Blog list page
@app.route("/blog")
def blog():
    template = '''
    <!DOCTYPE html>
    <html lang="tr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Yavuzlar Blog - Makaleler</title>
        <style>
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                margin: 0;
                padding: 0;
                background-color: #f4f4f4;
                color: #333;
                line-height: 1.6;
            }
            .container {
                width: 85%;
                margin: auto;
                overflow: hidden;
            }
            header {
                background: #35424a;
                color: #ffffff;
                padding-top: 20px;
                min-height: 70px;
                border-bottom: #e8491d 3px solid;
            }
            header a {
                color: #ffffff;
                text-decoration: none;
                text-transform: uppercase;
                font-size: 16px;
            }
            header ul {
                padding: 0;
                margin: 0;
                list-style: none;
                overflow: hidden;
            }
            header li {
                float: left;
                display: inline;
                padding: 0 20px 0 20px;
            }
            header #branding {
                float: left;
            }
            header #branding h1 {
                margin: 0;
            }
            header nav {
                float: right;
                margin-top: 10px;
            }
            header .highlight, header .current a {
                color: #e8491d;
                font-weight: bold;
            }
            header a:hover {
                color: #cccccc;
                font-weight: bold;
            }
            .blog-section {
                background: white;
                padding: 30px;
                margin-top: 30px;
                border-radius: 5px;
                box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            }
            .blog-list {
                margin-top: 30px;
            }
            .blog-item {
                border-bottom: 1px solid #ddd;
                padding: 20px 0;
                display: flex;
                flex-wrap: wrap;
            }
            .blog-item:last-child {
                border-bottom: none;
            }
            .blog-item-image {
                flex: 1;
                min-width: 250px;
                max-width: 300px;
                margin-right: 20px;
            }
            .blog-item-image img {
                width: 100%;
                border-radius: 5px;
            }
            .blog-item-content {
                flex: 2;
                min-width: 300px;
            }
            .blog-item-content h3 {
                margin-top: 0;
            }
            .blog-item-content .btn {
                display: inline-block;
                background: #e8491d;
                color: #fff;
                padding: 10px 15px;
                border: none;
                border-radius: 5px;
                text-decoration: none;
                margin-top: 10px;
            }
            .categories {
                margin-bottom: 20px;
            }
            .categories ul {
                padding: 0;
                list-style: none;
                display: flex;
                flex-wrap: wrap;
            }
            .categories li {
                margin-right: 10px;
                margin-bottom: 10px;
            }
            .categories a {
                display: inline-block;
                background: #f4f4f4;
                color: #333;
                padding: 5px 15px;
                border-radius: 20px;
                text-decoration: none;
            }
            .categories a:hover {
                background: #e8491d;
                color: #fff;
            }
            footer {
                background: #35424a;
                color: #ffffff;
                text-align: center;
                padding: 20px;
                margin-top: 30px;
            }
        </style>
    </head>
    <body>
        <header>
            <div class="container">
                <div id="branding">
                    <h1><span class="highlight">Yavuzlar</span> Blog</h1>
                </div>
                <nav>
                    <ul>
                        <li><a href="/">Anasayfa</a></li>
                        <li class="current"><a href="/blog">Makaleler</a></li>
                        <li><a href="/egitim">Eğitimler</a></li>
                        <li><a href="/hakkimizda">Hakkımızda</a></li>
                        <li><a href="/iletisim">İletişim</a></li>
                    </ul>
                </nav>
            </div>
        </header>

        <div class="container">
            <div class="blog-section">
                <h1>Makaleler</h1>
                <p>Siber güvenlik dünyasındaki en güncel bilgiler, teknikler ve haberler burada.</p>
                
                <div class="categories">
                    <h3>Kategoriler</h3>
                    <ul>
                        <li><a href="#">Güvenlik Açıkları</a></li>
                        <li><a href="#">CTF</a></li>
                        <li><a href="#">Penetrasyon Testleri</a></li>
                        <li><a href="#">Kriptografi</a></li>
                        <li><a href="#">Ağ Güvenliği</a></li>
                        <li><a href="#">Mobil Güvenlik</a></li>
                        <li><a href="#">Web Güvenliği</a></li>
                        <li><a href="#">Sosyal Mühendislik</a></li>
                    </ul>
                </div>
                
                <div class="blog-list">
                 
                    
                    <div class="blog-item">
                        <div class="blog-item-image">
                            <img src="/static/images/blog/1.jpg" alt="Siber Saldırılar">
                        </div>
                        <div class="blog-item-content">
                            <h3>Zero Day Açıkları ve Etkileri</h3>
                            <p>Zero Day açıkları, siber güvenlik dünyasında en tehlikeli güvenlik açıklarından biridir. Bu makalede, Zero Day açıklarının ne olduğunu, nasıl keşfedildiğini ve potansiyel etkilerini inceliyoruz.</p>
                            <p><small>Yayınlanma Tarihi: 10 Mayıs 2025 | Yazar: ****** ******</small></p>
                            <a href="/blog/zero-day-aciklari" class="btn">Devamını Oku</a>
                        </div>
                    </div>
                    
                    <div class="blog-item">
                        <div class="blog-item-image">
                            <img src="/static/images/blog/2.jpg" alt="Siber Saldırılar">
                        </div>
                        <div class="blog-item-content">
                            <h3>CTF Yarışmaları İçin Hazırlık</h3>
                            <p>Capture The Flag yarışmaları, siber güvenlik becerilerinizi test etmenin ve geliştirmenin en eğlenceli yollarından biridir. Bu makalede, CTF yarışmalarına nasıl hazırlanabileceğinizi ve başarılı olmanız için gereken teknikleri paylaşıyoruz.</p>
                            <p><small>Yayınlanma Tarihi: 5 Mayıs 2025 | Yazar: ****** ******</small></p>
                            <a href="/blog/ctf-egitimi" class="btn">Devamını Oku</a>
                        </div>
                    </div>
                    
                    <div class="blog-item">
                        <div class="blog-item-image">
                            <img src="/static/images/blog/3.jpg" alt="Siber Saldırılar">
                        </div>
                        <div class="blog-item-content">
                            <h3>Red Team Operasyonları</h3>
                            <p>Red Team operasyonları, kurumların güvenlik durumunu gerçekçi saldırı senaryoları ile test etmek için kullanılan önemli bir yöntemdir. Bu makalede, Red Team operasyonlarının nasıl planlandığını ve yürütüldüğünü detaylı bir şekilde anlatıyoruz.</p>
                            <p><small>Yayınlanma Tarihi: 1 Mayıs 2025 | Yazar: ****** ******</small></p>
                            <a href="/blog/red-team-operasyonlari" class="btn">Devamını Oku</a>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <footer>
            <p>Yavuzlar Blog &copy; 2025</p>
        </footer>
    </body>
    </html>
    '''
    return template

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

    