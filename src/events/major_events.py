import time #import mehanizmu czasu
import random
from links.nagrobek import nagrobek #import asci artow
from src.shared.switches import get_switch_state # to jest zmienna przełącznika, która będzie sprawdzana w każdym momencie



# ponizej definicja funkcji wazne wydarzenia uruchamianej w wątku dodatkowym

def wazne_wydarzenia(kot): # definicja funkcji 
    while True:
        if get_switch_state():  # sprawdzamy aktualny stan z pliku
            time.sleep(2)
            continue

        czas_oczekiwania = random.choice([600, 900, 900, 1200, 1500])  # losuje czas oczekiwania w sekundach

        # zamiast jednego długiego czekania, dzielimy je na sekundowe interwały i co sekunde sprawdzamy czy nie włączylismy kociego spanka
        for _ in range(czas_oczekiwania): #tworzy pętlę, która będzie wykonywać się tyle razy, ile wynosi wartość czas_oczekiwania
            if get_switch_state():  # sprawdzamy  co 1 sekunde
                break  # jeśli włączony, przerywamy czekanie
            time.sleep(1)           
        if get_switch_state():  # jeśli przełącznik został włączony, wracamy na początek głównej pętli
            continue
        

        kot.aktualizuj_statystyki() # aktualizacja statsow przed wydarzeniami


        if not kot.zyje():  # sprawdź czy kot żyje przed wydarzeniem
            print("\nTwój kot zmarł!") 
            print(nagrobek)
            kot.zapisz_log("R. I. P.") #zapis logu
            break

        wydarzenie = random.choice(["najedz_down2", "dostatekuw_down2", "najedz_up2", "dostatekuw_up2", "zadb_down2", "zadb_up2"]) # losowanie wydarzenia
        getattr(kot, wydarzenie)()  # Wywołuje metodę o nazwie wylosowanego wydarzenia na obiekcie kot . Na przykład, jeśli wylosowano "biegunka", to wykona się kot.biegunka()
        kot.zapisz_log(f"WAŻNE WYDARZENIE: {wydarzenie}") # zapisuje log
        kot.pokaz_stan()
        print("(Menu: enter)")
