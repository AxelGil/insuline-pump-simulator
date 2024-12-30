from flask import Flask

from app.dexcom_platform_app.dexcom_platform import DexcomPlatform

app = Flask(__name__)

dexcom_platform = DexcomPlatform

@app.route('/', methods=['GET'])
def home():
  return "Welcome to the dexcom_platform Microservice!"

@app.route('/user_basal_rate/<int:id>', methods=['GET'])
def user_basal_rate(id):
  return dexcom_platform.getDonneeUser(id)

@app.route('/user_basal_rate/<int:id>', methods=['POST'])
def new_user_basal_rate(id, data):
  return dexcom_platform.synchroniserDonnees(id, data.basal_rate)

if __name__ == '__main__':
  app.run(host="127.0.0.1", port=5003)