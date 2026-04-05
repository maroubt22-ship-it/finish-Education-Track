# frontend/gradio/app.py
"""
EduTrack IA - Gradio AI Demo Interface
Interactive demonstration of AI-powered report generation and competency classification
"""

import gradio as gr
import pandas as pd
import random
from datetime import datetime

# Sample data for demo
SAMPLE_STUDENTS = [
    "Youssef Alami", "Fatima Benali", "Mohamed Chakir", "Aisha Dahbi",
    "Hassan El Fassi", "Zineb Fahmi", "Omar Ghazi", "Salma Hilal"
]

SAMPLE_COMPETENCIES = [
    "Algèbre - Résolution d'équations",
    "Géométrie - Théorèmes",
    "Analyse - Dérivées",
    "Statistiques et probabilités",
    "Compréhension de texte",
    "Expression écrite",
    "Grammaire et conjugaison"
]


def classify_competency(grade_value):
    """
    Classify a grade into competency level
    
    Args:
        grade_value: Grade value (0-20)
    
    Returns:
        Classification text with emoji, explanation, and recommendations
    """
    try:
        grade = float(grade_value)
        
        if grade < 0 or grade > 20:
            return "❌ Erreur : La note doit être entre 0 et 20"
        
        if grade >= 14:
            level = "🟢 MAÎTRISÉE"
            color = "#10B981"
            explanation = f"Excellente performance ! La note de {grade:.1f}/20 indique une maîtrise solide de cette compétence."
            recommendations = """
**Recommandations :**
✓ Continuer sur cette excellente lancée
✓ Approfondir avec des exercices avancés
✓ Partager les bonnes pratiques avec les camarades
✓ Viser l'excellence en perfectionnant les détails
            """
        elif grade >= 10:
            level = "🟡 EN COURS D'ACQUISITION"
            color = "#F59E0B"
            explanation = f"Bon travail ! La note de {grade:.1f}/20 montre que la compétence est en cours d'acquisition avec des bases solides."
            recommendations = """
**Recommandations :**
• Réviser régulièrement les concepts fondamentaux
• Pratiquer davantage d'exercices variés
• Identifier et combler les lacunes spécifiques
• Demander de l'aide sur les points difficiles
            """
        else:
            level = "🔴 À RENFORCER"
            color = "#EF4444"
            explanation = f"Attention requise. La note de {grade:.1f}/20 indique que cette compétence nécessite un renforcement important."
            recommendations = """
**Recommandations urgentes :**
⚠ Revoir les bases avec l'enseignant
⚠ Prévoir des séances de soutien supplémentaires
⚠ Utiliser des ressources pédagogiques adaptées
⚠ Mettre en place un plan de remédiation personnalisé
            """
        
        result = f"""
# {level}

## 📊 Analyse de la note : {grade:.1f}/20

{explanation}

{recommendations}

---
**Système de classification EduTrack IA :**
- 🟢 Maîtrisée : ≥ 14/20
- 🟡 En cours : 10-14/20
- 🔴 À renforcer : < 10/20
        """
        
        return result
        
    except ValueError:
        return "❌ Erreur : Veuillez entrer un nombre valide entre 0 et 20"


