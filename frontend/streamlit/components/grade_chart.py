# frontend/streamlit/components/grade_chart.py
"""
Grade chart component for visualizing student progress
"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from frontend.shared.styles.theme import COLORS, get_grade_color


def display_grade_evolution(grades_df, student_name=""):
    """
    Display grade evolution line chart
    
    Args:
        grades_df: DataFrame with grades (must have 'evaluation_date' and 'value' columns)
        student_name: Optional student name for title
    """
    if len(grades_df) == 0:
        st.info("Aucune note disponible pour afficher l'évolution.")
        return
    
    # Sort by date
    grades_sorted = grades_df.sort_values('evaluation_date')
    grades_sorted['evaluation_date'] = pd.to_datetime(grades_sorted['evaluation_date'])
    
    # Create Plotly chart
    fig = go.Figure()
    
    # Add grade line
    fig.add_trace(go.Scatter(
        x=grades_sorted['evaluation_date'],
        y=grades_sorted['value'],
        mode='lines+markers',
        name='Notes',
        line=dict(color=COLORS['primary'], width=2),
        marker=dict(size=8, color=COLORS['primary'])
    ))
    
    # Add threshold lines
    fig.add_hline(y=14, line_dash="dash", line_color=COLORS['success'], 
                  annotation_text="Maîtrisée (14)", annotation_position="right")
    fig.add_hline(y=10, line_dash="dash", line_color=COLORS['warning'], 
                  annotation_text="En cours (10)", annotation_position="right")
    
    # Update layout
    title_text = f"Évolution des notes - {student_name}" if student_name else "Évolution des notes"
    fig.update_layout(
        title=title_text,
        xaxis_title="Date d'évaluation",
        yaxis_title="Note (/20)",
        yaxis=dict(range=[0, 20]),
        hovermode='x unified',
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)


def display_grade_distribution(grades_df):
    """
    Display grade distribution histogram
    
    Args:
        grades_df: DataFrame with grades
    """
    if len(grades_df) == 0:
        st.info("Aucune note disponible.")
        return
    
    fig, ax = plt.subplots(figsize=(10, 5))
    
    # Create histogram
    n, bins, patches = ax.hist(grades_df['value'], bins=[0, 5, 10, 14, 20], 
                                edgecolor='white', linewidth=1.5)
    
    # Color bars based on classification
    colors = [COLORS['danger'], COLORS['danger'], COLORS['warning'], COLORS['success']]
    for patch, color in zip(patches, colors):
        patch.set_facecolor(color)
    
    ax.set_xlabel('Note (/20)', fontsize=12)
    ax.set_ylabel('Nombre de notes', fontsize=12)
    ax.set_title('Distribution des notes', fontsize=14, fontweight='bold')
    ax.grid(axis='y', alpha=0.3)
    
    # Add labels
    ax.set_xticks([2.5, 7.5, 12, 17])
    ax.set_xticklabels(['0-5\n(Très faible)', '5-10\n(À renforcer)', 
                        '10-14\n(En cours)', '14-20\n(Maîtrisée)'])
    
    st.pyplot(fig)


def display_subject_performance(grades_df):
    """
    Display performance by subject as bar chart
    
    Args:
        grades_df: DataFrame with grades (must have 'subject' and 'value' columns)
    """
    if len(grades_df) == 0 or 'subject' not in grades_df.columns:
        st.info("Aucune donnée disponible par matière.")
        return
    
    # Calculate average by subject
    subject_avg = grades_df.groupby('subject')['value'].mean().sort_values(ascending=False)
    
    # Create color list based on averages
    colors_list = [get_grade_color(val) for val in subject_avg.values]
    
    # Create Plotly bar chart
    fig = go.Figure(data=[
        go.Bar(
            x=subject_avg.index,
            y=subject_avg.values,
            marker_color=colors_list,
            text=[f"{val:.1f}/20" for val in subject_avg.values],
            textposition='outside'
        )
    ])
    
    fig.update_layout(
        title="Performance par matière",
        xaxis_title="Matière",
        yaxis_title="Moyenne (/20)",
        yaxis=dict(range=[0, 20]),
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)


def display_recent_grades_table(grades_df, limit=10):
    """
    Display recent grades as a formatted table
    
    Args:
        grades_df: DataFrame with grades
        limit: Number of recent grades to show
    """
    if len(grades_df) == 0:
        st.info("Aucune note enregistrée.")
        return
    
    # Get recent grades
    recent = grades_df.sort_values('evaluation_date', ascending=False).head(limit)
    
    # Format for display
    display_df = recent[['evaluation_date', 'subject', 'competency_name', 'value', 'evaluation_type']].copy()
    display_df.columns = ['Date', 'Matière', 'Compétence', 'Note', 'Type']
    
    # Add classification emoji
    display_df['Niveau'] = display_df['Note'].apply(lambda x: 
        '🟢 Maîtrisée' if x >= 14 else '🟡 En cours' if x >= 10 else '🔴 À renforcer'
    )
    
    # Format date
    display_df['Date'] = pd.to_datetime(display_df['Date']).dt.strftime('%d/%m/%Y')
    
    st.dataframe(display_df, use_container_width=True, hide_index=True)


def render_grade_chart(df_grades):
    """Legacy wrapper used by notes page to display a grades table."""
    if df_grades is None or len(df_grades) == 0:
        st.info("Aucune note disponible.")
        return

    st.dataframe(df_grades, use_container_width=True, hide_index=True)


def render_grade_distribution(grade_values):
    """Legacy wrapper used by notes page to render grade distribution."""
    if grade_values is None or len(grade_values) == 0:
        st.info("Aucune note disponible pour la distribution.")
        return

    grades_df = pd.DataFrame({"value": grade_values})
    display_grade_distribution(grades_df)
