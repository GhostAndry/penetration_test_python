import socket
import threading

# Funzione per gestire la connessione di un singolo client
def handle_client(client_socket, address):
    while True:
        # Ricevi dati dal client
        request = client_socket.recv(1024).decode('utf-8')

        # Se il client si disconnette o invia 'exit', chiudi la connessione
        if not request or request.lower() == 'exit':
            print("Client", address, "disconnesso")
            clients.remove(client_socket)
            break
        else:
            print("Messaggio ricevuto dal client", address, ":", request)

            # Invia conferma al client
            client_socket.send("Messaggio ricevuto dal server".encode('utf-8'))

    # Chiudi la connessione con il client
    client_socket.close()

# Funzione per inviare un messaggio a tutti i client connessi
def send_message_to_clients(message):
    for client in clients:
        try:
            client.send(message.encode('utf-8'))
        except Exception as e:
            print("Errore durante l'invio del messaggio:", e)

# Funzione per avviare il server
def start_server(ip, port, threads):
    global server_running
    global server

    # Controlla se il server è già in esecuzione
    if server_running:
        print("Il server è già in esecuzione.")
        return

    # Crea il socket del server
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((ip, port))
    server.listen()

    print("Server in ascolto su", ip, "porta", port)

    # Avvia i thread per gestire i client
    for _ in range(threads):
        client_thread = threading.Thread(target=handle_clients)
        client_thread.daemon = True
        client_thread.start()

    server_running = True

    # Thread per accettare nuove connessioni
    accept_thread = threading.Thread(target=accept_connections)
    accept_thread.daemon = True
    accept_thread.start()

# Funzione per gestire i client
def handle_clients():
    while True:
        if not server_running:
            break

        if clients:
            client_socket, client_address = clients.pop(0)
            handle_client(client_socket, client_address)

# Funzione per accettare nuove connessioni
def accept_connections():
    global server_running

    while True:
        if not server_running:
            break

        # Accetta una nuova connessione
        client_socket, client_address = server.accept()
        print("Connessione da:", client_address)

        # Aggiungi il client alla lista dei client connessi
        clients.append((client_socket, client_address))

# Funzione per fermare il server
def stop_server():
    global server_running
    global server

    # Controlla se il server è in esecuzione
    if not server_running:
        print("Il server non è in esecuzione.")
        return

    # Chiudi il socket del server
    server.close()
    server_running = False
    print("Server fermato.")

# Funzione principale del server
def main():
    while True:
        print("\nMenu:")
        print("1. Avvia server")
        print("2. Ferma server")
        print("3. Invia messaggio ai client")
        print("4. Esci")

        choice = input("Seleziona un'opzione: ")

        if choice == '1':
            ip = input("Inserisci l'indirizzo IP del server: ")
            port = int(input("Inserisci il numero di porta del server: "))
            threads = int(input("Inserisci il numero di thread per gestire i client: "))
            start_server(ip, port, threads)
        elif choice == '2':
            stop_server()
        elif choice == '3':
            message = input("Inserisci il messaggio da inviare ai client: ")
            send_message_to_clients(message)
        elif choice == '4':
            stop_server()
            break
        else:
            print("Opzione non valida.")

# Variabili globali
server_running = False
server = None
clients = []

# Avvia il programma
if __name__ == "__main__":
    main()
