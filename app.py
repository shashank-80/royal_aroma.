import streamlit as st
import pandas as pd
import numpy as np
import os
import joblib
import plotly.express as px

# Establish production layout constraints
st.set_page_config(page_title="Royal Aroma | Luxury AI Fragrances", page_icon="👑", layout="wide")

from styles import inject_luxury_css
from database import register_user, authenticate_user, add_to_wishlist, remove_from_wishlist, get_user_wishlist
from recommender import FragranceRecommender

inject_luxury_css()

# Guard dataset availability states
if not os.path.exists("dataset/perfume_data.csv"):
    st.warning("⚠️ High Luxury Data Core missing! Running setup generators to build 5000+ records...")
    import dataset_generator
    import train_models
    dataset_generator.generate_perfume_dataset()
    train_models.train_pipelines()

# Initialize Engine Variables
@st.cache_resource
def load_recommender():
    return FragranceRecommender()

recommender_engine = load_recommender()
df_perfumes = recommender_engine.df

# Warm-cache session configurations
if 'user' not in st.session_state:
    st.session_state['user'] = None

# Custom Premium Navigation Top Header Bar
st.markdown("<h1 style='text-align: center; margin-bottom: 0;'>ROYAL AROMA</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-family:Cinzel; letter-spacing: 3px; color:#AA8822;'>HAUTE PARFUMERIE AI ARCHITECT</p>", unsafe_allow_html=True)
st.markdown("---")

# Navigation Routing Matrix Sidebar
with st.sidebar:
    st.markdown("<h3 style='font-family:Cinzel;'>Maison Navigation</h3>", unsafe_allow_html=True)
    page = st.radio("Go to Gallery", ["Maison d'Accueil (Home)", "AI Perfume Predictor", "The Perfume Explorer", "Analytics & Fragrance Trends", "My Sacred Wishlist"])
    
    st.markdown("---")
    if st.session_state['user']:
        st.markdown(f"✨ Welcome, **{st.session_state['user']['name']}**")
        if st.button("Log Out of Maison"):
            st.session_state['user'] = None
            st.rerun()
    else:
        st.markdown("<p style='font-size:12px; color:#888;'>Unlock personalized profile engines & wishlists</p>", unsafe_allow_html=True)
        auth_mode = st.radio("Access Level", ["Login", "Sign Up"])
        
        with st.form("auth_form"):
            user_input = st.text_input("Username")
            pass_input = st.text_input("Password", type="password")
            name_input = st.text_input("Display Name") if auth_mode == "Sign Up" else ""
            submit_auth = st.form_submit_button("Execute Authentication")
            
            if submit_auth:
                if auth_mode == "Login":
                    session = authenticate_user(user_input, pass_input)
                    if session:
                        st.session_state['user'] = session
                        st.success("Access Granted.")
                        st.rerun()
                    else:
                        st.error("Invalid credentials.")
                else:
                    if user_input and pass_input and name_input:
                        if register_user(user_input, pass_input, name_input):
                            st.success("Profile created! Please log in.")
                        else:
                            st.error("Username already registered.")
                    else:
                        st.error("Fill all parameter scopes.")

