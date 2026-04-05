# frontend/streamlit/components/competency_radar.py
"""
Competency radar chart component
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import numpy as np
from frontend.shared.styles.theme import COLORS


def display_competency_radar(competency_stats, title="Radar des compétences"):
    """
    Display radar chart of competency mastery levels
    
    Args:
        competency_stats: DataFrame with 'subject' and 'average' columns
        title: Chart title
    """
    if len(competency_stats) == 0:
        st.info("Aucune compétence évaluée.")
        return
    
    # Aggregate by subject (max 8 for readability)
    if 'subject' in competency_stats.columns:
        subject_avg = competency_stats.groupby('subject')['average'].mean().head(8)
    else:
        subject_avg = competency_stats.head(8)['average']
    
    subjects = subject_avg.index.tolist()
    values = subject_avg.values.tolist()
    
    # Close the radar (connect last point to first)
    subjects_closed = subjects + [subjects[0]]
    values_closed = values + [values[0]]
    
    # Create Plotly radar chart
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=values_closed,
        theta=subjects_closed,
        fill='toself',
        fillcolor=f'rgba(30, 58, 138, 0.3)',  # Primary color with transparency
        line=dict(color=COLORS['primary'], width=2),
        marker=dict(size=8, color=COLORS['primary']),
        name='Moyenne'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 20],
                tickvals=[5, 10, 14, 20],
                ticktext=['5', '10 (En cours)', '14 (Maîtrisée)', '20']
            )
        ),
        showlegend=False,
        title=title,
        height=500
    )
    
    st.plotly_chart(fig, use_container_width=True)


def display_matplotlib_radar(competency_stats, title="Radar des compétences"):
    """
    Display radar chart using Matplotlib (alternative implementation)
    
    Args:
        competency_stats: DataFrame with 'subject' and 'average' columns
        title: Chart title
    """
    if len(competency_stats) == 0:
        st.info("Aucune compétence évaluée.")
        return
    
    # Aggregate by subject (max 8 for readability)
    if 'subject' in competency_stats.columns:
        subject_avg = competency_stats.groupby('subject')['average'].mean().head(8)
    else:
        subject_avg = competency_stats.head(8)['average']
    
    subjects = subject_avg.index.tolist()
    values = subject_avg.values.tolist()
    
    # Number of variables
    num_vars = len(subjects)
    
    # Compute angle for each axis
    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
    
    # Close the plot
    values += values[:1]
    angles += angles[:1]
    subjects += subjects[:1]
    
    # Create figure
    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(projection='polar'))
    
    # Plot data
    ax.plot(angles, values, 'o-', linewidth=2, color=COLORS['primary'], label='Moyenne')
    ax.fill(angles, values, alpha=0.25, color=COLORS['primary'])
    
    # Set labels
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(subjects[:-1], size=10)
    
    # Set radial limits
    ax.set_ylim(0, 20)
    ax.set_yticks([5, 10, 14, 20])
    ax.set_yticklabels(['5', '10', '14', '20'])
    
    # Add threshold circles
    ax.plot(angles, [10] * len(angles), '--', color=COLORS['warning'], alpha=0.5, label='En cours (10)')
    ax.plot(angles, [14] * len(angles), '--', color=COLORS['success'], alpha=0.5, label='Maîtrisée (14)')
    
    # Grid
    ax.grid(True)
    
    # Title and legend
    ax.set_title(title, size=14, fontweight='bold', pad=20)
    ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1))
    
    st.pyplot(fig)


def display_competency_summary_table(competency_stats):
    """
    Display competency statistics as a formatted table
    
    Args:
        competency_stats: DataFrame with competency statistics
    """
    if len(competency_stats) == 0:
        st.info("Aucune statistique disponible.")
        return
    
    # Prepare display DataFrame
    display_df = competency_stats.copy()
    
    # Add classification emoji if not present
    if 'emoji' not in display_df.columns:
        display_df['emoji'] = display_df['average'].apply(lambda x: 
            '🟢' if x >= 14 else '🟡' if x >= 10 else '🔴'
        )
    
    if 'level' not in display_df.columns:
        display_df['level'] = display_df['average'].apply(lambda x: 
            'Maîtrisée' if x >= 14 else 'En cours' if x >= 10 else 'À renforcer'
        )
    
    # Select and rename columns
    if 'competency_name' in display_df.columns:
        display_cols = {
            'emoji': '📊',
            'competency_name': 'Compétence',
            'subject': 'Matière',
            'average': 'Moyenne',
            'level': 'Niveau',
            'count': 'Nb évals'
        }
    else:
        display_cols = {
            'emoji': '📊',
            'subject': 'Matière',
            'average': 'Moyenne',
            'level': 'Niveau'
        }
    
    # Filter existing columns
    available_cols = {k: v for k, v in display_cols.items() if k in display_df.columns}
    display_df = display_df[list(available_cols.keys())]
    display_df.columns = list(available_cols.values())
    
    # Format average
    if 'Moyenne' in display_df.columns:
        display_df['Moyenne'] = display_df['Moyenne'].apply(lambda x: f"{x:.1f}/20")
    
    st.dataframe(display_df, use_container_width=True, hide_index=True)
