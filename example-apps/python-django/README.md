# Django

Denne Django-løsningen består av `django_project` og `django_app`.
`django_project` tilsvarer hele web-applikasjonen, mens `django_app` er bare en liten uavhengig bit.
Tanken er at applikasjoner kan gjenbrukes på kryss av prosjekter.
`django_app` har sine egne modeller og migreringer, mens databaseforbindelsene er definert i `django_project`.

[Les om forskjellen mellom prosjekter og applikasjoner i Django.](https://docs.djangoproject.com/en/5.2/ref/applications/#projects-and-applications)

## Oppgaver

- Lag en test som lagrer en ny instans av en modell i en database i SQLite
- Finn ut hvordan databasemigreringer lages, og kjør den mot Postgres eller Oracle
- Dupliser testen, men kjør mot databasen du valgte over
- Legg til et nytt felt på modellen din
- Legg til en relasjon til en annen modell, og sett opp en fremmednøkkel

For hver oppgave, oppdater tester, lag nye migreringer, og se hvordan det ser ut i databasen.

## Kommandoer

Alle kommandoer kjøres fra mappen til `django_project`:

```
cd django_project
```

Kjør applikasjon:

```
python manage.py runserver
```

Kjør alle tester:

```
python manage.py test --verbosity=2
```

Lag ny migrering:

```
python manage.py makemigrations
```

Kjør migreringer:

```
python manage.py migrate
```

## Kommandoer brukt for å lage løsningen

Lage prosjekt og applikasjon:

```
curl -o .gitignore https://raw.githubusercontent.com/github/gitignore/main/Python.gitignore
django-admin startproject django_project
cd django_project
python manage.py startapp django_app
```

Installer avhengigheter:

```
pip install -r requirements.txt
```
