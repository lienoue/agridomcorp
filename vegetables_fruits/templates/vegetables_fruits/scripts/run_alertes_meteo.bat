@echo off
echo [%date% %time%] Début alertes météo >> ..\logs\alertes_meteo.log
cd /d E:\PROJET8AGRICULTURE\Agriculture_2.0\pythonProject1\agriculture\vegetablesfruits
call ..\.venv\Scripts\activate
python manage.py verifier_alertes_meteo_2 >> ..\logs\alertes_meteo.log 2>&1
echo [%date% %time%] Fin alertes météo >> ..\logs\alertes_meteo.log
echo. >> ..\logs\alertes_meteo.log