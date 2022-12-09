
import random
def tworz_liste():
    lista=[]
    for x in range(20):
        lista.append(x)
    return lista

lista = tworz_liste()
print(lista)
wylosowana = random.choice(lista)
print('wylosowana liczba: {}'.format(wylosowana))
while True:
    print('Aktualna lista: {}'.format(lista))
    print(20*'-')
    wybierz = input('Wpisz liczbę od {} do {}: '.format(lista[0], lista[-1]))
    print(20*'#')
    lista_a = lista[0: int(len(lista)/2)]
    lista_b = lista[int(len(lista)/2): ]
    
    if int(wybierz) == wylosowana:
        print('Gratulacje! Chodziło o liczbę {}'.format(wylosowana))
        break
    else:
        print('Sprawdzam zakresy...')
        if int(wybierz) in lista_a:
            if wylosowana in lista_a:
                print('- Twoja liczba znajduje się w wybranym zakresie...')
                del lista_b
                lista=lista_a
        elif int(wybierz) in lista_b:
            if wylosowana in lista_b:
                print('- Twoja liczba znajduje się w wybranym zakresie')
                del lista_a
                lista=lista_b