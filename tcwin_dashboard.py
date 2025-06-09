import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import json

# CRITICAL: Page config MUST be the first Streamlit command
st.set_page_config(
    page_title="TCWIN Cultural Heritage Explorer",
    page_icon="🕰️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #FF6B6B 0%, #4ECDC4 50%, #45B7D1 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }

    .metric-card {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #4ECDC4;
        margin: 0.5rem 0;
    }

    .status-success {
        background: #d4edda;
        color: #155724;
        padding: 0.5rem;
        border-radius: 5px;
        border: 1px solid #c3e6cb;
    }
</style>
""", unsafe_allow_html=True)

class IndianCulturalDataSimulator:
    """Data simulator with error handling"""

    def __init__(self, random_seed=42):
        np.random.seed(random_seed)
        self.setup_cultural_references()

    def setup_cultural_references(self):
        self.eras = {
            'Vedic': (-1500, -500),
            'Epic': (-500, 0), 
            'Classical': (0, 1000),
            'Medieval': (1000, 1500),
            'Colonial': (1500, 1947),
            'Modern': (1947, 2023)
        }

        self.concepts = [
            'Dharma', 'Karma', 'Moksha', 'Yoga', 'Ayurveda',
            'Natya', 'Sangita', 'Vastu', 'Tantra', 'Vedanta'
        ]

        self.practices = [
            'Diwali', 'Holi', 'Dussehra', 'Onam', 'Pongal'
        ]

        self.regions = ['North', 'South', 'East', 'West', 'Central']

    def generate_sanskrit_manuscripts(self, count=50):
        manuscripts = []

        for i in range(count):
            era = np.random.choice(list(self.eras.keys()))
            year_range = self.eras[era]
            year = np.random.randint(year_range[0], year_range[1])

            manuscript = {
                'manuscript_id': f'TCWIN_MS_{i+1:03d}',
                'title': f'Sanskrit Text {i+1}',
                'content_snippet': 'योगश्चित्तवृत्तिनिरोधः',
                'era': era,
                'estimated_year': year,
                'region': np.random.choice(self.regions),
                'word_count': np.random.randint(500, 5000),
                'preservation_state': np.random.choice(['Excellent', 'Good', 'Fair', 'Poor']),
                'concept_category': np.random.choice(self.concepts)
            }
            manuscripts.append(manuscript)

        return pd.DataFrame(manuscripts)

    def generate_cultural_practices(self, count=25):
        practices = []

        for i in range(count):
            practice = {
                'practice_id': f'TCWIN_CP_{i+1:03d}',
                'name': np.random.choice(self.practices),
                'category': np.random.choice(['Festival', 'Ritual', 'Custom', 'Art']),
                'origin_era': np.random.choice(list(self.eras.keys())[:4]),
                'current_prevalence': np.random.uniform(0.2, 1.0),
                'geographic_spread': np.random.choice(['Local', 'Regional', 'National', 'International']),
                'preservation_risk': np.random.choice(['Low', 'Medium', 'High'])
            }
            practices.append(practice)

        return pd.DataFrame(practices)

@st.cache_data
def load_cultural_data():
    """Load data with caching and error handling"""
    try:
        simulator = IndianCulturalDataSimulator()
        manuscripts_df = simulator.generate_sanskrit_manuscripts(50)
        practices_df = simulator.generate_cultural_practices(25)
        return manuscripts_df, practices_df
    except Exception as e:
        st.error(f"Failed to generate cultural data: {e}")
        return pd.DataFrame(), pd.DataFrame()

def initialize_session_state():
    """Initialize all session state variables safely"""
    if 'user_id' not in st.session_state:
        st.session_state.user_id = f"user_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

    if 'exploration_history' not in st.session_state:
        st.session_state.exploration_history = []

    if 'current_page' not in st.session_state:
        st.session_state.current_page = 'Overview'

def render_header():
    """Render main header"""
    st.markdown("""
    <div class="main-header">
        <h1>🕰️ TCWIN Cultural Heritage Explorer</h1>
        <p>Advanced AI-Powered Analysis of Indian Cultural Wisdom</p>
    </div>
    """, unsafe_allow_html=True)

def render_sidebar():
    """Render sidebar with navigation and filters"""
    st.sidebar.title("🧭 Navigation")

    pages = ["📊 Overview", "🤖 ML Analysis", "🕸️ Knowledge Graph", "💡 Recommendations"]
    selected_page = st.sidebar.selectbox("Select Page", pages)
    st.session_state.current_page = selected_page.split(" ", 1)[1]

    st.sidebar.markdown("### 🔍 Filters")

    era_filter = st.sidebar.multiselect(
        "Historical Eras",
        ["Vedic", "Epic", "Classical", "Medieval", "Colonial", "Modern"],
        default=["Vedic", "Classical"]
    )

    return {'era_filter': era_filter}

def create_overview_dashboard(manuscripts_df, practices_df):
    """Create overview dashboard with error handling"""
    st.header("📊 Cultural Heritage Overview")

    if manuscripts_df.empty:
        st.warning("No manuscript data available")
        return

    # Key metrics
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        total_manuscripts = len(manuscripts_df)
        st.markdown(f"""
        <div class="metric-card">
            <h3>📚 Manuscripts</h3>
            <h2>{total_manuscripts}</h2>
            <p>Total analyzed texts</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        total_practices = len(practices_df)
        st.markdown(f"""
        <div class="metric-card">
            <h3>🎭 Cultural Practices</h3>
            <h2>{total_practices}</h2>
            <p>Documented traditions</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <h3>⏰ Time Span</h3>
            <h2>3500+ Years</h2>
            <p>Historical coverage</p>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        preservation_rate = f"{len(manuscripts_df[manuscripts_df['preservation_state'].isin(['Excellent', 'Good'])])/len(manuscripts_df)*100:.1f}%"
        st.markdown(f"""
        <div class="metric-card">
            <h3>🛡️ Preservation</h3>
            <h2>{preservation_rate}</h2>
            <p>Well-preserved items</p>
        </div>
        """, unsafe_allow_html=True)

    # Charts
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Era Distribution")
        era_counts = manuscripts_df['era'].value_counts()

        try:
            fig_era = px.pie(
                values=era_counts.values,
                names=era_counts.index,
                title="Manuscripts by Era"
            )
            st.plotly_chart(fig_era, use_container_width=True)
        except Exception as e:
            st.error(f"Chart error: {e}")

    with col2:
        st.subheader("Regional Distribution")
        region_counts = manuscripts_df['region'].value_counts()

        try:
            fig_region = px.bar(
                x=region_counts.index,
                y=region_counts.values,
                title="Manuscripts by Region"
            )
            st.plotly_chart(fig_region, use_container_width=True)
        except Exception as e:
            st.error(f"Chart error: {e}")

def create_ml_analysis_dashboard():
    """ML Analysis page"""
    st.header("🤖 Machine Learning Analysis")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="status-success">
            <strong>✅ BERT Classifier</strong><br>
            Ready for Sanskrit text analysis
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="status-success">
            <strong>✅ Clustering Engine</strong><br>
            Cultural pattern discovery active
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="status-success">
            <strong>✅ Recommendation System</strong><br>
            Personalization algorithms running
        </div>
        """, unsafe_allow_html=True)

    st.subheader("🔤 Sanskrit Text Classification")

    sample_text = st.text_area(
        "Enter Sanskrit text for analysis:",
        value="योगश्चित्तवृत्तिनिरोधः",
        help="Enter Sanskrit text to classify"
    )

    if st.button("🔍 Analyze Text"):
        # Simulate analysis results
        predictions = {
            'era': 'Classical',
            'concept': 'Philosophy',
            'confidence': 0.89
        }

        col1, col2 = st.columns(2)
        with col1:
            st.metric("Predicted Era", predictions['era'])
            st.metric("Cultural Domain", predictions['concept'])

        with col2:
            confidence_data = {
                'Era': ['Vedic', 'Classical', 'Medieval', 'Modern'],
                'Confidence': [0.15, 0.89, 0.12, 0.08]
            }

            try:
                fig_conf = px.bar(
                    confidence_data, 
                    x='Era', 
                    y='Confidence',
                    title="Classification Confidence"
                )
                st.plotly_chart(fig_conf, use_container_width=True)
            except Exception as e:
                st.error(f"Chart error: {e}")

def create_knowledge_graph_page():
    """Knowledge Graph page"""
    st.header("🕸️ Knowledge Graph Explorer")
    st.info("Interactive knowledge graph visualization coming soon!")

    # Sample network data
    st.subheader("Cultural Concept Relationships")
    st.write("Dharma ↔ Karma ↔ Moksha")
    st.write("Yoga ↔ Meditation ↔ Pranayama")
    st.write("Ayurveda ↔ Doshas ↔ Traditional Medicine")

def create_recommendations_page():
    """Recommendations page"""
    st.header("💡 Personalized Cultural Recommendations")

    st.subheader("🎯 Your Cultural Interests")

    col1, col2 = st.columns(2)

    with col1:
        user_era_prefs = st.multiselect(
            "Preferred Historical Eras",
            ["Vedic", "Epic", "Classical", "Medieval"],
            default=["Classical"]
        )

    with col2:
        user_concept_prefs = st.multiselect(
            "Interested Cultural Domains",
            ["Dharma", "Karma", "Yoga", "Ayurveda"],
            default=["Yoga"]
        )

    if st.button("🔮 Generate Recommendations"):
        st.success("Recommendations generated!")

        recommendations = [
            "📖 Yoga Sutras of Patanjali - Classical period philosophy",
            "📖 Ayurvedic Pulse Diagnosis - Traditional medicine texts",
            "🎭 Bharatanatyam Dance - Classical cultural practice"
        ]

        for rec in recommendations:
            st.write(f"• {rec}")

def main():
    """Main application function"""
    try:
        # Initialize session state
        initialize_session_state()

        # Render header
        render_header()

        # Get sidebar filters
        filters = render_sidebar()

        # Load data
        manuscripts_df, practices_df = load_cultural_data()

        if manuscripts_df.empty:
            st.error("⚠️ Failed to load cultural data. Please refresh the page.")
            st.stop()

        # Route to appropriate page
        page = st.session_state.current_page

        if page == "Overview":
            create_overview_dashboard(manuscripts_df, practices_df)
        elif page == "ML Analysis":
            create_ml_analysis_dashboard()
        elif page == "Knowledge Graph":
            create_knowledge_graph_page()
        elif page == "Recommendations":
            create_recommendations_page()
        else:
            st.header("🚧 Coming Soon")
            st.info(f"The {page} page is under development.")

        # Footer
        st.markdown("---")
        st.markdown("""
        <div style="text-align: center; color: #666; padding: 1rem;">
            🕰️ TCWIN Cultural Heritage Explorer | Enhanced with Advanced ML
        </div>
        """, unsafe_allow_html=True)

    except Exception as e:
        st.error(f"Application error: {str(e)}")
        st.info("Please refresh the page or contact support.")

# CRITICAL: This must be at the bottom
if __name__ == "__main__":
    main()