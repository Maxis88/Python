import matplotlib.pyplot as plt 
import numpy as np


def read_data():
    h_start = float(input("Podaj wysokość początkową: "))
    v_start = float(input("Podaj prędkość początkową: "))

    # sprawdzanie danych
    if h_start<=2:
        print("Podana wysokość jest zbyt mała ! Podaj wartość większą niż 2m...")
        return None
    
    if v_start<=2:
        print("Podana prędkość jest za niska. Podaj wartość większą niż 2m/s")
        return None
    return (h_start, v_start)
dane_startowe = None

while dane_startowe is None:
    print("Podaj dane początkowe by rozpocząć pracę:")
    dane_startowe = read_data()
print("OK, dane zostały poprawnie wprowadzone! Zacznijmy więc pracę...")
# pobierz dane z krotki
H_START, V_START = dane_startowe
# dane potrzebne do obliczeń
#   przyciąganie ziemskie
g = 9.81
#   czas spadania
czas = ((H_START * 2) / g) ** (1/2)
#   zasieg spadania
zasieg = V_START * czas
x_points = np.arange(0, zasieg, zasieg/100)
y_points = H_START - ((g/2)*(x_points/V_START)**2)
# zacznij tworzyć wykres
plt.scatter(0, H_START, label=f"Wysokość = {H_START} m")
plt.scatter(zasieg, 0, label=f"Zasięg = {round(zasieg, 3)} m")
plt.plot(x_points, y_points, marker="o", color="red", label="Kolejne punkty wykresu")
plt.xlabel("Odległość w m")
plt.ylabel("Wysokość w m")
plt.title(f"Wykres lotu dla obiektu wyrzuconego z {H_START} m,\n oraz prędkością początkową:\
     {V_START} m/s, \nczas lotu: {round(czas, 3)} s")
plt.grid()
plt.legend()
plt.show()

    


