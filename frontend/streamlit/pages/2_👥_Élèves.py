# frontend/streamlit/pages/2_👥_Élèves.py
"""
Students Management Page
Manage students, view details, add/edit/archive students, import CSV
"""

import streamlit as st
import pandas as pd
from datetime import datetime
import io

# Imports from shared modules
from frontend.shared.data.mock_data import generate_students, CLASSES, FIRST_NAMES, LAST_NAMES
from frontend.shared.styles.theme import (
    apply_custom_css, create_header, create_alert, COLORS
)
from frontend.streamlit.components.student_card import display_student_card
from frontend.streamlit.utils.helpers import (
    filter_students, get_student_summary, format_date, calculate_average
)

# Page configuration
st.set_page_config(
    page_title="Gestion des Élèves - EduTrack IA",
    page_icon="👥",
    layout="wide"
)

# Apply custom styling
apply_custom_css()


def initialize_session_state():
    """Initialize session state variables"""
    if "students" not in st.session_state:
        st.session_state.students = generate_students(50)
    
    if "grades" not in st.session_state:
        # Import here to avoid circular dependency
        from frontend.shared.data.mock_data import generate_competencies, generate_grades
        competencies = generate_competencies()
        st.session_state.grades = generate_grades(st.session_state.students, competencies)
    
    if "selected_student_id" not in st.session_state:
        st.session_state.selected_student_id = None
    
    if "show_add_form" not in st.session_state:
        st.session_state.show_add_form = False
    
    if "show_edit_form" not in st.session_state:
        st.session_state.show_edit_form = False


