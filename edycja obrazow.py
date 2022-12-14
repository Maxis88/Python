
import os
from PIL import Image, ImageEnhance, ImageDraw, ImageFont
import numpy as np
import time
import shutil
import sqlite3
import re



def linia(dlugosc=60, znak="#"):
    print(int(dlugosc)*str(znak))


# ustalanie parametrów
try:
    os.mkdir("d:/Edycja")
    SOURCE = "D:/Edycja"
except FileExistsError:
    print('Ustawiono katalog D:\\Edycja jako domyślny')
    SOURCE = "D:/Edycja"
else:
    katalog = input('Podaj adres katalogu ze zdjęciami, na którym chcesz pracować: ')
    if os.path.isdir(katalog):
        SOURCE = katalog
linia()
# kreowanie bazy danych
OUTPUT = SOURCE + '/Edited/'
MINI = SOURCE + '/Resized/'
done = False
akt_menu = 'menu'

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

# wyświetla ustawienia profili


def pobierz_ustawienia(domyslny=True):
    if domyslny:
        pobierz_dane = kur.execute(
            'SELECT * FROM ustawienia WHERE domyslny="True"')
        dane = pobierz_dane.fetchone()
    else:
        pobierz_dane = kur.execute('SELECT * FROM ustawienia')
        dane = pobierz_dane.fetchall()
    return dane

# zmienia domyślny adres folderu


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

# Wyświetla wszystkie informacje o używnaym profilu


def informacje_o_profilu():
    zaznacz = kur.execute('SELECT * FROM ustawienia WHERE domyslny="True"')
    profil = zaznacz.fetchone()
    print("Informacje o aktualnym profilu zdjęciowym: ")
    print('\tNazwa: ', profil[5])
    print('\tOstrość: ', profil[0])
    print('\tJasność: ', profil[1])
    print('\tSaturacja: ', profil[2])
    print('\tKontrast: ', profil[3])
    print('\tPodpis: ', profil[4])

# wyświetla informacje o wszystkich profilach


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


# pozwala na edycje domyślnego profilu
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

# Pozwala ustawić podpis do zdjęcia

def ustaw_podpis():
    dane = pobierz_ustawienia()
    nowy_podpis = input('Podaj treść jaka ma znajdować się na zdjęciu: ')
    if nowy_podpis != "":
        kur.execute(
            f'UPDATE ustawienia SET podpis="{nowy_podpis}" WHERE nazwa="{dane[5]}" ')
        connection.commit()
        print('Nowy podpis ustawiony na "{}" dla profilu: {}'.format(
            nowy_podpis, dane[5]))

# Zmienia rozmiar zdjęcia

def zmien_rozmiar(rozmiar):
    global SOURCE, MINI, OUTPUT
    podfolder = SOURCE + "/Resized/"
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
                new_file = new_file.resize((int(width), int(height)))
                new_file.save(os.path.join(MINI, name))

# usuwa oryginalne pliki

def usun_oryginalne():
    global SOURCE
    pytanie = input(
        f'Czy jesteś pewien, że chcesz usunąć wszystkie oryginalne zdjęcia z katalogu: {SOURCE}? [T/N] ')
    if pytanie.lower() == 't':
        for plik in os.listdir(SOURCE):
            if ".jpg" in plik.lower():
                print(f'Usuwanie pliku: {plik.lower()}')
                try:
                    os.remove(os.path.join(SOURCE, plik))
                except Exception as e:
                    print('Nie można usunąć pliku: ',
                          plik.lower(), "Błąd: ", e.args[1])

# pyta czy usunąć pliki z katalogu głównego

def czy_usunac():
    pytanie = input('Czy usunąć oryginalne pliki? [T/N] ')
    if pytanie.lower() == 't':
        usun_oryginalne()


