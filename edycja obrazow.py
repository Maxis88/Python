
import os
from PIL import Image, ImageEnhance, ImageDraw, ImageFont
import numpy as np
import time
import shutil
import sqlite3

# ustalanie parametrów
SOURCE = "D:/testowy"
OUTPUT = SOURCE + "/edited/"


connection = sqlite3.connect('ustawienia.db')
kur = connection.cursor()

baza = kur.execute('CREATE TABLE IF NOT EXISTS ustawienia(ostrosc INTEGER, jasnosc INTEGER, \
    saturacja REAL, kontrast REAL, podpis TEXT, nazwa TEXT, domyslny BOOLEAN, nazwa_plikow TEXT)')
connection.commit()
pobierz_dane = kur.execute('SELECT * FROM ustawienia')
dane = pobierz_dane.fetchall()

if len(dane) == 0:
    print('Zapisuję domyślne ustawienia w bazie danych...')
    SHARPNESS = 3
    BRIGHTNESS = 120
    SATURATION = 0.4
    CONTRAST = 1.1
    zmien = kur.execute('INSERT INTO ustawienia VALUES("{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}")'.format(
        SHARPNESS, BRIGHTNESS, SATURATION, CONTRAST, "", "domyslne", True, ""))
    connection.commit()


def zmiana_folderu():
    global SOURCE
    domyslnyFolder = input(f'Czy użyć domyślnego folderu {SOURCE} ? [T/N] ')
    if domyslnyFolder.lower() == 'n':
        SOURCE = input('Podaj adres folderu ze zdjęciami: ')

        while not os.path.isdir(SOURCE):
            pytanie_1 = input(
                f"Podany folder nie istnieje. Wpisz adres folderu który chcesz edytować:  ")
            pytanie_1 = pytanie_1.replace("\\", "/")
            if "/" in pytanie_1:
                SOURCE = pytanie_1
            else:
                print("Podany adres jest nieprawidłowy... ")

        print(f"Ustawiam folder źródłowy: {SOURCE}")

    return (SOURCE)

def profile_zdjec():
    odczytZbazy = kur.execute("SELECT nazwa FROM ustawienia")
    nazwy = odczytZbazy.fetchall()
    print('Dostepne profile: ')
    for n, nazwa in enumerate(nazwy, start=1):
        print(f'{n}. {nazwa[0]}')

def zmiana_korekcji():
    # odczytaj ustawienia z bazy danych
    odczytZbazy = kur.execute("SELECT * FROM ustawienia WHERE domyslny='True'")
    opcja = odczytZbazy.fetchone()
    SHARPNESS = opcja[0]
    BRIGHTNESS = opcja[1]
    SATURATION = opcja[2]
    CONTRAST = opcja[3]
    podpis = opcja[4]
    nazwa = opcja[5]
    # wyświetl podstawową informację o profilu
    linia()
    print(f'Aktualnie pracujesz na profilu: {nazwa}')
    
    profile_zdjec()
    linia()
    
    # podaj jakiej ostrości używać
    ostrosc = input(f'Podaj wartość ostrości (aktualnie: {SHARPNESS}): ')
    if ostrosc.isdigit() and int(ostrosc) > 0:
        SHARPNESS = int(ostrosc)
        print('Ostrość wynosi: ', SHARPNESS)
    
    # podaj jakiej jasności używać
    jasnosc = input(f'Podaj próg jasności do którego ma dążyć program (aktualnie: {BRIGHTNESS}) ')
    if jasnosc.isdigit() and int(jasnosc) > 0:
        BRIGHTNESS = int(jasnosc)
        print('Jasność wynosi: ', BRIGHTNESS)
    
    # podaj jaką saturację używać w zdjęciach kolorowych
    saturacja = input(f'Podaj o jaką wartość ma się zmienić saturacja (aktualnie: {SATURATION}) ')
    if float(saturacja) > 0:
        SATURATION = float(saturacja)
        print('Saturacja wynosi: ', SATURATION)
    
    # podaj jaki kontrast używać do zdjęć
    kontrast = float(input(f'Podaj wartość kontrastu (aktualnie: {CONTRAST}) '))
    if float(kontrast) > 0:
        CONTRAST = float(kontrast)
        print('Kontrast wynosi: ', CONTRAST)
    
    # podaj jaki podpis ma być używany do zdjęć
    podpis = input(f'Podaj treść podpisu lub wciśnij ENTER: ')
    if podpis:
        print('Twój podpis: ', podpis)
    zaznacz_nazwy=kur.execute('SELECT nazwa FROM ustawienia')
    nazwy=zaznacz_nazwy.fetchall()
    
    
    nazwa_plikow = input(f'Podaj własną nazwę plików lub wciśnij ENTER: ')
    if nazwa_plikow!="":
        print('Pliki będą zapisywane pod nazwą: ', nazwa_plikow)
            
    else:
        print('Pliki zachowają swoją oryginalną nazwę')
            
    # upewnij się że taka nazwa profilu nie istnieje
    check=False
    while check:
        zaznacz_nazwy=kur.execute('SELECT nazwa FROM ustawienia')
        nazwy=zaznacz_nazwy.fetchall()

        czy_zapisac = input('Czy chcesz zapisać te ustawienia w profilu ? [Wpisz nazwę profilu lub ENTER aby zapisać w aktualnym]: ')
        if czy_zapisac.lower() == '':
            kur.execute('UPDATE ustawienia SET ostrosc="{}", jasnosc="{}", saturacja="{}", \
                kontrast="{}", podpis="{}", nazwa="{}", domyslny="{}", nazwa_plikow="{}" WHERE nazwa="{}"'.format(
                SHARPNESS, BRIGHTNESS, SATURATION, CONTRAST, podpis, "domyslne", True, nazwa_plikow, nazwa))
            connection.commit()
            check=True
            print(f'Zaktualizowano profil: {nazwa}')
        else:
            if czy_zapisac.lower() not in nazwy:
                kur.execute('UPDATE ustawienia SET domyslny="False" WHERE domyslny="True"')
                connection.commit()
                kur.execute('INSERT INTO ustawienia VALUES("{}", "{}", "{}", \
                    "{}", "{}", "{}", "{}", "{}")'.format(
                        SHARPNESS, BRIGHTNESS, SATURATION, CONTRAST, "", czy_zapisac.lower(), True, nazwa_plikow))
                connection.commit()
                check=True
            else:
                print('Nie można użyć tej nazwy, gdyż taki profil już istnieje...')
                continue
    print(f'Profil {czy_zapisac.lower()} jest teraz ustawiony jako domyślny')

