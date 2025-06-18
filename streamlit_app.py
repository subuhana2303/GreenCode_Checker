import streamlit as st
import ast
import io
from datetime import datetime
from analyzer import CodeAnalyzer
from suggestions import SuggestionEngine
from report_generator import ReportGenerator
from sample_code import SAMPLE_INEFFICIENT_CODE

def main():
    st.set_page_config(
        page_title="🌿 Green Code Checker",
        page_icon="🌿",
        layout="wide"
    )
    
    # Header
    st.title("🌿 Green Code Checker")
    st.subheader("A Sustainable Python Code Analyzer")
    st.markdown("---")
    
    # Introduction
    st.markdown("""
    Welcome to Green Code Checker! This tool analyzes your Python code for energy-inefficient patterns 
    and provides a **Green Score** (out of 100) along with smart coding suggestions to help you write 
    cleaner, more sustainable code.
    
    **What we analyze:**
    - 🔄 While loops that could be optimized
    - 📦 Unused imports
    - 🔢 Inefficient `range(len(...))` patterns
    - 🛠️ Function usage patterns
    """)
    
    # Sidebar
    with st.sidebar:
        st.header("⚙️ Settings")
        username = st.text_input("Your Name (for report)", value="Developer")
        
        st.header("📋 Quick Actions")
        if st.button("Load Sample Code"):
            st.session_state.sample_loaded = True
        
        st.header("ℹ️ About")
        st.markdown("""
        This tool promotes **Green AI** and **eco-conscious coding** practices. 
        Perfect for students, open-source projects, and portfolios!
        """)
    
    # Main content area
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.header("📝 Code Input")
        
        # Load sample code if requested
        default_code = ""
        if st.session_state.get('sample_loaded', False):
            default_code = SAMPLE_INEFFICIENT_CODE
            st.session_state.sample_loaded = False
        
        code_input = st.text_area(
            "Paste your Python code here:",
            value=default_code,
            height=400,
            placeholder="# Enter your Python code here...\nprint('Hello, World!')"
        )
        
        analyze_button = st.button("🔍 Analyze Code", type="primary", use_container_width=True)
    
    with col2:
        st.header("📊 Analysis Results")
        
        if analyze_button and code_input.strip():
            try:
                # Validate Python syntax
                ast.parse(code_input)
                
                # Initialize components
                analyzer = CodeAnalyzer()
                suggestion_engine = SuggestionEngine()
                
                # Analyze code
                with st.spinner("Analyzing your code..."):
                    analysis_results = analyzer.analyze(code_input)
                    suggestions = suggestion_engine.generate_suggestions(analysis_results)
                    green_score = analyzer.calculate_green_score(analysis_results)
                
                # Display results
                display_results(analysis_results, suggestions, green_score)
                
                # Generate and offer report download
                report_generator = ReportGenerator()
                report_content = report_generator.generate_report(
                    username, code_input, analysis_results, suggestions, green_score
                )
                
                st.download_button(
                    label="📄 Download Report",
                    data=report_content,
                    file_name=f"green_code_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                    mime="text/plain",
                    use_container_width=True
                )
                
            except SyntaxError as e:
                st.error(f"❌ **Syntax Error:** {str(e)}")
                st.error("Please check your Python code for syntax errors.")
            except Exception as e:
                st.error(f"❌ **Analysis Error:** {str(e)}")
                st.error("An unexpected error occurred during analysis.")
        
        elif analyze_button:
            st.warning("⚠️ Please enter some Python code to analyze.")

def display_results(analysis_results, suggestions, green_score):
    """Display the analysis results in a structured format"""
    
    # Green Score
    score_color = "green" if green_score >= 70 else "orange" if green_score >= 40 else "red"
    st.markdown(f"""
    <div style="text-align: center; padding: 20px; border-radius: 10px; background-color: #f0f2f6;">
        <h2 style="color: {score_color};">🌿 Green Score: {green_score}/100</h2>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Analysis Details
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 Code Statistics")
        st.metric("Lines of Code", analysis_results.get('lines_of_code', 0))
        st.metric("Functions Found", analysis_results.get('function_count', 0))
        st.metric("Imports Found", analysis_results.get('import_count', 0))
    
    with col2:
        st.subheader("⚠️ Issues Found")
        st.metric("While Loops", analysis_results.get('while_loop_count', 0))
        st.metric("Unused Imports", analysis_results.get('unused_imports_count', 0))
        st.metric("Inefficient Patterns", analysis_results.get('inefficient_patterns_count', 0))
    
    # Detailed Issues
    if analysis_results.get('issues'):
        st.subheader("🔍 Detailed Issues")
        for i, issue in enumerate(analysis_results['issues'], 1):
            with st.expander(f"Issue {i}: {issue['type']}"):
                st.write(f"**Line {issue['line']}:** {issue['description']}")
                if issue.get('suggestion'):
                    st.info(f"💡 **Suggestion:** {issue['suggestion']}")
    
    # Suggestions
    if suggestions:
        st.subheader("💡 Optimization Suggestions")
        for i, suggestion in enumerate(suggestions, 1):
            st.write(f"{i}. {suggestion}")

if __name__ == "__main__":
    main()
