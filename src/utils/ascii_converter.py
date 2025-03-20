from PIL import Image
import requests
from io import BytesIO
from duckduckgo_search import DDGS
import random #import mehanizmu losowego



# Funkcje do konwersji obrazów na ASCII art i wyszukiwania obrazów

def obraz_na_ascii(sciezka_lub_url, szerokosc_wyjscia=200):
    """Konwertuje obraz na ASCII art. Obsługuje zarówno lokalne pliki jak i URL-e."""

    try:
        # Sprawdź czy to URL czy ścieżka lokalna
        if sciezka_lub_url.startswith(('http://', 'https://')):
            # Pobierz obraz z URL
            response = requests.get(sciezka_lub_url)
            obraz = Image.open(BytesIO(response.content)).convert('L')
        else:
            # Otwórz lokalny plik
            obraz = Image.open(sciezka_lub_url).convert('L') # Otwórz obraz i przekonwertuj na skalę szarości ('L')
    except Exception as e:
        return f"Błąd podczas otwierania obrazu: {str(e)}"

    szerokosc_obrazu, wysokosc_obrazu = obraz.size
    stosunek_aspektu = wysokosc_obrazu / szerokosc_obrazu
    wysokosc_wyjscia = int(szerokosc_wyjscia * stosunek_aspektu * 0.5) # Dostosowanie wysokości, 0.5 bo znaki nie są kwadratowe

    obraz = obraz.resize((szerokosc_wyjscia, wysokosc_wyjscia))
    piksele = obraz.getdata()

    znaki_ascii = [" ", ".", ",", "-", "+", "*", "#", "@"] # Im dalej w prawo, tym gęstszy znak
    dlugosc_znakow = len(znaki_ascii)

    ascii_art = ""
    for i in range(0, wysokosc_wyjscia):
        for j in range(0, szerokosc_wyjscia):
            piksel_index = i * szerokosc_wyjscia + j
            jasnosc_piksela = piksele[piksel_index]
            index_znaku = int(jasnosc_piksela / 255 * (dlugosc_znakow - 1)) # Mapowanie jasności na index znaku
            ascii_art += znaki_ascii[index_znaku]
        ascii_art += "\n" # Nowa linia po każdym rzędzie

    return ascii_art

def wyszukaj_i_konwertuj(zapytanie, max_wynikow=20):
    """Wyszukuje obrazy za pomocą DuckDuckGo, losuje jeden i konwertuje na ASCII art."""
    try:
        with DDGS() as ddgs:
            # Pobieramy więcej wyników, aby mieć większą pulę do losowania
            wyniki = list(ddgs.images(zapytanie, max_results=max_wynikow))
        
        if not wyniki:
            raise Exception("Nie znaleziono wyników")
        
        # Używamy miniatur zamiast pełnych obrazów (a nie jak to zakomentowane ponizej)
        url_obrazow = [wynik['thumbnail'] for wynik in wyniki]        

        # Wyciągnij URL-e obrazów z wyników
        #url_obrazow = [wynik['image'] for wynik in wyniki] #tu pobierane byly pelne obrazy
        
        # Losowo wybierz jeden obraz
        losowy_url = random.choice(url_obrazow)
        
        # Konwertuj na ASCII art
        return obraz_na_ascii(losowy_url)
    except Exception as e:
        print(f"Błąd podczas wyszukiwania obrazów: {str(e)}")
        print("Napotkano limit zapytań. Używanie alternatywnej metody...")
        
        # Alternatywna metoda - używamy przykładowego URL-a obrazu
        przykladowy_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3a/Cat03.jpg/1200px-Cat03.jpg"
        
        # Konwertuj na ASCII art
        return obraz_na_ascii(przykladowy_url)