def generate_report(student_name, math_grade, physics_grade, french_grade, 
                   behavior_obs, progress_obs, difficulty_obs):
    """
    Generate AI-powered student progress report
    
    Args:
        student_name: Student's name
        math_grade, physics_grade, french_grade: Recent grades
        behavior_obs, progress_obs, difficulty_obs: Teacher observations
    
    Returns:
        Formatted report text
    """
    try:
        # Parse grades
        math = float(math_grade) if math_grade else 0
        physics = float(physics_grade) if physics_grade else 0
        french = float(french_grade) if french_grade else 0
        
        # Calculate average
        grades = [g for g in [math, physics, french] if g > 0]
        average = sum(grades) / len(grades) if grades else 0
        
        # Determine overall level
        if average >= 14:
            overall_emoji = "🟢"
            overall_level = "Excellent niveau général"
            overall_comment = "L'élève démontre une excellente maîtrise des compétences travaillées."
        elif average >= 10:
            overall_emoji = "🟡"
            overall_level = "Bon niveau avec axes d'amélioration"
            overall_comment = "L'élève progresse de manière satisfaisante avec quelques points à consolider."
        else:
            overall_emoji = "🔴"
            overall_level = "Renforcement nécessaire"
            overall_comment = "L'élève nécessite un accompagnement renforcé pour progresser."
        
        # Generate competencies section
        competencies_text = "**Compétences évaluées :**\n"
        if math > 0:
            comp_emoji = "🟢" if math >= 14 else "🟡" if math >= 10 else "🔴"
            competencies_text += f"- {comp_emoji} Mathématiques : {math:.1f}/20\n"
        if physics > 0:
            comp_emoji = "🟢" if physics >= 14 else "🟡" if physics >= 10 else "🔴"
            competencies_text += f"- {comp_emoji} Physique-Chimie : {physics:.1f}/20\n"
        if french > 0:
            comp_emoji = "🟢" if french >= 14 else "🟡" if french >= 10 else "🔴"
            competencies_text += f"- {comp_emoji} Français : {french:.1f}/20\n"
        
        # Generate progress section
        progress_text = ""
        if average >= 14:
            progress_text = f"Excellente progression constatée avec une moyenne de {average:.1f}/20. L'élève assimile bien les concepts et fait preuve de rigueur dans son travail."
        elif average >= 10:
            progress_text = f"Progression satisfaisante avec une moyenne de {average:.1f}/20. L'élève consolide ses acquis régulièrement et montre de la motivation."
        else:
            progress_text = f"Des difficultés persistent avec une moyenne de {average:.1f}/20. Un soutien personnalisé est recommandé pour renforcer les bases."
        
        if progress_obs:
            progress_text += f"\n\n*Note de l'enseignant :* {progress_obs}"
        
        # Generate areas to improve
        weak_subjects = []
        if math > 0 and math < 10:
            weak_subjects.append("Mathématiques")
        if physics > 0 and physics < 10:
            weak_subjects.append("Physique-Chimie")
        if french > 0 and french < 10:
            weak_subjects.append("Français")
        
        improve_text = ""
        if weak_subjects:
            improve_text = f"Renforcement nécessaire en : {', '.join(weak_subjects)}\n"
            improve_text += "• Revoir les concepts fondamentaux\n"
            improve_text += "• Pratiquer régulièrement des exercices\n"
            improve_text += "• Solliciter l'aide de l'enseignant si besoin\n"
        else:
            improve_text = "Continuer les efforts actuels pour maintenir ce bon niveau.\n"
            improve_text += "• Approfondir les sujets avancés\n"
            improve_text += "• Développer l'autonomie dans le travail\n"
        
        if difficulty_obs:
            improve_text += f"\n*Note de l'enseignant :* {difficulty_obs}"
        
        # Generate recommendations
        recommendations = ""
        if average >= 14:
            recommendations = "• Continuer sur cette excellente lancée\n"
            recommendations += "• Explorer des sujets plus avancés\n"
            recommendations += "• Développer l'esprit critique et la créativité\n"
        elif average >= 10:
            recommendations = "• Réviser régulièrement pour consolider les acquis\n"
            recommendations += "• Pratiquer davantage d'exercices variés\n"
            recommendations += "• Participer activement en classe\n"
        else:
            recommendations = "• Prévoir des séances de soutien supplémentaires\n"
            recommendations += "• Revoir les bases avec attention\n"
            recommendations += "• Mettre en place un suivi personnalisé\n"
            recommendations += "• Encourager la motivation et la confiance\n"
        
        # Build final report
        report = f"""
# 📋 RAPPORT DE PROGRESSION — {student_name}

**Date :** {datetime.now().strftime('%d/%m/%Y')}  
**Moyenne générale :** {overall_emoji} {average:.1f}/20  
**Bilan :** {overall_level}

---

## 1️⃣ COMPÉTENCES TRAVAILLÉES

{competencies_text}

{overall_comment}

---

## 2️⃣ PROGRÈS RÉALISÉS

{progress_text}

---

## 3️⃣ POINTS À AMÉLIORER

{improve_text}

---

## 4️⃣ OBSERVATIONS DE L'ENSEIGNANT

**Comportement :** {behavior_obs if behavior_obs else "Aucune observation particulière."}

---

## 5️⃣ RECOMMANDATIONS

{recommendations}

---

*Rapport généré automatiquement par EduTrack IA - Intelligence Artificielle Pédagogique*
        """
        
        return report.strip()
        
    except ValueError as e:
        return f"❌ Erreur dans la génération du rapport : {str(e)}\nVeuillez vérifier que les notes sont des nombres valides entre 0 et 20."


