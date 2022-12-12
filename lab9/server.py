import socket

HOST = '127.0.0.1'
PORT = 5000

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print("uruchomiono, nasłuchuję")
    conn, addr = s.accept()
    with conn:
        while True:
            data = conn.recv(32)
            if not data:
                break
            print("otrzymano liczbę: ", data.decode('utf-8'))
            wynik = str(int(data)**2 + 2)
            conn.sendall(wynik.encode('utf-8'))