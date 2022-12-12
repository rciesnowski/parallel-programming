import socket

HOST = '127.0.0.1'
PORT = 5000

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    print("połączono")
    liczba = input("podaj liczbę: ")
    s.sendall(liczba.encode('utf-8'))
    print("wysyłam liczbe")
    data = s.recv(32)

print("otrzymano wynik liczba**2 + 2: ", data.decode('utf-8'))