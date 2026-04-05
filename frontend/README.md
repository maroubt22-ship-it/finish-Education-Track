# 📚 EduTrack IA - Frontend Documentation

> Plateforme intelligente de suivi pédagogique pour centres de soutien scolaire au Maroc

## 🎯 Vue d'Ensemble

EduTrack IA est une solution complète de suivi pédagogique avec trois interfaces frontend distinctes :

1. **📊 Dashboard Enseignant** (Streamlit) - Interface principale pour les enseignants
2. **🤖 Démo IA** (Gradio) - Démonstration des capacités d'intelligence artificielle
3. **👨‍👩‍👧 Vue Parent** (Streamlit) - Portail simplifié pour les parents

## 🏗️ Architecture

```
frontend/
├── streamlit/              # Dashboard enseignant (port 8501)
│   ├── app.py             # Point d'entrée principal
│   ├── pages/             # Pages multi-pages Streamlit
│   │   ├── 1_🏠_Accueil.py
│   │   ├── 2_👥_Élèves.py
│   │   ├── 3_📊_Notes.py
│   │   ├── 4_🎯_Compétences.py
│   │   ├── 5_📈_Analyses.py
│   │   ├── 6_📋_Rapports.py
│   │   └── 7_✍️_Observations.py
│   ├── components/        # Composants réutilisables
│   │   ├── student_card.py
│   │   ├── grade_chart.py
│   │   ├── competency_radar.py
│   │   ├── alert_banner.py
│   │   └── report_preview.py
│   └── utils/             # Fonctions utilitaires
│       └── helpers.py
├── gradio/                # Démo IA (port 7860)
│   └── app.py
├── parent_view/           # Vue parent (port 8502)
│   ├── app.py
│   └── pages/
│       ├── 1_📊_Vue_d_ensemble.py
│       ├── 2_🎯_Compétences.py
│       ├── 3_📈_Historique.py
│       └── 4_📋_Rapports.py
└── shared/                # Ressources partagées
    ├── data/              # Générateurs de données fictives
    │   ├── mock_data.py
    │   └── samples/       # Fichiers CSV d'exemple
    └── styles/            # Thème et styles
        └── theme.py
```

## 🚀 Installation

### Prérequis

- Python 3.8 ou supérieur
- pip (gestionnaire de paquets Python)

### Étapes d'installation

1. **Cloner le projet ou se placer dans le répertoire**
   ```bash
   cd "C:\Users\pc\Desktop\EduTrack IA"
   ```

2. **Installer les dépendances Python**
   ```bash
   pip install -r frontend/requirements.txt
   ```

3. **Créer la structure du projet**
   ```bash
   python setup_structure.py
   ```

## 📱 Utilisation

### Option 1 : Lancement rapide (Windows)

Utilisez les scripts batch fournis :

- **Dashboard Enseignant** : Double-cliquez sur `run_teacher_dashboard.bat`
- **Démo IA Gradio** : Double-cliquez sur `run_gradio_demo.bat`
- **Vue Parent** : Double-cliquez sur `run_parent_view.bat`

### Option 2 : Lancement manuel

#### Dashboard Enseignant (port 8501)
```bash
streamlit run frontend/streamlit/app.py --server.port 8501
```
Accéder à : http://localhost:8501

#### Démo IA (port 7860)
```bash
python frontend/gradio/app.py
```
Accéder à : http://localhost:7860

#### Vue Parent (port 8502)
```bash
streamlit run frontend/parent_view/app.py --server.port 8502
```
Accéder à : http://localhost:8502

## 🎓 Guide d'Utilisation

### Dashboard Enseignant

#### Page Accueil (🏠)
- Vue d'ensemble avec statistiques clés
- Alertes pour élèves en difficulté
- Distribution des notes
- Activité récente

#### Page Élèves (👥)
- Liste de tous les élèves avec recherche et filtres
- Ajout/modification/archivage d'élèves
- Import CSV d'élèves
- Vue détaillée par élève

