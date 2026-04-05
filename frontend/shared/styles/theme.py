# frontend/shared/styles/theme.py
"""
Shared styling and theming for EduTrack IA frontends
"""

import streamlit as st
from contextlib import contextmanager

# Color scheme based on competency classification
COLORS = {
    "primary": "#1E3A8A",  # Dark blue
    "secondary": "#10B981",  # Green
    "success": "#10B981",  # Green - Maîtrisée
    "warning": "#F59E0B",  # Orange/Yellow - En cours
    "danger": "#EF4444",  # Red - À renforcer
    "info": "#3B82F6",  # Light blue
    "light": "#F3F4F6",  # Light gray
    "dark": "#1F2937",  # Dark gray
    "white": "#FFFFFF"
}

# Grade classification colors
GRADE_COLORS = {
    "maîtrisée": COLORS["success"],
    "en cours": COLORS["warning"],
    "à renforcer": COLORS["danger"]
}

# Emoji indicators
GRADE_EMOJIS = {
    "maîtrisée": "🟢",
    "en cours": "🟡",
    "à renforcer": "🔴"
}

# Trend indicators
TREND_EMOJIS = {
    "amélioration": "📈",
    "stable": "➡️",
    "régression": "📉"
}

TREND_COLORS = {
    "amélioration": COLORS["success"],
    "stable": COLORS["info"],
    "régression": COLORS["danger"]
}


