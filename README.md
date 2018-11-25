# kreathon2018
Smart Garbage Containers for Krefeld.

Placed 3rd in [Kreathon 2018](https://kreathon-krefeld.de/) Hackathon.
See the presentation [Video](https://www.facebook.com/SWK.Krefeld/videos/995938370589888/?t=349) and [Slides](https://docs.google.com/presentation/d/1hnPSgH4FVmWg0iBtqUmQ8y2B10gKDdMhcCNe62sMrZg/edit?usp=sharing).

Built with ❤️ by [@NikolasE](https://github.com/NikolasE), [@ffroehling](https://github.com/ffroehling) and [@lalten](https://github.com/lalten).

## Die Wichtigtsen Progamme und Ordner ##

### django_project:
 in django_project ist eine django application zu finden die ausschliesslich fuer die Kommunikation mit der 
SQLite-Datenbank eingesetzt wurde. Die einzelnen Tabellen sind in django_project/backend/models.py beschrieben. 

### scripts/mqtt_to_db.py:
Interface das die per MQTT gesendeten Daten der einzelnen Messknoten entgegen nimmt und in die Datenbank eintraegt. 

### scripts/rest_provider.py
Dieses Skript liest und schriebt die Datenbank und stellt die Informationen per REST-API fuer die Website und den Chatbot
zur Verfuegung, so dass diese Komponenten nicht von der Datenbankimplementation abhaengen und parallel entwickelt werden konnten.
Die einzelnen REST-API-Endpoints sind in der Datei selbst dokumentiert

### scripts/chatbot.py
Dieses Skript beinhaltet den Telegram-Chatbot mit sich der Nutzer den Weg zum naechsten leeren Container anzeigen und 
und Feedback zur Sauberkeit kann. Die einzelnen Befehle sind wieder in der Datei selbst dokumentiert. 

### here_connector.py
Hier sind die REST-API-Calls fuer die Routenplanung implementiert. 


### frontend
Website mit folgenden Funktionen:
    - Anzeige des Fuellstands (mit Zufallsdaten) an den korrekten Geopositionen
    - Berechnung des naehesten (leeren) Containers zu einer Route. Hier kann z.B. ein leerer Container auf dem
        Weg zur Arbeit berechnet werden fuer den der noetige Umweg minimal ist. 
    - Globale Optimierung einer Route um alle (vollen) Container zu leeren (Travelling-Salesman ueber HERE-API)



#### Datenbereinigung: ####

Aus den bereitgestellten Standortdaten mit Strassenbezeichnungen ("Glindholzstraße;Höhe Rathaus", siehe locations.csv) 
wurden mit Hilfe eines interaktiven Programs und dem Reverse-Lookup der HERE-API die GeoPositionen bestimmt. 
Diese Positionen sind in geo_locations.txt und wurden Freitag abend auch den anderen Teams zur Verfuegung gestellt. 


Bei der Bereining der Daten sind zwei Unstimmigkeiten aufgefallen:

Container 24 hat zwei Standorte
Altenheim vs. Seniorenheim bei Container 55



#### DJANGO ####
export DJANGO_SETTINGS_MODUL=awesome_container.settings

django_project-Ordner muss in den PYTHOPATH aufgenommen werdne. 
