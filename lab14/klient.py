import socket

host = "127.0.0.1"
port = 5000
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def drukuj_plansze(plansza):
    plansza_str = " \t   1 2 3 4 5 6 7 8 \n\t1 "
    licznik = 0
    for znak in plansza:
        if licznik % 8 == 0 and licznik != 0:
            plansza_str += "|\n\t" + str((licznik//8) + 1) + " "
        if znak == "0":
            plansza_str += "|_"
            licznik += 1
        elif znak == "1":
            plansza_str += "|X"
            licznik += 1
        elif znak == "2":
            plansza_str += "|O"
            licznik += 1
        elif znak == "3":
            plansza_str += "|▓"
            licznik += 1
    return plansza_str + "|"

def wyslij_ruch():
    play_or_wait = s.recv(1024).decode()
    if play_or_wait == "GRAMY":
        print("twój ruch")
        row = input("wiersz: \t")
        col = input("kolumna:\t")
        while type(row) != int and type(col) != int:
            try: 
                row = int(row)
                col = int(col)
            except:
                print("wiersz i kolumna muszą być liczbami 1-8")
                row = input("wiersz: \t")
                col = input("kolumna:\t")
        while row not in range(1,9) or col not in range(1,9):
            print("wiersz i kolumna muszą być liczbami 1-8")
            row = int(input("wiersz: \t"))
            col = int(input("kolumna:\t"))
        s.send(str(row).encode())
        s.send(str(col).encode())
        return True
    elif play_or_wait == "CZEKAJ":
        print("poczekaj na swoją kolej")
        return False


s.connect((host, port))
start_or_wait = s.recv(1024).decode()
if start_or_wait == "CZEKAJ":
    print("czekaj na drugiego gracza")
    start_or_wait = s.recv(1024).decode()
if start_or_wait == "START":
    while True:
        game_play = s.recv(1024).decode()
        if game_play == "GRAMY":
            s.send("OK".encode())
            player_playing = wyslij_ruch()
            if player_playing:
                is_placed = s.recv(1024).decode()
                while is_placed == "ZAJETE":
                    print("miejsce zajęte")
                    wyslij_ruch()
                    is_placed = s.recv(1024).decode()
            board = s.recv(1024).decode()
            while board == "CZEKAJ":
                board = s.recv(1024).decode()
            s.send("OK".encode())
            print(drukuj_plansze(board))
            if '0' not in board:
                if player_playing:
                    print("\n\tWygrałeś")
                    break
                else:
                    print("\n\tPrzegrałeś")
                    break
    s.close()


