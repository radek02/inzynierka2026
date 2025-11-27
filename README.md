# Architektura
API udostępniające system rekomendacyjny jest napisane w Python FastAPI, znajduje się w folderze `proj/`. 
Model korzystający z `collaborative filtering` znajduje się w `Models/ALS` i to na jego podstawie API zwraca rekomendacje dla użytkownika. 
Model korzystający z `content-based filtering` znajduje się w `Models/ContentBased`, na jego podstawie API będzie zwracać książki podobne do danej książki.

# Testowe uruchomienie modeli

Podane ścieżki w komendach zakładają uruchamianie z "korzenia" repozytorium.

### 1. Dane

Do wytrenowania modeli potrzebujemy danych, są dwie możliwości:
- skorzystanie z istniejących `input_data/goodreads_interactions_example.csv` oraz `input_data/goodreads_books_example.json.gz` (zawierają po 1000 pierwszych linijek z oryginalnych plików),
- pobranie oryginalnych plików:
  - (~4GB) `curl -L --progress-bar -o goodreads_interactions.csv "https://mcauleylab.ucsd.edu/public_datasets/gdrive/goodreads/goodreads_interactions.csv"`
  - (~2GB) `curl -L --progress-bar -o goodreads_books.json.gz "https://mcauleylab.ucsd.edu/public_datasets/gdrive/goodreads/goodreads_books.json.gz"`

### 2. Wytrenowanie modeli

W przypadku korzystania z plików innych niż `*_example*` należy dostosować argument `--input_file`.

**a) collaborative filtering:**
- `pip install -r Models/ALS/requirements.txt`
- `python Models/ALS/MatrixFactorization.py --input_file input_data/goodreads_interactions_example.csv`

**b) content-based filtering:**
- `pip install -r Models/ContentBased/requirements.txt`
- `python Models/ContentBased/train_tfidf.py --input_file input_data/goodreads_books_example.json.gz`

### 3. Uruchomienie

**a) collaborative filtering:**
- `python Models/ALS/test_recommendations.py --user_id=1`

**b) content-based filtering:**
- `python Models/ContentBased/test_similar_books.py --book_id=18628480`

# Testowe uruchomienie serwisu API:

- w folderze `proj/` należy uruchomić `docker-compose up`
  - program będzie działał, ale nie zwróci żadnych rekomendacji, bo wymaga to dodatkowej konfiguracji/trenowania modelu (docelowo będzie to zautomatyzowane celem łatwego odtworzenia)
  - żeby zobaczyć dokumentację API w Swagger należy odwiedzić `http://localhost:8000/docs`, tam też można wysłać zapytania

# Opis użytych algorytmów

### Collaborative Filtering (ALS)

Faktoryzacja macierzy rozkłada macierz interakcji użytkownik-książka na dwie mniejsze macierze: embeddingi użytkowników i embeddingi książek. Każdy użytkownik i każda książka są reprezentowane jako wektor o stałej długości (np. 32 wymiary).

Algorytm ALS (Alternating Least Squares) uczy się tych wektorów tak, aby iloczyn skalarny wektora użytkownika i wektora książki przybliżał ocenę, jaką użytkownik wystawił książce. Rekomendacje generujemy obliczając iloczyn skalarny wektora użytkownika ze wszystkimi wektorami książek i wybierając te z najwyższym wynikiem.

### Content-Based Filtering (TF-IDF)

TF-IDF (Term Frequency-Inverse Document Frequency) przekształca tekst w wektory liczbowe. Dla każdej książki tworzymy "dokument" składający się z tytułu, autorów i gatunków.

- **TF** (Term Frequency) - jak często słowo występuje w danym dokumencie
- **IDF** (Inverse Document Frequency) - jak rzadkie jest słowo w całym zbiorze (rzadsze słowa są ważniejsze)

Podobieństwo między książkami obliczamy za pomocą cosine similarity między ich wektorami TF-IDF. Książki o podobnych tytułach, autorach i gatunkach będą miały wysokie podobieństwo.


# Milestone 3
Na ten milestone dostarczamy częściowo rozłączny system, składający się z modułów: CommunicationService, RecommendationService, Background, Database, Vector Database oraz modułów rekomendacyjnych.
System można uruchomić używając docker compose, jednak na tym etapie nie będzie to działało od razu, ponieważ w tym momencie nie istnieje pipeline tworzenia embeddings → zapisywania ich do wektorowej bazy danych.

Część funkcjonalności nie jest jeszcze zintegrowana z serwisem API: 
1. Content-based (algorytm jest zdefiniowany, jednak nie jest w tym momencie dodany do samego serwisu; po dodaniu będzie użyty dla funkcjonalności „podaj podobne książki”).
2. Odświeżanie embeddings użytkownika po nowej interakcji wymaga pełnej integracji modeli ALS z serwisem.
3. System nie jest w tym momencie zintegrowany z cachem
4. Modele Ranking i Re-ranking są zamockowane


# Komentarz w sprawie wyboru ALS
Dla głównego modelu rekomendacyjnego stosujemy nowoczesną architekturę systemów rekomendacyjnych: `Candidate Generation → Ranking → Re-ranking`.
Faktoryzację macierzy metodą ALS stosujemy, aby znaleźć embeddings użytkowników i książek (które są wymagane na etapie candidate generation oraz ranking).
Używanie faktoryzacji macierzy jest dominującym podejściem w branży (szczególnie w przypadku ograniczonych zasobów obliczeniowych).
Wybór ALS został dokonany ze względu na to, że takie podejście jest bardzo efektywne pod względem kosztów obliczeniowych i ma bardzo dobrą zbieżność. Badania wykazują również, że ALS działa lepiej niż inne techniki faktoryzacji w przypadku większych zbiorów danych (`>100000` aktywnych użytkowników).
