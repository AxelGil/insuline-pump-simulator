# App insuline pump simulator

## run script

python -m venv venv

venv\Scripts\activate

pip install Flask

pip install -r requirements.txt

python run.py

to stop -> new terminal : taskkill /F /IM python.exe

## run tests

python -m unittest discover -s tests -v

test TP3 : pytest tests/tests_nom_app.py

Corentin Laurent - Axel GIL

Nous avons utilisé Chatgpt pour implémenter les classes et gagner du temps, comprendre certaines partie du sujet et surtout lire certaines erreurs qui était compliqué à lire pour la plupart (pour des nivices de python)
