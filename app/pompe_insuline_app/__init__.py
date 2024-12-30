from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
  return "Welcome to the pompe_insuline Microservice!"

if __name__ == '__main__':
  app.run(host="127.0.0.1", port=5004)