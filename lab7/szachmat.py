import sys
import sysv_ipc
import os
import random

moj_znak = ''
przec_znak = ''

def zakoncz(pam, moj_sem, przec_sem):
    przec_sem.release()
    moj_sem.remove()
    przec_sem.remove()
    pam.remove()

def drukuj(pam):
    print('\t1\t2\t3', end='')
    for i, znak in enumerate(pam.read()):
        if (i) % 3 == 0:
            print('\n', i//3, end=' ')
        print(chr(znak), end='\t|')

def ruch(pam):
    while True:
        move = int(input('\ntwoj ruch (1-9): ')) - 1
        field = pam.read(1, move)
        if field == b'\x00':
            return move
        else:
            print('zajete')

def warunki(plansza, znak):
    if plansza[0] == plansza[3] == plansza[6] == znak:
        return True
    elif plansza[1] == plansza[4] == plansza[7] == znak:
        return True
    elif plansza[2] == plansza[5] == plansza[8] == znak:
        return True
    elif plansza[0] == plansza[1] == plansza[2] == znak:
        return True
    elif plansza[3] == plansza[4] == plansza[5] == znak:
        return True
    elif plansza[6] == plansza[7] == plansza[8] == znak:
        return True
    elif plansza[0] == plansza[4] == plansza[8] == znak:
        return True
    elif plansza[2] == plansza[4] == plansza[6] == znak:
        return True
    #    elif '' not in plansza.values():
 #       return None
    else:
        return False
        
def czy_remis(plansza):
    if all((znak == 'x' or znak == 'o') for znak in plansza.values()):
        return True
    else:
        return False
    

def sprawdz(pam, moj_sem, przec_sem):
    plansza = {}
    for i, znak in enumerate(pam.read()):
        plansza[i] = chr(znak)
    if warunki(plansza, moj_znak):
        print('wygrana')
        zakoncz(pam, moj_sem, przec_sem)
        return True
    elif warunki(plansza, przec_znak):
        print('\nprzegrana')
        zakoncz(pam, moj_sem, przec_sem)
        return True
    elif czy_remis(plansza):
        print('\nremis')
        zakoncz(pam, moj_sem, przec_sem)
        return True
    return False

key_pam = 1001
key_x = 2001
key_o = 3001

try:
    pam = sysv_ipc.SharedMemory(key_pam, sysv_ipc.IPC_CREAT, size=9)
    moj_sem = sysv_ipc.Semaphore(key_x, sysv_ipc.IPC_CREX)
    przec_sem = sysv_ipc.Semaphore(key_o, sysv_ipc.IPC_CREX)
    moj_znak = 'x'
    przec_znak = 'o'
except sysv_ipc.ExistentialError as e:
    przec_sem = sysv_ipc.Semaphore(key_x, 0)
    moj_sem = sysv_ipc.Semaphore(key_o, 0)
    moj_znak = 'o'
    przec_znak = 'x'
try:
    print('twój znak: ', moj_znak)
    if moj_znak == 'X':
        print('\ngracz niezalogowany')
    else:
        przec_sem.release()
    moj_sem.acquire()
    while True:
        if sprawdz(pam, moj_sem, przec_sem): break
        drukuj(pam)
        nast = ruch(pam)
        pam.write(moj_znak.encode(), nast)
        drukuj(pam)
        if sprawdz(pam, moj_sem, przec_sem): break
        print("\nczekam")
        przec_sem.release()
        moj_sem.acquire()
except Exception as e:
    zakoncz(pam, moj_sem, przec_sem)
    print(e)
    print("nieoczekiwane zamkniecie")
    