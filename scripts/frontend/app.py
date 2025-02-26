import streamlit as st
import requests
import time
from datetime import datetime

# Configure page
st.set_page_config(
    page_title="Calories Burn Predictor",
    page_icon="🔥",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS with improved color scheme
st.markdown("""
<style>
    /* Main color palette */
    :root {
        --primary-color: #FF6B6B;
        --primary-light: #FFD0D0;
        --primary-dark: #E83A3A;
        --accent-color: #4ECDC4;
        --text-color: #2D3748;
        --light-bg: #F7FAFC;
        --card-bg: #FFFFFF;
        --gradient-start: #FF9A8B;
        --gradient-mid: #FF6A88;
        --gradient-end: #FF99AC;
    }
    
    .main {
        background: linear-gradient(135deg, var(--gradient-start) 0%, var(--gradient-mid) 55%, var(--gradient-end) 100%);
    }
    
    .stApp {
        max-width: 1200px;
        margin: 0 auto;
    }
    
    .title-container {
        background-color: rgba(255, 255, 255, 0.85);
        border-radius: 15px;
        padding: 30px;
        margin-bottom: 25px;
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.12);
        text-align: center;
        border-left: 8px solid var(--primary-color);
    }
    
    .prediction-container {
        background-color: var(--card-bg);
        border-radius: 15px;
        padding: 30px;
        margin-top: 25px;
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.12);
        text-align: center;
        border-left: 8px solid var(--accent-color);
    }
    
    .input-section {
        background-color: var(--card-bg);
        padding: 25px;
        border-radius: 15px;
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.12);
        margin-bottom: 25px;
        border-left: 5px solid var(--primary-color);
    }
    
    .stButton>button {
        background: linear-gradient(to right, var(--primary-color), var(--primary-dark));
        color: white;
        font-weight: bold;
        border-radius: 30px;
        padding: 12px 30px;
        font-size: 18px;
        border: none;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.15);
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        transform: translateY(-3px);
        box-shadow: 0 7px 15px rgba(0, 0, 0, 0.2);
        background: linear-gradient(to right, var(--primary-dark), var(--primary-color));
    }
    
    h1 {
        color: var(--primary-dark);
        font-weight: 800;
        letter-spacing: 1px;
    }
    
    h2, h3 {
        color: var(--primary-color);
        font-weight: 600;
    }
    
    p, label, .stMarkdown {
        color: var(--text-color) !important;
    }
    
    .highlight {
        background-color: var(--primary-color);
        color: white;
        padding: 5px 12px;
        border-radius: 8px;
        font-weight: bold;
    }
    
    .status-message {
        padding: 12px;
        border-radius: 8px;
        margin: 12px 0;
        font-weight: bold;
    }
    
    .footer {
        text-align: center;
        margin-top: 40px;
        padding: 15px;
        font-size: 14px;
        color: var(--text-color);
        background-color: rgba(255, 255, 255, 0.7);
        border-radius: 10px;
    }
    
    .user-info {
        font-style: italic;
        color: var(--text-color);
        text-align: right;
        margin-bottom: 20px;
    }
    
    /* Custom slider styling */
    .stSlider>div>div>div {
        background-color: var(--primary-color) !important;
    }
    
    /* Style for tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: rgba(255, 255, 255, 0.7);
        border-radius: 8px 8px 0 0;
        padding: 8px 16px;
        height: auto;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: var(--card-bg);
        border-top: 3px solid var(--primary-color);
    }
    
    /* Metrics styling */
    [data-testid="stMetricValue"] {
        font-size: 28px;
        color: var(--primary-color);
    }
    
    /* Success message */
    .element-container .stAlert {
        border-radius: 10px;
        border-left: 5px solid;
    }
</style>
""", unsafe_allow_html=True)

# Header with animated background (using columns for layout)
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    st.markdown("""
    <div class="title-container">
        <h1>🔥 CALORIE BURN CALCULATOR 🔥</h1>
        <p>Predict how many calories you'll burn during your workout session</p>
    </div>
    """, unsafe_allow_html=True)

# Display user info and time
current_time = datetime.now().strftime("%A, %B %d, %Y - %H:%M")
st.markdown(f"""
<div class="user-info">
    Last updated: {current_time}
</div>
""", unsafe_allow_html=True)

# Create tabs for different sections
tab1, tab2 = st.tabs(["📊 Predictor", "ℹ️ About"])

with tab1:
    # Split the form into two columns
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("<div class='input-section'>", unsafe_allow_html=True)
        st.subheader("💪 Personal Information")
        
        gender = st.selectbox("Gender", options=["male", "female"])
        age = st.slider("Age", min_value=15, max_value=80, value=30, step=1)
        height = st.slider("Height (cm)", min_value=150, max_value=220, value=170, step=1)
        weight = st.slider("Weight (kg)", min_value=40, max_value=150, value=70, step=1)
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("<div class='input-section'>", unsafe_allow_html=True)
        st.subheader("🏃‍♂️ Workout Parameters")
        
        heart_rate = st.slider("Heart Rate (bpm)", 
                              min_value=60, 
                              max_value=200, 
                              value=120)
        
        duration = st.slider("Duration (minutes)", 
                            min_value=5, 
                            max_value=120, 
                            value=30)
        
        body_temp = st.slider("Body Temp (°C)", 
                             min_value=36.0, 
                             max_value=39.0, 
                             value=36.8,
                             step=0.1)
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Button container for styling
    st.markdown("<div style='text-align: center; margin: 30px 0;'>", unsafe_allow_html=True)
    predict_button = st.button("🔥 CALCULATE CALORIES BURNED 🔥", use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
    API_URL = "http://localhost:8000/Calories_predict"
    
    if predict_button:
        input_data = {
            "Gender": gender,
            "Age": age,
            "Height": float(height),
            "Weight": float(weight),
            "Duration": float(duration),
            "Heart_Rate": float(heart_rate),
            "Body_Temp": float(body_temp)
        }
        
        # Show a spinner while "calculating"
        with st.spinner('Calculating calories burned...'):
            try:
                # Add a small delay for dramatic effect
                time.sleep(1.5)
                
                response = requests.post(API_URL, json=input_data)
                if response.status_code == 200:
                    result = response.json()
                    if 'error' in result:
                        st.error(f"Error in prediction: {result['error']}")
                    else:
                        prediction = result['Prediction']
                        
                        # Create a fun animation
                        progress_bar = st.progress(0)
                        for i in range(100):
                            progress_bar.progress(i + 1)
                            time.sleep(0.01)
                        
                        st.markdown(f"""
                        <div class="prediction-container">
                            <h2>🔥 Congratulations! 🔥</h2>
                            <p>Based on your workout parameters, you will burn approximately:</p>
                            <h1 style="font-size: 54px; background: linear-gradient(to right, #FF6B6B, #E83A3A);
                                       -webkit-background-clip: text; -webkit-text-fill-color: transparent; 
                                       margin: 25px 0;">{prediction} Calories</h1>
                            <p>That's approximately {prediction/7700:.2f} kg of fat burned!</p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Give a motivational message based on calories burned
                        if prediction > 500:
                            st.success("Excellent workout! You're crushing your fitness goals! 💪")
                        elif prediction > 300:
                            st.success("Great session! Keep up the good work! 👍")
                        else:
                            st.info("Good start! Every calorie counts toward your health journey. 🌱")
                        
                        # Calculate and show fun equivalents
                        st.markdown("<div class='input-section'>", unsafe_allow_html=True)
                        st.subheader("Your Burn Equivalents")
                        
                        cola_cans = prediction / 140
                        pizza_slices = prediction / 285
                        chocolate_bars = prediction / 230
                        
                        eq_col1, eq_col2, eq_col3 = st.columns(3)
                        with eq_col1:
                            st.metric("Cans of Cola", f"{cola_cans:.1f}")
                        with eq_col2:
                            st.metric("Pizza Slices", f"{pizza_slices:.1f}")
                        with eq_col3:
                            st.metric("Chocolate Bars", f"{chocolate_bars:.1f}")
                            
                        st.markdown("</div>", unsafe_allow_html=True)
                        
                else:
                    st.error(f"Error: {response.status_code}")
            except Exception as e:
                st.error(f"Exception: {str(e)}")

with tab2:
    st.markdown("<div class='input-section'>", unsafe_allow_html=True)
    
    st.subheader("ℹ️ About This App")
    
    st.markdown("""
    This application uses machine learning to predict how many calories you'll burn during your workout based on:
    
    * **Personal factors**: gender, age, height, weight
    * **Workout parameters**: duration, heart rate, body temperature
    
    The prediction model was trained on thousands of workout sessions and has been optimized to provide accurate estimates across different workout types and intensity levels.
    
    ### How It Works
    
    1. Enter your personal information and workout details
    2. Our AI model analyzes your data and compares it to patterns found in our training dataset
    3. The algorithm calculates the expected calorie burn based on these factors
    
    ### Tips for Accurate Results
    
    * Use a heart rate monitor for the most accurate heart rate values
    * Measure your actual workout duration precisely
    * Update your weight regularly for the most accurate calculations
    
    ### Remember
    
    Calorie expenditure varies between individuals. Use these predictions as estimates and always consult with healthcare professionals before beginning any new exercise program.
    """)
    
    st.markdown("</div>", unsafe_allow_html=True)

# Footer
st.markdown("""
<div class="footer">
    <p>© 2025 Calories Burn Predictor | Created with ❤️ using Streamlit</p>
    <p>This app uses machine learning to predict calorie burn during exercise. Results are estimates only.</p>
</div>
""", unsafe_allow_html=True)