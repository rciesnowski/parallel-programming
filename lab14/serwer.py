import socket

host = '127.0.0.1'
port = 5000
gracze = []

#plansza = [[3] * 8 for _ in range(8)]
#plansza[3][3] = 0
plansza = [[0] * 8 for _ in range(8)]
aktywny_gracz = 0


def wyslij_graczom(msg):
    for gracz in gracze:
        gracz.send(msg.encode())


def plansza_string():
    return "PLANSZA" + ''.join(''.join([str(e) for e in w]) for w in plansza)


def czy_koniec():
    for w in plansza:
        for z in w:
            if z == 0:
                return False
    return True


def plansza_list():
    return [e for w in plansza for e in w]


def pobierz_ruch():
    global aktywny_gracz
    for client in gracze:
        if gracze[aktywny_gracz] == client:
            client.send("GRAMY".encode())
        elif gracze[aktywny_gracz - 1] == client or gracze[aktywny_gracz + 1] == client:
            client.send("CZEKAJ".encode())
    row = gracze[aktywny_gracz].recv(1024).decode()
    col = gracze[aktywny_gracz].recv(1024).decode()
    return row, col


def zmiana_gracza():
    global aktywny_gracz
    if aktywny_gracz == 0:
        aktywny_gracz = 1
    elif aktywny_gracz == 1:
        aktywny_gracz = 0


def czy_puste(row, col):
    return plansza[row - 1][col - 1] == 0


def aktualizuj_plansze(row, col):
    if aktywny_gracz == 0:
        sign = 1
    else:
        sign = 2
    row = row - 1
    col = col - 1
    rows = [row - 1, row, row + 1]
    cols = [col - 1, col, col + 1]
    for r in rows:
        for c in cols:
            if r in range(0, 8) and c in range(0, 8):
                plansza[r][c] = 3
    plansza[row][col] = sign


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))
s.listen()
print("czekam na graczy...")
gracz_1, addr = s.accept()
gracze.append(gracz_1)
print("gracz pierwszy połączony")
gracz_1.send("CZEKAJ".encode())
gracz_2, addr = s.accept()
gracze.append(gracz_2)
print("gracz drugi połączony")
wyslij_graczom("START")
print("gra trwa")

try:
    game_play = True
    board_ready_to_send = False
    while game_play:
        if czy_koniec():
            print("koniec gry")
            break
        else:
            wyslij_graczom("GRAMY")
        for gracz in gracze:
            gracz.recv(1024).decode()
        row_col = pobierz_ruch()
        row = int(row_col[0])
        col = int(row_col[1])
        is_empty = czy_puste(row, col)
        while not is_empty:
            gracze[aktywny_gracz].send("ZAJETE".encode())
            row_col = pobierz_ruch()
            row = int(row_col[0])
            col = int(row_col[1])
            is_empty = czy_puste(row, col)
        if is_empty:
            aktualizuj_plansze(row, col)
            gracze[aktywny_gracz].send("OK".encode())
            board_ready_to_send = True
        if board_ready_to_send:
            str_board = plansza_string()
            wyslij_graczom(str_board)
        for gracz in gracze:
            gracz.recv(1024).decode()
        zmiana_gracza()
except ConnectionAbortedError:
    print("koniec")
    s.close()
except ConnectionResetError:
    print("użytkownicy rozłączyli się")
    s.close()