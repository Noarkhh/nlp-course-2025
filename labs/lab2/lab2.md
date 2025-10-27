### 1. Informacje o środowisku

  * **System operacyjny**: macOS 14.7.5 (23H527 arm64)
  * **CPU**: Apple M3 Pro
  * **RAM**: 18 GB (18432 MiB)
  * **GPU / VRAM**: Apple M3 Pro (Zunifikowana pamięć)
  * **Narzędzie**: Ollama (wnioskowane na podstawie poleceń w instrukcji)
  * **Modele**:
      * `SpeakLeash/bielik-1.5b-v3.0-instruct:Q8_0`
      * `SpeakLeash/bielik-7b-instruct-v0.1-gguf:Q8_0`

### 2. Przykładowe polecenia uruchamiające

Poniższe polecenia (zgodne z formatem `ollama run model -p "..." -t <temp>`) odtwarzają wybrane testy z dostarczonych wyników CSV:

1.  **Test wiedzy (Bielik 1.5B, niska temperatura)**

    ```bash
    ollama run SpeakLeash/bielik-1.5b-v3.0-instruct:Q8_0 -p "W którym roku Polska przystąpiła do Unii Europejskiej i kto był wtedy prezydentem Polski?" -t 0.2
    ```

    *(Wynik z CSV: "Polska przystąpiła do Unii Europejskiej w 2004 roku. Wtedy prezydentem Polski był Aleksander Kwaśniewski.")*

2.  **Test ekstrakcji JSON (Bielik 7B, niska temperatura)**

    ```bash
    ollama run SpeakLeash/bielik-7b-instruct-v0.1-gguf:Q8_0 -p "Z tekstu: 'Faktura nr 45/2023 dla firmy 'ABC-Pol' na kwotę 1500.50 PLN' wyodrębnij {numer, klient, kwota, waluta} i zapisz wynik ekstrakcji w formacie JSON." -t 0.2
    ```

    *(Wynik z CSV: JSON z błędnie wyodrębnionym numerem: "45" zamiast "45/2023")*

3.  **Test tłumaczenia (Bielik 1.5B, wysoka temperatura)**

    ```bash
    ollama run SpeakLeash/bielik-1.5b-v3.0-instruct:Q8_0 -p "Przetłumacz na angielski: Mój pociąg był opóźniony o dwadzieścia minut z powodu awarii." -t 1.0
    ```

    *(Wynik z CSV: Chaotyczna lista słów kluczowych, całkowita porażka wykonania zadania.)*

### 6.3. Tabela porównawcza i wnioski

Poniższa tabela syntetyzuje obserwacje z dostarczonych danych CSV, porównując dwa modele Bielika przy różnych temperaturach.

| Model | Temperatura | Obserwacje (na podstawie danych CSV) |
| :--- | :--- | :--- |
| **Bielik 1.5B** | **0.2** (Niska) | **Precyzyjny i spójny.** Poprawnie odpowiedział na pytanie o UE (fakt). Wykonał idealną ekstrakcję JSON. Poprawnie przetłumaczył zdanie (choć "emergency" zamiast "failure"). Odpowiedzi są na temat, choć nie zawsze trzymają się ograniczeń (np. długości). |
| **Bielik 1.5B** | **1.0** (Wysoka) | **Niestabilny i niespójny.** Całkowicie zawiódł przy tłumaczeniu (wygenerował listę słów). Na pytanie o UE odpowiedział formatem testu wielokrotnego wyboru, podając błędne informacje. Ekstrakcja JSON była poprawna, ale typ danych `kwota` został błędnie zapisany jako string. |
| **Bielik 7B** | **0.2** (Niska) | **Mieszane rezultaty, tendencja do angielskiego.** Popełnił błąd faktograficzny (podał złego prezydenta). Wykonał ekstrakcję JSON niepoprawnie (obciął numer faktury). Odpowiedzi na wiele pytań (np. o kawiarnię, sentyment) były generowane w języku angielskim. |
| **Bielik 7B** | **1.0** (Wysoka) | **Bardziej spójny niż 1.5B przy tej temp., ale wciąż nieprzewidywalny.** Poprawił swój błąd i *poprawnie* odpowiedział na pytanie o UE (inaczej niż przy temp. 0.2). Ekstrakcja JSON nadal była błędna (obcięty numer) i używała angielskich kluczy. |

**Krótkie wnioski:**

