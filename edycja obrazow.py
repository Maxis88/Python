
import os
from PIL import Image, ImageEnhance, ImageDraw, ImageFont
import numpy as np
import time
import shutil
import sqlite3

# ustalanie parametrów
SOURCE = "D:/testowy"
OUTPUT = SOURCE + '/edited/'
MINI =SOURCE + '/zmniejszone/'

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


def pobierz_ustawienia(domyslny=True):
    if domyslny:
        pobierz_dane = kur.execute(
            'SELECT * FROM ustawienia WHERE domyslny="True"')
        dane = pobierz_dane.fetchone()
    else:
        pobierz_dane = kur.execute('SELECT * FROM ustawienia')
        dane = pobierz_dane.fetchall()
    return dane


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

    nazwy = pobierz_ustawienia(False)
    print('Dostepne profile: ')
    for n, nazwa in enumerate(nazwy, start=1):
        if nazwa[6]:
            print(f'{n}. [x] {nazwa[5]}:\n\tPodpis: {nazwa[4]},\n\tOstrość: {nazwa[0]},\n\tJasność: {nazwa[1]},\
                \n\tSaturacja: {nazwa[2]},\n\tKontrast: {nazwa[3]}')
        else:
            print(
                f'{n}. {nazwa[5]}\n\tPodpis: {nazwa[4]},\n\tOstrość: {nazwa[0]},\n\tJasność: {nazwa[1]},\
                    \n\tSaturacja: {nazwa[2]},\n\tKontrast: {nazwa[3]}')


def zmiana_korekcji():
    # odczytaj ustawienia z bazy danych

    opcja = pobierz_ustawienia()
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
    jasnosc = input(
        f'Podaj próg jasności do którego ma dążyć program (aktualnie: {BRIGHTNESS}) ')
    if jasnosc.isdigit() and int(jasnosc) > 0:
        BRIGHTNESS = int(jasnosc)
        print('Jasność wynosi: ', BRIGHTNESS)

    # podaj jaką saturację używać w zdjęciach kolorowych
    saturacja = input(
        f'Podaj o jaką wartość ma się zmienić saturacja (aktualnie: {SATURATION}) ')
    if float(saturacja) > 0:
        SATURATION = float(saturacja)
        print('Saturacja wynosi: ', SATURATION)

    # podaj jaki kontrast używać do zdjęć
    kontrast = float(
        input(f'Podaj wartość kontrastu (aktualnie: {CONTRAST}) '))
    if float(kontrast) > 0:
        CONTRAST = float(kontrast)
        print('Kontrast wynosi: ', CONTRAST)

    # podaj jaki podpis ma być używany do zdjęć
    podpis = input(f'Podaj treść podpisu lub wciśnij ENTER: ')
    if podpis:
        print('Twój podpis: ', podpis)
    zaznacz_nazwy = kur.execute('SELECT nazwa FROM ustawienia')
    nazwy = zaznacz_nazwy.fetchall()

    nazwa_plikow = input(f'Podaj własną nazwę plików lub wciśnij ENTER: ')
    if nazwa_plikow != "":
        print('Pliki będą zapisywane pod nazwą: ', nazwa_plikow)

    else:
        print('Pliki zachowają swoją oryginalną nazwę')

    # upewnij się że taka nazwa profilu nie istnieje
    check = False
    while check:
        zaznacz_nazwy = kur.execute('SELECT nazwa FROM ustawienia')
        nazwy = zaznacz_nazwy.fetchall()

        czy_zapisac = input(
            'Czy chcesz zapisać te ustawienia w profilu ? [Wpisz nazwę profilu lub ENTER aby zapisać w aktualnym]: ')
        if czy_zapisac.lower() == '':
            kur.execute('UPDATE ustawienia SET ostrosc="{}", jasnosc="{}", saturacja="{}", \
                kontrast="{}", podpis="{}", nazwa="{}", domyslny="{}", nazwa_plikow="{}" WHERE nazwa="{}"'.format(
                SHARPNESS, BRIGHTNESS, SATURATION, CONTRAST, podpis, "domyslne", True, nazwa_plikow, nazwa))
            connection.commit()
            check = True
            print(f'Zaktualizowano profil: {nazwa}')
        else:
            if czy_zapisac.lower() not in nazwy:
                kur.execute(
                    'UPDATE ustawienia SET domyslny="False" WHERE domyslny="True"')
                connection.commit()
                kur.execute('INSERT INTO ustawienia VALUES("{}", "{}", "{}", \
                    "{}", "{}", "{}", "{}", "{}")'.format(
                    SHARPNESS, BRIGHTNESS, SATURATION, CONTRAST, "", czy_zapisac.lower(), True, nazwa_plikow))
                connection.commit()
                check = True
            else:
                print('Nie można użyć tej nazwy, gdyż taki profil już istnieje...')
                continue
    print(f'Profil {czy_zapisac.lower()} jest teraz ustawiony jako domyślny')


