import sys
import os
import time

if (__name__ == "__main__") & (len(sys.argv) == 2):
	# czyta parametry
	nazwa_pliku = sys.argv[1]
	if os.path.exists(str(nazwa_pliku)):
		os.remove(str(nazwa_pliku))
	# otwiera dane serwera, zapisuje do nich nazwe pliku i input 
	wiadomosc = input("pisz se smialo byczku!\nty:\t")
	do_pliku_str = str(nazwa_pliku) + "\n" + str(wiadomosc).split(chr(27))[0]
	do_pliku = bytes(do_pliku_str, 'utf-8')
	while os.path.exists("dane_serwera"):
		print("pan serwer jest zajęty")	
		time.sleep(3)
	f = os.open("dane_serwera", os.O_RDWR|os.O_CREAT)
	os.write(f, do_pliku)
	os.close(f)
	#czeka na stworzenie pliku przez serwer, odczytuje go i usuwa
	while not os.path.exists(str(nazwa_pliku)):
		time.sleep(2)
	f = os.open(str(nazwa_pliku), os.O_RDWR)
	odp = str(os.read(f, 200))
	odp = odp[2:-1]
	print("serwer:", odp)
	os.close(f)
else:
	print("uruchom ponownie, tym razem mądrzej")
