# Architektura
API udostępniające system rekomendacyjny jest napisane w Python FastAPI, znajduje się w folderze `proj/`. Model korzystający z `collaborative filetring` znajduje się w `Models/ALS` i to na jego podstawie API zwraca rekomendacje. 

# Uruchomienie systemu w trybie "Development":

- w folderze `proj/` należy uruchomić `docker-compose up`
  - program będzie działał, ale nie zwróci żadnych rekomendacji, bo wymaga to dodatkowej konfiguracji/trenowania modelu (docelowo będzie to zautomatyzowane celem łatwego odtworzenia)
  - żeby zobaczyć dokementację API w Swagger należy odwiedzić `http://localhost:8000/docs`, tam też można wysłać zapytania


