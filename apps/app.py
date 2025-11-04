# app.py
import time
import argparse
from flask import Flask, jsonify

app = Flask(__name__)


@app.route('/')
def home():
    """
    Endpoint principale che simula un'operazione
    che richiede un po' di tempo (es. una query al database).
    """
    try:

        start_time = time.time()
        result = sum(i * i for i in range(10**6))
        print(f"Risultato del calcolo: {result}")
        end_time = time.time()
        duration = end_time - start_time
        
        return jsonify({
            "status": "ok", 
            "message": "Lavoro completato!",
            "duration_sec": duration
        }), 200


    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


if __name__ == '__main__':
    # Aggiungiamo un parser per gli argomenti
    parser = argparse.ArgumentParser(description="Server app Flask CPU-Bound")
    parser.add_argument('--port', type=int, default=5000, 
                        help="Porta su cui eseguire il server.")
    args = parser.parse_args()
    
    print(f"Avvio del server Flask (CPU-BOUND) su http://127.0.0.1:{args.port}")
    app.run(host='127.0.0.1', port=args.port, debug=False, threaded=True)