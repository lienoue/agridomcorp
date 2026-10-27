@echo off
echo [%date% %time%] Début alertes traitements >> ..\logs\alertes_traitements.log
cd /d E:\PROJET8AGRICULTURE\Agriculture_2.0\pythonProject1\agriculture\vegetablesfruits
call ..\.venv\Scripts\activate
python manage.py verifier_alertes_traitements >> ..\logs\alertes_traitements.log 2>&1
echo [%date% %time%] Fin alertes traitements >> ..\logs\alertes_traitements.log
echo. >> ..\logs\alertes_traitements.log