def add_student(student_data):
    """Add a new student to the database"""
    # Generate new ID
    existing_ids = [int(sid.replace("STU", "")) for sid in st.session_state.students["id"]]
    new_id = f"STU{max(existing_ids) + 1:04d}"
    
    student_data["id"] = new_id
    student_data["is_active"] = True
    student_data["created_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Add to dataframe
    new_student = pd.DataFrame([student_data])
    st.session_state.students = pd.concat(
        [st.session_state.students, new_student], 
        ignore_index=True
    )
    
    return new_id


def update_student(student_id, updated_data):
    """Update student information"""
    idx = st.session_state.students[st.session_state.students["id"] == student_id].index[0]
    
    for key, value in updated_data.items():
        st.session_state.students.at[idx, key] = value


def archive_student(student_id):
    """Archive (deactivate) a student"""
    idx = st.session_state.students[st.session_state.students["id"] == student_id].index[0]
    st.session_state.students.at[idx, "is_active"] = False


def activate_student(student_id):
    """Activate an archived student"""
    idx = st.session_state.students[st.session_state.students["id"] == student_id].index[0]
    st.session_state.students.at[idx, "is_active"] = True


def parse_csv_students(csv_file):
    """Parse CSV file and return student data"""
    try:
        df = pd.read_csv(csv_file)
        
        # Expected columns
        required_cols = ["first_name", "last_name", "class_name", "date_of_birth", "parent_phone", "parent_email"]
        
        # Check if all required columns exist
        missing_cols = [col for col in required_cols if col not in df.columns]
        if missing_cols:
            return None, f"Colonnes manquantes : {', '.join(missing_cols)}"
        
        return df, None
    except Exception as e:
        return None, f"Erreur lors de la lecture du fichier : {str(e)}"


def import_students_from_csv(students_df):
    """Import students from CSV dataframe"""
    imported_count = 0
    
    for _, row in students_df.iterrows():
        student_data = {
            "first_name": row["first_name"],
            "last_name": row["last_name"],
            "class_name": row["class_name"],
            "date_of_birth": row["date_of_birth"],
            "parent_phone": row["parent_phone"],
            "parent_email": row["parent_email"]
        }
        
        add_student(student_data)
        imported_count += 1
    
    return imported_count


def display_student_list_view(filtered_students):
    """Display list of students with cards"""
    if len(filtered_students) == 0:
        st.info("🔍 Aucun élève trouvé avec ces critères de recherche.")
        return
    
    # Display count
    st.markdown(f"**{len(filtered_students)} élève(s) trouvé(s)**")
    st.markdown("---")
    
    # Display students in a grid (2 columns)
    cols = st.columns(2)
    
    for idx, (_, student) in enumerate(filtered_students.iterrows()):
        col = cols[idx % 2]
        
        with col:
            # Calculate student average
            student_grades = st.session_state.grades[
                st.session_state.grades["student_id"] == student["id"]
            ]
            
            average = None
            trend = None
            
            if len(student_grades) > 0:
                average = round(student_grades["value"].mean(), 2)
                
                # Calculate trend
                if len(student_grades) >= 4:
                    mid = len(student_grades) // 2
                    prev_avg = student_grades.iloc[:mid]["value"].mean()
                    recent_avg = student_grades.iloc[mid:]["value"].mean()
                    diff = recent_avg - prev_avg
                    
                    if diff > 2:
                        trend = "amélioration"
                    elif diff < -2:
                        trend = "régression"
                    else:
                        trend = "stable"
            
            # Display card
            display_student_card(student, average, trend)
            
            # Add click button to view details
            if st.button(
                f"Voir détails", 
                key=f"view_{student['id']}", 
                use_container_width=True
            ):
                st.session_state.selected_student_id = student["id"]
                st.rerun()
            
            # Show archived badge if inactive
            if not student["is_active"]:
                st.markdown(
                    f'<div style="background: {COLORS["danger"]}; color: white; padding: 0.5rem; '
                    f'text-align: center; border-radius: 5px; margin-top: 0.5rem;">'
                    f'📦 ARCHIVÉ</div>',
                    unsafe_allow_html=True
                )
            
            st.markdown("<br>", unsafe_allow_html=True)


def display_student_detail_view(student_id):
    """Display detailed view of a student"""
    student = st.session_state.students[
        st.session_state.students["id"] == student_id
    ].iloc[0]
    
    # Header with back button
    col1, col2 = st.columns([1, 5])
    with col1:
        if st.button("← Retour"):
            st.session_state.selected_student_id = None
            st.rerun()
    
    with col2:
        st.markdown(
            f"<h2 style='color: {COLORS['primary']};'>"
            f"👤 {student['first_name']} {student['last_name']}</h2>",
            unsafe_allow_html=True
        )
    
    st.markdown("---")
    
    # Student information in columns
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### 📋 Informations générales")
        st.markdown(f"**ID:** {student['id']}")
        st.markdown(f"**Classe:** {student['class_name']}")
        st.markdown(f"**Date de naissance:** {format_date(student['date_of_birth'])}")
        
        status_color = COLORS["success"] if student["is_active"] else COLORS["danger"]
        status_text = "Actif" if student["is_active"] else "Archivé"
        st.markdown(
            f"**Statut:** <span style='color: {status_color}; font-weight: bold;'>{status_text}</span>",
            unsafe_allow_html=True
        )
    
    with col2:
        st.markdown("### 📞 Contact Parents")
        st.markdown(f"**Téléphone:** {student['parent_phone']}")
        st.markdown(f"**Email:** {student['parent_email']}")
        st.markdown(f"**Ajouté le:** {format_date(student['created_at'].split()[0])}")
    
    with col3:
        # Performance summary
        student_grades = st.session_state.grades[
            st.session_state.grades["student_id"] == student_id
        ]
        
        st.markdown("### 📊 Performance")
        
        if len(student_grades) > 0:
            average = round(student_grades["value"].mean(), 2)
            avg_color = (
                COLORS["success"] if average >= 14 
                else COLORS["warning"] if average >= 10 
                else COLORS["danger"]
            )
            
            st.markdown(
                f"<div style='background: {avg_color}; color: white; padding: 1rem; "
                f"border-radius: 10px; text-align: center;'>"
                f"<div style='font-size: 2rem; font-weight: bold;'>{average}/20</div>"
                f"<div>Moyenne générale</div>"
                f"</div>",
                unsafe_allow_html=True
            )
            
            st.markdown(f"**Notes enregistrées:** {len(student_grades)}")
            st.markdown(f"**Meilleure note:** {student_grades['value'].max()}/20")
            st.markdown(f"**Note la plus basse:** {student_grades['value'].min()}/20")
        else:
            st.info("Aucune note enregistrée")
    
    st.markdown("---")
    
    # Action buttons
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("✏️ Modifier", use_container_width=True):
            st.session_state.show_edit_form = True
            st.rerun()
    
    with col2:
        if student["is_active"]:
            if st.button("📦 Archiver", use_container_width=True):
                archive_student(student_id)
                st.success(f"✅ {student['first_name']} {student['last_name']} a été archivé")
                st.rerun()
        else:
            if st.button("♻️ Réactiver", use_container_width=True):
                activate_student(student_id)
                st.success(f"✅ {student['first_name']} {student['last_name']} a été réactivé")
                st.rerun()
    
    with col3:
        if st.button("📊 Voir Notes", use_container_width=True):
            st.info("Fonctionnalité à venir : Vue détaillée des notes")
    
    with col4:
        if st.button("📄 Générer Rapport", use_container_width=True):
            st.info("Fonctionnalité à venir : Génération de rapport")
    
    # Edit form if requested
    if st.session_state.show_edit_form:
        display_edit_form(student)
    
    # Recent grades section
    if len(student_grades) > 0:
        st.markdown("---")
        st.markdown("### 📈 Notes Récentes")
        
        recent_grades = student_grades.sort_values("evaluation_date", ascending=False).head(10)
        
        # Format for display
        display_df = recent_grades[
            ["evaluation_date", "subject", "competency_name", "value", "evaluation_type"]
        ].copy()
        display_df.columns = ["Date", "Matière", "Compétence", "Note", "Type"]
        display_df["Date"] = display_df["Date"].apply(format_date)
        
        st.dataframe(display_df, use_container_width=True, hide_index=True)


def display_add_form():
    """Display form to add new student"""
    st.markdown("---")
    st.markdown(
        f"<h3 style='color: {COLORS['primary']};'>➕ Ajouter un Nouvel Élève</h3>",
        unsafe_allow_html=True
    )
    
    with st.form("add_student_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            first_name = st.text_input("Prénom *", placeholder="Ex: Youssef")
            last_name = st.text_input("Nom *", placeholder="Ex: Alami")
            class_name = st.selectbox("Classe *", CLASSES)
            date_of_birth = st.date_input(
                "Date de naissance *",
                value=datetime(2010, 1, 1),
                min_value=datetime(2000, 1, 1),
                max_value=datetime.now()
            )
        
        with col2:
            parent_phone = st.text_input(
                "Téléphone parent *",
                placeholder="+212 6XX XXX XXX"
            )
            parent_email = st.text_input(
                "Email parent *",
                placeholder="parent@example.com"
            )
        
        col1, col2 = st.columns([1, 4])
        
        with col1:
            submitted = st.form_submit_button("✅ Ajouter", use_container_width=True)
        
        with col2:
            if st.form_submit_button("❌ Annuler", use_container_width=True):
                st.session_state.show_add_form = False
                st.rerun()
        
        if submitted:
            # Validation
            if not first_name or not last_name:
                st.error("❌ Le prénom et le nom sont obligatoires")
            elif not parent_phone or not parent_email:
                st.error("❌ Les coordonnées du parent sont obligatoires")
            else:
                # Create student data
                student_data = {
                    "first_name": first_name,
                    "last_name": last_name,
                    "class_name": class_name,
                    "date_of_birth": date_of_birth.strftime("%Y-%m-%d"),
                    "parent_phone": parent_phone,
                    "parent_email": parent_email
                }
                
                # Add student
                new_id = add_student(student_data)
                st.success(f"✅ Élève ajouté avec succès ! ID: {new_id}")
                st.session_state.show_add_form = False
                st.rerun()


def display_edit_form(student):
    """Display form to edit student information"""
    st.markdown("---")
    st.markdown(
        f"<h3 style='color: {COLORS['primary']};'>✏️ Modifier l'Élève</h3>",
        unsafe_allow_html=True
    )
    
    with st.form("edit_student_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            first_name = st.text_input("Prénom *", value=student["first_name"])
            last_name = st.text_input("Nom *", value=student["last_name"])
            class_name = st.selectbox(
                "Classe *",
                CLASSES,
                index=CLASSES.index(student["class_name"])
            )
            date_of_birth = st.date_input(
                "Date de naissance *",
                value=datetime.strptime(student["date_of_birth"], "%Y-%m-%d")
            )
        
        with col2:
            parent_phone = st.text_input("Téléphone parent *", value=student["parent_phone"])
            parent_email = st.text_input("Email parent *", value=student["parent_email"])
        
        col1, col2 = st.columns([1, 4])
        
        with col1:
            submitted = st.form_submit_button("✅ Enregistrer", use_container_width=True)
        
        with col2:
            if st.form_submit_button("❌ Annuler", use_container_width=True):
                st.session_state.show_edit_form = False
                st.rerun()
        
        if submitted:
            # Validation
            if not first_name or not last_name:
                st.error("❌ Le prénom et le nom sont obligatoires")
            elif not parent_phone or not parent_email:
                st.error("❌ Les coordonnées du parent sont obligatoires")
            else:
                # Update student data
                updated_data = {
                    "first_name": first_name,
                    "last_name": last_name,
                    "class_name": class_name,
                    "date_of_birth": date_of_birth.strftime("%Y-%m-%d"),
                    "parent_phone": parent_phone,
                    "parent_email": parent_email
                }
                
                # Update student
                update_student(student["id"], updated_data)
                st.success("✅ Élève modifié avec succès !")
                st.session_state.show_edit_form = False
                st.rerun()


def display_csv_import():
    """Display CSV import section"""
    with st.expander("📥 Importer des Élèves depuis CSV", expanded=False):
        st.markdown("""
        **Format CSV requis:**
        - `first_name` : Prénom de l'élève
        - `last_name` : Nom de l'élève
        - `class_name` : Classe (doit correspondre aux classes existantes)
        - `date_of_birth` : Date de naissance (format YYYY-MM-DD)
        - `parent_phone` : Téléphone du parent
        - `parent_email` : Email du parent
        """)
        
        # Sample CSV download
        sample_data = pd.DataFrame({
            "first_name": ["Youssef", "Fatima"],
            "last_name": ["Alami", "Benali"],
            "class_name": ["1ère année collège", "2ème année collège"],
            "date_of_birth": ["2010-05-15", "2009-08-22"],
            "parent_phone": ["+212 6XX XXX XXX", "+212 6YY YYY YYY"],
            "parent_email": ["youssef.parent@example.com", "fatima.parent@example.com"]
        })
        
        csv_buffer = io.StringIO()
        sample_data.to_csv(csv_buffer, index=False)
        csv_str = csv_buffer.getvalue()
        
        st.download_button(
            label="📄 Télécharger un modèle CSV",
            data=csv_str,
            file_name="modele_eleves.csv",
            mime="text/csv"
        )
        
        st.markdown("---")
        
        # File upload
        uploaded_file = st.file_uploader(
            "Choisir un fichier CSV",
            type=["csv"],
            help="Sélectionnez un fichier CSV au format requis"
        )
        
        if uploaded_file is not None:
            students_df, error = parse_csv_students(uploaded_file)
            
            if error:
                st.error(f"❌ {error}")
            else:
                st.success(f"✅ Fichier valide : {len(students_df)} élève(s) trouvé(s)")
                
                # Preview
                st.markdown("**Aperçu des données:**")
                st.dataframe(students_df, use_container_width=True)
                
                # Import button
                if st.button("📥 Importer ces élèves", type="primary"):
                    count = import_students_from_csv(students_df)
                    st.success(f"✅ {count} élève(s) importé(s) avec succès !")
                    st.rerun()


def main():
    """Main function"""
    # Initialize session state
    initialize_session_state()
    
    # Header
    st.markdown(
        create_header("👥 Gestion des Élèves", "Consulter, ajouter et gérer les élèves"),
        unsafe_allow_html=True
    )
    
    # If viewing student detail
    if st.session_state.selected_student_id:
        display_student_detail_view(st.session_state.selected_student_id)
        return
    
    # Main view - List of students
    st.markdown("---")
    
    # Search and filter section
    col1, col2, col3 = st.columns([3, 2, 1])
    
    with col1:
        search_term = st.text_input(
            "🔍 Rechercher un élève",
            placeholder="Rechercher par nom ou prénom...",
            label_visibility="collapsed"
        )
    
    with col2:
        # Get unique classes
        all_classes = ["Toutes les classes"] + sorted(
            st.session_state.students["class_name"].unique().tolist()
        )
        class_filter = st.selectbox(
            "Filtrer par classe",
            all_classes,
            label_visibility="collapsed"
        )
    
    with col3:
        status_options = {
            "Actifs": "active",
            "Archivés": "inactive",
            "Tous": "all"
        }
        status_label = st.selectbox(
            "Statut",
            list(status_options.keys()),
            label_visibility="collapsed"
        )
        status_filter = status_options[status_label]
    
    # Action buttons
    col1, col2, col3 = st.columns([2, 2, 2])
    
    with col1:
        if st.button("➕ Ajouter un Élève", use_container_width=True, type="primary"):
            st.session_state.show_add_form = True
            st.rerun()
    
    with col2:
        # Export button
        csv_data = st.session_state.students.to_csv(index=False)
        st.download_button(
            label="📤 Exporter CSV",
            data=csv_data,
            file_name=f"eleves_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv",
            use_container_width=True
        )
    
    with col3:
        # Statistics button
        if st.button("📊 Statistiques", use_container_width=True):
            st.info("Fonctionnalité à venir : Statistiques détaillées")
    
    # Add student form
    if st.session_state.show_add_form:
        display_add_form()
    
    # CSV Import section
    display_csv_import()
    
    st.markdown("---")
    
    # Filter students
    filtered_students = filter_students(
        st.session_state.students,
        search_term=search_term,
        class_filter=class_filter if class_filter != "Toutes les classes" else None,
        status_filter=status_filter
    )
    
    # Display stats
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_students = len(st.session_state.students[st.session_state.students["is_active"]])
        st.metric("Total Élèves", total_students)
    
    with col2:
        total_classes = len(st.session_state.students["class_name"].unique())
        st.metric("Classes", total_classes)
    
    with col3:
        archived_count = len(st.session_state.students[~st.session_state.students["is_active"]])
        st.metric("Archivés", archived_count)
    
    with col4:
        filtered_count = len(filtered_students)
        st.metric("Résultats", filtered_count)
    
    st.markdown("---")
    
    # Display student list
    display_student_list_view(filtered_students)


if __name__ == "__main__":
    main()