def apply_custom_css():
    """Apply custom CSS to Streamlit app"""
    st.markdown(f"""
    <style>
    @import url(
        'https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap'
    );

    /* Main theme colors */
    :root {{
        --primary-color: #5A4AA3;
        --secondary-color: #7D72C4;
        --surface-color: #FFFFFF;
        --app-bg: #F3F4F9;
        --text-primary: #23253A;
        --text-muted: #8D91A8;
        --success-color: {COLORS['success']};
        --warning-color: {COLORS['warning']};
        --danger-color: {COLORS['danger']};
        --info-color: {COLORS['info']};
    }}

    html, body, [class*="css"], [data-testid="stAppViewContainer"] {{
        font-family: 'Poppins', sans-serif;
    }}

    [data-testid="stAppViewContainer"] {{
        background:
            radial-gradient(circle at 15% 10%, #E9E7F7 0%, transparent 30%),
            radial-gradient(circle at 90% 0%, #FCE8EF 0%, transparent 28%),
            var(--app-bg);
    }}

    .main .block-container {{
        padding-top: 1.4rem;
        padding-bottom: 2rem;
        max-width: 1260px;
    }}

    [data-testid="stSidebar"] > div:first-child {{
        background: linear-gradient(
            180deg, #5B4DA0 0%, #4B3D8A 55%, #403278 100%
        );
        border-top-right-radius: 22px;
        padding-top: 1rem;
    }}

    [data-testid="stSidebar"] * {{
        color: #F1F1FC;
    }}

    [data-testid="stSidebar"] .stMetric label,
    [data-testid="stSidebar"] .stMetric [data-testid="stMetricLabel"],
    [data-testid="stSidebar"] .stMarkdown p {{
        color: #D9D8EE !important;
    }}

    [data-testid="stSidebar"] .stMetric [data-testid="stMetricValue"] {{
        color: #FFFFFF !important;
    }}

    [data-testid="stSidebar"] .stAlert {{
        background: rgba(255, 255, 255, 0.12);
        border: none;
        border-radius: 12px;
    }}

    [data-testid="stSidebarNav"] {{
        margin-top: 0.75rem;
    }}

    [data-testid="stSidebarNav"] a {{
        border-radius: 14px;
        margin: 0.25rem 0.4rem;
        color: #E9E8FA !important;
        font-size: 0.92rem;
    }}

    [data-testid="stSidebarNav"] a:hover {{
        background: rgba(255, 255, 255, 0.14);
        color: #FFFFFF !important;
    }}

    [data-testid="stSidebarNav"] a[aria-current="page"] {{
        background: #F6F5FC;
        color: #4B3D8A !important;
        font-weight: 600;
    }}

    /* Header styling */
    .main-header {{
        background: linear-gradient(120deg, #FFFFFF 0%, #F7F7FD 100%);
        padding: 1.25rem 1.6rem;
        border-radius: 16px;
        color: var(--text-primary);
        margin-bottom: 1.25rem;
        border: 1px solid #E8EAF3;
        box-shadow: 0 12px 26px rgba(35, 37, 58, 0.08);
    }}

    .main-header h1 {{
        margin: 0;
        font-size: 1.45rem;
        font-weight: 700;
    }}

    .main-header p {{
        margin: 0.3rem 0 0 0;
        color: var(--text-muted);
        font-size: 0.93rem;
        font-weight: 500;
    }}

    .main-header .eyebrow {{
        color: #7B7E95;
        font-size: 0.8rem;
        letter-spacing: 0.04em;
        text-transform: uppercase;
        margin-bottom: 0.35rem;
    }}

    /* Card styling */
    .metric-card {{
        background: var(--surface-color);
        padding: 1.1rem 1.2rem;
        border-radius: 14px;
        box-shadow: 0 8px 20px rgba(45, 49, 74, 0.08);
        border-left: 5px solid #5A4AA3;
        border: 1px solid #ECEEF6;
        margin-bottom: 0.9rem;
    }}

    .metric-card h3 {{
        margin: 0;
        color: var(--text-muted);
        font-size: 0.82rem;
        font-weight: 500;
        letter-spacing: 0.02em;
    }}

    .metric-card h2 {{
        margin: 0.35rem 0 0 0;
        color: var(--text-primary);
        font-size: 2rem;
        font-weight: 700;
    }}

    .metric-card .metric-note {{
        margin-top: 0.35rem;
        color: var(--text-muted);
        font-size: 0.78rem;
        font-weight: 500;
    }}

    .metric-card.success {{
        border-left-color: {COLORS['success']};
    }}

    .metric-card.warning {{
        border-left-color: {COLORS['warning']};
    }}

    .metric-card.danger {{
        border-left-color: {COLORS['danger']};
    }}

    .metric-card.info {{
        border-left-color: {COLORS['info']};
    }}

    .dashboard-panel {{
        background: #FFFFFF;
        border: 1px solid #E8EAF3;
        border-radius: 16px;
        padding: 1rem 1.15rem;
        box-shadow: 0 10px 22px rgba(35, 37, 58, 0.07);
        margin-bottom: 0.9rem;
    }}

    .dashboard-panel h3 {{
        margin: 0 0 0.75rem 0;
        color: var(--text-primary);
        font-size: 1rem;
        font-weight: 600;
    }}

    .dashboard-top-strip {{
        height: 10px;
        border-radius: 12px;
        background: linear-gradient(90deg, #D42468 0%, #BE1D5A 100%);
        margin-bottom: 0.7rem;
    }}

    .dashboard-welcome {{
        background: #FFFFFF;
        border: 1px solid #E6E8F2;
        border-radius: 14px;
        padding: 0.8rem 1rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 0.9rem;
    }}

    .welcome-title {{
        color: #2C2F46;
        font-weight: 600;
        font-size: 1rem;
    }}

    .welcome-year {{
        color: #646A82;
        font-size: 0.88rem;
        font-weight: 600;
    }}

    .kpi-tile {{
        background: #FFFFFF;
        border: 1px solid #E8EAF3;
        border-radius: 14px;
        padding: 0.85rem 1rem;
        display: flex;
        align-items: center;
        gap: 0.85rem;
        box-shadow: 0 8px 18px rgba(34, 38, 57, 0.06);
        border-left: 5px solid #D9DEEF;
    }}

    .kpi-tile.accent-red {{
        border-left-color: #F0A2A8;
    }}

    .kpi-tile.accent-violet {{
        border-left-color: #7868BD;
    }}

    .kpi-tile.accent-yellow {{
        border-left-color: #F0C63D;
    }}

    .kpi-tile.accent-green {{
        border-left-color: #39A35E;
    }}

    .kpi-icon {{
        width: 42px;
        height: 42px;
        border-radius: 10px;
        display: grid;
        place-items: center;
        background: #F5F6FC;
        font-size: 1.15rem;
    }}

    .kpi-label {{
        color: #8C90A7;
        font-size: 0.8rem;
        font-weight: 500;
    }}

    .kpi-value {{
        color: #242741;
        font-size: 1.65rem;
        line-height: 1.2;
        font-weight: 700;
    }}

    .section-fixed {{
        min-height: 260px;
    }}

    .month-strip {{
        display: flex;
        gap: 0.3rem;
        flex-wrap: wrap;
        margin-bottom: 0.65rem;
    }}

    .month-pill {{
        background: #F0F2F9;
        border: 1px solid #E2E6F2;
        color: #7E839A;
        font-size: 0.7rem;
        padding: 0.2rem 0.42rem;
        border-radius: 8px;
        font-weight: 600;
    }}

    .month-pill.active {{
        background: #5B4DA0;
        color: #FFFFFF;
        border-color: #5B4DA0;
    }}

    .calendar-grid {{
        display: grid;
        gap: 0.28rem;
    }}

    .calendar-row {{
        display: grid;
        grid-template-columns: repeat(7, 1fr);
        gap: 0.28rem;
    }}

    .calendar-day {{
        background: #F5F6FC;
        border: 1px solid #ECEFF7;
        border-radius: 7px;
        min-height: 26px;
        display: grid;
        place-items: center;
        color: #4A4E69;
        font-size: 0.8rem;
    }}

    .calendar-day.empty {{
        background: transparent;
        border-color: transparent;
    }}

    .calendar-day.marked {{
        color: #D29F00;
        font-weight: 700;
        background: #FFF8DD;
        border-color: #F7E5AA;
    }}

    .stage-row {{
        display: grid;
        grid-template-columns: 1fr auto;
        gap: 0.45rem 0.6rem;
        align-items: center;
        margin-bottom: 0.72rem;
    }}

    .stage-label {{
        color: #343952;
        font-size: 0.9rem;
        font-weight: 600;
        display: flex;
        align-items: center;
        gap: 0.45rem;
    }}

    .stage-value {{
        color: #2A2E45;
        font-size: 0.9rem;
        font-weight: 700;
    }}

    .dot {{
        width: 9px;
        height: 9px;
        border-radius: 50%;
        display: inline-block;
    }}

    .dot.violet {{
        background: #7464BC;
    }}

    .dot.yellow {{
        background: #E8BC2A;
    }}

    .dot.green {{
        background: #3CA95E;
    }}

    .stage-bar {{
        grid-column: 1 / span 2;
        height: 8px;
        background: #ECEFF7;
        border-radius: 999px;
        overflow: hidden;
    }}

    .stage-bar span {{
        display: block;
        height: 100%;
        background: linear-gradient(90deg, #7A6BC2 0%, #4CA967 100%);
        border-radius: 999px;
    }}

    .panel-head {{
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 0.55rem;
    }}

    .view-all {{
        border: 1px solid #C7D7C7;
        color: #4B9268;
        border-radius: 999px;
        padding: 0.2rem 0.55rem;
        font-size: 0.72rem;
        font-weight: 600;
    }}

    .events-list {{
        list-style: none;
        margin: 0;
        padding: 0;
    }}

    .events-list li {{
        border-bottom: 1px solid #EFF1F8;
        padding: 0.5rem 0;
        color: #2D3047;
        font-size: 0.86rem;
        display: flex;
        justify-content: space-between;
        gap: 0.5rem;
    }}

    .events-list li span {{
        color: #8D92AA;
        white-space: nowrap;
        font-size: 0.74rem;
    }}

    .top-cards-wrap {{
        display: grid;
        grid-template-columns: repeat(3, minmax(0, 1fr));
        gap: 0.55rem;
    }}

    .top-card {{
        border-radius: 14px;
        color: #FFFFFF;
        padding: 0.72rem;
        min-height: 160px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        box-shadow: 0 10px 20px rgba(35, 37, 58, 0.13);
    }}

    .top-card.rank-green {{
        background: linear-gradient(145deg, #34A85E 0%, #25944E 100%);
    }}

    .top-card.rank-violet {{
        background: linear-gradient(145deg, #7060B6 0%, #5F4FA8 100%);
    }}

    .top-card.rank-yellow {{
        background: linear-gradient(145deg, #F2C11F 0%, #E1AF12 100%);
    }}

    .top-name {{
        font-size: 0.92rem;
        font-weight: 700;
        line-height: 1.3;
    }}

    .top-score {{
        font-size: 1.28rem;
        font-weight: 700;
    }}

    .top-rank {{
        background: rgba(255, 255, 255, 0.2);
        border-radius: 8px;
        text-align: center;
        padding: 0.3rem;
        font-size: 0.85rem;
        font-weight: 700;
    }}

    .activity-item {{
        background: #FFFFFF;
        border: 1px solid #ECEEF6;
        border-left: 4px solid #D6DAEA;
        border-radius: 12px;
        margin-bottom: 0.55rem;
        padding: 0.8rem 1rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
        gap: 0.8rem;
    }}

    .activity-item .activity-title {{
        font-size: 0.92rem;
        color: #2E3148;
        font-weight: 600;
    }}

    .activity-item .activity-subtitle {{
        font-size: 0.8rem;
        color: #8E93AA;
        margin-top: 0.14rem;
    }}

    .score-chip {{
        background: #F5F7FD;
        border: 1px solid #E2E7F5;
        border-radius: 999px;
        padding: 0.33rem 0.7rem;
        font-size: 0.82rem;
        font-weight: 700;
        color: #30334B;
        white-space: nowrap;
    }}

    /* Student card */
    .student-card {{
        background: white;
        padding: 1.2rem;
        border-radius: 14px;
        box-shadow: 0 8px 20px rgba(0,0,0,0.08);
        margin-bottom: 1rem;
        border-top: 4px solid #5A4AA3;
        border: 1px solid #ECEEF6;
    }}

    /* Alert boxes */
    .alert {{
        padding: 1rem;
        border-radius: 8px;
        margin-bottom: 1rem;
        border-left: 4px solid;
    }}

    .alert-success {{
        background-color: #D1FAE5;
        border-left-color: {COLORS['success']};
        color: #065F46;
    }}

    .alert-warning {{
        background-color: #FEF3C7;
        border-left-color: {COLORS['warning']};
        color: #92400E;
    }}

    .alert-danger {{
        background-color: #FEE2E2;
        border-left-color: {COLORS['danger']};
        color: #991B1B;
    }}

    .alert-info {{
        background-color: #DBEAFE;
        border-left-color: {COLORS['info']};
        color: #1E40AF;
    }}

    /* Badge styling */
    .badge {{
        display: inline-block;
        padding: 0.32rem 0.7rem;
        border-radius: 999px;
        font-size: 0.78rem;
        font-weight: 600;
        margin: 0.25rem;
    }}

    .badge-success {{
        background-color: {COLORS['success']};
        color: white;
    }}

    .badge-warning {{
        background-color: {COLORS['warning']};
        color: white;
    }}

    .badge-danger {{
        background-color: {COLORS['danger']};
        color: white;
    }}

    .badge-info {{
        background-color: {COLORS['info']};
        color: white;
    }}

    /* Table styling */
    .dataframe {{
        font-size: 0.9rem;
    }}

    /* Report preview */
    .report-preview {{
        background-color: {COLORS['light']};
        padding: 2rem;
        border-radius: 10px;
        border: 1px solid #E5E7EB;
        font-family: 'Georgia', serif;
        line-height: 1.8;
    }}

    .report-section {{
        margin-bottom: 1.5rem;
    }}

    .report-section-title {{
        color: {COLORS['primary']};
        font-size: 1.1rem;
        font-weight: bold;
        margin-bottom: 0.5rem;
        border-bottom: 2px solid {COLORS['primary']};
        padding-bottom: 0.3rem;
    }}

    /* Button styling */
    .stButton>button {{
        border-radius: 12px;
        font-weight: 600;
        border: 1px solid #D9DFF0;
        background: #FFFFFF;
        color: #2E3148;
        transition: all 0.2s ease;
    }}

    .stButton>button:hover {{
        transform: translateY(-1px);
        border-color: #BFC7E2;
        box-shadow: 0 6px 16px rgba(46, 49, 72, 0.12);
    }}

    .stDataFrame, .stPlotlyChart, .stMetric {{
        background: #FFFFFF;
        border-radius: 14px;
        border: 1px solid #E8EAF3;
        box-shadow: 0 8px 20px rgba(35, 37, 58, 0.06);
        padding: 0.35rem;
    }}

    .stExpander {{
        border: 1px solid #E6E8F3;
        border-radius: 12px;
    }}

    /* Grade indicator */
    .grade-indicator {{
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: 600;
    }}

    .grade-indicator.maitrisee {{
        background-color: #D1FAE5;
        color: #065F46;
    }}

    .grade-indicator.en-cours {{
        background-color: #FEF3C7;
        color: #92400E;
    }}

    .grade-indicator.a-renforcer {{
        background-color: #FEE2E2;
        color: #991B1B;
    }}

    @media (max-width: 900px) {{
        .main-header {{
            padding: 1rem;
        }}

        .metric-card h2 {{
            font-size: 1.5rem;
        }}

        .activity-item {{
            flex-direction: column;
            align-items: flex-start;
        }}

        .dashboard-welcome {{
            flex-direction: column;
            align-items: flex-start;
            gap: 0.35rem;
        }}

        .top-cards-wrap {{
            grid-template-columns: 1fr;
        }}

        .section-fixed {{
            min-height: auto;
        }}
    }}
    </style>
    """, unsafe_allow_html=True)


