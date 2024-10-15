
readme_content = """
# URL Shortener API

URL Shortener API to aplikacja stworzona przy użyciu FastAPI, która pozwala na skracanie długich URL-i, zarządzanie zadaniami asynchronicznymi, oraz korzystanie z automatycznej dokumentacji Swagger (OpenAPI).

## Wymagania wstępne

Aby uruchomić aplikację, potrzebujesz:

- **Docker** (z Docker Compose)
- **Python 3.9+** (jeśli chcesz uruchamiać aplikację lokalnie, bez Dockera)

## Zestawienie środowiska deweloperskiego

### 1. Klonowanie repozytorium

Zacznij od sklonowania repozytorium na lokalny komputer:

git clone https://github.com/your-repo/url-shortener.git
cd url-shortener

### 2. Uruchomienie aplikacji przy użyciu Docker Compose
Aby szybko uruchomić aplikację z Docker Compose, postępuj zgodnie z poniższymi krokami:

Krok 1: Zbuduj i uruchom kontenery

docker-compose up --build

To polecenie uruchomi aplikację FastAPI, bazę danych PostgreSQL, oraz usługi Celery i RabbitMQ. Cała aplikacja zostanie zainstalowana w kontenerach, więc nie musisz instalować dodatkowego oprogramowania na swoim komputerze.

Krok 2: Dostęp do aplikacji
Aplikacja FastAPI będzie dostępna pod adresem: http://localhost:8000
Automatycznie wygenerowana dokumentacja Swaggera będzie dostępna pod adresem: http://localhost:8000/docs
Alternatywna dokumentacja ReDoc: http://localhost:8000/redoc

### 3. Uruchomienie aplikacji lokalnie (bez Dockera)
Jeśli nie chcesz używać Dockera, aplikację można uruchomić lokalnie. Wykonaj następujące kroki:

Krok 1: Zainstaluj zależności
Upewnij się, że masz zainstalowane wirtualne środowisko Pythona, a następnie zainstaluj wymagane pakiety z pliku requirements.txt.

Na systemie Linux/macOS:
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt


Na systemie Windows:

python -m venv env
.\env\Scripts\activate
pip install -r requirements.txt

Krok 2: Uruchom aplikację
Aby uruchomić aplikację lokalnie, użyj komendy:

uvicorn app.api:app --reload --host 0.0.0.0 --port 8000

Aplikacja FastAPI będzie dostępna pod adresem: http://localhost:8000
Dokumentacja Swaggera: http://localhost:8000/docs
Dokumentacja ReDoc: http://localhost:8000/redoc

### 4. Uruchamianie testów
Aby uruchomić testy jednostkowe, upewnij się, że aplikacja działa, a następnie uruchom testy za pomocą pytest:

pytest tests/

Struktura projektu
app/: Główna logika aplikacji, modele, funkcje związane z API.
tests/: Testy jednostkowe dla API.
Dockerfile: Definicja obrazu Dockera dla aplikacji.
docker-compose.yml: Konfiguracja Docker Compose, uruchamiająca aplikację, bazę danych, RabbitMQ oraz Celery.