#### Page Notes (📊)
- Saisie de nouvelles notes
- Historique des évaluations
- Distribution des notes par classe
- Filtrage par élève, matière, date

#### Page Compétences (🎯)
- Référentiel de compétences par matière
- Visualisation des niveaux de maîtrise
- Statistiques par compétence
- Ajout de nouvelles compétences

#### Page Analyses (📈)
- Graphiques d'évolution des notes
- Radar des compétences par élève
- Heatmap de performance de classe
- Analyse de tendances (amélioration/stable/régression)
- Alertes automatiques

#### Page Rapports (📋)
- Génération automatique de rapports
- Prévisualisation du rapport
- Export PDF
- Envoi WhatsApp simulé
- Historique des rapports

#### Page Observations (✍️)
- Ajout d'observations sur les élèves
- Catégorisation (comportement/progrès/difficulté)
- Historique filtrable
- Statistiques par catégorie

### Démo IA Gradio

#### Onglet "Génération de Rapports"
1. Sélectionner un élève
2. Entrer les notes récentes (Math, Physique, Français)
3. Ajouter les observations enseignant
4. Cliquer sur "Générer le Rapport"
5. Voir le rapport structuré en 5 sections

#### Onglet "Classification de Compétences"
1. Entrer une note (0-20)
2. Cliquer sur "Classifier la Compétence"
3. Voir le niveau de maîtrise et les recommandations

### Vue Parent

Interface simplifiée en lecture seule pour les parents :

- **Vue d'ensemble** : Performance globale, tendances
- **Compétences** : Radar des compétences par matière
- **Historique** : Évolution des notes dans le temps
- **Rapports** : Accès aux rapports générés

## 📊 Données de Démonstration

L'application fonctionne avec des **données fictives générées automatiquement** :

- 50 élèves avec noms marocains réalistes
- 40 compétences réparties en 4 catégories
- ~1000 notes générées avec tendances réalistes
- Observations enseignant catégorisées
- Rapports de progression

### Profils d'élèves simulés
- **Excellents** : Moyenne ≥ 16/20
- **Bons** : Moyenne 14-17/20
- **Moyens** : Moyenne 10-14/20
- **En difficulté** : Moyenne < 10/20
- **En amélioration** : Progression positive
- **En régression** : Progression négative

## 🎨 Système de Classification

### Notes (Échelle Marocaine 0-20)

| Niveau | Plage | Emoji | Couleur | Description |
|--------|-------|-------|---------|-------------|
| **Maîtrisée** | ≥ 14/20 | 🟢 | Vert | Compétence bien acquise |
| **En cours** | 10-14/20 | 🟡 | Orange | En cours d'acquisition |
| **À renforcer** | < 10/20 | 🔴 | Rouge | Renforcement nécessaire |

### Tendances

| Tendance | Critère | Emoji | Description |
|----------|---------|-------|-------------|
| **Amélioration** | +2 points | 📈 | Progression positive |
| **Stable** | ±2 points | ➡️ | Performance constante |
| **Régression** | -2 points | 📉 | Baisse de performance |

## 🔧 Personnalisation

### Modification des couleurs

Éditez `frontend/shared/styles/theme.py` :

```python
COLORS = {
    "primary": "#1E3A8A",    # Bleu foncé
    "success": "#10B981",    # Vert
    "warning": "#F59E0B",    # Orange
    "danger": "#EF4444",     # Rouge
    ...
}
```

### Ajout de nouvelles compétences

Modifiez `frontend/shared/data/mock_data.py` dans la variable `COMPETENCIES`.

### Modification du port

Pour changer le port Streamlit :
```bash
streamlit run frontend/streamlit/app.py --server.port NOUVEAU_PORT
```

## 📦 Dépendances Principales

