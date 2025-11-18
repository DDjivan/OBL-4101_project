= Notes pour le projet

== Configuration

```bash
cd code_python
```

=== Environnement virtuel

Créer.

```bash
python -m venv .venv
```

Activer.

```bash
source .venv/bin/activate
```

Désactiver.

```bash
deactivate
```

#link("https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/")[
  Source et instructions supplémentaires
]



=== Dépendances

Installer les bibliothèques requises.

```bash
pip install -r requirements.txt
```

Le fichier `requirements.txt` doit contenir chaque bibliothèque ligne par ligne.




== Quoi utiliser ?

Contrairement à Matlab, il y a beaucoup de choix avec Python.

Pour le moment, Djivan a testé :

+ Matplotlib : complet, simple, zoom, sauvegarder, mais très lent ;
+ PyQtGraph / PyQt6 : moderne, très fluide, pratique pour faire un
  projet joli, mais à maîtriser ;
+ Plotly : s'ouvre dans un navigateur web, pas sûr de comment l'utiliser.

À explorer :

+ VisPy : tracés avec OpenGL (avec le processeur graphique) ;
+ Bokeh : dans un navigateur web ("serveur optionnel" ?) ;
+ Dash (Plotly Dash) : application web avec Plotly ;
+ Altair/Vega-Lite ;
+ Holoviews + Datashader.



