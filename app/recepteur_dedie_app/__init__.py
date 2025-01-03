from flask import Flask, request
import requests

app = Flask(__name__)

@app.route('/')
def home():
  return "Welcome to the pompe_insuline Microservice!"

@app.route('/transmettre', methods=['POST'])
def transmettre():
  taux_glucose = request.json.get("taux_glucose")
  addicherDonnées(taux_glucose)
  return transmettre_dexcom_platform(taux_glucose, request.json.get("user_id"))
  
def transmettre_dexcom_platform(taux_glucose, user_id):
    payload = {"taux_glucose": taux_glucose, "user_id": user_id}
    try:
        response = requests.post("http://127.0.0.1:5004/transmettre", json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}
      
def addicherDonnées(taux_glucose):
    print(f"(afficher sur recepteur dedie) Le taux de glucose est de {taux_glucose}")
    
@app.route('/alerte', methods=['POST'])
def alerte():
  alerte = request.json.get("alerte")
  print(f"Alerte reçue : {alerte}")
  return(f"Alerte reçue : {alerte}")

if __name__ == '__main__':
  app.run(host="127.0.0.1", port=5006)