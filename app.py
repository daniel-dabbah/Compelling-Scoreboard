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
        text-align: center;
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
    
    .assessment-input-container {
        background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        border: 1px solid #e2e8f0;
    }
    
    .stSlider > div > div {
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
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #4299e1 0%, #667eea 100%);
        color: white;
        border-color: #4299e1;
        box-shadow: 0 4px 15px rgba(66, 153, 225, 0.3);
    }
</style>
""", unsafe_allow_html=True)

# Assessment subjects and questions in Hebrew
SUBJECTS = ["אנגלית", "ספרות", "תנ״ך", "מתמטיקה", "היסטוריה", "עברית", "מגמה א'", "מגמה ב'", "מגמה ג'"]
ADDITIONAL_QUESTIONS = [
    "עד כמה אני מרגיש שאני מצליח להחזיר לעצמי את האנרגיה שאני מוציא על הלימודים",
    "עד כמה אני מרגיש שאני עוזר לאחרים מהכיתה"
]

def get_feedback_message(score):
    """Generate short feedback based on the total score"""
    if score >= 90:
        return "מצוין! כל הכבוד!"
    elif score >= 80:
        return "עבודה טובה!"
    elif score >= 70:
        return "יפה, ממשיכים לעבוד!"
    else:
        return "עבודה טובה, בוא נשפר עוד קצת!"

def load_manual_assessments():
    """Load manually entered assessments from session state"""
    if 'manual_assessments' not in st.session_state:
        st.session_state.manual_assessments = {}
    return st.session_state.manual_assessments

def save_manual_assessments(assessments):
    """Save manually entered assessments to session state"""
    st.session_state.manual_assessments = assessments

def create_simple_progress_chart(assessments):
    """Create a simple progress chart using Streamlit's built-in chart"""
    if not assessments:
        return None
    
    # Filter out empty assessments and sort by assessment number
    valid_assessments = [(num, score) for num, score in assessments.items() if score is not None and score > 0]
    valid_assessments.sort(key=lambda x: x[0])
    
    if not valid_assessments:
        return None
    
    return valid_assessments

