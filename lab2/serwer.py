import os
import time

while True:
	print("czekanie na wiadomosc..")
	while not os.path.isfile("dane_serwera"):
		time.sleep(1)
	print("witaj serwerze, masz nową wiadomosc:")
	f = os.open("dane_serwera", os.O_RDWR)
	z_pliku = os.read(f,200)
	z_pliku_list = z_pliku.split(None, 1)
	wiadomosc = str(z_pliku_list[1])
	print("klient:", wiadomosc[2:-1])
	nazwa_pliku = z_pliku_list[0]
	odp_str = input("ty:\t")
	odp = bytes(str(odp_str), 'utf-8') 
	os.close(f)
	os.remove("dane_serwera")
	f = os.open(nazwa_pliku, os.O_RDWR|os.O_CREAT)
	os.write(f, odp)
	os.close(f)
	print("klient zalatwiony! czekamy na nastepnego..")
	