def ustaw_podpis():
    dane = pobierz_ustawienia()
    nowy_podpis = input('Podaj treść jaka ma znajdować się na zdjęciu: ')
    if nowy_podpis != "":
        kur.execute(
            f'UPDATE ustawienia SET podpis="{nowy_podpis}" WHERE nazwa="{dane[5]}" ')
        connection.commit()
        print('Nowy podpis ustawiony na "{}" dla profilu: {}'.format(
            nowy_podpis, dane[5]))


def zmien_rozmiar(rozmiar):
    global SOURCE, MINI, OUTPUT
    podfolder=os.path.join(SOURCE, 'zmniejszone')
    try:
        os.mkdir(podfolder)
    except FileExistsError:
        pass
    
    for name in os.listdir(SOURCE):
        # weź pod uwagę tylko zdjęcia w formacie JPG

        if ".jpg" in name.lower():
            
            file_adress = os.path.join(SOURCE, name)
            # wyświetl nazwę obrabianego pliku
            print("Pracuję nad: ", name, "\n")
            # dla każdego zdjęcia zmień jego rozmiar
            with Image.open(file_adress) as new_file:
                print(f'- Zmieniam rozmiar zdjęcia na {rozmiar*100} %')
                width = new_file.width * rozmiar
                height = new_file.height * rozmiar
                new_file=new_file.resize((int(width), int(height)))
                new_file.save(os.path.join(MINI, name))
    dane=pobierz_ustawienia()

    korekcja(MINI, dane[4], adres_zapisu=OUTPUT)


def menu(opcja='menu'):
    print("Wybierz opcję, która Cię interesuje: ")
    linia()
    print("1. Koryguj zdjęcia teraz ")
    print("2. Przerób zdjęcia na czarbo-białe")
    print("3. Zmień rozmiar zdjęć")
    print("4. Ustaw domyślną nazwę zdjęć")
    print("5. Ustaw podpis")
    print("6. Wybierz domyślny profil zdjęć")
    print("7. Wyczyść profile zdjęć")
    print('8. Zakończ działanie')
    wybor = input('Wybieram opcję: ')

    opcja = pobierz_ustawienia()
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
                poprawki = input(
                    'Czy chcesz wprowadzić korekty parametrów ? [T/N]')
                if poprawki.lower() == 't':
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
                poprawki = input(
                    'Czy chcesz wprowadzić korekty parametrów ? [T/N]')
                if poprawki.lower() == 't':
                    zmiana_korekcji()
        
        case "3":
            # edytowanie zdjęcia
            rozmiar = input("Wpisz jaki % rozmiar powinno mieć finalne zdjęcie: ")
            if "%" in rozmiar and int(rozmiar)<100 and int(rozmiar)>0:
                rozmiar=rozmiar.replace("%", "")
            elif int(rozmiar)<100 and int(rozmiar)>0:
                rozmiar=int(rozmiar)/100
                zmien_rozmiar(rozmiar)


            else:
                print('Niepoprawne dane ...')
        
        case "4":
            nowa_nazwa = input(
                f"Aktualnie używana nazwa to: {nazwa_plikow}, wpisz nową nazwę: ")
            if nowa_nazwa != "":
                kur.execute(
                    'UPDATE ustawienia SET nazwa_plikow="{}" WHERE nazwa="{}"')
                connection.commit()
                print("- Dane zostały zaktualizowane.")
        case "5":
            ustaw_podpis()

        case "6":
            # lista profili
            profile_zdjec()
            profil = input('Podaj numer profilu, który chcesz wybrać: ')
            dane = pobierz_ustawienia(False)
            profile={}
            if int(profil)<=len(dane) and int(profil)>0:
                for x, info in enumerate(dane, start=1):
                    profile[x]=info[5]
                print(f'Wybrano profil: {profile[int(profil)]}')
                kur.execute(f'UPDATE ustawienia SET domyslny="{False}"')
                connection.commit()
                kur.execute(f'UPDATE ustawienia SET domyslny="{True}" WHERE nazwa="{profile[int(profil)]}"')
                connection.commit()
            else:
                print('Podano błędny numer...')
        case "7":
            # czyść profile 
            zapytaj= input('Czy jesteś pewny, że chcesz usunąć wszystkie profile ( prócz domyślnego ) ? [T/N]')
            if zapytaj.lower()=='t':
                kur.execute('DELETE FROM ustawienia WHERE nazwa!="domyslne"')
                connection.commit()
                print('Profile usunięte...')
                linia()
            else:
                print('Przechodzę więc do menu...')
        case "8":
            quit()
            


