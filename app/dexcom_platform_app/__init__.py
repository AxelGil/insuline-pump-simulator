from flask import Flask, request
import requests

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
  return "Welcome to the dexcom_platform Microservice!"

@app.route('/transmettre', methods=['POST'])
def transmettre():
  taux_glucose = request.json.get("taux_glucose")
  user_id = request.json.get("user_id")
  
  if not taux_glucose:
    return {"error": "taux_glucose is required"}, 400
  
  if not user_id:
    return {"error": "user_id is required"}, 400
  
  check = checkBasalRate(int(taux_glucose))
  if check is not None:
    transmettre_recepteur_dedie(check)
  addicherDonnées(taux_glucose)
  return transmettre_dexcom_platform(taux_glucose, user_id)

def transmettre_dexcom_platform(taux_glucose, user_id):
    payload = {"taux_glucose": taux_glucose, "user_id": user_id}
    try:
        responseClarity = requests.get("http://127.0.0.1:5002/analyser", json=payload)
        responseClarity.raise_for_status()
        responseFollow = requests.get("http://127.0.0.1:5003/suivredonnee", json=payload)
        responseFollow.raise_for_status()
        
        return {
            "responseClarity": responseClarity.json(),
            "responseFollow": responseFollow.json()
        }
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}
      
def addicherDonnées(taux_glucose):
    print(f"(afficher sur dexcom platform) Le taux de glucose est de {taux_glucose}")
    
def checkBasalRate(taux_glucose):
    if taux_glucose < 70:
      return "Le taux glycémique est trop bas"
    elif taux_glucose > 180:
        return "Le taux glycémique est trop haut"
    else:
        return None
      
def transmettre_recepteur_dedie(alerte):
    payload = {"alerte": alerte}
    try:
        response = requests.post("http://127.0.0.1:5006/alerte", json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

if __name__ == '__main__':
  app.run(host="127.0.0.1", port=5004)