# ==========================================
# PAGE 1: HOME PAGE
# ==========================================
if page == "Maison d'Accueil (Home)":
    st.markdown("""
    <div style='background: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.9)), url("https://images.unsplash.com/photo-1541643600914-78b084683601?auto=format&fit=crop&w=1200&q=80"); background-size: cover; padding: 100px 40px; text-align: center; border-radius: 8px; border: 1px solid #332200;'>
        <h2 style='color:#F3D065 !important; font-size: 42px;'>Calculated Elegance. Powered by Intelligence.</h2>
        <p style='color:#DDD; max-width: 600px; margin: 20px auto; font-size:16px;'>Discover your hyper-personalized ultimate olfactory sensory identity signature matching algorithmic predictive parameters.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br><h3 class='luxury-title'>The Curated Collection Imperial</h3>", unsafe_allow_html=True)
    cols = st.columns(3)
    featured_samples = df_perfumes.sample(3, random_state=7)
    
    for idx, (_, row) in enumerate(featured_samples.iterrows()):
        with cols[idx]:
            st.markdown(f"""
            <div class="perfume-card">
                <span style="color:#D4AF37; font-size:12px; font-weight:bold; letter-spacing:1px;">{row['Brand'].upper()}</span>
                <h4 style="margin:5px 0; font-family:'Cinzel';">{row['Perfume_Name']}</h4>
                <p style="font-size:12px; color:#BBB; height:60px; overflow:hidden;">{row['Description']}</p>
                <div style="margin: 10px 0;">
                    <span class="note-badge">★ {row['Rating']}</span>
                    <span class="note-badge">${row['Price']}</span>
                    <span class="note-badge">{row['Fragrance_Family']}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

# ==========================================
# PAGE 2: AI PERFUME PREDICTOR
# ==========================================
elif page == "AI Perfume Predictor":
    st.markdown("<h2 class='luxury-title'>Predictive Olfactory Engine</h2>", unsafe_allow_html=True)
    st.markdown("Input your desired characteristics. Our trained high-dimension machine learning architecture will select your signature profile.")
    
    col1, col2 = st.columns(2)
    with col1:
        gender_in = st.selectbox("Target Gender Alignment", sorted(df_perfumes['Gender'].unique()))
        age_in = st.selectbox("Age Classification Segment", sorted(df_perfumes['Age_Group'].unique()))
        occasion_in = st.selectbox("Scent Environment/Occasion", sorted(df_perfumes['Occasion'].unique()))
        season_in = st.selectbox("Climatic Season Alignment", sorted(df_perfumes['Season'].unique()))
    with col2:
        longevity_in = st.selectbox("Required Structural Longevity", sorted(df_perfumes['Longevity'].unique()))
        projection_in = st.selectbox("Sillage / Projection Matrix", sorted(df_perfumes['Projection'].unique()))
        favorite_note = st.text_input("Enter a Core Desired Note (e.g., Oud, Rose, Amber)", "Oud")
        
    if st.button("Compute Optimal Formulation Profile"):
        # Load ML pipelines gracefully
        try:
            models_meta = joblib.load("models/label_encoders.pkl")
            rf_model = joblib.load("models/rf_perfume_model.pkl")
            
            # Map structural array inputs safely via serialization
            input_vector = [
                models_meta['Gender'].transform([gender_in])[0],
                models_meta['Age_Group'].transform([age_in])[0],
                models_meta['Occasion'].transform([occasion_in])[0],
                models_meta['Season'].transform([season_in])[0],
                models_meta['Longevity'].transform([longevity_in])[0],
                models_meta['Projection'].transform([projection_in])[0]
            ]
            
            predicted_class_idx = rf_model.predict([input_vector])[0]
            predicted_family = models_meta['Fragrance_Family'].inverse_transform([predicted_class_idx])[0]
            
            st.markdown(f"""
            <div style="background:rgba(212,175,55,0.1); border:1px solid #D4AF37; padding:20px; border-radius:8px; margin: 20px 0;">
                <h3 style="margin:0; color:#F3D065;">Algorithmic Verdict: {predicted_family} Family</h3>
                <p style="margin:5px 0 0 0; color:#DDD;">Our predictive model computed your sensory inputs against 5000+ formulation instances with high confidence.</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Fetch content recommendations based on calculated context arrays
            recs = recommender_engine.recommend_by_preferences(gender_in, occasion_in, favorite_note, top_n=3)
            st.markdown("### Tailored Candidate Formulations")
            for _, r in recs.iterrows():
                st.markdown(f"""
                <div class="perfume-card">
                    <h4>{r['Perfume_Name']} ({r['Brand']})</h4>
                    <p><strong>Top Notes:</strong> {r['Top_Notes']} | <strong>Base Notes:</strong> {r['Base_Notes']}</p>
                    <p style="font-size:13px; color:#D4AF37;">MSRP Valuation: ${r['Price']} — Global Rating Profile: ★ {r['Rating']}</p>
                </div>
                """, unsafe_allow_html=True)
                
        except Exception as e:
            st.error(f"Prediction Pipeline optimization error: {str(e)}")

# ==========================================
# PAGE 3: THE PERFUME EXPLORER
# ==========================================
elif page == "The Perfume Explorer":
    st.markdown("<h2 class='luxury-title'>The Imperial Exhibition Room</h2>", unsafe_allow_html=True)
    
    # Advanced Multi-Dimensional Filtering UI
    search_q = st.text_input("Search Formulation Matrix or Brands", "")
    c1, c2, c3 = st.columns(3)
    with c1:
        selected_brand = st.multiselect("Filter by Luxury Brand House", sorted(df_perfumes['Brand'].unique()))
    with c2:
        selected_family = st.multiselect("Filter by Fragrance Family", sorted(df_perfumes['Fragrance_Family'].unique()))
    with c3:
        price_range = st.slider("Max Valuation Allocation ($)", 100, 500, 500)
        
    filtered = df_perfumes[df_perfumes['Price'] <= price_range]
    if search_q:
        filtered = filtered[filtered['Perfume_Name'].str.contains(search_q, case=False) | filtered['Brand'].str.contains(search_q, case=False)]
    if selected_brand:
        filtered = filtered[filtered['Brand'].isin(selected_brand)]
    if selected_family:
        filtered = filtered[filtered['Fragrance_Family'].isin(selected_family)]
        
    st.markdown(f"Showing **{len(filtered)}** premium formulations matching selections.")
    
    # Display elements in structured loop grids
    for idx, row in filtered.head(20).iterrows():
        st.markdown(f"""
        <div class="perfume-card">
            <span style="color:#D4AF37; font-size:11px; font-weight:bold; letter-spacing:1px;">{row['Brand'].upper()}</span>
            <h3 style="margin:5px 0 0 0; color:#FFF; font-family:'Cinzel';">{row['Perfume_Name']}</h3>
            <p style="color:#CCC; font-size:13px; margin:8px 0;">{row['Description']}</p>
            <div>
                <span class="note-badge">Top: {row['Top_Notes']}</span>
                <span class="note-badge">Heart: {row['Middle_Notes']}</span>
                <span class="note-badge">Base: {row['Base_Notes']}</span>
            </div>
            <div style="margin-top:12px; font-size:13px;">
                <span style="color:#F3D065;">Rating: ★ {row['Rating']}</span> | 
                <span style="color:#FFF;">Price: ${row['Price']}</span> |
                <span style="color:#AAA;">Sillage: {row['Projection']}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.session_state['user']:
            if st.button(f"Add to Sacred Wishlist Profile", key=f"wish_{row['Perfume_ID']}"):
                add_to_wishlist(st.session_state['user']['username'], row['Perfume_ID'])
                st.toast(f"{row['Perfume_Name']} saved safely to profile.")

# ==========================================
# PAGE 4: ANALYTICS & FRAGRANCE TRENDS
# ==========================================
elif page == "Analytics & Fragrance Trends":
    st.markdown("<h2 class='luxury-title'>Maison Informatics Analytics</h2>", unsafe_allow_html=True)
    st.markdown("Global market statistics and composition density patterns derived from the database.")
    
    # Custom Luxury Gold Colors banaye gaye hain
    luxury_colors = ['#D4AF37', '#F3D065', '#B38F24', '#FFF8D6', '#997A00']
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### Brand Formulation Distribution Matrix")
        fig_brand = px.pie(df_perfumes, names='Brand', color_discrete_sequence=luxury_colors)
        fig_brand.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color='#FFF')
        st.plotly_chart(fig_brand, use_container_width=True)
        
    with col2:
        st.markdown("#### Valuation Dynamics Across Fragrance Families")
        fig_price = px.box(df_perfumes, x='Fragrance_Family', y='Price', color_discrete_sequence=['#D4AF37'])
        fig_price.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color='#FFF')
        st.plotly_chart(fig_price, use_container_width=True)
        
    st.markdown("#### Scent Performance Metrics (Longevity vs. Rating Dynamics)")
    fig_scatter = px.scatter(df_perfumes.sample(500), x='Price', y='Rating', color='Longevity', size='Rating', color_discrete_sequence=luxury_colors)
    fig_scatter.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color='#FFF')
    st.plotly_chart(fig_scatter, use_container_width=True)