# funkcja do zmiany nazw plików
def zmiana_nazw():
    opcje = ['Własna nazwa + numery', "Skrócona nazwa- X pierwszych znaków", "Numery", "Prefix 'Edited'"]
    for numer, opcja in enumerate(opcje, start=1):
        print(f"{numer}. {opcja}")
    opcja = int(input('Wybierz z listy powyżej opcję zmiany nazw plików[1-4]: '))
    if opcja>=1 and opcja<=4:
        match opcja:
            case 1:
                nazwa = input("Wpisz własną nazwę dla pliku: ")
                if nazwa!="":
                    kur.execute("UPDATE ustawienia SET nazwa_plikow='1:{}'".format(nazwa))
                else:
                    print('Element nie może być pusty. Nazwy plikow pozostają bez zmian...')
            case 2:
                znakow = input("Ile znaków chcesz zachować? ")
                if znakow!="" and int(znakow)>0:
                    kur.execute("UPDATE ustawienia SET nazwa_plikow='2:{}'".format(znakow))
                else:
                    print('Błędne dane. Nazwy pozostają bez zmian..')
            case 3:
                kur.execute("UPDATE ustawienia SET nazwa_plikow='3:'")
            case 4:
                kur.execute("UPDATE ustawienia SET nazwa_plikow='4:'")
        connection.commit()
    else:
        print('Nie wybrano żadnej opcji lub była ona nieprawidłowa. Nazwy pozostają bez zmian...')


# generowanie nowej nazwy wg numeru w bazie
def generwuj_nazwe(oryginalna, numer=0):
    dane=pobierz_ustawienia()
    kod_nazwy = dane[7]
    kod = kod_nazwy.split(":")
    
    match kod[0]:
        case "1":
            nowa_nazwa = kod[1] + "_" + str(numer) + ".jpg"
        case "2":
           
            podziel_oryginalna = oryginalna.split(".")
            print(len(podziel_oryginalna[0]), kod[1])
            if len(podziel_oryginalna[0])>int(kod[1]):
                print('wlazlem do warunku if')
                nowa_nazwa = podziel_oryginalna[0][:int(kod[1])] + "." + podziel_oryginalna[1]
                if os.path.isfile(OUTPUT + nowa_nazwa):
                    print('wlazlem fo warunki if 2')
                    nowa_nazwa = podziel_oryginalna[0][:int(kod[1])] + "(1)." + podziel_oryginalna[1]
                    if os.path.isfile(OUTPUT + nowa_nazwa):
                        print('wlazlem do warunku if 3')
                        podziel = re.split(r'[()]', nowa_nazwa)
                        
                        numer=int(podziel[1])
                        
                        numer+=1
                        nowa_nazwa = podziel_oryginalna[0][:int(kod[1])] + "("+ str(numer) + ")" + "." + podziel_oryginalna[1]
            else:
                nowa_nazwa = oryginalna
        case "3":
            nowa_nazwa = str(numer) + ".jpg"
        case "4":
            nowa_nazwa = "edited_" + oryginalna
    return nowa_nazwa

# Wyświetla menu i steruje programem

