# ✅ Checklist de non-régression

À tester après CHAQUE étape de refactoring.

## 🌐 Pages publiques
- [ ] / (accueil) charge
- [ ] /connexion/ fonctionne
- [ ] /creation-compte/ fonctionne

## 👤 Particulier (Darkmaul)
- [ ] Dashboard particulier charge
- [ ] /suggestions-personnalisees/ affiche 8 suggestions avec conseils
- [ ] /figure/<id>/ affiche les crops + conseils
- [ ] /journal/ liste et création OK
- [ ] /ecologie/ onglets OK
- [ ] /alertes/ onglets OK
- [ ] /guide-cultures/ onglets OK

## 👨‍🎓 Junior (mineur sans classe)
- [ ] Dashboard junior charge
- [ ] Mêmes pages accessibles

## 👨‍🏫 Enseignant
- [ ] /dashboard-enseignant/ charge
- [ ] Création classe OK
- [ ] Forum école OK

## 👦 Élève
- [ ] Dashboard élève charge
- [ ] Missions/compétences OK

## 🔧 Admin
- [ ] /admin/ charge
- [ ] Listes Culture/Fruit/Vegetable/ConseilsFamille OK

## 💳 Stripe
- [ ] /tarification/ charge
- [ ] Bouton abonnement → Stripe Checkout OK

## 📊 Logs
- [ ] Aucune erreur 500 dans la console
- [ ] Aucun warning Django inhabituel

## 🧹 Journal de nettoyage

- [x] get_client_ip : V1 supprimée (gardé V2)
- [x] get_culture_emoji
- [x] get_saison_actuelle
- [x] inscription_eleve
- [x] autosuffisance
- [x] ecologie_tabs
- [ ] ignorer_alerte (⚠️ renommage, pas suppression)