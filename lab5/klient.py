import os
import time
import select
from message import create_msg
from message import get_message

plik_klienta = "klientfifo"
if not os.path.exists(plik_klienta):
	os.mkfifo(plik_klienta)
klientfifo = os.open(plik_klienta, os.O_RDONLY | os.O_NONBLOCK)

plik_serwera = "serwerfifo"
while not os.path.exists(plik_serwera):
	print("serwer nie jest uruchomiony chyba")
	time.sleep(3)
serwerfifo = os.open(plik_serwera, os.O_WRONLY)
id = str(input("podaj ID po którym chcesz szukać nazwisko: "))
home = str(input("podaj swoją nazwę $HOME: "))
while not os.path.exists("/home/"+home+"/"):
	home = str(input("uzytkownik nie istnieje, podaj innego: "))
tresc = id + " " + home
msg = create_msg(tresc.encode("utf8"))
os.write(serwerfifo, msg)
os.close(serwerfifo)

poll = select.poll()
poll.register(klientfifo, select.POLLIN)
while True:
	if (klientfifo, select.POLLIN) in poll.poll():
		msg = get_message(klientfifo)
		print("otrzymalem odp.: " + msg)
		break

poll.unregister(klientfifo)
os.close(klientfifo)
os.remove(plik_klienta)
