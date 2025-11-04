# app.py
import time
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    """
    Endpoint principale che simula un'operazione
    che richiede un po' di tempo (es. una query al database).
    """
    try:
        # Simula 500ms di lavoro
        time.sleep(0.5) 
        return jsonify({"status": "ok", "message": "Lavoro completato!"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    # Esegui l'app. 
    # 'threaded=True' permette a Flask di gestire più richieste 
    # contemporaneamente (in thread separati), che è fondamentale 
    # per il nostro test.
    print("Avvio del server Flask su http://127.0.0.1:5000")
    app.run(host='127.0.0.1', port=5000, debug=False, threaded=True)