# frontend/streamlit/components/report_preview.py
"""
Report preview component for displaying generated reports
"""

import streamlit as st
from frontend.shared.styles.theme import COLORS, format_report_section


def display_report_preview(report_text, title="Aperçu du Rapport"):
    """
    Display formatted report preview
    
    Args:
        report_text: Report text content
        title: Preview title
    """
    st.markdown(f"### 📄 {title}")
    
    report_html = f"""
    <div class="report-preview" style="background-color: #F9FAFB; 
                                       padding: 2rem; 
                                       border-radius: 10px; 
                                       border: 2px solid #E5E7EB;
                                       font-family: 'Georgia', serif;
                                       line-height: 1.8;
                                       margin: 1rem 0;">
        <pre style="white-space: pre-wrap; 
                    font-family: 'Georgia', serif; 
                    font-size: 0.95rem;
                    color: #1F2937;
                    margin: 0;">{report_text}</pre>
    </div>
    """
    
    st.markdown(report_html, unsafe_allow_html=True)


def display_structured_report(report_data):
    """
    Display report with structured sections
    
    Args:
        report_data: Dictionary with report sections
            {
                'header': {...},
                'competencies': [...],
                'progress': str,
                'improvements': str,
                'observations': [...],
                'recommendations': [...]
            }
    """
    # Header
    header = report_data.get('header', {})
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, {COLORS['primary']} 0%, {COLORS['info']} 100%);
                padding: 2rem; border-radius: 10px; color: white; text-align: center;">
        <h2 style="margin: 0;">📋 RAPPORT DE PROGRESSION</h2>
        <h3 style="margin: 0.5rem 0;">{header.get('student_name', 'Élève')}</h3>
        <p style="margin: 0;">Date : {header.get('date', '')} • Classe : {header.get('class', '')}</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Section 1: Competencies
    st.markdown("#### 1️⃣ COMPÉTENCES TRAVAILLÉES")
    competencies = report_data.get('competencies', [])
    if competencies:
        for comp in competencies:
            st.markdown(f"- **{comp.get('name', '')}** ({comp.get('subject', '')}) - Moyenne: {comp.get('average', 0)}/20")
    else:
        st.info("Aucune compétence évaluée pour cette période.")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Section 2: Progress
    st.markdown("#### 2️⃣ PROGRÈS RÉALISÉS")
    progress_text = report_data.get('progress', 'Aucun commentaire.')
    st.markdown(progress_text)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Section 3: Areas to improve
    st.markdown("#### 3️⃣ POINTS À AMÉLIORER")
    improvements_text = report_data.get('improvements', 'Continuer les efforts actuels.')
    st.markdown(improvements_text)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Section 4: Observations
    st.markdown("#### 4️⃣ OBSERVATIONS DE L'ENSEIGNANT")
    observations = report_data.get('observations', [])
    if observations:
        for obs in observations:
            category_icon = {"comportement": "👤", "progrès": "📈", "difficulté": "⚠️"}.get(obs.get('category', ''), "•")
            st.markdown(f"{category_icon} {obs.get('content', '')}")
    else:
        st.info("Aucune observation particulière.")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Section 5: Recommendations
    st.markdown("#### 5️⃣ RECOMMANDATIONS")
    recommendations = report_data.get('recommendations', [])
    if recommendations:
        for rec in recommendations:
            st.markdown(f"✓ {rec}")
    else:
        st.markdown("- Continuer sur cette lancée")


def display_report_card(report_summary):
    """
    Display compact report card with summary
    
    Args:
        report_summary: Dictionary with report summary info
    """
    card_html = f"""
    <div style="background: white; 
                padding: 1.5rem; 
                border-radius: 10px; 
                box-shadow: 0 2px 8px rgba(0,0,0,0.1);
                border-left: 4px solid {COLORS['primary']};
                margin: 1rem 0;">
        <div style="display: flex; justify-content: space-between; align-items: start;">
            <div style="flex: 1;">
                <h4 style="margin: 0; color: {COLORS['dark']};">
                    📋 {report_summary.get('student_name', 'Rapport')}
                </h4>
                <p style="color: #6B7280; margin: 0.5rem 0; font-size: 0.9rem;">
                    📅 {report_summary.get('date', '')}
                </p>
                <p style="color: #6B7280; margin: 0.25rem 0; font-size: 0.9rem;">
                    📚 {report_summary.get('period', '')}
                </p>
            </div>
            <div style="text-align: right;">
                <span style="background: {COLORS['success']}; 
                           color: white; 
                           padding: 0.5rem 1rem; 
                           border-radius: 20px;
                           font-size: 0.85rem;
                           font-weight: 600;">
                    {report_summary.get('status', 'Généré')}
                </span>
            </div>
        </div>
    </div>
    """
    
    st.markdown(card_html, unsafe_allow_html=True)


def create_pdf_report_html(report_text):
    """
    Create HTML template for PDF generation
    
    Args:
        report_text: Report text content
    
    Returns:
        HTML string for PDF conversion
    """
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            body {{
                font-family: 'Georgia', serif;
                line-height: 1.8;
                color: #1F2937;
                max-width: 800px;
                margin: 0 auto;
                padding: 2rem;
            }}
            h1, h2 {{
                color: {COLORS['primary']};
                border-bottom: 2px solid {COLORS['primary']};
                padding-bottom: 0.5rem;
            }}
            .header {{
                background: {COLORS['primary']};
                color: white;
                padding: 2rem;
                text-align: center;
                border-radius: 10px;
                margin-bottom: 2rem;
            }}
            .section {{
                margin-bottom: 2rem;
            }}
            .section-title {{
                color: {COLORS['primary']};
                font-size: 1.2rem;
                font-weight: bold;
                margin-bottom: 0.5rem;
                border-bottom: 2px solid {COLORS['primary']};
                padding-bottom: 0.3rem;
            }}
            pre {{
                white-space: pre-wrap;
                font-family: 'Georgia', serif;
            }}
        </style>
    </head>
    <body>
        <pre>{report_text}</pre>
    </body>
    </html>
    """
    return html
