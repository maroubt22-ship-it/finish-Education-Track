# EduTrack IA - Copilot Instructions

## Project Overview

EduTrack IA is an intelligent educational tracking platform for tutoring centers in Morocco. The current implementation is a **frontend-only demo** with three Python-based web interfaces using mock data.

### Architecture

```
Three independent frontend applications:
1. Streamlit Teacher Dashboard (port 8501) - Main teacher interface
2. Gradio AI Demo (port 7860) - AI feature demonstrations
3. Streamlit Parent View (port 8502) - Simplified parent portal

All share common mock data and styling from frontend/shared/
```

## Running the Application

### Installation
```bash
pip install -r frontend/requirements.txt
```

### Launch Commands
```bash
# Teacher Dashboard
streamlit run frontend/streamlit/app.py --server.port 8501

# AI Demo
python frontend/gradio/app.py

# Parent View
streamlit run frontend/parent_view/app.py --server.port 8502

# Windows shortcuts also available:
run_teacher_dashboard.bat
run_gradio_demo.bat
run_parent_view.bat
```

### No Tests or Linting
This is a demo project with no test suite or linting configuration. The focus is on functional UI demonstrations.

## Moroccan Education System Context

**Critical**: This application is specifically designed for the Moroccan educational system. Always use:

- **Grading scale**: 0-20 (not 0-100 or letter grades)
- **Pass threshold**: 10/20
- **Grade classifications**:
  - 🟢 **Maîtrisée** (Mastered): ≥ 14/20
  - 🟡 **En cours** (In progress): 10-14/20
  - 🔴 **À renforcer** (Needs reinforcement): < 10/20
- **Mentions**: TB ≥16, Bien ≥14, AB ≥12
- **School levels**:
  - Collège: 1ère, 2ème, 3ème année (ages 12-15)
  - Lycée: Tronc Commun, 1ère Bac, 2ème Bac (ages 15-18)
- **Subject categories**: Sciences, Langues, Humanités, Techniques

### Language
All UI text, documentation, and user-facing content MUST be in **French** (not English), as this is the primary language of instruction in Moroccan education.

## Key Architectural Patterns

### 1. Mock Data System

All data is generated in `frontend/shared/data/mock_data.py` with realistic Moroccan student profiles:

```python
# Data is loaded once into session state on app startup
from frontend.shared.data.mock_data import get_all_mock_data

if 'data_loaded' not in st.session_state:
    mock_data = get_all_mock_data()
    st.session_state.students = mock_data['students']  # DataFrame
    st.session_state.grades = mock_data['grades']      # DataFrame
    # etc.
```

**Important**: Mock data includes intentional diversity:
- Excellent students (avg ≥16)
- Struggling students (avg <10)
- Improving trends (progression +2 pts)
- Declining trends (regression -2 pts)

### 2. Streamlit Multi-Page Architecture

Teacher dashboard uses Streamlit's native multi-page pattern:
- Main app: `frontend/streamlit/app.py`
- Pages: `frontend/streamlit/pages/N_emoji_Name.py` (numbered for order)
- Session state shared across all pages
- Each page checks for `data_loaded` in session state

**Pattern for new pages**:
```python
import streamlit as st
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from frontend.shared.styles.theme import apply_custom_css

st.set_page_config(...)
apply_custom_css()

if 'data_loaded' not in st.session_state:
    st.error("⚠️ Données non chargées. Veuillez retourner à la page principale.")
    st.stop()
```

### 3. Shared Component System

Reusable UI components in `frontend/streamlit/components/`:
- `student_card.py` - Display student info with grades/trends
- `grade_chart.py` - Various grade visualization charts
- `competency_radar.py` - Radar charts for skill assessment
- `alert_banner.py` - Styled notification banners
- `report_preview.py` - Report formatting and preview

**Usage pattern**:
```python
from frontend.streamlit.components.student_card import display_student_card
from frontend.streamlit.components.grade_chart import display_grade_evolution

# Components work with DataFrames from session state
display_student_card(student, average=avg, trend=trend)
display_grade_evolution(grades_df, student_name)
```

### 4. Styling System

Centralized in `frontend/shared/styles/theme.py`:

```python
from frontend.shared.styles.theme import COLORS, apply_custom_css, create_badge

# Apply CSS to every page
apply_custom_css()

# Use consistent colors
border_color = COLORS['success']  # green for maîtrisée
text_color = COLORS['danger']     # red for à renforcer

# Use helper functions for consistency
badge_html = create_badge("Maîtrisée", "success")
```

**Color scheme is semantic**:
- `primary` - Main brand color (dark blue)
- `success/green` - Maîtrisée (≥14)
- `warning/orange` - En cours (10-14)
- `danger/red` - À renforcer (<10)

