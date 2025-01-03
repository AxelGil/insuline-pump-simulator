import sqlite3
from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def home():
  return "Welcome to the DexCom Clarity Microservice!"

@app.route("/analyser", methods=['GET'])
def analyser():
  conn = sqlite3.connect('my_database.db')
  cursor = conn.cursor()
  
  cursor.execute("SELECT * FROM user_basal_rate WHERE id_user = ?", (request.json.get("user_id"),))
  data = cursor.fetchall()
  conn.close()
  
  basal_rates = [rate[1] for rate in data]
  
  average_basal_rates = sum(basal_rates) / len(basal_rates)
  
  if average_basal_rates < 70:
    print(f"(Dexcom Clarity)la moyenne de taux glycémique est trop bas: {average_basal_rates:.2f} mg/dL")
    return f"la moyenne de taux glycémique est trop bas: {average_basal_rates:.2f} mg/dL"
  elif average_basal_rates > 180:
    print(f"(Dexcom Clarity)la moyenne de taux glycémique est trop haut: {average_basal_rates:.2f} mg/dL")
    return f"la moyenne de taux glycémique est trop haut: {average_basal_rates:.2f} mg/dL"
  else:
    print(f"(Dexcom Clarity)la moyenne de taux glycémique est normal: {average_basal_rates:.2f} mg/dL")
    return f"la moyenne de taux glycémique est normal: {average_basal_rates:.2f} mg/dL"

if __name__ == '__main__':
  app.run(host="0.0.0.0", port=5002)