import sqlite3
from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def home():
  return "Welcome to the dexcom_follow Microservice!"

@app.route("/suivredonnee", methods=['GET'])
def suivredonnee():
  
  conn = sqlite3.connect('my_database.db')
  cursor = conn.cursor()
  
  cursor.execute("SELECT * FROM user_basal_rate WHERE id_user = ?", (request.json.get("user_id"),))
  data = cursor.fetchall()
  conn.close()
  
  basal_rates = [rate[1] for rate in data]
  
  print(f"affichage Follow : {basal_rates}")
  exportFile(basal_rates)
  
  return basal_rates

def exportFile(basal_rates):
  file_path = "basal_rates.txt" 

  with open(file_path, "w") as f:
      for rate in basal_rates:
          f.write(f"{rate}\n")
  

if __name__ == '__main__':
  app.run(host="0.0.0.0", port=5003)