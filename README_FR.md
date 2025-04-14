# 🪖 Orbat Generator

**Orbat Generator** est une application Python qui génère automatiquement une présentation PowerPoint représentant l'organigramme d'une structure militaire (ORBAT — Order of Battle), à partir de données structurées dans un fichier Excel et enrichies via des fichiers CSV et des pictogrammes graphiques.

## 🗂 Structure du projet

```
.
├── main.py                   # Script principal à exécuter
├── datas/                   
│   ├── EquipmentType.csv     # Définit les types d’équipement
│   ├── datas.xls             # Données source (unités & hiérarchie)
│   ├── sidc.csv              # Table de correspondance pour les symboles OTAN
│   └── SYMB_PNG/             # Pictogrammes associés aux unités                           
├── orbat_gen/
│   ├── __init__.py           # Initialise le package
│   ├── config.py             # Configurations des constantes
│   ├── classes.py            # Définition des classes Unit et EqType
│   ├── units_gen.py          # Génère les objets Unit à partir des données Excel
│   └── powerpoint_gen.py     # Gère la génération des slides PowerPoint
├── tests/                    # Contient tous les fichiers pour tests unitaires   
```

## ▶️ Lancer l'application

```bash
python main.py
```

Cela génère une présentation `.pptx` avec une ou plusieurs diapositives selon la hiérarchie décrite dans `datas.xls`.

## 🔧 Fonctionnalités principales

- Lecture de données Excel avec hiérarchie militaire.
- Création d'objets `Unit` avec équipements et subordonnés.
- Génération automatique de slides PowerPoint avec :
  - Symboles OTAN (via images PNG).
  - Tableaux d'équipements par unité.
  - Visualisation hiérarchique ("peignes").

## 📁 Données utilisées

- `datas.xls` : hiérarchie et équipements des unités.
- `EquipmentType.csv` : catégories d’équipement.
- `sidc.csv` : codes OTAN pour les symboles.
- `SYMB_PNG/` : images associées aux unités.

## ✅ Dépendances

- `pandas`
- `python-pptx`


Installez-les avec :

```bash
pip install pandas python-pptx
```