# ==========================================
# PAGE 5: USER WISHLIST
# ==========================================
elif page == "My Sacred Wishlist":
    st.markdown("<h2 class='luxury-title'>Your Private Scent Vault</h2>", unsafe_allow_html=True)
    
    if not st.session_state['user']:
        st.info("🔒 Access restricted. Please authenticate through the Maison control panel in the sidebar menu to view your private vault collection.")
    else:
        user = st.session_state['user']['username']
        wishlist_ids = get_user_wishlist(user)
        
        if not wishlist_ids:
            st.markdown("<p style='color:#888;'>Your vault is currently empty. Explore the exhibition room to build your private collection.</p>", unsafe_allow_html=True)
        else:
            wishlist_df = df_perfumes[df_perfumes['Perfume_ID'].isin(wishlist_ids)]
            
            for _, row in wishlist_df.iterrows():
                st.markdown(f"""
                <div class="perfume-card">
                    <h3 style="margin:0; font-family:'Cinzel'; color:#D4AF37;">{row['Perfume_Name']}</h3>
                    <p style="font-size:12px; color:#AAA;">{row['Brand']} — {row['Fragrance_Family']}</p>
                </div>
                """, unsafe_allow_html=True)
                
                if st.button("Purge Formulation from Vault", key=f"remove_{row['Perfume_ID']}"):
                    remove_from_wishlist(user, row['Perfume_ID'])
                    st.toast("Item removed from collection.")
                    st.rerun()
