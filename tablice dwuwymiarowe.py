rozmiar=int(input('Wpisz rozmiar tablicy: '))
tablica = [[0 for x in range(rozmiar)] for y in range(rozmiar)]
print('Pusta tablica:')
for x in tablica:
    print(x)
print('Uzupelniona tablica:')

for x in range(rozmiar):
    for y in range(rozmiar):
        if x==y:
            tablica[x][y]=y
for x in tablica:
    print(x)
print('Suma tablicy:')
suma=0
for x in tablica:
    for y in x:
        suma+=y

print(suma)
czy_zapisac=input('Czy zapisać wyniki do pliku [T/N]? ')
if czy_zapisac=='T':
    plik = open('maciez.txt', 'w')
    tresc = f"{tablica}\n Suma tablicy: {suma}"
    plik.write(tresc)
    plik.close()
    print('Plik zapisany...')