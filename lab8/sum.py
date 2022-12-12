import threading
import random
import time

lst = [random.randint(0,100) for _ in range(252000)]

def thread_task(lista):
	global suma
	suma += sum(lista)

suma = 0
n_watkow = int(input("podaj liczbe watkow: "))
duza_lista = [lst[i:i + n_watkow] for i in range(0, len(lst), n_watkow)]
lista_watkow = [threading.Thread(target = thread_task(mala_lista)) for mala_lista in duza_lista]
start = time.time()
for watek in lista_watkow:
	watek.start()
for watek in lista_watkow:
	watek.join()
print("suma: " + str(suma) + "\nczas: " + str(time.time() - start))
