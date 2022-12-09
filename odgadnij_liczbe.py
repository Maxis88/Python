import random

liczba = random.randint(0,100)
print(liczba)
start=0
stop=100
while True:
    odp = input(f'Podaj liczbę z przedziału {start} - {stop}: ')
    
    if int(odp)==liczba:
        print('Gratulacje! Odgadłeś liczbę!')
        break
    elif int(odp)<liczba:
        start=odp
        print('Twoja liczba jest mniejsza od szukanej! Zawężam pole poszukiwań do {} - {}'.format(start, stop))
    elif int(odp)>liczba:
        stop=odp
        print('Twoja liczba jest większa od szukanej! Zawężam pole poszukiwań do: {} - {}'.format(start, stop))
        