def menu(menu='menu'):
    global akt_menu
    print("Wybierz opcję, która Cię interesuje: \n")
    
    if menu == "menu":
        print("1. Koryguj zdjęcia teraz ")
        print("2. Przerób zdjęcia na czarbo-białe")
        print("3. Zmień rozmiar zdjęć")
        print("4. Ustawienia")
        print('5. Zakończ działanie')
    elif menu == 'ustawienia':
        print("1. Ustaw domyślną nazwę zdjęć")
        print("2. Ustaw podpis")
        print("3. Wybierz domyślny profil zdjęć")
        print("4. Wyczyść profile zdjęć")
        print("5. <- Wstecz")

    wybor = input('Wybieram opcję: ')

    opcja = pobierz_ustawienia()
    SHARPNESS = opcja[0]
    BRIGHTNESS = opcja[1]
    SATURATION = opcja[2]
    CONTRAST = opcja[3]
    podpis = opcja[4]
    nazwa_plikow = opcja[7]
    if menu == 'menu':
        match wybor:
            case "1":
                folder = zmiana_folderu()
                korekcja(folder, podpis, True)
                informacje_o_profilu()
                if len(os.listdir(SOURCE + '/Sample/'))>0:
                    Sample = input(
                        'W wybranym katalogu został utworzony folder "Sample" a w nim jedno zdjęcie prezentujące ustawienia.\n\
        Czy zastosować te ustawienia do wszystkich plików? [T/N] ')
                    if Sample.lower() == 't':
                        try:
                            shutil.rmtree(folder + "/Sample")
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
                    czy_usunac()
                else:
                    linia()
                    print("-Brak plików w katalogu głównym...")
                    linia()
            case "2":
                folder = zmiana_folderu()
                korekcja(folder, podpis, True, bw=True)
                if len(os.listdir(SOURCE + '/Sample/'))>0:
                    
                    Sample = input(
                        'W wybranym katalogu został utworzony folder "Sample" a w nim jedno zdjęcie prezentujące ustawienia.\n\
                        Czy zastosować te ustawienia do wszystkich plików? [T/N] ')
                    if Sample.lower() == 't':
                        try:
                            shutil.rmtree(folder + "/Sample")
                        except:
                            pass
                        korekcja(SOURCE, podpis, bw=True)
                        czy_usunac()
                    else:
                        poprawki = input(
                            'Czy chcesz wprowadzić korekty parametrów ? [T/N]')
                        if poprawki.lower() == 't':
                            zmiana_korekcji()
                else:
                    linia()
                    print("-Brak plików w katalogu głównym...")
                    linia()

            case "3":
                # edytowanie rozmiaru zdjęcia
                if len(os.listdir(SOURCE + '/Sample/'))>0:
                    rozmiar = input(
                        "Wpisz jaki procentowy rozmiar powinno mieć finalne zdjęcie: ")
                    if "%" in rozmiar and int(rozmiar) < 100 and int(rozmiar) > 0:
                        rozmiar = rozmiar.replace("%", "")
                    elif int(rozmiar) < 100 and int(rozmiar) > 0:
                        rozmiar = int(rozmiar)/100
                        zmien_rozmiar(rozmiar)
                        czy_usunac()
                    else:
                        print('Niepoprawne dane ...')
                else:
                    linia()
                    print("-Brak plików w katalogu głównym...")
                    linia()

            case "4":
                akt_menu = 'ustawienia'
            case "5":
                quit()

    else:
        match wybor:
            case "1":
                linia()
                if nazwa_plikow!="":
                    print(f"Aktualnie używana nazwa to: {nazwa_plikow}, wpisz nową nazwę: \n")  
                else:
                    print(f"Aktualnie używana nazwa to: -Nie Zdefiniowano-, wpisz nową nazwę: \n")
                zmiana_nazw()
            
            case "2":
                ustaw_podpis()

            case "3":
                # lista profili
                profile_zdjec()
                profil = input('Podaj numer profilu, który chcesz wybrać: ')
                dane = pobierz_ustawienia(False)
                profile = {}
                if int(profil) <= len(dane) and int(profil) > 0:
                    for x, info in enumerate(dane, start=1):
                        profile[x] = info[5]
                    print(f'Wybrano profil: {profile[int(profil)]}')
                    kur.execute(f'UPDATE ustawienia SET domyslny="{False}"')
                    connection.commit()
                    kur.execute(
                        f'UPDATE ustawienia SET domyslny="{True}" WHERE nazwa="{profile[int(profil)]}"')
                    connection.commit()
                else:
                    print('Podano błędny numer...')
            
            case "4":
                # czyść profile
                zapytaj = input(
                    'Czy jesteś pewny, że chcesz usunąć wszystkie profile ( prócz domyślnego ) ? [T/N]')
                if zapytaj.lower() == 't':
                    kur.execute(
                        'DELETE FROM ustawienia WHERE nazwa!="domyslne"')
                    connection.commit()
                    print('Profile usunięte...')
                    linia()
                else:
                    print('Przechodzę więc do menu...')
            case "5":
                akt_menu = 'menu'

