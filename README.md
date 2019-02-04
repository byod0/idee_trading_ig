# idee_trading_ig

Dev avec python 3

Descriptif des fichiers : 




crontab: ligne a mettre dans votre crontab du raspi (0 * * * 1-5 ...)
         s'execute tout les jours (1 a 5 -> Lundi au Vendredi) toutes les heures à 00 minutes
         pour ouvrir votre crontab : "crontab -e" dans le terminal

idee.py: fichier python qui contient tous le code :) 

launsher.sh : contient la ligne de lancement du programme, composé de python3 et l'appel du fichier python

requierements.txt : contient toutes les bibliotheques necessaire pour executer tout ce petit monde. 
                    j'utilise virtualenv, ca creer une environnement virtuel python3 ou on install juste ce qui nous interesse.
                    
tradin_ig_config.py: contient vos infos de connexion. ATTENTION: c'est "config2" qui est appeler dans le idee.py.

le dossier trading_ig contient tout les bibliotheque pour facilité l'utilisation des api IG 
https://github.com/ig-python/ig-markets-api-python-library

