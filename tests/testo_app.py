# test_carico.py
import requests
import time
import argparse
import concurrent.futures

# L'URL del nostro server
TARGET_URL = "http://127.0.0.1:5000/"

def fetch_url(url):
    """
    Funzione per eseguire una singola richiesta HTTP.
    Restituisce True se la richiesta ha successo (HTTP 200), False altrimenti.
    """
    try:
        response = requests.get(url, timeout=10) # Timeout di 10 sec
        return response.status_code == 200
    except requests.RequestException:
        # Gestisce errori di connessione, timeout, ecc.
        return False

def run_test(num_requests):
    """
    Esegue un test inviando 'num_requests' richieste in parallelo.
    """
    print(f"--- Test con {num_requests} richieste parallele ---")
    
    success_count = 0
    failure_count = 0
    
    start_time = time.time()
    
    # Usiamo un ThreadPoolExecutor per inviare richieste in parallelo.
    # 'max_workers' è impostato al numero di richieste che vogliamo
    # inviare simultaneamente.
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_requests) as executor:
        
        # Sottomettiamo tutti i task (le richieste) al pool
        futures = [executor.submit(fetch_url, TARGET_URL) for _ in range(num_requests)]
        
        # Raccogliamo i risultati man mano che sono pronti
        for future in concurrent.futures.as_completed(futures):
            if future.result():
                success_count += 1
            else:
                failure_count += 1
                
    end_time = time.time()
    
    total_time = end_time - start_time
    
    # Calcoliamo le performance
    # Richieste al secondo (Requests Per Second)
    rps = num_requests / total_time if total_time > 0 else float('inf')
    
    print(f"Completato in: {total_time:.4f} secondi")
    print(f"Richieste totali: {num_requests}")
    print(f"  - Successo: {success_count}")
    print(f"  - Fallite:  {failure_count}")
    print(f"Performance:  {rps:.2f} RPS (Richieste al Secondo)")
    print("--------------------------------------------------\n")

def main():
    parser = argparse.ArgumentParser(description="Script per test di carico base.")
    parser.add_argument('-m', '--min', type=int, required=True, 
                        help="Numero minimo di richieste parallele.")
    parser.add_argument('-x', '--max', type=int, required=True, 
                        help="Numero massimo di richieste parallele.")
    parser.add_argument('-s', '--step', type=int, required=True, 
                        help="Incremento del numero di richieste ad ogni passo.")
    
    args = parser.parse_args()

    if args.min > args.max:
        print("Errore: 'min' non può essere maggiore di 'max'")
        return

    print(f"Avvio test di carico su {TARGET_URL}")
    print(f"Configurazione: Min={args.min}, Max={args.max}, Step={args.step}\n")

    # Ciclo di test: da 'min' a 'max' con incremento 'step'
    for num_req in range(args.min, args.max + 1, args.step):
        run_test(num_req)
        time.sleep(1) # Pausa di 1 sec tra i test per far "respirare" il server

if __name__ == "__main__":
    main()