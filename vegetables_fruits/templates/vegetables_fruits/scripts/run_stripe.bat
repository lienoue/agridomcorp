@echo off
echo [%date% %time%] Début synchronisation Stripe >> ..\logs\stripe.log
cd /d E:\PROJET8AGRICULTURE\Agriculture_2.0\pythonProject1\agriculture\vegetablesfruits
call ..\.venv\Scripts\activate
python manage.py synchroniser_abonnements_stripe >> ..\logs\stripe.log 2>&1
echo [%date% %time%] Fin synchronisation Stripe >> ..\logs\stripe.log
echo. >> ..\logs\stripe.log