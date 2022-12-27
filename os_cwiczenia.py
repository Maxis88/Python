import os
import time
import shutil
import string
# zwraca alfabet
alfabet = list(string.ascii_lowercase)


def przeksztalc(czas):
    ang = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
           'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    pol = ['Sty', 'Lut', 'Mar', 'Kwi', 'Maj', 'Cze',
           'Lip', 'Sie', 'Wrz', 'Paz', 'Lis', 'Gru']
    nowy = czas.split(" ")
    for month in ang:
        if nowy[1] == month:
            index = month.index(month)
            nowy[1] = pol[index]

    if nowy[2] != "":
        format = nowy[2] + "-" + nowy[1]
    else:
        format = nowy[3] + "-" + nowy[1]
    return format


def przywroc_nazwy(adres):
    pl = []
    zlicz = 0

    for foldery, podfoldery, pliki in os.walk(adres):
        for plik in pliki:
            podziel = plik.split('(')
            print(podziel)
            if len(podziel) > 1:
                nazwa = podziel[1]
                zmien = nazwa.replace('(', "").replace(')', "")
                zlicz += 1
                adres = foldery + "\\" + plik
                # dokonczyc

                os.rename(adres, foldery + "\\" + zmien)


def wykryj_foldery():
    foldery = []
    for x in os.listdir(folder):
        plik = x.split(".")
        if len(plik) > 1:
            foldery.append(plik[-1].upper())
    for x in foldery:
        if not os.path.exists(os.path.join(folder, x)):
            os.mkdir(os.path.join(folder, x))


def zmien_nazwy():

    for x in os.listdir(folder):
        print(x)
        nazwa = x.split('.')
        print(nazwa)
        cTime = os.path.getmtime(folder+"\\"+x)
        czas = przeksztalc(time.ctime(cTime))
        if len(nazwa) == 2:
            nowaNazwa = czas + "(" + nazwa[0] + ")"
            zmieniony = x.replace(nazwa[0], nowaNazwa)
            if "(" in nazwa[0] and ")" in nazwa[0]:
                print(f'Pomijam {x}, gdyż nazwa już jest zmieniona.')
                continue
            else:
                os.rename(os.path.join(folder, x),
                          os.path.join(folder, zmieniony))
                print('Nowa nazwa: ' + nowaNazwa)
    print("Zmiana nazw została zakończona...")


def zmienione_nazwy(adres):
    zmienionych = 0
    for x in os.listdir(adres):
        if os.path.isfile(os.path.join(adres, x)):
            if "(" in x and ")" in x:
                zmienionych += 1
    return zmienionych


def przenies_pliki():
    for x in os.listdir(folder):
        if os.path.isfile(os.path.join(folder, x)):

            nazwa = x.split('.')

            print('Przenosze: ' + x)
            shutil.move(os.path.join(folder, x), folder+'\\'+nazwa[1])


def sprawdz_pliki(folder):
    lista_plikow = os.listdir(folder)
    plikow = 0
    nazwy = []
    for x in lista_plikow:
        if os.path.isfile(os.path.join(folder, x)):
            nazwy.append(x)
            plikow += 1

    return [plikow, nazwy]


folder = "D:\\testowy"

pytanie1 = input('Podaj adres jaki chcesz uporządkować: ')

if os.path.isdir(pytanie1):
    folder = pytanie1
    plikow = sprawdz_pliki(folder)
    if plikow[0] > 0:
        print(f'Znaleziono: {plikow[0]} plików...\n{plikow[1]}')
        zmienionych = zmienione_nazwy(folder)
        if zmienionych > 0:
            print(f'Znaleziono {zmienionych} plików ze zmodyfikowaną nazwą')
        pytanie2 = input('Czy zmienić nazwy plików na związane z datą? [T/N] ')
        if pytanie2.lower() == 't':
            zmien_nazwy()
        else:
            print('Nazwy plików zostają bez zmian...')
            if zmienionych > 0:
                pytanie2 = input('Czy przywrócić stare nazwy plików ? [T/N] ')
                if pytanie2.lower() == 't':
                    przywroc_nazwy(folder)
        pytanie3 = input(
            'Czy przenieść pliki do dedykowanych folderów? [T/N] ')
        if pytanie3.lower() == 't':
            wykryj_foldery()
            przenies_pliki()
        else:
            print('Pliki zostały w folderze głównym')
            pytanie4 = input(
                'Czy chcesz przenieść pliki do innego folderu? [T/N] ')
            if pytanie4.lower() == 't':
                pytanie5 = input('Podaj adres docelowego folderu: ')
                if os.path.isdir(pytanie5):
                    for x in os.listdir(folder):
                        print(f'Przenoszę {x} do {pytanie5}')
                        if shutil.move(os.path.join(folder, x), pytanie5):
                            print(f'Przeniesiono {x}')
    else:
        print('Nie znaleziono żadnych plików w wybranym folderze. Kończę działanie...')
