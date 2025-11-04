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



