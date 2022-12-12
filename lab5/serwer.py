import os
import select
import sys
from message import get_message
from message import create_msg

dict = {
	1 : "Akira",
	2 : "Mills",
	3 : "Ivy",
	4 : "Harper",
	5 : "Ames",
	6 : "Polla",
	7 : "Mia",
	8 : "Texas",
	9 : "Ann",
	10 : "Danger",
	11 : "Aniston",
	12 : "Paul",
	13 : "Chechik",
	14 : "Love",
	15 : "Malkova",
	16 : "Reid",
	17 : "Khalifa",
	18 : "Daniels",
	19 : "Granger",
	20 : "Rhoades"
}

plik_serwera = "serwerfifo"
if os.path.exists(plik_serwera):
	os.remove(plik_serwera)
os.mkfifo(plik_serwera)

serwerfifo = os.open(plik_serwera, os.O_RDONLY | os.O_NONBLOCK)
poll = select.poll()
poll.register(serwerfifo, select.POLLIN)
print("proszę niech ktoś do mnie napisze w końcu")
while True:
	try:
		if (serwerfifo, select.POLLIN) in poll.poll():
			msg = get_message(serwerfifo)
			print("otrzymałem wiadomość: " + msg)
			msg = msg.split(" ")
			id = int(msg[0])
			if id in dict:
				nazwisko = dict[id]
			else:
				nazwisko = "nie ma"
			path = "/home/"+msg[1]+"/lab05/klientfifo"
			if os.path.exists(path):
				klientfifo = os.open(path, os.O_WRONLY)
				msg = create_msg(nazwisko.encode("utf8"))
				os.write(klientfifo, msg)
				os.close(klientfifo)
				print("wysłałem odpowiedz, czekam dalej")
			else:
				print("nie ma takiego uzytkownika niestety")
	except KeyboardInterrupt:
		poll.unregister(serwerfifo)
		os.close(serwerfifo)
		os.remove(plik_serwera)
		print("\nok elo")
		sys.exit()