def display_statistics(assessments):
    """Display progress statistics in Hebrew"""
    # Filter valid assessments
    valid_scores = [score for score in assessments.values() if score is not None and score > 0]
    
    if not valid_scores:
        return
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        latest_score = valid_scores[-1]
        st.markdown(f"""
        <div class="progress-stats">
            <h3 style="color: #2D3748; margin: 0;">הציון האחרון שלי</h3>
            <h2 style="color: #4299e1; margin: 5px 0;">{latest_score}/100</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        best_score = max(valid_scores)
        st.markdown(f"""
        <div class="progress-stats">
            <h3 style="color: #2D3748; margin: 0;">הציון הכי טוב שלי</h3>
            <h2 style="color: #68d391; margin: 5px 0;">{best_score}/100</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        average_score = round(sum(valid_scores) / len(valid_scores), 1)
        st.markdown(f"""
        <div class="progress-stats">
            <h3 style="color: #2D3748; margin: 0;">הממוצע שלי</h3>
            <h2 style="color: #9f7aea; margin: 5px 0;">{average_score}/100</h2>
        </div>
        """, unsafe_allow_html=True)

def main():
    # Header
    st.markdown('<h1 class="main-header">הערכה פנימית - לוח תוצאות</h1>', unsafe_allow_html=True)
    
    # Initialize session state
    if 'current_responses' not in st.session_state:
        st.session_state.current_responses = {}
    if 'show_results' not in st.session_state:
        st.session_state.show_results = False
    
    # Create tabs
    tab1, tab2 = st.tabs(["הערכה חדשה", "להסתכל על ההתקדמות שלי"])
    
    with tab1:
        if not st.session_state.show_results:
            st.markdown("<div style='text-align: center; margin-bottom: 2rem;'><p style='font-size: 1.1rem; color: #2D3748;'>תן לכל מקצוע ציון מ-1 (בכלל לא בטוח) עד 10 (מאוד בטוח) - לפי איך שאתה מרגיש ממש עכשיו.</p></div>", unsafe_allow_html=True)
            
            # Display all questions at once
            with st.form("assessment_form"):
                responses = {}
                question_index = 0
                
                # Subject questions
                for i, subject in enumerate(SUBJECTS):
                    st.markdown(f"""
                    <div class="question-container">
                        <h4>עד כמה אני מרגיש שאני שולט בחומר ב{subject}?</h4>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    responses[question_index] = st.slider(
                        f"הציון שלי ב{subject}:",
                        min_value=1,
                        max_value=10,
                        value=st.session_state.current_responses.get(question_index, 5),
                        key=f"q_{question_index}",
                        label_visibility="collapsed"
                    )
                    question_index += 1
                
                # Additional questions
                for i, question in enumerate(ADDITIONAL_QUESTIONS):
                    st.markdown(f"""
                    <div class="question-container">
                        <h4>{question}?</h4>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    responses[question_index] = st.slider(
                        f"השאלה מס׳ {question_index + 1}:",
                        min_value=1,
                        max_value=10,
                        value=st.session_state.current_responses.get(question_index, 5),
                        key=f"q_{question_index}",
                        label_visibility="collapsed"
                    )
                    question_index += 1
                
                # Submit button
                submitted = st.form_submit_button("לשלוח את ההערכה", type="primary", use_container_width=True)
                
                if submitted:
                    st.session_state.current_responses = responses
                    st.session_state.show_results = True
                    st.rerun()
        
        else:
            # Show results
            responses = st.session_state.current_responses
            total_score = round((sum(responses.values()) / ((len(SUBJECTS) + len(ADDITIONAL_QUESTIONS)) * 10)) * 100, 1)
            
            # Display score
            st.markdown(f"""
            <div class="score-display">
                הציון הכללי שלי: {total_score}/100
            </div>
            """, unsafe_allow_html=True)
            
            # Display general feedback
            feedback = get_feedback_message(total_score)
            if feedback:
                st.markdown(f"""
                <div class="feedback-box">
                    <p style="font-size: 1.1rem; margin: 0; text-align: center; color: #2D3748; font-weight: 500;">{feedback}</p>
                </div>
                """, unsafe_allow_html=True)
            
            # Button to take new assessment
            if st.button("לעשות הערכה חדשה", type="primary", use_container_width=True):
                st.session_state.current_responses = {}
                st.session_state.show_results = False
                st.rerun()
    
    with tab2:
        st.markdown("<h3 style='text-align: center;'>הזן את הציונים שלך כדי לראות התקדמות</h3>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #666; margin-bottom: 2rem;'>הזן ציונים מ-0 עד 100 עבור עד 20 הערכות</p>", unsafe_allow_html=True)
        
        # Load existing manual assessments
        manual_assessments = load_manual_assessments()
        
        # Create input fields for up to 20 assessments
        with st.form("manual_assessments_form"):
            st.markdown("### הזן את הציונים שלך:")
            
            new_assessments = {}
            
            # Create columns for better layout
            cols = st.columns(4)
            for i in range(1, 21):
                col_index = (i - 1) % 4
                with cols[col_index]:
                    current_value = manual_assessments.get(i, 0)
                    score = st.number_input(
                        f"הערכה {i}:",
                        min_value=0,
                        max_value=100,
                        value=current_value,
                        key=f"assessment_{i}",
                        step=1
                    )
                    new_assessments[i] = score if score > 0 else None
            
            # Save button
            if st.form_submit_button("לשמור ולהראות גרף", type="primary", use_container_width=True):
                save_manual_assessments(new_assessments)
                st.rerun()
        
        # Show progress if there are valid assessments
        valid_assessments = {k: v for k, v in manual_assessments.items() if v is not None and v > 0}
        
        if valid_assessments:
            st.markdown("---")
            st.markdown("<h3 style='text-align: center;'>ההתקדמות שלי</h3>", unsafe_allow_html=True)
            
            # Statistics
            display_statistics(manual_assessments)
            
            # Progress chart
            chart_data = create_simple_progress_chart(manual_assessments)
            if chart_data:
                st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                st.markdown('<div class="chart-title">הגרף של ההתקדמות שלי</div>', unsafe_allow_html=True)
                
                # Create chart data for Streamlit
                chart_dict = {}
                for assessment_num, score in chart_data:
                    chart_dict[f"הערכה {assessment_num}"] = score
                
                # Display as line chart
                st.line_chart(chart_dict, height=400)
                st.markdown('</div>', unsafe_allow_html=True)
            

        
        else:
            st.info("הזן לפחות ציון אחד כדי לראות את הגרף שלך!")

if __name__ == "__main__":
    main()
