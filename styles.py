import streamlit as st

def inject_luxury_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;600;700&family=Montserrat:wght@300;400;500;600&display=swap');
    
    /* Root application overrides */
    .stApp {
        background-color: #0A0A0A;
        color: #F5F5F5;
        font-family: 'Montserrat', sans-serif;
    }
    
    /* High luxury headers */
    h1, h2, h3, .luxury-title {
        font-family: 'Cinzel', serif !important;
        color: #D4AF37 !important; /* Metallic Royal Gold */
        text-shadow: 0px 2px 4px rgba(0, 0, 0, 0.8);
        font-weight: 600;
    }
    
    /* Sidebar adjustments */
    [data-testid="stSidebar"] {
        background-color: #111111 !important;
        border-right: 1px solid #222222;
    }
    
    /* Glassmorphic Perfume Presentation Card */
    .perfume-card {
        background: rgba(25, 25, 25, 0.65);
        border: 1px solid rgba(212, 175, 55, 0.25);
        border-radius: 12px;
        padding: 24px;
        margin-bottom: 20px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        backdrop-filter: blur(8px);
        -webkit-backdrop-filter: blur(8px);
        transition: transform 0.3s ease, border-color 0.3s ease;
    }
    
    .perfume-card:hover {
        transform: translateY(-4px);
        border-color: rgba(212, 175, 55, 0.7);
    }
    
    /* Custom Luxury Pill Badges */
    .note-badge {
        display: inline-block;
        background: rgba(212, 175, 55, 0.1);
        border: 1px solid rgba(212, 175, 55, 0.4);
        color: #E6C657;
        padding: 2px 8px;
        border-radius: 4px;
        font-size: 11px;
        margin: 2px;
    }
    
    /* Custom CTA Premium Buttons */
    .stButton>button {
        background: linear-gradient(135deg, #B38F24 0%, #F3D065 50%, #B38F24 100%) !important;
        color: #000000 !important;
        font-weight: 600 !important;
        border: none !important;
        border-radius: 4px !important;
        padding: 0.5rem 2rem !important;
        transition: all 0.3s ease-in-out !important;
        box-shadow: 0px 4px 15px rgba(212, 175, 55, 0.2);
    }
    
    .stButton>button:hover {
        transform: scale(1.02);
        box-shadow: 0px 6px 20px rgba(212, 175, 55, 0.4);
        color: #000000 !important;
    }
    
    /* Analytics container backgrounds */
    div[data-testid="stMetricValue"] {
        color: #F3D065 !important;
        font-family: 'Cinzel', serif;
    }
    </style>
    """, unsafe_allow_html=True)