# Create Gradio interface for report generation
with gr.Blocks(title="EduTrack IA - Démo IA", theme=gr.themes.Soft()) as demo_report:
    gr.Markdown("""
    # 🤖 EduTrack IA - Génération Automatique de Rapports
    ## Démonstration de l'Intelligence Artificielle Pédagogique
    
    Cette interface démontre comment l'IA peut générer automatiquement des rapports de progression 
    personnalisés pour les élèves en fonction de leurs notes et des observations de l'enseignant.
    """)
    
    with gr.Row():
        with gr.Column():
            gr.Markdown("### 📝 Informations de l'Élève")
            
            student_name_input = gr.Dropdown(
                choices=SAMPLE_STUDENTS,
                label="Nom de l'élève",
                value=SAMPLE_STUDENTS[0],
                allow_custom_value=True
            )
            
            gr.Markdown("### 📊 Notes Récentes")
            
            math_input = gr.Slider(
                minimum=0, maximum=20, step=0.5, value=12.5,
                label="Mathématiques (/20)"
            )
            
            physics_input = gr.Slider(
                minimum=0, maximum=20, step=0.5, value=14.0,
                label="Physique-Chimie (/20)"
            )
            
            french_input = gr.Slider(
                minimum=0, maximum=20, step=0.5, value=11.0,
                label="Français (/20)"
            )
            
            gr.Markdown("### ✍️ Observations Enseignant")
            
            behavior_input = gr.Textbox(
                label="Comportement",
                placeholder="Ex: Élève attentif et participatif",
                lines=2
            )
            
            progress_input = gr.Textbox(
                label="Progrès constatés",
                placeholder="Ex: Amélioration notable en résolution de problèmes",
                lines=2
            )
            
            difficulty_input = gr.Textbox(
                label="Difficultés rencontrées",
                placeholder="Ex: Besoin de renforcement sur les équations",
                lines=2
            )
            
            generate_btn = gr.Button("📋 Générer le Rapport", variant="primary", size="lg")
        
        with gr.Column():
            gr.Markdown("### 📄 Rapport Généré")
            report_output = gr.Markdown(label="Rapport de progression")
    
    generate_btn.click(
        fn=generate_report,
        inputs=[student_name_input, math_input, physics_input, french_input,
                behavior_input, progress_input, difficulty_input],
        outputs=report_output
    )
    
    # Examples
    gr.Examples(
        examples=[
            ["Youssef Alami", 16.5, 17.0, 15.5, "Excellent élève, très motivé", "Progrès remarquables", ""],
            ["Fatima Benali", 12.0, 10.5, 13.0, "Bonne participation", "Amélioration constante", "Difficulté en physique"],
            ["Omar Ghazi", 8.5, 9.0, 7.5, "Manque de concentration", "", "Lacunes importantes à combler"]
        ],
        inputs=[student_name_input, math_input, physics_input, french_input,
                behavior_input, progress_input, difficulty_input]
    )

# Create Gradio interface for competency classification
with gr.Blocks(title="EduTrack IA - Classification", theme=gr.themes.Soft()) as demo_classifier:
    gr.Markdown("""
    # 🎯 EduTrack IA - Classification des Compétences
    ## Analyse Automatique du Niveau de Maîtrise
    
    Cette interface démontre la classification automatique des compétences en fonction des notes obtenues.
    Le système utilise le référentiel pédagogique marocain (échelle 0-20).
    """)
    
    with gr.Row():
        with gr.Column():
            grade_input = gr.Slider(
                minimum=0, maximum=20, step=0.5, value=12.0,
                label="Note obtenue (/20)"
            )
            
            classify_btn = gr.Button("🔍 Classifier la Compétence", variant="primary", size="lg")
            
            gr.Markdown("""
            ### 📚 Exemples de notes
            - **18/20** : Excellence - Compétence maîtrisée
            - **12/20** : Satisfaisant - En cours d'acquisition
            - **7/20** : Insuffisant - À renforcer
            """)
        
        with gr.Column():
            classification_output = gr.Markdown(label="Résultat de la classification")
    
    classify_btn.click(
        fn=classify_competency,
        inputs=grade_input,
        outputs=classification_output
    )
    
    # Examples
    gr.Examples(
        examples=[[18.5], [12.0], [7.5], [14.0], [9.5], [16.0]],
        inputs=grade_input
    )

# Combine both interfaces in tabs
demo = gr.TabbedInterface(
    [demo_report, demo_classifier],
    ["📋 Génération de Rapports", "🎯 Classification de Compétences"],
    title="EduTrack IA - Démonstration Intelligence Artificielle"
)

if __name__ == "__main__":
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,
        show_error=True
    )
