# Architektura
API udostępniające system rekomendacyjny jest napisane w Python FastAPI, znajduje się w folderze `proj/`. Model korzystający z `collaborative filetring` znajduje się w `Models/ALS` i to na jego podstawie API zwraca rekomendacje. 

# Uruchomienie systemu w trybie "Development":

- w folderze `proj/` należy uruchomić `docker-compose up`
  - program będzie działał, ale nie zwróci żadnych rekomendacji, bo wymaga to dodatkowej konfiguracji/trenowania modelu (docelowo będzie to zautomatyzowane celem łatwego odtworzenia)
  - żeby zobaczyć dokementację API w Swagger należy odwiedzić `http://localhost:8000/docs`, tam też można wysłać zapytania

# Milestone 3
Na ten milestone dostarczamy częściowo rozłączny system, składający się z modułów: CommunicationService, RecommendationService, Background, Database, Vector Database oraz modułów rekomendacyjnych.
System można uruchomić używając docker compose, jednak na tym etapie nie będzie to działało od razu, ponieważ w tym momencie nie istnieje pipeline tworzenia embeddings → zapisywania ich do wektorowej bazy danych.

Dla skutecznego uruchomienia systemu i próby wykorzystania w trybie testowym wymagane jest:
1. Pobrać plik goodreads_interaction.csv ze strony Goodreads: https://cseweb.ucsd.edu/~jmcauley/datasets/goodreads.html
2. Uruchomić skrypt MatrixFactorization.py znajdujący się w folderze Models/ALS (poprawiając ścieżki ustawione w tym skrypcie).
3. Uruchomić skrypt UploadToVectorDb używając plików, które otrzymaliśmy w poprzednim kroku. Instrukcja uruchomienia jest podana w odpowiednim pliku README [Background](proj/Background/README.md)

Część funkcjanalności nie jest jeszcze zintegrowane z aplikacją główną: 
1. Content-based (algorytm jest zdefiniowany, jednak nie jest w tym momencie dodany do samego serwisu; po dodaniu będzie użyty dla funkcjonalności „podaj podobne książki”).
2. Odświeżanie embeddings użytkownika po nowej interakcji wymaga pełnej integracji modeli ALS z serwisem.
3. System nie jest w tym momęcie zintegrowany z cachem
4. Modele Ranking i Re-ranking są zamockowane

# Komentarz w sprawie wyboru ALS
Dla głównego modelu rekomendacyjnego stosujemy nowoczesną architekturę systemów rekomendacyjnych: Candidate Generation → Ranking → Re-ranking.
Faktoryzację macierzy metodą ALS stosujemy, aby znaleźć embeddings użytkowników i książek (które są wymagane na etapie candidate generation oraz ranking).
Używanie faktoryzacji macierzy jest dominującym podejściem w branży (szczególnie w przypadku ograniczonych zasobów obliczeniowych).
Wybór ALS został dokonany ze względu na to, że takie podejście jest bardzo efektywne pod względem kosztów obliczeniowych i ma bardzo dobrą zbieżność. Badania wykazują również, że ALS działa lepiej niż inne techniki faktoryzacji w przypadku większych zbiorów danych (>100000 aktywnych użytkowników).