### 5. Report Generation Structure

AI-generated reports follow a **mandatory 5-section structure**:

1. **Compétences travaillées** - Skills evaluated
2. **Progrès réalisés** - Progress achieved
3. **Points à améliorer** - Areas to improve
4. **Observations de l'enseignant** - Teacher notes
5. **Recommandations** - AI recommendations

Use `frontend/streamlit/utils/helpers.py::generate_report_text()` for consistency.

### 6. Trend Calculation

Standard formula across the application:
```python
def calculate_trend(grades_df):
    mid = len(grades_df) // 2
    previous_avg = grades_df[:mid]['value'].mean()
    recent_avg = grades_df[mid:]['value'].mean()
    trend_value = recent_avg - previous_avg
    
    if trend_value > 2: return "amélioration"
    elif trend_value < -2: return "régression"
    else: return "stable"
```

## Important Conventions

### Naming Patterns

- **Student IDs**: `STU####` (e.g., STU0001)
- **Grade IDs**: `GRD#####` (e.g., GRD00001)
- **Competency IDs**: `COMP####` (e.g., COMP0001)
- **Observation IDs**: `OBS#####` (e.g., OBS00001)
- **Phone numbers**: Moroccan format `+212 6XXXXXXXX`

### DataFrame Column Names

Standard column names (used consistently across mock data):
- Students: `id, first_name, last_name, class_name, date_of_birth, parent_phone, parent_email, is_active`
- Grades: `id, student_id, competency_id, competency_name, subject, value, evaluation_type, evaluation_date`
- Competencies: `id, name, subject, category, level`
- Observations: `id, student_id, teacher_name, content, category, observation_date`

### Evaluation Types
Standard values in `evaluation_type` field:
- `contrôle` - Regular test
- `test blanc` - Mock exam
- `exercice` - Exercise
- `devoir maison` - Homework

### Observation Categories
Fixed values for teacher observations:
- `comportement` - Behavior
- `progrès` - Progress
- `difficulté` - Difficulty

## Data Flow

```
Mock Data Generation (once on startup)
    ↓
Session State (st.session_state.students, .grades, etc.)
    ↓
Pages read from session state
    ↓
Components receive DataFrames as parameters
    ↓
Visualizations (Plotly/Matplotlib/Seaborn)
```

**No persistence**: Changes made in the UI are stored in session state but lost on page refresh. This is intentional for the demo.

## Common Pitfalls

1. **Import paths**: All pages need `sys.path.insert(0, ...)` to find `frontend.shared`
2. **Session state checks**: Always verify `data_loaded` before accessing data
3. **Grade range validation**: Must be 0-20, not 0-100
4. **French text**: Never use English in user-facing strings
5. **Emoji in filenames**: Page files use emoji in names (e.g., `1_🏠_Accueil.py`)
6. **DataFrames not dicts**: Mock data returns pandas DataFrames, not lists of dicts

## Adding New Features

### New Streamlit Page
1. Create `frontend/streamlit/pages/N_emoji_Name.py` with proper numbering
2. Copy import boilerplate from existing page
3. Call `apply_custom_css()` and check `data_loaded`
4. Access data via `st.session_state`
5. Use components from `frontend/streamlit/components/`

### New Component
1. Create in `frontend/streamlit/components/your_component.py`
2. Accept DataFrames as parameters (not raw dicts)
3. Use `COLORS` from theme for consistency
4. Return None, render with `st.markdown()` or Streamlit widgets
5. Handle empty DataFrame cases gracefully

### New Mock Data Type
1. Add generator function in `frontend/shared/data/mock_data.py`
2. Follow naming conventions (IDs, columns)
3. Return pandas DataFrame
4. Update `get_all_mock_data()` to include new data
5. Initialize in session state in `app.py`

## Visualization Guidelines

- **Plotly**: Preferred for interactive charts (line, bar, radar)
- **Matplotlib**: Use for simple static charts
- **Seaborn**: Use for heatmaps and statistical plots
- Always set `use_container_width=True` for Streamlit charts
- Include threshold lines at 10 and 14 for grade charts

## Backend Integration (Future)

Currently mock data only. When integrating with Flask backend:
- Replace `get_all_mock_data()` with API calls
- Keep DataFrame structure unchanged
- Session state becomes cache for API responses
- Add authentication middleware
- See `CAHIER_DES_CHARGES.md` for API endpoint specifications

## Documentation

- `CAHIER_DES_CHARGES.md` - Complete functional specifications (741 lines)
- `frontend/README.md` - User guide and setup instructions
- `IMPLEMENTATION_SUMMARY.md` - Technical implementation details
- `GETTING_STARTED.md` - Quick start guide