# czyszczenie okna konsoli
def clear_screen():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')
# główna funkcja korygująca wszystkie zdjęcia lub próbkę w katalogu
def korekcja(adres, podpis, Sample=False, adres_zapisu="", bw=False):
    clear_screen()
    dane = pobierz_ustawienia()
    SHARPNESS = dane[0]
    BRIGHTNESS = dane[1]
    SATURATION = dane[2]
    CONTRAST = dane[3]
    SOURCE = adres
    OUTPUT = SOURCE + "/Edited/"
    FILES_COUNT = 0
    new_output = SOURCE + '/Sample/'
    watermark_folder = SOURCE + '/Watermark/'
    add_logo=False
    numer=1
    if Sample:
        if not os.path.isdir(new_output):
            print('- Tworzenie nowego katalogu pod zdjęcie próbne...')
            try:
                os.mkdir(new_output)
                os.mkdir(watermark_folder)
            except FileExistsError:
                pass
        else:
            try:
                print('- Tworzenie folderu "Watermark" na znak wodny do zdjęcia...')
                os.mkdir(watermark_folder)
            except FileExistsError:
                pass
    else:
        try:
            os.mkdir(SOURCE + "/Edited")
            os.mkdir(watermark_folder)
        except:
            pass
    if os.path.isdir(SOURCE + "/Watermark/"):
        lista = os.listdir(SOURCE + "/Watermark/")
        if len(lista)>0:
            if ".png" in lista[0].lower():
                plik_logo = lista[0]
                print('Logo: ', plik_logo)
                pytanie = input("Znaleziono folder ze znakiem wodnym. Czy chcesz dodać go zamiast podpisu? [T/N] ")
                if pytanie.lower()=='t':
                    add_logo=True
            else:
                print('- Znaleziono znaki wodne, jednak muszą być z rozszerzeniem PNG aby je zastosować.')
        else:
            print("- Nie znaleziono znaków wodnych lub w folderze znajduje się więcej niż jeden...")
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
                width, height = new_file.size
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
                # podpisz zdjęcie jeśli zdefiniowano
                if podpis != "" and not add_logo:
                    print("- Dodaję podpis...")

                    kwadrat = ImageDraw.Draw(new_file, mode='RGBA')

                    napis = ImageDraw.Draw(new_file)
                    czcionka = ImageFont.truetype(
                        'arial.ttf', int(width*0.015))
                    pos_x, pos_y, szerokosc_czcionki, wysokosc_czcionki = czcionka.getbbox(
                        podpis)

                    text_x = width - szerokosc_czcionki - (width*0.015)
                    text_y = height - wysokosc_czcionki - (height*0.015)
                    kwadrat.rectangle((text_x-(width*0.007), text_y-(height*0.007),
                                   width-(width*0.007), height-(height*0.007)), fill=(0, 0, 0, 100))
                    napis.text((text_x, text_y), podpis,
                               font=czcionka, fill=(255, 255, 255))

                if not bw:
                    # zmiana nasycenia kolorów
                    print(f'- Zmieniam saturacje o {SATURATION*100}%')
                    # obrazek tymczasowy
                    tymczasowy = new_file.convert('HSV')
                    tylko_saturacja = tymczasowy.split()[1]
                    nasycenie_zmodyfikowane = tylko_saturacja.point(
                        lambda x: x+(x*SATURATION))
                    tymczasowy = Image.merge(
                        'HSV',
                        (tymczasowy.split()[0], nasycenie_zmodyfikowane, tymczasowy.split()[2]))
                    new_file = tymczasowy.convert('RGB')
                else:
                    print("- Zmieniam obraz na czarbo-biały...")
                    new_file = new_file.convert("L")
                
                if add_logo:
                    print('- Dodaję logo...')
                    logo = Image.open(watermark_folder + plik_logo)
                    logo_width, logo_height = logo.size
                    logo_mini_width = int(width/10)
                    skala = logo_mini_width / logo_width
                    logo_mini_height = int(skala * logo_height)
                    logo=logo.resize((logo_mini_width, logo_mini_height))
                    new_file.paste(logo, (width-logo_mini_width, height - logo_mini_height), logo)
                
                # zapis poprawionego pliku
                # zapisz jeśli ma byc to próbka
                if Sample:                    
                    new_file.save(new_output + generwuj_nazwe(name, numer))
                    OUTPUT = OUTPUT.replace("//", "\\")
                # zapisz jeśli zaakceptowano próbkę
                else:
                    new_file.save(OUTPUT + generwuj_nazwe(name, numer))
                    OUTPUT = OUTPUT.replace("//", "\\")
                numer+=1
                linia()

        if Sample and FILES_COUNT > 0:
            break

    if new_output and Sample:
        print('- Pliki zostały zapisane do: ', new_output)
    else:
        print('- Pliki zostały zapisane do: ', OUTPUT)
    # wyświetl czas potrzebny do obróbki zdjęć
    TIME_AFTER = time.time()
    czas = int(TIME_AFTER-TIME_BEFORE)
    print(f'- Przetworzonych plików: {FILES_COUNT}')
    if FILES_COUNT>0:
        print(f"- Czas wykonania: {czas} sekund ({czas/FILES_COUNT}/sek na zdjęcie)")
    linia()


while not done:
    menu(akt_menu)

connection.close()

# dodać interface graficzny
# dodać suwaki do parametrów
