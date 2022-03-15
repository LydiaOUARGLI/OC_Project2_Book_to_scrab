Project: Book\_to\_scrab
========================

Information générale
--------------------

------------------------------------------------------------------------

Le code parcour la page principal du site, récupère les liens de la
première page de chaque catégorie de livre en liste, on parcour la liste
des liens et on crès une sous liste provisoire comportant toutes les
pages d'une seule catégorie, cette sous\_liste est initialisée avant le
passage à la catégorie suivante, en parallèle on récupères tous les
liens des livres qui vont être parcourus à leur tours.

Technologies
------------

------------------------------------------------------------------------

Python : Version 3.9

Création et Activation de l'environnement :
-------------------------------------------

------------------------------------------------------------------------

Cette étape est nécessaire pour limiter les installations de packages au
niveua de notre environnement de travail et ne pas encombrer l'espace de
stockage global

### Création :

1.  Se positionner dans le répertoir de travail,
    exemple:C:`\Users`{=tex}`\glk`{=tex}\_u`\Documents`{=tex}`\lydia`{=tex}\_doc`\OC`{=tex}\_Projet\_2
2.  Lancer Git Bash\
    \$ python -m venv env

### Activation :

#### Activation sur Windows

\$ Source env/Scripts/activate

#### Activation sur macos et Linux

\$ Source env/bin/activation

3.  Apparition de (env)

Installation Packages
---------------------

------------------------------------------------------------------------

Le fichier requierement.txt contient tous les packages nécessaire pour
l'éxécution du code Book\_to\_scrab.py

\$ pip install -r requirement.txt

Exécution du script
-------------------

\$ python Book\_to\_scrab.py
