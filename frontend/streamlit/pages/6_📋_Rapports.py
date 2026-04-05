"""
Page de génération des rapports pour EduTrack IA
"""
import streamlit as st
from datetime import datetime, timedelta
from frontend.shared.styles.theme import apply_theme, get_colors
from frontend.streamlit.components.report_preview import render_report_preview
from frontend.streamlit.utils.helpers import generate_report_text


def main():
    """Page principale de génération des rapports"""
    st.set_page_config(
        page_title="Rapports - EduTrack IA",
        page_icon="📋",
        layout="wide"
    )
    
    # Appliquer le thème
    apply_theme()
    colors = get_colors()
    
    # En-tête
    st.title("📋 Génération de Rapports")
    st.markdown("""
    <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                padding: 1.5rem; border-radius: 10px; color: white; margin-bottom: 2rem;'>
        <h3 style='margin: 0; color: white;'>Créez des rapports détaillés pour vos élèves</h3>
        <p style='margin: 0.5rem 0 0 0; opacity: 0.9;'>
            Générez des rapports complets incluant les progrès, observations et recommandations
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Layout en colonnes
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown(f"""
        <div style='background: {colors["surface"]}; padding: 1.5rem; 
                    border-radius: 10px; margin-bottom: 1rem;'>
            <h3 style='color: {colors["primary"]}; margin-top: 0;'>
                🎯 Générateur de Rapport
            </h3>
        </div>
        """, unsafe_allow_html=True)
        
        # Formulaire de génération
        with st.form("report_generator"):
            # Sélection de l'élève
            students = [
                "Sophie Martin",
                "Lucas Dubois",
                "Emma Bernard",
                "Noah Petit",
                "Léa Rousseau",
                "Louis Garcia"
            ]
            selected_student = st.selectbox(
                "👤 Sélectionner un élève",
                students,
                help="Choisissez l'élève pour lequel générer le rapport"
            )
            
            # Période du rapport
            st.markdown("📅 **Période du rapport**")
            col_date1, col_date2 = st.columns(2)
            
            with col_date1:
                start_date = st.date_input(
                    "Date de début",
                    value=datetime.now() - timedelta(days=30),
                    max_value=datetime.now()
                )
            
            with col_date2:
                end_date = st.date_input(
                    "Date de fin",
                    value=datetime.now(),
                    max_value=datetime.now()
                )
            
            # Type de rapport
            report_type = st.selectbox(
                "📑 Type de rapport",
                ["Rapport mensuel complet", "Rapport bimensuel", "Rapport trimestriel"],
                help="Sélectionnez le type de rapport à générer"
            )
            
            # Inclure les sections
            st.markdown("**Sections à inclure**")
            col_opt1, col_opt2 = st.columns(2)
            
            with col_opt1:
                include_competencies = st.checkbox("Compétences", value=True)
                include_observations = st.checkbox("Observations", value=True)
            
            with col_opt2:
                include_recommendations = st.checkbox("Recommandations", value=True)
                include_stats = st.checkbox("Statistiques", value=True)
            
            # Bouton de génération
            generate_button = st.form_submit_button(
                "🔄 Générer le rapport",
                use_container_width=True,
                type="primary"
            )
        
        # Traitement de la génération
        if generate_button:
            with st.spinner("Génération du rapport en cours..."):
                # Simuler un délai de traitement
                import time
                time.sleep(1)
                
                # Stocker les informations dans la session
                st.session_state.report_generated = True
                st.session_state.report_student = selected_student
                st.session_state.report_start_date = start_date
                st.session_state.report_end_date = end_date
                st.session_state.report_type = report_type
                st.session_state.include_sections = {
                    "competencies": include_competencies,
                    "observations": include_observations,
                    "recommendations": include_recommendations,
                    "stats": include_stats
                }
                
                st.success("✅ Rapport généré avec succès !")
    
    with col2:
        st.markdown(f"""
        <div style='background: {colors["surface"]}; padding: 1.5rem; 
                    border-radius: 10px; margin-bottom: 1rem;'>
            <h3 style='color: {colors["primary"]}; margin-top: 0;'>
                👁️ Aperçu du Rapport
            </h3>
        </div>
        """, unsafe_allow_html=True)
        
        # Aperçu du rapport
        if st.session_state.get("report_generated", False):
            student = st.session_state.report_student
            start = st.session_state.report_start_date
            end = st.session_state.report_end_date
            
            # Données simulées pour l'aperçu
            student_summary = {
                "name": student,
                "period": f"{start.strftime('%d/%m/%Y')} - {end.strftime('%d/%m/%Y')}",
                "total_evaluations": 8,
                "average_score": 85.5
            }
            
            observations = [
                {
                    "date": "2024-01-15",
                    "type": "Progrès",
                    "content": "Excellente participation en classe. Montre un intérêt marqué pour les mathématiques."
                },
                {
                    "date": "2024-01-22",
                    "type": "Point d'attention",
                    "content": "Pourrait améliorer la qualité de la rédaction dans les devoirs écrits."
                }
            ]
            
            competency_stats = {
                "Mathématiques": {"score": 88, "trend": "up"},
                "Français": {"score": 82, "trend": "stable"},
                "Sciences": {"score": 90, "trend": "up"},
                "Histoire": {"score": 78, "trend": "down"}
            }
            
            # Générer le texte du rapport
            report_text = generate_report_text(
                student_summary,
                observations,
                competency_stats
            )
            
            # Afficher l'aperçu du rapport
            render_report_preview(report_text, student_summary)
            
            # Actions sur le rapport
            st.markdown("---")
            st.markdown("**📤 Actions**")
            
            col_action1, col_action2 = st.columns(2)
            
            with col_action1:
                # Bouton d'export PDF
                pdf_data = report_text.encode()
                st.download_button(
                    label="📥 Télécharger PDF",
                    data=pdf_data,
                    file_name=f"rapport_{student.replace(' ', '_')}_{start.strftime('%Y%m%d')}.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )
            
            with col_action2:
                # Bouton d'envoi WhatsApp
                if st.button("📱 Envoyer via WhatsApp", use_container_width=True):
                    st.success("✅ Rapport envoyé avec succès via WhatsApp !")
                    st.info(f"📲 Message envoyé au tuteur de {student}")
        
        else:
            st.info("👆 Remplissez le formulaire et cliquez sur 'Générer le rapport' pour voir l'aperçu")
    
    # Section des rapports récents
    st.markdown("---")
    st.markdown(f"""
    <div style='background: {colors["surface"]}; padding: 1.5rem; 
                border-radius: 10px; margin-top: 2rem;'>
        <h3 style='color: {colors["primary"]}; margin-top: 0;'>
            📚 Rapports Récents
        </h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Liste des rapports récents
    recent_reports = [
        {
            "student": "Sophie Martin",
            "date": "2024-01-20",
            "type": "Rapport mensuel",
            "status": "Envoyé",
            "score": 87.5
        },
        {
            "student": "Lucas Dubois",
            "date": "2024-01-18",
            "type": "Rapport bimensuel",
            "status": "En attente",
            "score": 82.0
        },
        {
            "student": "Emma Bernard",
            "date": "2024-01-15",
            "type": "Rapport mensuel",
            "status": "Envoyé",
            "score": 91.3
        },
        {
            "student": "Noah Petit",
            "date": "2024-01-12",
            "type": "Rapport mensuel",
            "status": "Envoyé",
            "score": 78.5
        },
        {
            "student": "Léa Rousseau",
            "date": "2024-01-10",
            "type": "Rapport trimestriel",
            "status": "Envoyé",
            "score": 89.2
        }
    ]
    
    # Afficher les rapports dans un tableau stylisé
    for i, report in enumerate(recent_reports):
        status_color = "#4ade80" if report["status"] == "Envoyé" else "#fbbf24"
        status_icon = "✓" if report["status"] == "Envoyé" else "⏳"
        
        score_color = "#4ade80" if report["score"] >= 85 else "#fbbf24" if report["score"] >= 70 else "#f87171"
        
        st.markdown(f"""
        <div style='background: {colors["surface"]}; padding: 1rem; 
                    border-radius: 8px; margin-bottom: 0.5rem;
                    border-left: 4px solid {colors["primary"]};'>
            <div style='display: flex; justify-content: space-between; align-items: center;'>
                <div style='flex: 1;'>
                    <strong style='color: {colors["text_primary"]}; font-size: 1.1em;'>
                        {report["student"]}
                    </strong>
                    <div style='color: {colors["text_secondary"]}; font-size: 0.9em; margin-top: 0.2rem;'>
                        📅 {report["date"]} • {report["type"]}
                    </div>
                </div>
                <div style='text-align: right;'>
                    <div style='background: {status_color}; color: white; 
                                padding: 0.3rem 0.8rem; border-radius: 15px;
                                display: inline-block; font-size: 0.85em; margin-bottom: 0.3rem;'>
                        {status_icon} {report["status"]}
                    </div>
                    <div style='color: {score_color}; font-weight: bold; font-size: 1.2em;'>
                        {report["score"]}%
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Actions pour chaque rapport
        col_r1, col_r2, col_r3, col_r4 = st.columns([1, 1, 1, 1])
        
        with col_r1:
            if st.button("👁️ Voir", key=f"view_{i}", use_container_width=True):
                st.info(f"Affichage du rapport de {report['student']}")
        
        with col_r2:
            st.download_button(
                label="📥 PDF",
                data=f"Rapport pour {report['student']}".encode(),
                file_name=f"rapport_{report['student'].replace(' ', '_')}.pdf",
                mime="application/pdf",
                key=f"download_{i}",
                use_container_width=True
            )
        
        with col_r3:
            if st.button("📱 WhatsApp", key=f"whatsapp_{i}", use_container_width=True):
                st.success(f"Envoyé à {report['student']} !")
        
        with col_r4:
            if st.button("✏️ Modifier", key=f"edit_{i}", use_container_width=True):
                st.info(f"Modification du rapport de {report['student']}")
        
        st.markdown("<br>", unsafe_allow_html=True)
    
    # Statistiques des rapports
    st.markdown("---")
    st.markdown("### 📊 Statistiques des Rapports")
    
    col_stat1, col_stat2, col_stat3, col_stat4 = st.columns(4)
    
    with col_stat1:
        st.metric(
            label="Rapports ce mois",
            value="15",
            delta="3"
        )
    
    with col_stat2:
        st.metric(
            label="Rapports envoyés",
            value="12",
            delta="2"
        )
    
    with col_stat3:
        st.metric(
            label="Moyenne générale",
            value="85.2%",
            delta="1.5%"
        )
    
    with col_stat4:
        st.metric(
            label="Taux d'envoi",
            value="80%",
            delta="-5%"
        )


if __name__ == "__main__":
    main()