def menu(opcja='menu'):
    print("Wybierz opcję, która Cię interesuje: ")
    linia()
    print("1. Obrabiaj zdjęcia teraz ")
    print("2. Przerób zdjęcia na czarbo-białe")
    print("3. Ustaw domyślną nazwę zdjęć")
    print("4. Ustaw podpis")
    print("5. Wybierz domyślny profil zdjęć")
    print("6. Wyczyść profile zdjęć")
    print('7. Zakończ działanie')
    wybor = input('Wybieram opcję: ')

    odczytZbazy = kur.execute("SELECT * FROM ustawienia WHERE domyslny='True'")
    opcja = odczytZbazy.fetchone()
    SHARPNESS = opcja[0]
    BRIGHTNESS = opcja[1]
    SATURATION = opcja[2]
    CONTRAST = opcja[3]
    podpis = opcja[4]
    nazwa_plikow = opcja[7]

    match wybor:
        case "1":
            folder = zmiana_folderu()
            korekcja(folder, podpis, True)
            
            probka = input(
                'W wybranym katalogu został utworzony folder "probka" a w nim jedno zdjęcie prezentujące ustawienia.\n\
                Czy zastosować te ustawienia do wszystkich plików? [T/N] ')
            if probka.lower() == 't':
                try:
                    shutil.rmtree(folder + "/probka")
                except:
                    pass
                korekcja(SOURCE, podpis)
            else:
                poprawki = input('Czy chcesz wprowadzić korekty parametrów ? [T/N]')
                if poprawki.lower()=='t':
                    zmiana_korekcji()
                else:
                    korekcja(SOURCE, podpis)
        case "2":
            folder = zmiana_folderu()
            korekcja(folder, podpis, True, bw=True)
            
            probka = input(
                'W wybranym katalogu został utworzony folder "probka" a w nim jedno zdjęcie prezentujące ustawienia.\n\
                Czy zastosować te ustawienia do wszystkich plików? [T/N] ')
            if probka.lower() == 't':
                try:
                    shutil.rmtree(folder + "/probka")
                except:
                    pass
                korekcja(SOURCE, podpis, bw=True)
            else:
                poprawki = input('Czy chcesz wprowadzić korekty parametrów ? [T/N]')
                if poprawki.lower()=='t':
                    zmiana_korekcji()
        case "3":
            nowa_nazwa = input(f"Aktualnie używana nazwa to: {nazwa_plikow}, wpisz nową nazwę: ")
            if nowa_nazwa!="":
                kur.execute('UPDATE ustawienia SET nazwa_plikow="{}" WHERE nazwa="{}"')
                connection.commit()
                print("- Dane zostały zaktualizowane.")
            

def linia():
    print()
    print(60*"#")


