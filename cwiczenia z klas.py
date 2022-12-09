class Zwierze:
    def __init__(self, nazwa, rasa):
        self.nazwa=nazwa
        self.rasa = rasa
        self.kierunki=['prawo', 'lewo', 'gora', 'dol']
    def ruch(self, kierunek):
        if kierunek in self.kierunki:
            print(self.nazwa, ' rusza się w ', kierunek)
        else:
            print(self.nazwa, f' nie rozumie komendy {kierunek}!')
    def glos(self):
        if self.rasa=='pies':
            print('HauHau')
        elif self.rasa=='kot':
            print('MiauMiau')
        elif self.rasa=='ptak':
            print('PiPiPi')
        else:
            print(f'{self.rasa} nie wydaje dźwięków ...')

    


rudy = Zwierze('tofik', 'chomik')
rudy.ruch('skacz')
rudy.glos()