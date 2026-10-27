@echo off
set BACKUP_DIR=E:\PROJET8AGRICULTURE\Agriculture_2.0\pythonProject1\agriculture\vegetablesfruits\backups
set DATE=%date:~6,4%%date:~3,2%%date:~0,2%
echo [%date% %time%] Début sauvegarde >> ..\logs\backup.log

cd /d E:\PROJET8AGRICULTURE\Agriculture_2.0\pythonProject1\agriculture\vegetablesfruits
call ..\.venv\Scripts\activate

python manage.py dumpdata --exclude auth.permission --exclude contenttypes --exclude sessions > %BACKUP_DIR%\backup_%DATE%.json 2>> ..\logs\backup.log

echo [%date% %time%] Fin sauvegarde >> ..\logs\backup.log
echo. >> ..\logs\backup.log