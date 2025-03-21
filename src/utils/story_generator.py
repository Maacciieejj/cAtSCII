import textwrap  # dodajemy import dla zawijania tekstu
import requests #potrzebne do komunikacji z api llm





#ponizej funkcja do generowania historyjki
def generuj_historyjke(prompt):
    try:
        response = requests.post(
            "https://odd-bonus-11b1.panasm.workers.dev/",  # Twój worker URL
            headers={
                "Content-Type": "application/json",
                "HTTP-Referer": "https://localhost:5000",
                "X-Title": "Local Test"
            },
            json={
                "prompt": prompt  # Worker oczekuje pola "prompt"
            }
        )
        response.raise_for_status()
        data = response.json()
        
        if 'error' in data:
            return f"Error: {data['error']}"

        ## ponizej generujemy tekst na 2 wyjscia - niepolamany do spis_wydarzen i polamany do gry
        if 'candidates' in data and len(data['candidates']) > 0:
            text = data['candidates'][0]['content']['parts'][0]['text']
            return text  # Zwracamy czysty tekst
        else:
            return "Nie udało się wygenerować historyjki: Nieprawidłowa odpowiedź"
            
    except Exception as e:
        return f"Nie udało się wygenerować historyjki: {str(e)}"

# Nowa funkcja do formatowania tekstu do wyświetlenia
def formatuj_do_wyswietlenia(text):   
    return textwrap.fill(text, width=70)