1.  **Temperatura jest kluczowa:** Dla małych modeli (1.5B) temperatura `1.0` prowadzi do całkowitej utraty spójności. Niska temperatura (np. `0.2`) jest niezbędna do zadań wymagających precyzji.
2.  **Większy nie znaczy lepszy:** Model 1.5B (przy niskiej temp.) okazał się lepszy w zadaniu ekstrakcji JSON i bardziej konsekwentny w używaniu języka polskiego niż model 7B.
3.  **Halucynacje:** Wystąpiły w obu modelach. Co ciekawe, model 7B halucynował przy niskiej temperaturze, a podał poprawną odpowiedź przy wysokiej.

-----

## 7\. Pytania o umiejętności modelu

### 1\. Język polski

Na podstawie testów, mniejszy model **Bielik 1.5B** (przy niskiej temp.) radzi sobie z językiem polskim poprawnie gramatycznie i spójnie. Model **Bielik 7B** ma wyraźną tendencję do "uciekania" w język angielski, nawet gdy pytanie jest zadane po polsku (np. w teście kreatywnym i analizie sentymentu).

### 2\. Faktyczność

Tak, model halucynował. **Bielik 7B** (temp 0.2) błędnie podał Lecha Kaczyńskiego jako prezydenta w 2004 r. **Bielik 1.5B** (temp 1.0) również podał błędne informacje w formacie testu ABCD. Co ciekawe, Bielik 7B przy temp 1.0 podał poprawną odpowiedź, co sugeruje, że niska temperatura nie zawsze gwarantuje poprawność faktograficzną.

### 3\. Instrukcje

Modele słabo podążają za precyzyjnymi instrukcjami dotyczącymi formatu. W teście "Wyjaśnij w dwóch zdaniach..." oba modele (niezależnie od temperatury) wygenerowały odpowiedzi znacznie dłuższe niż dwa zdania, ignorując to ograniczenie.

### 4\. Rozumowanie

Dostarczone dane CSV (testy wiedzy, ekstrakcji, tłumaczenia) nie zawierają zapytań wystarczająco złożonych, aby ocenić myślenie wieloetapowe.

### 5\. Ekstrakcja informacji

Model **Bielik 1.5B (temp 0.2)** poradził sobie z ekstrakcją do formatu JSON *idealnie*, poprawnie identyfikując wszystkie pola i zachowując typy danych. Model **Bielik 7B** popełnił błąd, obcinając `numer` faktury (z "45/2023" na "45"). Wysoka temperatura w 1.5B spowodowała błąd w typowaniu (kwota jako string).

### 6\. Kreatywność vs precyzja

W przypadku tych modeli, **temperatura `1.0` prowadzi do chaosu**, a nie kreatywności. Bielik 1.5B przy `t=1.0` był bezużyteczny w teście tłumaczenia. Dla precyzji (fakty, JSON, tłumaczenie) absolutnie konieczna jest niska temperatura (np. `0.2`). Kompromis dla zadań kreatywnych musiałby leżeć znacznie niżej niż `1.0`, być może w okolicach `0.5-0.7` (co nie zostało przetestowane).

### 7\. Wydajność

**Nie można zweryfikować** wpływu GPU ani różnic w czasie generowania na podstawie dostarczonych danych CSV, ponieważ nie zawierają one pomiarów wydajności (np. tokeny/s lub czas odpowiedzi).

### 8\. Bezpieczeństwo

**Nie zaobserwowano** odmawiania odpowiedzi ani cenzury. Żadne z pytań testowych w dostarczonych danych nie dotyczyło jednak tematów drażliwych, kontrowersyjnych ani nie próbowało obejść zabezpieczeń.

### 9\. Porównanie narzędzi

Sprawozdanie bazuje wyłącznie na testach przeprowadzonych przy użyciu jednego zestawu narzędzi (najprawdopodobniej Ollama, sądząc po instrukcji). **Porównanie do LM Studio nie jest możliwe** na podstawie tych danych.

-----

### I ostatnia-refleksja

Testy pokazały, że nawet bardzo małe lokalne modele (1.5B) potrafią być zaskakująco skuteczne w wąskich, ustrukturyzowanych zadaniach, takich jak ekstrakcja JSON – radząc sobie lepiej niż model 7B. Nauczyłem się też, jak krytycznym i niestabilnym parametrem jest temperatura; dla małych modeli jej podniesienie nie tyle zwiększa "kreatywność", co prowadzi do utraty spójności. W kolejnych laboratoriach planuję sprawdzić, czy większe modele (np. 11B+) lepiej radzą sobie z instrukcjami i czy faktycznie akceleracja GPU (w porównaniu do samego CPU) drastycznie skraca czas generowania odpowiedzi na tej platformie (Apple M3 Pro).
