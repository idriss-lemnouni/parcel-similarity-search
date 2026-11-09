# Recherche de parcelles expérimentales similaires

Le script transforme les 72 rendements réels de l’essai d’avoine Oats en 18 profils de parcelles principales. Chaque profil contient le rendement observé à quatre doses d’azote. La recherche renvoie les cinq profils les plus proches dans les autres blocs, avec une distance euclidienne après mise à l’échelle. Les échelles sont calculées sur les candidats.

Télécharger [Oats.csv](https://raw.githubusercontent.com/vincentarelbundock/Rdatasets/master/csv/nlme/Oats.csv), puis lancer `python search.py Oats.csv --block I --variety Victory`. Python 3 suffit.

La [documentation R nlme](https://stat.ethz.ch/R-manual/R-devel/library/nlme/html/Oats.html) décrit le plan expérimental de Yates (1935). Le taux de correspondance de variété au premier rang sert de diagnostic. La distance mesure une ressemblance des réponses à l’azote sur cet essai, sans coordonnées ni validation dans une autre exploitation.
