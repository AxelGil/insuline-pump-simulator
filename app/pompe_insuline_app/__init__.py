from flask import Flask, jsonify, request

from .pompe_insuline import PompeInsuline

app = Flask(__name__)

@app.route('/ajuster', methods=['POST'])
def ajuster():
    data = request.json
    taux_glucose = data.get("taux_glucose")
    if taux_glucose is None:
        return jsonify({"error": "Taux de glucose manquant"}), 400

    action = PompeInsuline.ajusterTraitementAutomatique(taux_glucose)
    
    return jsonify({
        "taux_glucose": taux_glucose,
        "action": action
    })

if __name__ == '__main__':
  app.run(host="127.0.0.1", port=5005)