import socket
import threading

# Funzione per gestire i messaggi dal server
def receive_messages_from_server(client_socket):
    while True:
        # Ricevi dati dal server
        message = client_socket.recv(1024).decode('utf-8')

        # Se il messaggio è vuoto, il server si è disconnesso
        if not message:
            print("Il server si è disconnesso.")
            break
        print("Messaggio dal server:", message)

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
