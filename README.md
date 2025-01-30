## Nötige Instalationen
1. Python und Python Extension Pack v1.7.0 von Don Jayamanne in VS-Code herunterladen
2. Docker installieren 
3. Todo Tree v0.0.226 herunterladen

## Venv erstellen:
- auf setup.py gehen 
- auf die aktuelle python version gehen in der Statusanzeige
    - Create Virtual enviroment
    - Venv auswählen
    - Venv sollte aktiviert sein
- mit dem Befehl:

```shell
deactivate
```

kannst du venv deaktivieren
- mit dem Befehl:  
```shell
source .venv/bin/activate
```
- kannst du venv wieder aktivieren 

## Netbox in Venv
- https://github.com/netbox-community/netbox/tree/v4.1.11 anklicken 
- auf den CODE button klicken und ZIP Download Datei herunterladen
- in dem ZIP Document auf den 'netbox' ordner klicken
- alle Ordner dort koopieren
- auf .venv/lib/python3.12/site-packages gehen und es in FileExplorer öffnen
    - die kopierten Ordner hier einfügen
    - Glücklich sein

##  Docker 
- im terminal auf /netbox/applications/docker gehen

mit:
```shell
cd docker 
 ``` 
     
kommst du auf ../docker
     
 den Befehl:
 ```
 docker compose up --build
  ```
  eingeben
- auf docker gehen und local_docker_netbox_applications_plugin öffnen
- bei VS-Code auf Ports gehen und bei Add Port '13000' eingeben
- warten bis es lädt 

## Netbox Community
- http://localhost:13000/ im browser öffnen
- Auf Log In klicken
- User: admin
- Passwort: admin
    - Glücklich sein




