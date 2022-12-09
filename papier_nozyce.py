import random

#punktacja graczy
gracz=0
komputer=0
graj= True
figury={
    1: 'papier',
    2: 'nożyce',
    3: 'kamień',
}

def losuj():
    losuj=random.randint(1,3)

    return losuj

def sprawdz_ruch(odpowiedz):
    if odpowiedz.lower() in figury.values():
        
        return True
    else:
        
        return False

class Gracz:
    def __init__(self):
        self.wygranych=0
        self.przegranych=0
        self.ruch=[]
    def aktualizuj(self, rodzaj):
        if rodzaj=='win':
            self.wygranych+=1
        else:
            self.przegranych+=1
    def wynik(self):
        print(20*'-')
        print('WYGRAMYCH :  {}'.format(self.wygranych))
        print('PRZEGRANYCH: {}'.format(self.przegranych))
        print('Wykonywane ruchy: {}'.format(self.ruch))
        print(20*'-')
    def zapisz_ruch(self, ruch):
        self.ruch.append(ruch)

def nadaj_symbol(odpowiedz):
    if odpowiedz=='papier':
        symbol=1
    elif odpowiedz == 'nożyce':
        symbol=2
    elif odpowiedz == 'kamień':
        symbol=3
    else:
        return False
    return symbol
gracz = Gracz()
komputer = Gracz()

while graj:
    
    odpowiedz = input('Wybierz: [Papier / Nożyce / Kamień] lub "Koniec" aby zakończyć: ')
    if odpowiedz.lower()=='koniec': 
        print('Twoje wyniki:')
        gracz.wynik()
        print('Wyniki komputera: ')
        komputer.wynik()
        break
    numer = nadaj_symbol(odpowiedz.lower())
    figura = losuj()
    
    if sprawdz_ruch(odpowiedz)==True and nadaj_symbol(odpowiedz):
        
        #jeżeli odpowiedz jest poprawna
        if (numer-figura)==1 or (numer-figura)==-2:
            print('----- GRATULACJE - WYGRYWASZ !!! ----- {} - {}'.format(figury[numer], figury[figura]))
            gracz.aktualizuj('win')
            komputer.aktualizuj('loose')
            gracz.zapisz_ruch(figury[numer])
            komputer.zapisz_ruch(figury[figura])
        elif numer==figura:
            print('----- REMIS ---')
            gracz.zapisz_ruch(figury[numer])
            komputer.zapisz_ruch(figury[figura])
        else:
            print('Niestety komputer wygrał ({} - {})'.format(figury[numer], figury[figura]))
            gracz.aktualizuj('loose')
            komputer.aktualizuj('win')
            gracz.zapisz_ruch(figury[numer])
            komputer.zapisz_ruch(figury[figura])