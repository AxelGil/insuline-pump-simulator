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
  
  user_id = request.json.get("user_id")
  
  # Vérifier si user_id est présent et est un entier valide
  if not user_id:
    return {"error": "user_id is required"}, 400 
    
  if not isinstance(user_id, int):
    return {"error": "user_id must be an integer"}, 404
  
  cursor.execute("SELECT * FROM user_basal_rate WHERE id_user = ?", (user_id,))
  data = cursor.fetchall()
  conn.close()
  
  if not data:
      return {"error": "No basal rates found for user_id {}".format(user_id)}, 404
  
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