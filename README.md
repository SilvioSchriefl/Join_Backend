# Join – Backend

REST-API für **Join**, ein Kanban-Board für Teams: Aufgaben anlegen, Kategorien und Kontakte
verwalten, Aufgaben zwischen Spalten verschieben. Gebaut mit **Django** und dem
**Django REST Framework** während meiner Ausbildung zum Entwickler bei der Developer Akademie (2023).

Das passende Angular-Frontend liegt hier: [SilvioSchriefl/Join-Angular](https://github.com/SilvioSchriefl/Join-Angular)

## Funktionen

- Registrierung und Login mit E-Mail und Passwort (Token-Authentifizierung), Logout
- Eigenes User-Modell mit Farbe, Initialen und Telefonnummer für die Anzeige im Board
- Kontakte anlegen, bearbeiten und löschen, mit Prüfung auf doppelte E-Mail-Adressen
- Kategorien mit Farbe anlegen und löschen
- Aufgaben anlegen, abrufen, ändern (z. B. Status oder Unteraufgaben) und löschen
- Alle Daten nur für angemeldete Nutzer; offen sind allein Registrierung und Login
- 27 automatisierte Tests

## Technik

| Bereich | Eingesetzt |
| --- | --- |
| Framework | Django 4.2, Django REST Framework |
| Authentifizierung | DRF Token Authentication |
| Datenbank | SQLite (lokal) |
| Weiteres | django-cors-headers |

## API-Endpunkte

| Methode | Pfad | Zweck |
| --- | --- | --- |
| POST | `/sign_up/` | Konto anlegen |
| POST | `/log_in/` | Anmelden, Token erhalten |
| POST | `/log_out/` | Abmelden |
| GET | `/users/` | Alle Nutzer |
| GET / POST | `/contacts/` | Kontakte abrufen / anlegen |
| PUT | `/edit_contact/<id>/` | Kontakt bearbeiten |
| DELETE | `/delete_contact/<id>/` | Kontakt löschen |
| GET / POST | `/category/` | Kategorien abrufen / anlegen |
| DELETE | `/category/<id>/` | Kategorie löschen |
| GET / POST / PATCH | `/task/` | Aufgaben abrufen / anlegen / ändern |
| DELETE | `/task/<id>/` | Aufgabe löschen |

## Lokal starten

Voraussetzung: Python 3.11+

```bash
git clone https://github.com/SilvioSchriefl/Join_Backend.git
cd Join_Backend/join_backend
python -m venv env
source env/bin/activate        # Windows: env\Scripts\activate
pip install -r requirements.txt

python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Die API läuft dann unter `http://127.0.0.1:8000/`.

Für den Betrieb auf einem Server werden diese Umgebungsvariablen gesetzt:

| Variable | Bedeutung |
| --- | --- |
| `DJANGO_SECRET_KEY` | geheimer Schlüssel, lang und zufällig |
| `DJANGO_DEBUG` | auf `False` setzen |

## Tests

```bash
python manage.py test
```