def create_header(title, subtitle=None):
    """Create styled header"""
    if subtitle:
        return f"""
        <div class="main-header">
            <h1>{title}</h1>
            <p>{subtitle}</p>
        </div>
        """
    else:
        return f"""
        <div class="main-header">
            <h1>{title}</h1>
        </div>
        """


def apply_theme():
    """Backward-compatible alias used by legacy pages."""
    apply_custom_css()


def apply_custom_theme():
    """Parent view alias for the shared Streamlit CSS theme."""
    apply_custom_css()


def get_colors():
    """Return the color palette expected by legacy components/pages."""
    return {
        **COLORS,
        "surface": COLORS["light"],
        "background": COLORS["white"],
        "text": COLORS["dark"],
    }


def get_theme_colors():
    """Alias for analytics pages."""
    return get_colors()


def get_color_scheme():
    """Alias for parent view pages."""
    return get_colors()


@contextmanager
def apply_card_style():
    """Render content inside a metric-card wrapper for grade pages."""
    st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
    try:
        yield
    finally:
        st.markdown("</div>", unsafe_allow_html=True)


def get_grade_color(value):
    """Return a semantic color based on the Moroccan 0-20 grading scale."""
    if value >= 14:
        return COLORS["success"]
    if value >= 10:
        return COLORS["warning"]
    return COLORS["danger"]