def linia():
    print()
    print(60*"#")


def korekcja(adres, podpis, probka=False, adres_zapisu="", bw=False):
    global OUTPUT
    dane = pobierz_ustawienia()
    SHARPNESS = dane[0]
    BRIGHTNESS = dane[1]
    SATURATION = dane[2]
    CONTRAST = dane[3]
    SOURCE = adres
    
    FILES_COUNT = 0
    new_output = SOURCE + '/probka/'
    
    if probka:
        if not os.path.isdir(new_output):
            print('- Tworzenie nowego katalogu pod zdjęcie próbne...')
            os.mkdir(new_output)
        #OUTPUT = new_output
    else:
        try:
            os.mkdir(SOURCE + "/edited")
        except:
            pass

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
                    nasycenie_zmodyfikowane = tylko_saturacja.point(lambda x: x+(x*SATURATION))
                    tymczasowy = Image.merge(
                        'HSV', 
                        (tymczasowy.split()[0], nasycenie_zmodyfikowane, tymczasowy.split()[2]))
                    new_file = tymczasowy.convert('RGB')
                else:
                    print("- Zmieniam obraz na czarbo-biały...")
                    new_file = new_file.convert("L")
                
                # podpisz zdjęcie jeśli zdefiniowano
                if podpis != "":
                    width, height = new_file.size
                    
                    rect = ImageDraw.Draw(new_file, mode='RGBA')
                    
                    
                    rysuj = ImageDraw.Draw(new_file)
                    czcionka = ImageFont.truetype('arial.ttf', 80)
                    pos_x, pos_y, szerokosc_czcionki, wysokosc_czcionki = czcionka.getbbox(
                        podpis)

                    text_x = width - szerokosc_czcionki - 100
                    text_y = height - wysokosc_czcionki - 100
                    rect.rectangle((text_x-50, text_y-50, width-50, height-50), fill=(0,0,0, 80))
                    rysuj.text((text_x, text_y), podpis,
                               font=czcionka, fill=(255, 255, 255))
                
                # zapis poprawionego pliku
                if probka:
                    new_file.save(new_output + name)
                    OUTPUT = OUTPUT.replace("//", "\\")
                    
                else:
                    new_file.save(OUTPUT + name)
                    OUTPUT = OUTPUT.replace("//", "\\")
                   
                linia()

        if probka and FILES_COUNT > 0:
            break
    
    if new_output:
        print('- Pliki zostały zapisane do: ', new_output)
    else:
        print('- Pliki zostały zapisane do: ', OUTPUT)
    # wyświetl czas potrzebny do obróbki zdjęć
    TIME_AFTER = time.time()
    czas = int(TIME_AFTER-TIME_BEFORE)
    print(f'- Przetworzonych plików: {FILES_COUNT}')
    print(
        f"- Czas wykonania: {czas} sekund ({czas/FILES_COUNT}/sek na zdjęcie)")
    
    linia()


done = False


while not done:
    menu()
connection.close()


# dodać menu w którym wybieramy czy chcemy obrabiać pliki czy je edytować itp
