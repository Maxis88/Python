import random
tablica = ['a','b', 'c', 
            'd','e','f',
            'g','h','i']

def plansza():
    tab=''
    for i in range(len(tablica)):
        if i==3 or i==6 or i==9:
            tab+='\n'
        tab+=str(tablica[i]) + " | "
    print(tab)
def sprawdz_wynik():
    
    if (tablica[0]=='O' and tablica[4]=='O' and tablica[8]=='O') or \
        (tablica[0]=='O' and tablica[1]=='O' and tablica[2]=='O') or \
        (tablica[3]=='O' and tablica[4]=='O' and tablica[5]=='O') or \
        (tablica[6]=='O' and tablica[7]=='O' and tablica[8]=='O') or \
        (tablica[2]=='O' and tablica[5]=='O' and tablica[8]=='O') or \
        (tablica[1]=='O' and tablica[4]=='O' and tablica[7]=='O') or \
        (tablica[0]=='O' and tablica[3]=='O' and tablica[6]=='O') or \
        (tablica[2]=='O' and tablica[4]=='O' and tablica[6]=='O'):

        print('Gratulacje! Wygrałeś !')
        return True
    else:
        if (tablica[0]=='X' and tablica[4]=='X' and tablica[8]=='X') or \
        (tablica[0]=='X' and tablica[1]=='X' and tablica[2]=='X') or \
        (tablica[3]=='X' and tablica[4]=='X' and tablica[5]=='X') or \
        (tablica[6]=='X' and tablica[7]=='X' and tablica[8]=='X') or \
        (tablica[2]=='X' and tablica[5]=='X' and tablica[8]=='X') or \
        (tablica[1]=='X' and tablica[4]=='X' and tablica[7]=='X') or \
        (tablica[0]=='X' and tablica[3]=='X' and tablica[6]=='X') or \
        (tablica[2]=='X' and tablica[4]=='X' and tablica[6]=='X'):
            print('Niestety komputer wygrał ')
            return True
    
plansza()
while True:
    wybor=input('Wpisz pole do uzupelnienia: ')
    index_gracz=tablica.index(wybor)
    if tablica[index_gracz]!='O' and tablica[index_gracz]!='X':
        tablica[index_gracz]= 'O'
    
    #ruch komputera
    #losuj ruch
    ruch_komputera=''
    while ruch_komputera =='':
        sprawdz = random.choice(tablica)
        
        if sprawdz!='O' and sprawdz!='X':
            index_komp=tablica.index(sprawdz)
            tablica[index_komp]='X'
            ruch_komputera=sprawdz
    plansza()
    wynik=sprawdz_wynik()
    if wynik:
        break
