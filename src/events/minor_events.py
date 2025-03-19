import time #import mehanizmu czasu
import random
from links.nagrobek import nagrobek #import asci artow
from src.shared.switches import get_switch_state # importujemy stan przełącznika chyba



# ponizej definicja funkcji drobnych wydarzeń uruchamianej w wątku dodatkowym

def drobne_wydarzenia(kot): # definicja funkcji 
    while True:
        if get_switch_state():  # sprawdzamy aktualny stan z pliku
            time.sleep(2)
            continue
    
        czas_oczekiwania = random.choice([120, 120, 120, 120, 120, 120, 60, 60, 60, 60, 180, 180, 300, 300])  # losuje czas oczekiwania w sekundach
        
        
        for _ in range(czas_oczekiwania):
            if get_switch_state():  #
                break
            time.sleep(1)           
        if get_switch_state():  
            continue


        kot.aktualizuj_statystyki() # aktualizacja statsow przed wydarzeniami


        if not kot.zyje():  # sprawdź czy kot żyje przed wydarzeniem
            print("\nTwój kot zmarł!") 
            print(nagrobek)
            kot.zapisz_log("R. I. P.") #zapis logu
            break

        wydarzenie = random.choice(["szwedanie","przeciaganie", "upadek_z_krzesla", "mruczenie", "kaslanie", "upolowanie_muchy", "gonitwa_po_meblach", "upolowanie_pajaka", "wycieczka_na_dach", "wizyta_kota_sasiada", "utkniecie_pod_zlewem", "spotkanie_z_jezem", "koci_marazm"]) # losowanie wydarzenia
        getattr(kot, wydarzenie)()  # Wywołuje metodę o nazwie wylosowanego wydarzenia na obiekcie kot . Na przykład, jeśli wylosowano "biegunka", to wykona się kot.biegunka()
        kot.zapisz_log(f"Drobne wydarzenie:{ wydarzenie}") # zapisuje log
        kot.pokaz_stan()
        print("(Menu: enter)")

