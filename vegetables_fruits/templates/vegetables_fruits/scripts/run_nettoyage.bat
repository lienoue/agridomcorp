@echo off
echo [%date% %time%] Début nettoyage >> ..\logs\nettoyage.log
cd /d E:\PROJET8AGRICULTURE\Agriculture_2.0\pythonProject1\agriculture\vegetablesfruits
call ..\.venv\Scripts\activate
python manage.py nettoyer_orphelins >> ..\logs\nettoyage.log 2>&1
echo [%date% %time%] Fin nettoyage >> ..\logs\nettoyage.log
echo. >> ..\logs\nettoyage.log