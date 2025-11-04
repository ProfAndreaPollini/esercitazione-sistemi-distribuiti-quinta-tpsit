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
python apps/app.py --port 5001
python apps/app.py --port 5002
```

Ora dobbiamo creare il load balancer. Come potrebbe essere realizzato? Prova a farlo tu stesso, poi vedi la mia proposta facendo checkout del branch `load-balancer`:

```bash
git checkout load-balancer
```

In questo branch, ho creato un semplice load balancer che distribuisce le richieste tra le istanze del server Flask in modo round-robin. Ora puoi eseguire nuovamente i test per vedere come il load balancer migliora la gestione del carico di richieste.

```bash
python .\tests\testo_app.py --min 10 --max 100 --step 10   
warning: `VIRTUAL_ENV=.venv` does not match the project environment path `C:\Users\profa\Documents\GitHub\.venv` and will be ignored
Avvio test di carico su http://127.0.0.1:5000/
Configurazione: Min=10, Max=100, Step=10

--- Test con 10 richieste parallele ---
Completato in: 0.6201 secondi
Richieste totali: 10
  - Successo: 10
  - Fallite:  0
Performance:  16.13 RPS (Richieste al Secondo)
--------------------------------------------------

--- Test con 20 richieste parallele ---
Completato in: 1.2145 secondi
Richieste totali: 20
  - Successo: 20
  - Fallite:  0
Performance:  16.47 RPS (Richieste al Secondo)
--------------------------------------------------

--- Test con 30 richieste parallele ---
Completato in: 1.8119 secondi
Richieste totali: 30
  - Successo: 30
  - Fallite:  0
Performance:  16.56 RPS (Richieste al Secondo)
--------------------------------------------------

--- Test con 40 richieste parallele ---
Completato in: 2.4094 secondi
Richieste totali: 40
  - Successo: 40
  - Fallite:  0
Performance:  16.60 RPS (Richieste al Secondo)
--------------------------------------------------

--- Test con 50 richieste parallele ---
Completato in: 3.0365 secondi
Richieste totali: 50
  - Successo: 50
  - Fallite:  0
Performance:  16.47 RPS (Richieste al Secondo)
--------------------------------------------------

--- Test con 60 richieste parallele ---
Completato in: 3.5907 secondi
Richieste totali: 60
  - Successo: 60
  - Fallite:  0
Performance:  16.71 RPS (Richieste al Secondo)
--------------------------------------------------

--- Test con 70 richieste parallele ---
Completato in: 4.1629 secondi
Richieste totali: 70
  - Successo: 70
  - Fallite:  0
Performance:  16.82 RPS (Richieste al Secondo)
--------------------------------------------------

--- Test con 80 richieste parallele ---
Completato in: 4.7324 secondi
Richieste totali: 80
  - Successo: 80
  - Fallite:  0
Performance:  16.90 RPS (Richieste al Secondo)
```

In questo modo, abbiamo migliorato significativamente la capacità del sistema di gestire un carico di richieste elevato utilizzando un semplice load balancer. Nota che per un'applicazione di produzione, si dovrebbe considerare l'uso di soluzioni di load balancing più robuste e scalabili come Nginx, HAProxy o servizi cloud dedicati.

**Analizziamo insieme cosa stai vedendo:**

**Tempo di Calcolo:**

- Con 10 richieste, il tempo totale è 0.62s. Il LB le divide: 5 al server 1, 5 al server 2. Lavorando in parallelo, il test finisce quando entrambi hanno gestito le loro 5 richieste.

- Con 20 richieste (10 per server), il tempo è 1.21s (circa il doppio).

- Con 30 richieste (15 per server), il tempo è 1.81s (circa il triplo).

Possiamo stimare che il tuo heavy_computation impieghi circa 120ms (0.12 secondi) sulla tua macchina.

**Performance (RPS):**

Se un server impiega 0.12s per richiesta, la sua capacità massima (il suo "tetto") è: 1 / 0.120s = ~8.3 RPS.

Con un solo server (Passo 1, CPU-bound), avresti visto le performance crollare e stabilizzarsi proprio intorno a 8-9 RPS.

Tu hai due server. La tua capacità teorica totale è: 8.3 RPS * 2 = ~16.6 RPS.

**Le tue performance si stabilizzano esattamente intorno a 16.1 - 16.9 RPS.**

Hai dimostrato che aggiungendo un secondo server e un load balancer hai raddoppiato la capacità di carico del tuo sistema. Non importa quante richieste aggiungi (fino a 100 nel test), il sistema non può andare più veloce di ~16.6 RPS, perché tutte le tue risorse (i 2 server) sono sature al 100%.

il problema ora resta quello della lista statica dei server nel load balancer. In un sistema reale, vorresti che il load balancer scoprisse dinamicamente le istanze del server (ad esempio, tramite un servizio di registrazione o un orchestratore come Kubernetes) piuttosto che avere una lista hardcoded.

Noi risolveremo il problema introducendo un servizio di discovery, ma questa è un'altra storia! 

per vedere il branch successivo con il servizio di discovery fai:

```bash
git checkout service-discovery
```