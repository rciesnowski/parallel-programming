#!/bin/bash

if [ -d "/home/$1" ] && [[ "$2" =~ ^[0-9]+$ ]]; then
	lacze="$HOME/lab04/klientfifo"
	if [ -p $lacze ]; then
		rm $lacze
	fi

	mkfifo $lacze
	echo $lacze $2 > "/home/$1/lab04/serwerfifo"

	read odp < $lacze
	echo "odpowiedz: "  $odp
	rm $lacze
	exit 0
else
	echo "Para skryptów klient-serwer komunikująca się przez parę łącz nazwanych klientfifo i serwerfifo. Klient wpisuje do lacza serwerfifo swoją wartość HOME i jedną liczbę całkowitą. Serwer przekazuje je do procesu potomnego, który oblicza pewną funkcję arytmetyczną i wynik wstawia do łącza. Skrypt klienta otrzymuje dwa argumenty wywołania: liczbę i nazwę konta, na którym działa serwer. Klient działa jednorazowo. Program serwera przechwytuje sygnały wylogowania i wyłączenia okna, co pozwala mu działać cały czas (trap). Prawidłowe zakończenie pracy serwera następuje po przechwyceniu sygnału SIGUSR1."
	echo "Możliwość przerwania wykonywania funkcji odczytu z łącza przez proces rodzicielski wskutek (asynchronicznego) otrzymania sygnały SIGCHLD od któregoś z kończących pracę potomków"
	exit 1
fi
