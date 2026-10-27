@echo off
echo ========================================
echo Execution de tous les scripts...
echo ========================================

call run_alertes_traitements.bat
call run_alertes_meteo.bat
call run_rappels_semis.bat
call run_nettoyage.bat
call run_stripe.bat
call run_backup.bat

echo ========================================
echo Tous les scripts ont ete executes
echo ========================================
pause