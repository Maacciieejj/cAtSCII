import time #import mehanizmu czasu
import random
from links.nagrobek import nagrobek #import asci artow




# ponizej definicja funkcji wazne wydarzenia uruchamianej w wątku dodatkowym

def wazne_wydarzenia(kot): # definicja funkcji 
    global przelacznik1  # deklarujemy użycie zmiennej globalnej
    
    while True:
        if przelacznik1: # jeśli przełącznik włączony, czekamy w pierwszej pętli (sen)
            time.sleep(2)
            continue

        czas_oczekiwania = random.choice([600, 900, 900, 1200, 1500])  # losuje czas oczekiwania w sekundach

        # zamiast jednego długiego czekania, dzielimy je na sekundowe interwały i co sekunde sprawdzamy czy nie włączylismy kociego spanka
        for _ in range(czas_oczekiwania): #tworzy pętlę, która będzie wykonywać się tyle razy, ile wynosi wartość czas_oczekiwania
            if przelacznik1:  # sprawdzamy przełącznik co 1 sekunde
                break  # jeśli włączony, przerywamy czekanie
            time.sleep(1)           
        if przelacznik1:  # jeśli przełącznik został włączony, wracamy na początek głównej pętli
            continue
        

        kot.aktualizuj_statystyki() # aktualizacja statsow przed wydarzeniami


        if not kot.zyje():  # sprawdź czy kot żyje przed wydarzeniem
            print("\nTwój kot zmarł!") 
            print(nagrobek)
            kot.zapisz_log("R. I. P.") #zapis logu
            break

        wydarzenie = random.choice(["biegunka", "smutek", "upolowanie_myszy", "spotkanie_kocich_znajomych", "psia_inwazja", "dzieci_głaszcza", "szwedanie"]) # losowanie wydarzenia
        getattr(kot, wydarzenie)()  # Wywołuje metodę o nazwie wylosowanego wydarzenia na obiekcie kot . Na przykład, jeśli wylosowano "biegunka", to wykona się kot.biegunka()
        kot.zapisz_log(f"WAŻNE WYDARZENIE: {wydarzenie}") # zapisuje log
        kot.pokaz_stan()
        print("(Menu: enter)")
