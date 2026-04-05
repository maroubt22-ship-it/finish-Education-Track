# 📋 EduTrack IA — Cahier des Charges
> **Version** 1.0 · **Date** 21 mars 2026 · **Équipe** PFE N°9 · **Durée** 8 semaines (23 mars – 15 mai 2026)

---

## Table des Matières
1. [Contexte & Objectifs](#01-contexte--objectifs)
2. [Analyse des Besoins](#02-analyse-des-besoins)
3. [Spécifications Fonctionnelles](#03-spécifications-fonctionnelles)
4. [Spécifications Techniques](#04-spécifications-techniques)
5. [Architecture Système](#05-architecture-système)
6. [Modèle de Données](#06-modèle-de-données)
7. [Intelligence Artificielle](#08-intelligence-artificielle)
8. [Sécurité & Conformité](#09-sécurité--conformité)
9. [Planning Détaillé](#10-planning-détaillé)
10. [Backlog Jira Scrum](#105-backlog-jira-scrum)
11. [Équipe & Responsabilités](#11-équipe--responsabilités)
12. [Livrables](#12-livrables)
13. [Critères d'Acceptation](#13-critères-dacceptation)
14. [Risques & Mitigation](#14-risques--mitigation)
15. [Annexes](#15-annexes)

---

## 01 — Contexte & Objectifs

### 1.1 Contexte

**EduTrack IA** est une plateforme pédagogique intelligente destinée aux **centres de cours de soutien scolaire au Maroc**. Elle permet aux enseignants de suivre la progression des élèves du collège et du lycée et de communiquer automatiquement avec les parents grâce à l'intelligence artificielle.

#### Système Éducatif Cible

| Niveau | Classes | Âge Typique | Examen National |
|--------|---------|-------------|-----------------|
| Collège | 1ère, 2ème, 3ème année | 12-15 ans | Brevet (3ème année) |
| Lycée | Tronc Commun, 1ère Bac, 2ème Bac | 15-18 ans | Baccalauréat (2ème Bac) |

#### Matières Enseignées

| Catégorie | Matières | Coefficient Bac |
|-----------|----------|----------------|
| Sciences | Mathématiques, Physique-Chimie, SVT | 7-9 |
| Langues | Arabe, Français, Anglais | 2-4 |
| Humanités | Histoire-Géographie, Philosophie, Éducation Islamique | 2-3 |
| Techniques | Informatique, Sciences de l'Ingénieur | 3-5 |

#### Système de Notation
- **Échelle :** 0 à 20
- **Moyenne de passage :** 10/20
- **Mention TB :** ≥ 16/20 · **Mention Bien :** ≥ 14/20 · **Mention AB :** ≥ 12/20

### 1.2 Problématique

> ⚠️ **Défis identifiés**
> - Suivi manuel chronophage
> - Communication inefficace avec les parents
> - Manque de visibilité sur les compétences à renforcer
> - Absence d'historique de progression longitudinale

### 1.3 Objectifs du Projet

| # | Objectif | Indicateur de Succès |
|---|----------|----------------------|
| O1 | Analyser automatiquement les résultats scolaires | Temps d'analyse réduit de 80% |
| O2 | Identifier les compétences maîtrisées / à renforcer | Précision classification > 75% |
| O3 | Suivre la progression temporelle des élèves | Graphiques de tendance disponibles |
| O4 | Générer des rapports automatiques pour les parents | Rapport généré en < 10 secondes |

### 1.4 Périmètre

**✅ Inclus**
- Gestion des données élèves, notes, compétences
- Analyse IA de la progression
- Génération de rapports personnalisés
- Envoi de notifications WhatsApp
- Dashboard enseignant et vue parent

**❌ Exclus**
- Gestion administrative (facturation, inscriptions)
- Application mobile native
- Intégration ENT / Pronote

---

## 02 — Analyse des Besoins

### 2.1 Parties Prenantes

| Acteur | Rôle | Besoins Principaux |
|--------|------|--------------------|
| 🧑‍🏫 Enseignant | Utilisateur principal | Saisir notes, voir progression, générer rapports |
| 👨‍👩‍👧 Parent | Destinataire des rapports | Consulter progression enfant, recevoir notifications |
| ⚙️ Administrateur | Gestionnaire du centre | Configurer le système, gérer les utilisateurs |
| 👧 Élève | Sujet du suivi (indirect) | Bénéficier d'un suivi personnalisé |

### 2.2 User Stories Principales

#### Enseignant
- **US-E1** — En tant qu'enseignant, je veux enregistrer les notes d'une évaluation, afin de conserver un historique des résultats de chaque élève.
- **US-E2** — En tant qu'enseignant, je veux voir un tableau de bord de ma classe, afin d'identifier rapidement les élèves en difficulté.
- **US-E3** — En tant qu'enseignant, je veux ajouter des observations sur un élève, afin de compléter l'analyse quantitative par des remarques qualitatives.
- **US-E4** — En tant qu'enseignant, je veux générer un rapport de progression en un clic, afin de gagner du temps sur la communication avec les parents.
- **US-E5** — En tant qu'enseignant, je veux visualiser la progression d'un élève dans le temps, afin de mesurer l'efficacité de mon accompagnement.

#### Parent
- **US-P1** — En tant que parent, je veux recevoir un rapport WhatsApp après chaque séance, afin d'être informé de la progression de mon enfant.
- **US-P2** — En tant que parent, je veux accéder à un portail simplifié, afin de consulter l'historique des évaluations de mon enfant.
- **US-P3** — En tant que parent, je veux voir un graphique radar des compétences, afin de comprendre les forces et faiblesses de mon enfant.

### 2.3 Exigences Non-Fonctionnelles

| Catégorie | Métrique | Cible |
|-----------|----------|-------|
| Performance | Temps de réponse API | < 500ms |
| Performance | Génération rapport IA | < 10s |
| Disponibilité | Uptime | 99% |
| Scalabilité | Élèves / centre | 500 |
| Sécurité | Données personnelles | RGPD |
| Interface | Responsive | Oui |

---

## 03 — Spécifications Fonctionnelles

### 3.1 Module 1 — Gestion des Données Pédagogiques

#### 3.1.1 Gestion des Élèves

| Ref | Fonctionnalité | Priorité |
|-----|----------------|----------|
| F1.1 | Créer un profil élève (nom, prénom, classe, date de naissance) | Haute |
| F1.2 | Modifier les informations d'un élève | Haute |
| F1.3 | Archiver un élève (soft delete) | Moyenne |
| F1.4 | Rechercher / filtrer les élèves par classe, nom | Haute |
| F1.5 | Importer des élèves depuis un fichier CSV | Moyenne |

**Endpoints REST :**
```
GET    /api/students          → Liste des élèves (pagination)
GET    /api/students/{id}     → Détail d'un élève
POST   /api/students          → Créer un élève
PUT    /api/students/{id}     → Modifier un élève
DELETE /api/students/{id}     → Archiver un élève
POST   /api/students/import   → Import CSV
```

#### 3.1.2 Gestion des Compétences

| Ref | Fonctionnalité | Priorité |
|-----|----------------|----------|
| F1.6 | Créer une compétence (nom, matière, niveau) | Haute |
| F1.7 | Organiser les compétences par matière | Haute |
| F1.8 | Définir des niveaux de maîtrise (1-4 ou pourcentage) | Haute |

#### 3.1.3 Gestion des Évaluations et Notes

> **Classification des niveaux :**
> 🟢 **Maîtrisée** — Note moyenne ≥ 14/20
> 🟡 **En cours** — 10 ≤ note < 14
> 🔴 **À renforcer** — Note < 10/20

| Ref | Fonctionnalité | Priorité |
|-----|----------------|----------|
| F1.9 | Enregistrer une note (0-20) avec date | Haute |
| F1.10 | Associer une note à une ou plusieurs compétences | Haute |
| F1.11 | Type d'évaluation (contrôle, test blanc, exercice) | Moyenne |
| F1.12 | Consulter l'historique des notes d'un élève | Haute |

#### 3.1.4 Gestion des Observations Enseignants

| Ref | Fonctionnalité | Priorité |
|-----|----------------|----------|
| F1.13 | Ajouter une observation textuelle sur un élève | Haute |
| F1.14 | Associer une observation à une séance/date | Haute |
| F1.15 | Catégoriser les observations (comportement, progrès, difficulté) | Moyenne |
| F1.16 | Inclure les observations dans les rapports | Haute |

### 3.2 Module 2 — Analyse IA de la Progression

**Calcul de la tendance :**
```python
tendance = moyenne_période_récente - moyenne_période_précédente
# si tendance > +2  → "Amélioration"
# si tendance < -2  → "Régression"
# sinon             → "Stagnation"
```

**Endpoints Analytics :**
```
GET /api/analytics/student/{id}/progression  → Indicateurs de progression
GET /api/analytics/student/{id}/trend        → Tendance temporelle
GET /api/analytics/alerts                    → Élèves en régression
GET /api/analytics/student/{id}/radar        → Données radar (JSON)
GET /api/analytics/class/{id}/heatmap        → Données heatmap classe
```

### 3.3 Module 3 — Rapports et Communication Parents

**Structure du rapport généré :**
```
📋 RAPPORT DE PROGRESSION – [Nom Élève]
   Date : [Date]  ·  Enseignant : [Nom]

1. COMPÉTENCES TRAVAILLÉES
   - [Liste des compétences de la séance]

2. PROGRÈS RÉALISÉS
   - [Texte généré par IA sur les améliorations]

3. POINTS À AMÉLIORER
   - [Texte généré par IA sur les difficultés]

4. OBSERVATIONS DE L'ENSEIGNANT
   - [Observations saisies manuellement]

5. RECOMMANDATIONS
   - [Conseils générés par IA pour les parents]
```

| Ref | Fonctionnalité | Priorité |
|-----|----------------|----------|
| F3.1 | Générer un rapport texte personnalisé avec IA | Haute |
| F3.5 | Inclure les recommandations pédagogiques | Haute |
| F3.7 | Générer le rapport en PDF | Moyenne |
| F3.9 | Envoyer un rapport via WhatsApp | Haute |
| F3.13 | Afficher des alertes pour les élèves en difficulté | Moyenne |

---

## 04 — Spécifications Techniques

### 4.1 Stack Technologique

| Couche | Technologie | Version | Justification |
|--------|-------------|---------|---------------|
| Backend | Flask | 2.3+ | Léger, flexible, écosystème Python |
| BDD | PostgreSQL | 15+ | Robuste, requêtes complexes, JSON support |
| ORM | SQLAlchemy | 2.0+ | Migrations Alembic intégrées |
| ML | Scikit-learn | 1.3+ | Classification, métriques |
| Data | Pandas / NumPy | 2.x / 1.24+ | Manipulation & calculs vectorisés |
| NLP | Transformers | 4.35+ | Génération de texte (HuggingFace) |
| Viz | Matplotlib / Seaborn | 3.8+ / 0.13+ | Graphiques & heatmaps |
| Frontend | Streamlit | 1.30+ | Dashboard rapide & intégré |
| Démo IA | Gradio | 4.x | Interface interactive IA |
| PDF | WeasyPrint | 60+ | Génération PDF depuis HTML |
| Notif. | Twilio / WhatsApp | 8.x | API WhatsApp Business |

### 4.2 Variables d'Environnement

| Variable | Description | Exemple |
|----------|-------------|---------|
| `DATABASE_URL` | URL PostgreSQL | `postgresql://user:pass@host:5432/edutrack` |
| `FLASK_ENV` | Environnement | `development / production` |
| `SECRET_KEY` | Clé secrète Flask | `your-secret-key-here` |
| `TWILIO_ACCOUNT_SID` | ID compte Twilio | `ACxxxxxxxx` |
| `HF_MODEL` | Modèle HuggingFace | `tiiuae/falcon-7b-instruct` |

---

## 05 — Architecture Système

### 5.2 Ports & Services

| Service | Port | Description |
|---------|------|-------------|
| Streamlit Dashboard | :8501 | Interface enseignant principale |
| Gradio Demo IA | :7860 | Interface de démonstration IA |
| Vue Parent | :8502 | Portail simplifié parent |
| Flask API | :5000 | API REST centrale |
| PostgreSQL | :5432 | Base de données |

### 5.3 Structure du Projet

```
edutrack-ia/
├── 📁 app/
│   ├── 📁 api/            # students, grades, analytics, reports, notifications
│   ├── 📁 models/         # SQLAlchemy models
│   ├── 📁 schemas/        # Marshmallow schemas
│   ├── 📁 services/       # ml_classifier, progression, report_generator, whatsapp
│   └── 📁 ml/             # models/*.joblib + training scripts
├── 📁 frontend/
│   ├── 📁 streamlit/      # Dashboard principal + pages
│   ├── 📁 gradio/         # Interface démo IA
│   └── 📁 parent_view/    # Vue simplifiée parent
├── 📁 data/               # CSV fixtures d'exemple
├── 📁 migrations/         # Alembic versions
├── 📁 tests/              # unit/ + integration/
├── 📁 docs/               # ADR, brand-guide, api-reference
├── .env.example
├── requirements.txt
├── README.md
└── docker-compose.yml
```

### 5.4 API REST — Authentification

```http
POST   /api/auth/login     → Connexion utilisateur
POST   /api/auth/logout    → Déconnexion (JWT)
POST   /api/auth/refresh   → Renouveler le token
GET    /api/auth/me        → Profil utilisateur connecté
```

**Réponse standard :**
```json
{
  "success": true,
  "data": { ... },
  "meta": { "page": 1, "per_page": 20, "total": 150 }
}
```

**Réponse erreur :**
```json
{
  "success": false,
  "error": { "code": "VALIDATION_ERROR", "message": "La note doit être entre 0 et 20", "field": "value" }
}
```

---

## 06 — Modèle de Données

### 6.1 Tables Principales

```sql
-- students
id UUID PK, first_name VARCHAR(100), last_name VARCHAR(100),
date_of_birth DATE, class_name VARCHAR(50), parent_phone VARCHAR(20),
parent_email VARCHAR(255), is_active BOOLEAN DEFAULT TRUE, created_at TIMESTAMP

-- grades
id UUID PK, student_id UUID FK, competency_id UUID FK,
value DECIMAL(4,2) CHECK 0-20, evaluation_type ENUM(controle|test_blanc|exercice),
evaluation_date DATE, created_at TIMESTAMP

-- competencies
id UUID PK, name VARCHAR(200), description TEXT,
subject_id UUID FK, level VARCHAR(20), created_at TIMESTAMP

-- observations
id UUID PK, student_id UUID FK, teacher_name VARCHAR(100),
content TEXT, category ENUM(comportement|progres|difficulte),
observation_date DATE, created_at TIMESTAMP

-- users
id UUID PK, email VARCHAR(255) UNIQUE, password_hash VARCHAR(255),
role ENUM(admin|teacher|parent), first_name VARCHAR(100),
last_name VARCHAR(100), is_active BOOLEAN, created_at TIMESTAMP

-- reports
id UUID PK, student_id UUID FK, generated_by UUID FK,
report_type ENUM(progress|alert|summary), content_json JSONB,
pdf_path VARCHAR(500), whatsapp_sent BOOLEAN DEFAULT FALSE, created_at TIMESTAMP

-- ai_predictions
id UUID PK, student_id UUID FK, classification VARCHAR(50),
confidence DECIMAL(5,4), features_json JSONB, created_at TIMESTAMP
```

---

## 08 — Intelligence Artificielle

### 8.4 Configuration du Modèle ML

```python
# config/ml_config.py
ML_CONFIG = {
    "model": {
        "type": "RandomForestClassifier",
        "params": {
            "n_estimators": 100, "max_depth": 10,
            "min_samples_split": 5, "min_samples_leaf": 2,
            "random_state": 42, "n_jobs": -1
        }
    },
    "features": [
        "avg_grade", "std_grade", "trend_coefficient",
        "num_evaluations", "last_grade", "days_since_last",
        "competency_coverage", "improvement_rate"
    ],
    "target_classes": {
        0: "en_difficulte",   # Score < 10 ou tendance négative forte
        1: "stable",           # Score entre 10-14, tendance neutre
        2: "en_progression"   # Score ≥ 14 ou tendance positive
    },
    "thresholds": {
        "alert_confidence": 0.75,
        "min_evaluations": 3,
        "difficulty_grade": 10.0
    }
}
```

### 8.5 Configuration WhatsApp Twilio

```python
# config/whatsapp_config.py
WHATSAPP_CONFIG = {
    "account_sid": "TWILIO_ACCOUNT_SID",
    "auth_token":  "TWILIO_AUTH_TOKEN",
    "from_number": "whatsapp:+14155238886",
    "message_templates": {
        "report_ready": "EduTrack IA - Rapport de Progression\nBonjour,\nLe rapport de progression de {student_name} est disponible.\nMoyenne: {avg_grade}/20 | Classification: {classification}\nTendance: {trend}\nRapport complet: {pdf_url}",
        "alert": "⚠️ Alerte EduTrack IA - Concernant {student_name}\n{alert_message}"
    }
}
```

---

## 09 — Sécurité & Conformité

### 9.1 Protection des Données RGPD

| Mesure | Description |
|--------|-------------|
| Minimisation | Collecter uniquement les données nécessaires |
| Pseudonymisation | IDs UUID dans les logs |
| Chiffrement | HTTPS obligatoire, BDD chiffrée au repos |
| Droit d'accès | Export des données d'un élève sur demande |
| Droit à l'oubli | Suppression complète possible |

### 9.2 Authentification

| Acteur | Méthode |
|--------|---------|
| Enseignant | Session Flask + mot de passe hash bcrypt |
| Parent | Code unique par élève (6 caractères) |
| API | JWT avec expiration 24h |

---

## 10 — Planning Détaillé

### 10.1 Dates Clés

| Sprint | Dates | Goal | Indicateur de Succès |
|--------|-------|------|----------------------|
| **S0** | 25-31 Mars | Préparer les fondations | Tous les devs peuvent lancer le projet localement |
| **S1** | 01-07 Avril | Authentification + BDD | Login/Logout opérationnel, 0 erreur console |
| **S2** | 08-14 Avril | Collecter les données | Un enseignant peut saisir et valider des notes |
| **S3** | 15-21 Avril | Analyser avec l'IA | API predict retourne une prédiction en ≤ 500ms |
| **S4** | 22-28 Avril | Visualiser et démontrer | Dashboard affiche graphiques, Gradio accessible |
| **S5** | 29 Avr - 05 Mai | Communiquer et tester | Rapport PDF généré, coverage pytest ≥ 80% |
| **S6** | 06-12 Mai | Stabiliser et documenter | 0 erreur Sentry critique, doc PDF prête |
| **S7** | 13-19 Mai | Excellence PFE | Démo 15 min prête, Lighthouse Security+A11y ≥ 90 |
| **🎓 SOUTENANCE** | 13-16 Mai | Présentation 10 minutes devant le jury FQIA 2026 | — |

---

## 10.5 — Backlog Jira Scrum

### Definition of Done (DoD)
Une User Story est considérée **Done** lorsque :
1. ✅ Le code est écrit et respecte les conventions du projet
2. ✅ Les tests unitaires sont écrits (couverture ≥ 80%)
3. ✅ Les tests passent sur la CI/CD
4. ✅ Le code a été review par au moins 1 autre membre
5. ✅ La documentation est mise à jour (README, docstrings)
6. ✅ Les critères d'acceptation sont validés
7. ✅ Le code est mergé dans la branche `develop`
8. ✅ Aucune dette technique critique introduite

### Epics du Projet

| Epic ID | Nom | SP Total |
|---------|-----|----------|
| EPIC-0 | Sprint 0 - Setup & Architecture | 19 |
| EPIC-1 | Authentification & Sécurité | 26 |
| EPIC-2 | Gestion Académique | 49 |
| EPIC-3 | Intelligence Artificielle | 45 |
| EPIC-4 | Dashboard & Visualisations | 64 |
| EPIC-5 | Rapports & Notifications | 35 |
| EPIC-6 | Data Engineering | 34 |
| EPIC-7 | Qualité & Excellence PFE | 26 |
| **TOTAL** | **71 Stories** | **298 SP** |

> **Vélocité estimée :** 33 SP/sprint sur 8 sprints

### Sprint 0 — Setup & Architecture

| ID | User Story | SP | Assign |
|----|------------|-----|--------|
| US-SETUP-1 | Définir l'architecture système | 5 | Ahmed |
| US-SETUP-2 | Configurer l'environnement ML | 3 | Chaimae |
| US-SETUP-3 | Créer les maquettes UI/UX | 5 | Zakaria |
| US-SETUP-4 | Configurer PostgreSQL local | 3 | Ouidad |
| US-SETUP-5 | Configurer l'environnement de dev | 3 | Ahmed |

### Sprint 1 — Authentification & Fondations

| ID | User Story | SP | Assign |
|----|------------|-----|--------|
| US-AUTH-1 | Connexion avec email/mot de passe | 5 | Chaimae |
| US-AUTH-2 | Déconnexion sécurisée | 2 | Chaimae |
| US-AUTH-3 | Créer des comptes enseignants | 5 | Chaimae |
| US-AUTH-4 | Formulaires d'authentification UI | 5 | Zakaria |
| US-AUTH-5 | Pipeline CI/CD GitHub Actions | 3 | Ahmed |
| US-DATA-1 | BDD PostgreSQL configurée | 5 | Ouidad |
| US-DATA-2 | Migrations Alembic en place | 5 | Chaimae |
| US-DATA-3 | Fixtures matières marocaines | 5 | Ouidad |
| US-DATA-4 | Fixtures compétences collège | 5 | Taoufiq |
| US-DATA-5 | Fixtures compétences lycée | 5 | Ouidad |

### Sprint 2 — CRUD Académique

| ID | User Story | SP | Assign |
|----|------------|-----|--------|
| US-STU-1 | Créer un profil élève | 3 | Chaimae |
| US-STU-2 | Modifier les informations d'un élève | 2 | Chaimae |
| US-STU-3 | Archiver un élève (soft delete) | 2 | Ahmed |
| US-STU-4 | Rechercher/filtrer les élèves | 3 | Ahmed |
| US-STU-5 | Formulaires CRUD élèves UI | 5 | Zakaria |
| US-STU-6 | Importer des élèves via CSV | 5 | Ouidad |
| US-GRD-1 | Saisir une note pour un élève | 5 | Chaimae |
| US-GRD-2 | Modifier une note existante | 3 | Chaimae |
| US-GRD-3 | Voir l'historique des notes | 5 | Ahmed |
| US-CMP-1 | Créer une compétence | 3 | Ahmed |
| US-CMP-2 | Organiser compétences par matière | 3 | Chaimae |

### Sprint 3 — Intelligence Artificielle

| ID | User Story | SP | Assign |
|----|------------|-----|--------|
| US-ML-1 | Calculer les features ML d'un élève | 8 | Chaimae |
| US-ML-2 | Classifier un élève (ML pipeline) | 8 | Chaimae |
| US-ML-3 | Voir la prédiction IA pour chaque élève | 5 | Zakaria |
| US-ML-4 | Intégrer l'API ML au système | 5 | Ahmed |
| US-ML-5 | Valider les données pour le ML | 3 | Ouidad |
| US-ML-6 | Préparer le dataset d'entraînement | 3 | Taoufiq |
| US-OBS-1 | Ajouter une observation sur un élève | 3 | Chaimae |
| US-OBS-2 | Catégoriser les observations | 2 | Chaimae |

### Sprint 4 — Dashboard & Visualisations

| ID | User Story | SP | Assign |
|----|------------|-----|--------|
| US-DASH-1 | Dashboard avec KPIs de la classe | 8 | Zakaria |
| US-DASH-2 | Heatmap des compétences | 5 | Zakaria |
| US-DASH-3 | Graphique radar pour un élève | 5 | Zakaria |
| US-DASH-4 | Courbe de progression d'un élève | 5 | Zakaria |
| US-DASH-5 | Alertes élèves en difficulté | 5 | Zakaria |
| US-DASH-6 | Optimiser les performances dashboard | 3 | Ahmed |
| US-DASH-7 | Endpoints Dashboard | 5 | Chaimae |
| US-DASH-8 | Seeder les données de démo | 3 | Ouidad |
| US-GRADIO-1 | Interface Gradio interactive | 5 | Chaimae |
| US-GRADIO-2 | Exemples prêchargés Gradio | 3 | Zakaria |
| US-ML-7 | Entraîner le modèle avec nouvelles données | 5 | Chaimae |

### Sprint 5 — Rapports & Notifications

| ID | User Story | SP | Assign |
|----|------------|-----|--------|
| US-RPT-1 | Générer un rapport PDF avec l'IA | 8 | Chaimae |
| US-RPT-2 | Envoyer le rapport par WhatsApp | 8 | Ahmed |
| US-RPT-3 | Alertes automatiques aux parents | 5 | Ahmed |
| US-RPT-4 | Télécharger le rapport PDF (parent) | 3 | Zakaria |
| US-RPT-5 | Créer les templates de rapports | 3 | Ouidad |
| US-RPT-6 | Tests intégration end-to-end | 3 | Taoufiq |
| US-DASH-10 | Dashboard simplifié parent | 5 | Zakaria |
| US-TEST-1 | Tests unitaires API Flask | 5 | Taoufiq |
| US-TEST-2 | Tests unitaires ML | 3 | Chaimae |

### Sprint 6 — Finalisation & Documentation

| ID | User Story | SP | Assign |
|----|------------|-----|--------|
| US-MON-1 | Intégrer Sentry | 3 | Ahmed |
| US-DOC-1 | Guide utilisateur | 3 | Ouidad |
| US-RESP-1 | Dashboard responsive mobile | 2 | Ahmed |
| US-RPT-7 | Historique des rapports envoyés | 5 | Ahmed |
| US-DATA-7 | Script de seed pour la démo | 3 | Ouidad |
| US-DASH-12 | Filtrer le dashboard par période | 3 | Ahmed |

### Sprint 7 — Excellence PFE

| ID | User Story | SP | Assign |
|----|------------|-----|--------|
| US-DEMO-1 | Mode démonstration guidé | 5 | Ahmed |
| US-SEC-1 | Audit sécurité OWASP Top 10 | 3 | Taoufiq |
| US-A11Y-1 | Interface accessible WCAG | 2 | Ouidad |
| US-ML-8 | Score de confiance de la prédiction | 3 | Zakaria |
| US-ML-9 | Métriques du modèle (admin) | 5 | Chaimae |

---

## 11 — Équipe & Responsabilités

### 11.1 Composition de l'équipe

| Membre | Rôle | Responsabilités Principales |
|--------|------|-----------------------------|
| Ahmed | Chef de Projet / Full-stack | Coordination équipe, architecture, full-stack, rapport final |
| Chaimae | IA / Backend | Modèles ML Scikit-learn, Flask API, Transformers HuggingFace |
| Zakaria | IA / Frontend | Interface Streamlit/Gradio, visualisations ML, dashboard UX |
| Ouidad | Data Engineer | BDD PostgreSQL, fixtures données éducatives Maroc |
| Taoufiq | Data Engineer | Pipelines ETL, migrations Alembic, données test, documentation |

### 11.2 Matrice RACI

| Tâche | Ahmed | Chaimae | Zakaria | Ouidad | Taoufiq |
|-------|-------|---------|---------|--------|---------|
| Architecture | R | A | C | I | I |
| BDD PostgreSQL | A | C | I | R | R |
| API Flask | C | R | I | I | I |
| ML Classification | A | R | C | I | I |
| Dashboard Streamlit | C | C | R | I | I |
| Tests E2E | A | R | C | C | C |
| Documentation | R | C | C | C | C |

> **R** = Responsable · **A** = Accountable · **C** = Consulté · **I** = Informé

---

## 12 — Livrables

| Livrable | Format | Date Limite |
|----------|--------|-------------|
| L1 | Dépôt GitHub documenté | 15/05/2026 |
| L2 | README.md complet | 08/05/2026 |
| L3 | Documentation API (Markdown + Swagger) | 08/05/2026 |
| L4 | Prototype fonctionnel déployable | 15/05/2026 |
| L5 | Rapport technique (10-15 pages PDF) | 15/05/2026 |
| L6 | Slides présentation 10 min | 15/05/2026 |
| L7 | Script de démo jury | 15/05/2026 |

---

## 13 — Critères d'Acceptation

### 13.1 Critères Fonctionnels

| Module | Critère | Validation |
|--------|---------|-----------|
| Module 1 | CRUD élèves fonctionnel | 100% tests passent |
| Module 1 | CRUD notes fonctionnel | 100% tests passent |
| Module 1 | CRUD observations fonctionnel | 100% tests passent |
| Module 2 | Classification précision ≥ 75% | Métriques affichées |
| Module 2 | Graphiques Radar + Courbe + Heatmap | Rendus dans Streamlit |
| Module 3 | Rapport généré en ≤ 10s | Temps mesuré |
| Module 3 | WhatsApp envoyé avec succès | Log de confirmation |

### 13.2 Critères Non-Fonctionnels

| Critère | Cible | Outil |
|---------|-------|-------|
| Couverture tests | ≥ 80% | pytest-cov |
| Temps réponse API | < 500ms | Locust / k6 |
| Documentation | Complète | Revue équipe |
| Disponibilité | ≥ 99.5% | Monitoring |

### 13.3 Scénarios de Tests E2E

| Scénario | Étapes | Résultat Attendu |
|----------|--------|-----------------|
| 1. Login enseignant | Accéder login → Entrer credentials → Soumettre | Dashboard affiché, token JWT stocké |
| 2. Ajouter un élève | Clic "Nouvel élève" → Remplir formulaire → Valider | Élève créé en BDD, affiché dans liste |
| 3. Saisir une note | Sélectionner élève → Formulaire → Valider | Note en BDD, ML mis à jour, graphe actualisé |
| 4. Générer rapport IA | Sélectionner élève → Clic "Générer rapport" → Attendre | PDF disponible en ≤ 10s, texte IA pertinent |
| 5. Envoyer WhatsApp | Ouvrir rapport → Clic "Envoyer WhatsApp" | Message reçu par parent, log confirmé |
| 6. Vue parent | Connexion parent → Voir progression | Données enfant uniquement, graphes lisibles |

---

## 14 — Risques & Mitigation

| # | Risque | Probabilité | Impact | Mitigation |
|---|--------|------------|--------|------------|
| R1 | API WhatsApp non disponible | Moyenne | Haut | Simuler avec logs console + mode démo Twilio sandbox |
| R2 | Modèle IA pas assez précis | Moyenne | Moyen | Ajuster features, fallback sur règles métier (seuils fixes) |
| R3 | Retard sur un sprint | Haute | Moyen | Buffer Sprint 7, repriorisation backlog chaque vendredi |
| R4 | Problème configuration AWS RDS | Faible | Haut | SQLite local en backup, migration vers RDS en Sprint 1 |
| R5 | Membre de l'équipe absent | Moyenne | Moyen | Documentation cross-training, pair programming |

---

## 15 — Annexes

### A. Glossaire

| Terme | Définition |
|-------|------------|
| Compétence | Savoir-faire évalué (ex: Résoudre une équation du 1er degré) |
| Évaluation | Session notée (contrôle, test blanc, exercice) |
| Progression | Évolution des notes dans le temps |
| Classification | Attribution d'un niveau : Maîtrisée / En cours / À renforcer |
| Rapport | Document texte résumant la progression pour les parents |
| Observation | Remarque qualitative de l'enseignant sur une séance |

### B. Charte Graphique EduTrack IA

```
Couleurs :
  Navy Deep  : #0D1B2A
  Teal Primary : #00C9A7
  Sky Blue   : #0EA5E9
  Amber      : #FFB347

Typographie :
  Titres  : Syne 700/800
  Corps   : DM Sans 400/500
  Code    : JetBrains Mono

Fichiers de charte (à créer en Sprint 1) :
  docs/brand-guide.md
  assets/logo.svg
  assets/logo.png
  .streamlit/config.toml
```

### C. Structure des Tests

```
tests/
├── unit/
│   ├── test_models.py         # Tests modèles SQLAlchemy
│   ├── test_schemas.py        # Tests validation Marshmallow
│   ├── test_ml_features.py    # Tests calcul features ML
│   └── test_classification.py # Tests pipeline ML
├── integration/
│   ├── test_api_students.py   # Tests CRUD élèves
│   ├── test_api_grades.py     # Tests CRUD notes
│   ├── test_api_analytics.py  # Tests endpoints analytics
│   ├── test_api_reports.py    # Tests génération rapports
│   └── test_whatsapp.py       # Tests intégration Twilio
└── e2e/
    ├── test_teacher_flow.py   # Parcours enseignant complet
    ├── test_parent_flow.py    # Parcours parent
    └── test_report_flow.py    # Génération + envoi rapport
```

---

*EduTrack IA — Plateforme Pédagogique Intelligente*
*Cahier des Charges v1.0 · PFE N°9 · FQIA 2026 · 21 mars 2026*
*Document confidentiel — Usage interne équipe projet*