| Package | Version | Usage |
|---------|---------|-------|
| streamlit | ≥1.30 | Framework dashboard |
| gradio | ≥4.0 | Interface IA |
| pandas | ≥2.0 | Manipulation données |
| plotly | ≥5.0 | Graphiques interactifs |
| matplotlib | ≥3.8 | Visualisations |
| seaborn | ≥0.13 | Heatmaps |

Voir `frontend/requirements.txt` pour la liste complète.

## 🐛 Dépannage

### Problème : Module non trouvé
```bash
# Réinstaller les dépendances
pip install -r frontend/requirements.txt --upgrade
```

### Problème : Port déjà utilisé
```bash
# Utiliser un port différent
streamlit run frontend/streamlit/app.py --server.port 8503
```

### Problème : Erreur d'import
```bash
# Vérifier que vous êtes dans le bon répertoire
cd "C:\Users\pc\Desktop\EduTrack IA"
```

### Problème : Les données ne se chargent pas
- Vérifier que `setup_structure.py` a été exécuté
- Relancer l'application
- Vider le cache Streamlit : Settings → Clear cache

## 🎯 Mode Production

### Connexion à un Backend

Pour connecter à une API Flask réelle :

1. Créer un fichier `.env` :
   ```
   API_URL=http://localhost:5000/api
   ENVIRONMENT=production
   ```

2. Modifier les fonctions de chargement de données dans chaque page :
   ```python
   # Remplacer
   from frontend.shared.data.mock_data import get_all_mock_data
   
   # Par
   import requests
   response = requests.get(f"{API_URL}/students")
   students = response.json()
   ```

### Déploiement

Pour déployer en production :

1. **Streamlit Cloud** : Connecter le repo GitHub et déployer
2. **Heroku** : Utiliser le buildpack Python + Procfile
3. **Docker** : Créer un Dockerfile (voir documentation Streamlit)

## 📝 Import de Données CSV

### Format Attendu

#### Élèves (`students.csv`)
```csv
id,first_name,last_name,class_name,date_of_birth,parent_phone,parent_email
STU0001,Youssef,Alami,2ème Bac Sciences Math,2007-03-15,+212 612345678,youssef.parent@gmail.com
```

#### Notes (`grades.csv`)
```csv
id,student_id,competency_id,competency_name,subject,value,evaluation_type,evaluation_date
GRD0001,STU0001,COMP0001,Algèbre,Mathématiques,16.5,contrôle,2026-03-15
```

Des exemples sont disponibles dans `frontend/shared/data/samples/`.

## 🔐 Sécurité

**⚠️ Important** : Cette version de démonstration ne contient :
- ❌ Pas d'authentification utilisateur
- ❌ Pas de connexion base de données
- ❌ Pas de validation côté serveur
- ❌ Pas de chiffrement des données

Pour la production, ajouter :
- ✅ Authentification JWT
- ✅ Validation des entrées
- ✅ Protection CSRF
- ✅ HTTPS obligatoire
- ✅ Gestion des permissions

## 🌍 Internationalisation

L'application est actuellement en **français** pour le marché marocain.

Pour ajouter d'autres langues, créer un système de traduction :
```python
TRANSLATIONS = {
    "fr": {"dashboard": "Tableau de Bord"},
    "ar": {"dashboard": "لوحة القيادة"},
    "en": {"dashboard": "Dashboard"}
}
```

## 📧 Support

Pour toute question ou problème :
- Consulter la documentation complète : `CAHIER_DES_CHARGES.md`
- Vérifier les issues GitHub
- Contacter l'équipe de développement

## 🎉 Fonctionnalités Futures

- [ ] Mode hors ligne avec synchronisation
- [ ] Application mobile native
- [ ] Intégration WhatsApp Business réelle
- [ ] Export Excel avancé
- [ ] Templates de rapports personnalisables
- [ ] Tableau de bord administrateur
- [ ] Notifications push
- [ ] Module de paiement

## 📄 Licence

© 2026 EduTrack IA - Tous droits réservés

---

**Version** : 1.0  
**Date** : 2 avril 2026  
**Mode** : Démonstration avec données fictives
