# esercitazione-sistemi-distribuiti-quinta-tpsit
Proposta di lezione pratica  sui sistemi distribuiti per una quinta ITIA - Tecnologie di progettazione di sistemi informatici e di telecomunicazioni


## Prerequisiti

- Python 3.x
- Flask
- Requests

## Setup 

1. Clona il repository:
   ```bash
   git clone https://github.com/tuo-username/esercitazione-sistemi-distribuiti-quinta-tpsit.git
    cd esercitazione-sistemi-distribuiti-quinta-tpsit
    ``` 
2. Installa le dipendenze:
    ```bash
    pip install -r requirements.txt
    ```
3. Avvia l'applicazione Flask:
    ```bash
    python apps/app.py
    ```
4. Apri il browser e vai a `http://localhost:5000` per vedere l'app in azione.
5. Esegui gli script di test per verificare il funzionamento:
    ```bash
    python tests/test_app.py
    ```

## Descrizione
Questa esercitazione dimostra come creare un'applicazione web semplice utilizzando Flask, che simula operazioni asincrone e gestisce richieste HTTP. Include anche script di test per verificare il corretto funzionamento dell'applicazione.

## Passo 1

Eseguendo il file `apps/app.py`, viene avviato un server Flask che espone un endpoint `/do_work`. Quando questo endpoint viene chiamato, simula un'operazione che richiede tempo (ad esempio, una query al database) e restituisce una risposta JSON. mediante il programma di test `tests/test_app.py`, viene inviata una richiesta HTTP a questo endpoint per verificare che l'operazione venga completata correttamente e che la risposta sia quella attesa. In particolare dovrà essere chiamanto con dei paramtri che sono:
- min: numero minimo di richieste da inviare
- max: numero massimo di richieste da inviare
- step: passo con cui incrementare il numero di richieste da inviare

ad esempio per inviare da 1 a 10 richieste con passo 2 si dovrà eseguire:
```bash
python tests/test_app.py --min 1 --max 10 --step 2
```

prova a fare in modo che vengano eseguiti  da 100 a 1000 con passo 100:
```bash
python tests/test_app.py --min 100 --max 1000 --step 100
```

scoprirai che il server non inizia a rallentare come ci si aspetterebbe. Qeusto perchè il lavoro che stiamo simulando (utilizzando la `time.sleep(0.5)`) blocca ma non utilizza la CPU.

Se vogliamo  vedere i problemi di scalabilità dobbiamo fare in modo che il lavoro sia CPU bound. Per fare questo modifica il file `apps/app.py` in modo che invece di usare `time.sleep(0.5)` esegua un calcolo intensivo della CPU, ad esempio calcolando i numeri primi fino a un certo limite. Esegui nuovamente i test per osservare come il server gestisce un carico di richieste crescente.

prova a realizzare tu stesso una modifica che simuli un lavoro CPU bound, poi vedi una mia proposta facendo checkout del branch `cpu-bound`:

```bash
git checkout cpu-bound
```

Come potrai vedere , ho sostituito la chiamata a `time.sleep(0.5)` con un calcolo intensivo della CPU (ad esempio, calcolando la somma dei quadrati di un grande intervallo di numeri). Esegui nuovamente i test per osservare come il server gestisce un carico di richieste crescente in questo scenario CPU-bound.

Quello che vedrai esendo i test è che il server inizia a rallentare significativamente

```bash
python .\tests\testo_app.py --min 100 --max 1000 --step 100
Avvio test di carico su http://127.0.0.1:5000/
Configurazione: Min=100, Max=1000, Step=100

--- Test con 100 richieste parallele ---
Completato in: 10.1261 secondi
Richieste totali: 100
  - Successo: 97
  - Fallite:  3
Performance:  9.88 RPS (Richieste al Secondo)
--------------------------------------------------

--- Test con 200 richieste parallele ---
Completato in: 10.1296 secondi
Richieste totali: 200
  - Successo: 99
  - Fallite:  101
Performance:  19.74 RPS (Richieste al Secondo)
--------------------------------------------------
```

Ecco il nostro problema, abbiamo raggiunto un punto in cui il server non riesce a gestire il carico di richieste a causa del lavoro intensivo della CPU. 

ABBIAMO ROTTO IL SERVER!! E ADESSO?

Lo strumento per risolvere questo problema è un load balancer, che distribuisce le richieste tra più istanze del server, permettendo di sfruttare meglio le risorse di sistema e migliorare la scalabilità. Creeremo il nostro load balancer semplicemente utilizzando Flask e il modulo `requests` per inoltrare le richieste alle istanze del server. Modifico anche il gile apps/app.py per porter decidere su che porta avviare il server.

Prova ad avviare più istanze del server Flask su porte diverse:

```bash
python apps/app.py --port 5000
python apps/app.py --port 5001
python apps/app.py --port 5002
```

Ora dobbiamo creare il load balancer. Come potrebbe essere realizzato? Prova a farlo tu stesso, poi vedi la mia proposta facendo checkout del branch `load-balancer`:

```bash
git checkout load-balancer
```