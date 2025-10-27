import ollama
import csv
import datetime
import sys

# --- 1. Konfiguracja ---

print("Uruchamianie skryptu testującego Ollama...")

# Upewnij się, że usługa Ollama jest uruchomiona.
# Skrypt zakłada, że modele są już pobrane (ollama pull ...)

MODELS_TO_TEST = [
    "SpeakLeash/bielik-1.5b-v3.0-instruct:Q8_0",
    "SpeakLeash/bielik-7b-instruct-v0.1-gguf:Q8_0"
]

PROMPTS = [
    # 1. Wiedza ogólna
    "W którym roku Polska przystąpiła do Unii Europejskiej i kto był wtedy prezydentem Polski?",
    # 2. Instrukcje
    "Wyjaśnij w dwóch zdaniach, czym jest inflacja i podaj jeden konkretny przykład, jak wpływa ona na codzienne zakupy.",
    # 3. Kreatywność
    "Wymyśl nazwę dla nowej kawiarni w Warszawie, która specjalizuje się w kawie i starych książkach. Podaj jedno zdanie uzasadnienia dla tej nazwy.",
    # 4. Tłumaczenie
    "Przetłumacz na angielski: Mój pociąg był opóźniony o dwadzieścia minut z powodu awarii.",
    # 5. Ekstrakcja informacji (JSON)
    "Z tekstu: 'Faktura nr 45/2023 dla firmy 'ABC-Pol' na kwotę 1500.50 PLN' wyodrębnij {numer, klient, kwota, waluta} i zapisz wynik ekstrakcji w formacie JSON.",
    # 6. Analiza sentymentu
    "Zdanie: 'Film był trochę przydługi, ale scenografia robiła wrażenie.' — pozytywny / negatywny / neutralny i dlaczego?"
]

# Definiujemy niską i wysoką temperaturę
TEMPERATURES = [0.2, 1.0] 

# Nazwa pliku wyjściowego z unikalnym znacznikiem czasu
timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
OUTPUT_FILE = f"wyniki_testu_ollama_{timestamp}.csv"

# --- 2. Główna pętla testująca ---

all_results = []
total_runs = len(MODELS_TO_TEST) * len(PROMPTS) * len(TEMPERATURES)
current_run = 0

print(f"Rozpoczynam {total_runs} testów...")

try:
    for model_name in MODELS_TO_TEST:
        for prompt_text in PROMPTS:
            for temp in TEMPERATURES:
                current_run += 1
                print(f"\n--- Postęp: {current_run}/{total_runs} ---")
                print(f"Model: {model_name}")
                print(f"Temp:  {temp}")
                print(f"Prompt: {prompt_text[:60]}...") # Wyświetl początek promptu

                try:
                    # Wywołanie klienta Ollama
                    # Używamy ollama.chat() i przekazujemy temperaturę w 'options'
                    response = ollama.chat(
                        model=model_name,
                        messages=[{'role': 'user', 'content': prompt_text}],
                        options={'temperature': temp}
                    )
                    
                    # Ekstrakcja czystej odpowiedzi
                    response_text = response['message']['content'].strip()
                    print(f"Odpowiedź: {response_text}") # Wyświetl początek odpowiedzi

                except Exception as e:
                    # Obsługa błędów, np. gdy model nie jest pobrany lub serwer nie działa
                    print(f"!!! BŁĄD podczas wywołania modelu: {e}")
                    response_text = f"BŁĄD: {str(e)}"
                
                # Dodanie wyników do listy
                all_results.append([model_name, prompt_text, response_text, temp])

except KeyboardInterrupt:
    print("\nTesty przerwane przez użytkownika. Zapisuję dotychczasowe wyniki...")

# --- 3. Zapis wyników do pliku CSV ---

print(f"\nZakończono wszystkie testy. Zapisywanie wyników do pliku: {OUTPUT_FILE}")

try:
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        writer = csv.writer(f)
        
        # Zapis nagłówka
        writer.writerow(["Model", "Prompt", "Odpowiedź", "Temperatura"])
        
        # Zapis wszystkich zebranych wyników
        writer.writerows(all_results)
        
    print(f"Pomyślnie zapisano {len(all_results)} wyników do {OUTPUT_FILE}")

except IOError as e:
    print(f"!!! Krytyczny błąd zapisu pliku: {e}")
    print("Oto wyniki, które nie zostały zapisane (skopiuj je ręcznie):")
    for row in all_results:
        print(row)

print("Skrypt zakończył działanie.")
