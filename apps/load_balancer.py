# load_balancer.py
from flask import Flask, request, jsonify
import requests
import itertools  # Useremo questo per il Round Robin

app = Flask(__name__)

# --- CONFIGURAZIONE ---
# La lista dei nostri server "backend".
# Per ora è statica. Nei passi successivi, 
# la renderemo dinamica con il Service Discovery!
BACKEND_SERVERS = [
    "http://127.0.0.1:5001",
    "http://127.0.0.1:5002",
    # Puoi aggiungerne altri! Es: "http://127.0.0.1:5003"
]

# Creiamo un "iteratore ciclico" che ci darà
# un server diverso ad ogni chiamata, ricominciando 
# da capo alla fine della lista.
server_pool = itertools.cycle(BACKEND_SERVERS)
# --------------------

@app.route('/')
def forward_request():
    """
    Questa è l'unica rotta del nostro LB.
    Intercetta la richiesta, sceglie un server backend, 
    inoltra la richiesta e restituisce la sua risposta.
    """
    target_server = None
    try:
        # 1. Scegli il prossimo server dalla lista (Round Robin)
        target_server = next(server_pool)
        
        # print(f"Inoltro richiesta a: {target_server}") # Utile per il debug
        
        # 2. Inoltra la richiesta GET al server scelto
        # (Un vero LB copierebbe metodo, header, body, ecc.)
        response = requests.get(target_server, timeout=10)
        
        # 3. Restituisce la risposta esatta del backend
        return response.content, response.status_code
        
    except requests.RequestException as e:
        # Se un server è down, lo segnaliamo.
        error_msg = f"Errore: Impossibile connettersi a {target_server}"
        print(error_msg, e)
        # 503 Service Unavailable: un codice HTTP appropriato
        return jsonify({"status": "error", "message": error_msg}), 503

if __name__ == '__main__':
    print(f"Avvio del Load Balancer su http://127.0.0.1:5000")
    print(f"Server Backend: {BACKEND_SERVERS}")
    # Eseguiamo anche il LB in modalità threaded per
    # non essere lui stesso il collo di bottiglia.
    app.run(host='127.0.0.1', port=5000, threaded=True)