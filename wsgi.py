from main import app

if __name__ == '__main__':
    app.run()

#gunicorn --bind 127.0.0.1:5000 wsgi:app