@echo off
echo [%date% %time%] Début rappels semis >> ..\logs\rappels.log
cd /d E:\PROJET8AGRICULTURE\Agriculture_2.0\pythonProject1\agriculture\vegetablesfruits
call ..\.venv\Scripts\activate
python manage.py verifier_rappels_semis >> ..\logs\rappels.log 2>&1
echo [%date% %time%] Fin rappels semis >> ..\logs\rappels.log
echo. >> ..\logs\rappels.log