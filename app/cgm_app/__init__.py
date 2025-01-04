import random
import sqlite3
from flask import Flask, jsonify, request
from .cgm import CapteurGlucose
import requests

app = Flask(__name__)


@app.route('/mesurer', methods=['GET'])
def mesurer():
    conn = sqlite3.connect('my_database.db')
    cursor = conn.cursor()
    
    taux_glucose = random.randint(60, 180)
    user_id = request.args.get("user_id")
    if not user_id:
        conn.close()
        return jsonify({"error": "Identifiant is missing"}), 400
      
    try:
        user_id = int(user_id)
    except ValueError:
        conn.close()
        return jsonify({"error": "Identifiant must be an integer"}), 400
      
    cursor.execute("INSERT INTO user_basal_rate (id_user, basal_rate) VALUES (?, ?)", (user_id, taux_glucose))
    conn.commit()
    conn.close()
    
    pompe_insuline_url = "http://127.0.0.1:5005"
    
    pompe_response = transmettre_a_la_pompe(taux_glucose, pompe_insuline_url)
    transmettre_recepteur_dedie(taux_glucose, user_id)
    
    return jsonify({"taux_glucose": taux_glucose, "pomp_response": pompe_response})
  
def transmettre_a_la_pompe(taux_glucose, pompe_url):
    payload = {"taux_glucose": taux_glucose}
    try:
        response = requests.post(f"{pompe_url}/ajuster", json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}
      
def transmettre_recepteur_dedie(taux_glucose, user_id):
    payload = {"taux_glucose": taux_glucose, "user_id": user_id}
    try:
        response = requests.post("http://127.0.0.1:5006/transmettre", json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}
      
      
@app.route('/configurer', methods=['POST'])
def configurer():
  CapteurGlucose.configurer()

      
@app.route('/')
def home():
  return "Welcome to the cgm_app Microservice!"

if __name__ == '__main__':
  app.run(host="127.0.0.1", port=5001)