def korekcja(adres, podpis, probka=False, adres_zapisu="", bw=False):
    odczyt = kur.execute('SELECT * FROM ustawienia WHERE domyslny="True"')
    dane = odczyt.fetchone()
    SHARPNESS = dane[0]
    BRIGHTNESS = dane[1]
    SATURATION = dane[2]
    CONTRAST = dane[3]
    SOURCE = adres
    if adres_zapisu == "":
        OUTPUT = SOURCE + "/edited/"
    else:
        OUTPUT = SOURCE + "/" + adres_zapisu + "/"
    FILES_COUNT = 0
    new_output = SOURCE + "/probka/"
    if probka:
        if not os.path.isdir(new_output):
            print('- Tworzenie nowego katalogu...')
            os.mkdir(new_output)
        OUTPUT = new_output

    TIME_BEFORE = time.time()
    for name in os.listdir(SOURCE):
        # weź pod uwagę tylko zdjęcia w formacie JPG

        if ".jpg" in name.lower():
            FILES_COUNT += 1
            file_adress = os.path.join(SOURCE, name)
            # wyświetl nazwę obrabianego pliku
            print("Pracuję nad: ", name, "\n")
            # dla każdego zdjęcia popraw wartości ostrości, jasności i kontrastu
            with Image.open(file_adress) as new_file:
                # tworzenie miniatury dla zoptymalizowania czasu obróbki
                nowe_wymiary = new_file.width // 4, new_file.height // 4
                mini = new_file.resize(nowe_wymiary)
                # znajdź średnią wartość jasności zdjęcia
                pixels = np.array(mini.getdata())
                srednia = np.average(pixels)

                # popraw jasność zdjęcia
                wartosc = (BRIGHTNESS/srednia)*100
                przelicz = BRIGHTNESS/srednia
                print('- Ustawiam jasność na: ', round(wartosc, 0), "%")
                enhance = ImageEnhance.Brightness(new_file)
                new_file = enhance.enhance(przelicz)

                # popraw kontrast zdjęcia
                print(f"- Poprawiam kontrast ({CONTRAST})...")
                enhance = ImageEnhance.Contrast(new_file)
                new_file = enhance.enhance(CONTRAST)

                # popraw ostrość zdjęcia
                print(f"- Poprawiam ostrość ({SHARPNESS})...")
                enhance = ImageEnhance.Sharpness(new_file)
                new_file = enhance.enhance(SHARPNESS)
                if not bw:
                    # zmiana nasycenia kolorów
                    print(f'- Zmieniam saturacje o {SATURATION*100}%')
                    # obrazek tymczasowy
                    tymczasowy = new_file.convert('HSV')
                    tylko_saturacja = tymczasowy.split()[1]
                    nasycenie_zmodyfikowane = tylko_saturacja.point(
                        lambda x: x+(x*SATURATION))
                    tymczasowy = Image.merge(
                        'HSV', (tymczasowy.split()[0], nasycenie_zmodyfikowane, tymczasowy.split()[2]))
                    new_file = tymczasowy.convert('RGB')
                # podpisz zdjęcie jeśli zdefiniowano
                if podpis != "":
                    width, height = new_file.size
                    rysuj = ImageDraw.Draw(new_file)
                    czcionka = ImageFont.truetype('arial.ttf', 80)
                    pos_x, pos_y, szerokosc_czcionki, wysokosc_czcionki = czcionka.getbbox(
                        podpis)

                    text_x = width - szerokosc_czcionki - 100
                    text_y = height - wysokosc_czcionki - 100
                    rysuj.text((text_x, text_y), podpis,
                               font=czcionka, fill=(255, 255, 255))
                if bw:
                    print("- Zmieniam obraz na czarbo-biały...")
                    new_file=new_file.convert("L")
                # zapis poprawionego pliku
                new_file.save(OUTPUT + name)
                linia()

        if probka and FILES_COUNT > 0:
            break

    # wyświetl czas potrzebny do obróbki zdjęć
    TIME_AFTER = time.time()
    czas = int(TIME_AFTER-TIME_BEFORE)
    print(f'- Przetworzonych plików: {FILES_COUNT}')
    print(
        f"- Czas wykonania: {czas} sekund ({czas/FILES_COUNT}/sek na zdjęcie)")
    OUTPUT = OUTPUT.replace("//", "\\")
    print('- Pliki zostały zapisane do: ', OUTPUT)
    linia()


done = False



while not done:
    menu()
connection.close()
    

# dodać możliwość zmiany nazw plików oraz umieścić parametr w bazie danych
# dodać w menu opcję wyboru profilu
# dodać menu w którym wybieramy czy chcemy obrabiać pliki czy je edytować itp