def format_report_section(title, content):
    """Generate a small reusable HTML block for report sections."""
    return f"""
    <div class="report-section">
        <div class="report-section-title">{title}</div>
        <div>{content}</div>
    </div>
    """


def create_metric_card(title, value, delta=None, card_type="primary"):
    """Create a styled metric card"""
    delta_html = ""
    if delta:
        delta_color = COLORS['success'] if delta > 0 else COLORS['danger']
        delta_sign = "+" if delta > 0 else ""
        delta_html = (
            f'<p style="color: {delta_color}; font-size: 1rem; margin: 0;">'
            f'{delta_sign}{delta}</p>'
        )

    return f"""
    <div class="metric-card {card_type}">
        <h3 style="color: #6B7280; font-size: 0.9rem; margin: 0;">{title}</h3>
        <h2 style="color: #111827; font-size: 2rem; margin: 0.5rem 0;">
            {value}
        </h2>
        {delta_html}
    </div>
    """


def create_alert(message, alert_type="info"):
    """Create styled alert box"""
    return f"""
    <div class="alert alert-{alert_type}">
        {message}
    </div>
    """


def create_badge(text, badge_type="info"):
    """Create colored badge"""
    return f'<span class="badge badge-{badge_type}">{text}</span>'


def create_grade_badge(value):
    """Create grade classification badge"""
    if value >= 14:
        return (
            f'{GRADE_EMOJIS["maîtrisée"]} '
            f'<span class="badge badge-success">Maîtrisée ({value}/20)</span>'
        )
    elif value >= 10:
        return (
            f'{GRADE_EMOJIS["en cours"]} '
            f'<span class="badge badge-warning">En cours ({value}/20)</span>'
        )
    else:
        return (
            f'{GRADE_EMOJIS["à renforcer"]} '
            f'<span class="badge badge-danger">À renforcer ({value}/20)</span>'
        )


def create_trend_badge(trend):
    """Create trend indicator badge"""
    emoji = TREND_EMOJIS.get(trend, "➡️")
    color = TREND_COLORS.get(trend, COLORS['info'])
    return (
        f'<span style="color: {color}; font-weight: bold;">'
        f'{emoji} {trend.capitalize()}</span>'
    )
