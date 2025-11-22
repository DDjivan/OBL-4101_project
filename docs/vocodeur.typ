#set text(lang: "fr")
#show link: set text(fill: blue,)// weight: 700)
#show link: underline

// #show raw.where(block: false): highlight.with(
//   fill:luma(245),
//   radius: 4pt,
//   extent: 1pt,
//   top-edge: 1.1em,
//   bottom-edge: -0.3em,
// )

// #show raw.where(block: true): block.with(
//  fill: luma(240), // fill: luma(240),
//  inset: 0pt, //10pt,
//  radius: 4pt,
//  outset: 4pt,
// )

#import "@preview/codly:1.3.0": *
#import "@preview/codly-languages:0.1.1": *
#show: codly-init.with()

#codly(languages: codly-languages)
#codly(number-format: none)

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

PySide6 est pas sur Python 3.14 mais 3.13.

```bash
ls /home/linuxbrew/.linuxbrew/bin/python*
```

```bash
python3.13 -m venv .venv
```

```bash
pip install pyside6
```



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



