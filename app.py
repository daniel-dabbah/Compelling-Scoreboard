import streamlit as st
from datetime import datetime, date
import json

# Configure page
st.set_page_config(
    page_title="הערכה פנימית - לוח תוצאות",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for better styling with RTL support, pleasant colors, and background
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Heebo:wght@300;400;500;700&display=swap');
    
    * {
        font-family: 'Heebo', sans-serif;
    }
    
    .main .block-container {
        background: linear-gradient(135deg, #f7fafc 0%, #edf2f7 50%, #e2e8f0 100%);
        min-height: 100vh;
    }
    
    .stApp {
        background: linear-gradient(135deg, #f0f4f8 0%, #d6e8f5 50%, #c8d8e4 100%);
    }
    
    .main-header {
        font-size: 2.8rem;
        font-weight: 700;
        text-align: center;
        color: #2D3748;
        margin-bottom: 2.5rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .question-container {
        background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
        padding: 2rem;
        border-radius: 18px;
        margin: 1.8rem 0;
        border-right: 6px solid #4299e1;
        box-shadow: 0 6px 20px rgba(66, 153, 225, 0.15);
        direction: rtl;
        text-align: right;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    
    .question-container:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(66, 153, 225, 0.2);
    }
    
    .question-container h4 {
        color: #2D3748;
        font-weight: 500;
        font-size: 1.3rem;
        margin: 0;
        direction: rtl;
        line-height: 1.6;
    }
    
    .score-display {
        font-size: 3.2rem;
        font-weight: bold;
        text-align: center;
        padding: 3rem;
        background: linear-gradient(135deg, #4299e1 0%, #667eea 50%, #764ba2 100%);
        color: white;
        border-radius: 25px;
        margin: 2.5rem 0;
        box-shadow: 0 10px 30px rgba(66, 153, 225, 0.4);
        direction: ltr;
    }
    
    .feedback-box {
        background: linear-gradient(135deg, #e6fffa 0%, #b2f5ea 100%);
        padding: 2.2rem;
        border-radius: 18px;
        margin: 1.8rem 0;
        border: 2px solid #4fd1c7;
        box-shadow: 0 6px 20px rgba(79, 209, 199, 0.15);
        direction: rtl;
        text-align: center;
    }
    
    .improvement-box {
        background: linear-gradient(135deg, #f0fff4 0%, #c6f6d5 100%);
        padding: 2.2rem;
        border-radius: 18px;
        margin: 1.8rem 0;
        border: 2px solid #68d391;
        box-shadow: 0 6px 20px rgba(104, 211, 145, 0.15);
        direction: rtl;
        text-align: right;
    }
    
    .progress-stats {
        background: linear-gradient(135deg, #ffffff 0%, #f7fafc 100%);
        padding: 2rem;
        border-radius: 18px;
        box-shadow: 0 6px 20px rgba(0,0,0,0.1);
        margin: 1.2rem 0;
        border-top: 4px solid #4299e1;
        text-align: center;
        transition: transform 0.2s ease;
    }
    
    .progress-stats:hover {
        transform: translateY(-3px);
    }
    
    .chart-container {
        background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
        padding: 2rem;
        border-radius: 18px;
        margin: 2rem 0;
        box-shadow: 0 6px 20px rgba(0,0,0,0.1);
        border: 1px solid #e2e8f0;
    }
    
    .chart-title {
        text-align: center;
        font-size: 1.5rem;
        font-weight: 600;
        color: #2D3748;
        margin-bottom: 1.5rem;
    }
    
    .input-container {
        background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
        padding: 2rem;
        border-radius: 18px;
        margin: 1.8rem 0;
        border: 2px solid #e2e8f0;
        box-shadow: 0 6px 20px rgba(0,0,0,0.1);
    }
    
    .stSlider > div > div {
        direction: ltr;
    }
    
    .stNumberInput > div > div {
        direction: ltr;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
        background: rgba(255, 255, 255, 0.3);
        padding: 0.5rem;
        border-radius: 15px;
        justify-content: center;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: linear-gradient(135deg, #ffffff 0%, #f1f5f9 100%);
        border-radius: 12px;
        padding: 1rem 2rem;
        border: 2px solid transparent;
        font-weight: 500;
    }
