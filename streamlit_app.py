import streamlit as st
import ast
import io
import json
from datetime import datetime
from analyzer import CodeAnalyzer
from suggestions import SuggestionEngine
from report_generator import ReportGenerator
from sample_code import SAMPLE_INEFFICIENT_CODE, get_sample_code, get_all_sample_types
from visualization import CodeVisualization
from history_tracker import HistoryTracker
from gamification import GamificationEngine
from security_checker import SecurityChecker
from ai_refactor import AIRefactorEngine
from carbon_calculator import CarbonCalculator
import plotly.graph_objects as go

# Disable complex dependencies to avoid numpy issues
PANDAS_AVAILABLE = False
PLOTLY_EXPRESS_AVAILABLE = False

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
    
    # Initialize components
    if 'history_tracker' not in st.session_state:
        st.session_state.history_tracker = HistoryTracker()
    if 'gamification' not in st.session_state:
        st.session_state.gamification = GamificationEngine()
    
    # Sidebar
    with st.sidebar:
        st.header("⚙️ Settings")
        username = st.text_input("Your Name (for report)", value="Developer")
        
        st.header("📋 Quick Actions")
        sample_types = get_all_sample_types()
        selected_sample = st.selectbox("Choose Sample Code:", [""] + sample_types)
        if st.button("Load Sample Code") and selected_sample:
            st.session_state.sample_loaded = selected_sample
        
        # User Level and Stats
        if username != "Developer":
            try:
                user_stats = st.session_state.history_tracker.get_user_stats(username)
                if user_stats and user_stats.get('total_analyses', 0) > 0:
                    level_info = st.session_state.gamification.calculate_user_level(user_stats)
                    
                    st.header("🏆 Your Progress")
                    st.write(f"**Level:** {level_info['level_name']}")
                    st.write(f"**Best Score:** {user_stats['best_score']}/100")
                    st.write(f"**Analyses:** {user_stats['total_analyses']}")
                    
                    if level_info['next_level']:
                        progress_bar = st.progress(level_info['progress_to_next'] / 100)
                        st.write(f"Progress to {level_info['next_level_name']}: {level_info['progress_to_next']:.0f}%")
            except Exception:
                st.info("Complete an analysis to see your progress!")
        
        # Global Leaderboard
        st.header("🥇 Leaderboard")
        leaderboard = st.session_state.history_tracker.get_leaderboard(5)
        if leaderboard:
            for i, leader in enumerate(leaderboard, 1):
                emoji = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else "🏆"
                st.write(f"{emoji} **{leader['username']}** - Avg: {leader['average_score']:.1f}/100")
        
        st.header("ℹ️ About")
        st.markdown("""
        This tool promotes **Green AI** and **eco-conscious coding** practices. 
        Perfect for students, open-source projects, and portfolios!
        
        **New Features:**
        - 📊 Interactive dashboards
        - 🏆 Achievement system
        - 📈 Score tracking
        - 🔒 Security analysis
        - ⚡ AI-powered refactoring
        """)
    
    # Main content area
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.header("📝 Code Input")
        
        # Load sample code if requested
        default_code = ""
        if st.session_state.get('sample_loaded', False):
            sample_type = st.session_state.sample_loaded
            if sample_type == True:  # Backward compatibility
                default_code = SAMPLE_INEFFICIENT_CODE
            else:
                default_code = get_sample_code(sample_type)
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
                visualizer = CodeVisualization()
                security_checker = SecurityChecker()
                ai_refactor = AIRefactorEngine()
                carbon_calc = CarbonCalculator()
                
                # Analyze code
                with st.spinner("Analyzing your code..."):
                    analysis_results = analyzer.analyze(code_input)
                    suggestions = suggestion_engine.generate_suggestions(analysis_results)
                    green_score = analyzer.calculate_green_score(analysis_results)
                    security_analysis = security_checker.analyze_security(code_input)
                
                # Calculate additional metrics for database storage
                energy_data = carbon_calc.calculate_energy_consumption(analysis_results)
                carbon_data = carbon_calc.calculate_carbon_footprint(energy_data)
                
                # Store in history with enhanced data
                st.session_state.history_tracker.add_analysis(
                    username, green_score, analysis_results, code_input[:100],
                    security_analysis['security_score'],
                    energy_data['total_energy_uj'],
                    carbon_data['carbon_emissions_g']
                )
                
                # Display results with enhanced visualizations
                display_enhanced_results(analysis_results, suggestions, green_score, 
                                       security_analysis, visualizer, username, carbon_calc)
                
                # Show AI refactoring suggestions
                if st.button("🤖 Generate AI Refactor Suggestions", use_container_width=True):
                    with st.spinner("Generating optimized code..."):
                        refactor_results = ai_refactor.generate_refactored_code(code_input, analysis_results)
                        display_refactor_suggestions(refactor_results)
                
                # Generate and offer report download
                report_generator = ReportGenerator()
                report_content = report_generator.generate_report(
                    username, code_input, analysis_results, suggestions, green_score
                )
                
                col1, col2 = st.columns(2)
                with col1:
                    st.download_button(
                        label="📄 Download Report",
                        data=report_content,
                        file_name=f"green_code_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                        mime="text/plain",
                        use_container_width=True
                    )
                
                with col2:
                    # LinkedIn sharing feature
                    if st.button("🔗 Share on LinkedIn", use_container_width=True):
                        user_stats = st.session_state.history_tracker.get_user_stats(username)
                        level_info = st.session_state.gamification.calculate_user_level(user_stats)
                        badge_text = st.session_state.gamification.get_level_badge_text(level_info, user_stats)
                        st.text_area("Copy this text to share on LinkedIn:", badge_text, height=200)
                
            except SyntaxError as e:
                st.error(f"❌ **Syntax Error:** {str(e)}")
                st.error("Please check your Python code for syntax errors.")
            except Exception as e:
                st.error(f"❌ **Analysis Error:** {str(e)}")
                st.error("An unexpected error occurred during analysis.")
        
        elif analyze_button:
            st.warning("⚠️ Please enter some Python code to analyze.")

def display_enhanced_results(analysis_results, suggestions, green_score, security_analysis, visualizer, username, carbon_calc):
    """Display enhanced analysis results with visualizations and gamification"""
    
    # Create tabs for different views
    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(["📊 Dashboard", "🔍 Details", "🔒 Security", "🏆 Achievements", "📈 History", "🌍 Carbon Impact", "🗃️ Database"])
    
    with tab1:
        # Green Score Gauge
        col1, col2 = st.columns([1, 1])
        
        with col1:
            gauge_fig = visualizer.create_green_score_gauge(green_score)
            st.plotly_chart(gauge_fig, use_container_width=True)
        
        with col2:
            # Environmental Impact
            visualizer.display_environmental_impact(analysis_results, green_score)
        
        # Charts
        col1, col2 = st.columns(2)
        
        with col1:
            stats_chart = visualizer.create_code_stats_chart(analysis_results)
            st.plotly_chart(stats_chart, use_container_width=True)
        
        with col2:
            issues_chart = visualizer.create_issues_pie_chart(analysis_results)
            st.plotly_chart(issues_chart, use_container_width=True)
        
        # Complexity Radar
        complexity_radar = visualizer.create_complexity_radar(analysis_results)
        st.plotly_chart(complexity_radar, use_container_width=True)
    
    with tab2:
        # Detailed Issues
        if analysis_results.get('issues'):
            st.subheader("🔍 Detailed Issues")
            for i, issue in enumerate(analysis_results['issues'], 1):
                with st.expander(f"Issue {i}: {issue['type'].replace('_', ' ').title()}"):
                    st.write(f"**Line {issue['line']}:** {issue['description']}")
                    if issue.get('suggestion'):
                        st.info(f"💡 **Suggestion:** {issue['suggestion']}")
        
        # Suggestions
        if suggestions:
            st.subheader("💡 Optimization Suggestions")
            for i, suggestion in enumerate(suggestions, 1):
                st.write(f"{i}. {suggestion}")
    
    with tab3:
        # Security Analysis
        st.subheader(f"🔒 Security Analysis - Risk Level: {security_analysis['risk_level']}")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Security Score", f"{security_analysis['security_score']}/100")
        with col2:
            st.metric("High Risk Issues", security_analysis['high_risk_count'])
        with col3:
            st.metric("Total Vulnerabilities", security_analysis['total_vulnerabilities'])
        
        if security_analysis['security_issues']:
            st.subheader("🚨 Security Issues Found")
            for issue in security_analysis['security_issues']:
                severity_color = "🔴" if issue['severity'] == 'HIGH' else "🟡" if issue['severity'] == 'MEDIUM' else "🟢"
                with st.expander(f"{severity_color} {issue['severity']} - Line {issue['line']}"):
                    st.write(f"**Issue:** {issue['description']}")
                    st.info(f"**Recommendation:** {issue['suggestion']}")
        
        # Security recommendations
        st.subheader("🛡️ Security Best Practices")
        checker = SecurityChecker()
        security_recs = checker.get_security_recommendations(security_analysis)
        for rec in security_recs:
            st.write(f"• {rec}")
    
    with tab4:
        # Gamification System
        st.subheader("🏆 Achievements & Progress")
        
        try:
            user_stats = st.session_state.history_tracker.get_user_stats(username)
            
            if user_stats and user_stats.get('total_analyses', 0) > 0:
                gamification = GamificationEngine()
                level_info = gamification.calculate_user_level(user_stats)
                
                # Level Progress
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.write(f"### Level {level_info['current_level']}: {level_info['level_name']}")
                    progress = level_info['progress_to_next'] / 100.0
                    st.progress(progress, text=f"Progress to next level: {level_info['progress_to_next']:.1f}%")
                    
                    if level_info['current_level'] < 6:
                        st.write(f"**Next Level:** {level_info['next_level_name']} (Need {level_info['points_to_next']} more points)")
                    else:
                        st.write("Maximum Level Achieved!")
                
                with col2:
                    st.write(f"## 🏅")
                    st.write(f"**{level_info['level_name']}**")
                
                # User Statistics
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Total Analyses", user_stats.get('total_analyses', 0))
                with col2:
                    st.metric("Best Score", f"{user_stats.get('best_score', 0)}/100")
                with col3:
                    st.metric("Average Score", f"{user_stats.get('average_score', 0):.1f}/100")
                
                # Achievement System
                user_history = st.session_state.history_tracker.get_history(username)
                achievements = gamification.check_achievements(user_history, user_stats)
                
                if achievements:
                    st.subheader("🏆 Unlocked Achievements")
                    for achievement in achievements:
                        with st.expander(f"🏅 {achievement['name']}"):
                            st.write(achievement['description'])
                            if achievement.get('unlocked_date'):
                                st.caption(f"Unlocked: {achievement['unlocked_date']}")
                
                # LinkedIn Sharing
                st.subheader("📱 Share Your Achievement")
                badge_text = gamification.get_level_badge_text(level_info, user_stats)
                
                # URL encode the badge text for LinkedIn sharing
                encoded_summary = badge_text.replace(' ', '%20').replace('\n', '%0A')
                linkedin_url = f"https://www.linkedin.com/sharing/share-offsite/?url=https://replit.com&title=Green%20Code%20Achievement&summary={encoded_summary}"
                
                col1, col2 = st.columns([1, 1])
                with col1:
                    if st.button("📱 Share on LinkedIn"):
                        st.success("LinkedIn sharing link generated!")
                        st.write("Click the link below to share your achievement:")
                        st.markdown(f"[Share on LinkedIn]({linkedin_url})")
                with col2:
                    if st.button("📋 Copy Badge Text"):
                        st.code(badge_text, language=None)
                        st.success("Badge text displayed above - copy and paste to share!")
            
            else:
                st.info("Complete your first analysis to start earning achievements!")
                st.subheader("🎯 Available Achievements")
                st.write("- **First Steps**: Complete your first code analysis")
                st.write("- **Improving**: Achieve a score of 80 or higher")
                st.write("- **Green Champion**: Achieve a perfect score of 100")
                st.write("- **Consistency**: Complete analyses 5 days in a row")
                
        except Exception as e:
            st.error("Achievement system temporarily unavailable")
            st.info("Complete an analysis to unlock the achievement system.")
    
    with tab5:
        # History and Analytics
        st.subheader("📈 Analysis History")
        
        try:
            user_history = st.session_state.history_tracker.get_history(username)
            
            if user_history and len(user_history) > 0:
                # Create history chart
                history_chart = visualizer.create_score_history_chart(user_history)
                st.plotly_chart(history_chart, use_container_width=True)
                
                # Recent analyses table
                st.subheader("📊 Recent Analyses")
                recent_analyses = user_history[-10:]
                
                for i, analysis in enumerate(reversed(recent_analyses), 1):
                    timestamp_str = str(analysis.get('timestamp', 'Unknown'))[:19]
                    with st.expander(f"Analysis {len(recent_analyses) - i + 1}: Score {analysis['green_score']}/100 - {timestamp_str}"):
                        col1, col2, col3 = st.columns(3)
                        
                        with col1:
                            st.write(f"**Score:** {analysis['green_score']}/100")
                            st.write(f"**Lines:** {analysis.get('lines_of_code', 'N/A')}")
                        
                        with col2:
                            st.write(f"**Issues:** {analysis.get('issues_count', 'N/A')}")
                            st.write(f"**Functions:** {analysis.get('function_count', 'N/A')}")
                        
                        with col3:
                            st.write(f"**Complexity:** {analysis.get('complexity_score', 'N/A')}")
                            st.write(f"**Security:** {analysis.get('security_score', 100)}/100")
                        
                        if analysis.get('code_preview'):
                            preview = str(analysis['code_preview'])
                            st.code(preview[:200] + "..." if len(preview) > 200 else preview, language='python')
                
                # Export functionality
                if st.button("📥 Export History as CSV"):
                    try:
                        csv_data = st.session_state.history_tracker.export_history(username)
                        st.download_button(
                            label="Download CSV",
                            data=csv_data,
                            file_name=f"{username}_green_code_history.csv",
                            mime="text/csv"
                        )
                    except Exception as e:
                        st.error("Export temporarily unavailable")
            
            else:
                st.info("No analysis history available yet. Complete some code analyses to see your progress here!")
                st.subheader("📊 What you'll see here:")
                st.write("- Interactive chart showing your score progression over time")
                st.write("- Detailed history of all your code analyses")
                st.write("- Ability to export your data as CSV")
                st.write("- Code snippets from previous analyses")
                
        except Exception as e:
            st.error("History system temporarily unavailable")
            st.info("Complete an analysis to start building your history.")
    
    with tab6:
        # Carbon Impact Analysis
        st.subheader("🌍 Environmental Impact Analysis")
        
        energy_data = carbon_calc.calculate_energy_consumption(analysis_results)
        carbon_data = carbon_calc.calculate_carbon_footprint(energy_data)
        efficiency_rating = carbon_calc.get_efficiency_rating(analysis_results)
        
        # Main metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Energy Consumption", f"{energy_data['total_energy_uj']:.1f} μJ")
        with col2:
            st.metric("Carbon Emissions", carbon_data['carbon_display'])
        with col3:
            st.metric("Efficiency Rating", efficiency_rating)
        
        # Energy breakdown chart
        if energy_data['energy_breakdown']:
            breakdown_data = [
                {'Category': k, 'Energy': v} 
                for k, v in energy_data['energy_breakdown'].items() if v > 0
            ]
            
            if breakdown_data:
                # Simple pie chart using graph objects only
                fig = go.Figure(data=[go.Pie(
                    labels=[item['Category'] for item in breakdown_data],
                    values=[item['Energy'] for item in breakdown_data],
                    title="Energy Consumption Breakdown"
                )])
                fig.update_layout(title="Energy Consumption Breakdown")
                st.plotly_chart(fig, use_container_width=True)
        
        # Environmental equivalents
        if carbon_data['equivalent_metrics']:
            st.subheader("🌱 Environmental Context")
            for metric, value in carbon_data['equivalent_metrics'].items():
                st.write(f"• **{metric.replace('_', ' ').title()}:** {value}")
        
        # Optimization potential
        issues_count = len(analysis_results.get('issues', []))
        if issues_count > 0:
            potential_savings = issues_count * 2.5  # Estimated energy savings
            st.subheader("⚡ Optimization Potential")
            st.info(f"By fixing the identified issues, you could potentially save approximately {potential_savings:.1f} μJ of energy per execution.")
        
        # Generate carbon report
        if st.button("📄 Generate Carbon Report"):
            carbon_report = carbon_calc.generate_carbon_report(analysis_results)
            st.text_area("Carbon Footprint Report", carbon_report, height=300)
    
    with tab7:
        # Database Analytics and Management
        st.subheader("🗃️ Database Analytics")
        
        # Check if database is available
        if st.session_state.history_tracker.use_database and st.session_state.history_tracker.db_manager:
            st.success("Database connection active")
            
            # Platform statistics
            try:
                analytics = st.session_state.history_tracker.db_manager.get_analytics_summary()
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Total Users", analytics.get('total_users', 0))
                with col2:
                    st.metric("Total Analyses", analytics.get('total_analyses', 0))
                with col3:
                    st.metric("Platform Avg Score", f"{analytics.get('average_platform_score', 0):.1f}/100")
                
                # Global leaderboard
                st.subheader("🏆 Global Leaderboard")
                leaderboard = st.session_state.history_tracker.get_leaderboard(10)
                if leaderboard:
                    # Create a simple table display
                    st.write("| Rank | Username | Avg Score | Best Score | Total Analyses |")
                    st.write("|------|----------|-----------|------------|----------------|")
                    for i, leader in enumerate(leaderboard, 1):
                        avg_score = leader.get('average_score', 0)
                        best_score = leader.get('best_score', 0)
                        total_analyses = leader.get('total_analyses', 0)
                        username = leader.get('username', 'Unknown')
                        st.write(f"| {i} | {username} | {avg_score:.1f} | {best_score} | {total_analyses} |")
                else:
                    st.info("No leaderboard data available yet.")
                
                # User analytics (if logged in as non-default user)
                if username != "Developer":
                    st.subheader(f"📊 Your Analytics - {username}")
                    user_history = st.session_state.history_tracker.get_history(username)
                    
                    if user_history:
                        if PANDAS_AVAILABLE:
                            # Create analytics charts with pandas
                            history_df = pd.DataFrame(user_history)
                            history_df['timestamp'] = pd.to_datetime(history_df['timestamp'])
                            
                            # Score trend over time
                            if PLOTLY_EXPRESS_AVAILABLE:
                                fig = px.line(history_df, x='timestamp', y='green_score', 
                                            title='Your Green Score Progress',
                                            labels={'green_score': 'Green Score', 'timestamp': 'Date'})
                            else:
                                fig = go.Figure()
                                fig.add_trace(go.Scatter(
                                    x=history_df['timestamp'],
                                    y=history_df['green_score'],
                                    mode='lines+markers',
                                    name='Green Score'
                                ))
                                fig.update_layout(title='Your Green Score Progress')
                            st.plotly_chart(fig, use_container_width=True)
                            
                            # Performance metrics
                            col1, col2 = st.columns(2)
                            with col1:
                                # Issues over time
                                recent_data = history_df.tail(10)
                                if PLOTLY_EXPRESS_AVAILABLE:
                                    fig2 = px.bar(recent_data, x='timestamp', y='issues_count',
                                                title='Issues Count (Last 10 Analyses)')
                                else:
                                    fig2 = go.Figure()
                                    fig2.add_trace(go.Bar(
                                        x=recent_data['timestamp'],
                                        y=recent_data['issues_count'],
                                        name='Issues Count'
                                    ))
                                    fig2.update_layout(title='Issues Count (Last 10 Analyses)')
                                st.plotly_chart(fig2, use_container_width=True)
                            
                            with col2:
                                # Code complexity trend
                                if PLOTLY_EXPRESS_AVAILABLE:
                                    fig3 = px.scatter(history_df, x='lines_of_code', y='green_score',
                                                    size='complexity_score', 
                                                    title='Score vs Code Complexity',
                                                    labels={'lines_of_code': 'Lines of Code'})
                                else:
                                    fig3 = go.Figure()
                                    fig3.add_trace(go.Scatter(
                                        x=history_df['lines_of_code'],
                                        y=history_df['green_score'],
                                        mode='markers',
                                        marker=dict(size=[entry['complexity_score'] for entry in user_history]),
                                        name='Complexity'
                                    ))
                                    fig3.update_layout(title='Score vs Code Complexity')
                                st.plotly_chart(fig3, use_container_width=True)
                        else:
                            # Simple fallback without pandas
                            st.write("Analytics charts require pandas. Showing basic statistics:")
                            scores = [entry['green_score'] for entry in user_history]
                            st.metric("Average Score", f"{sum(scores)/len(scores):.1f}")
                            st.metric("Recent Analyses", len(user_history[-5:]))
                    else:
                        st.info("No analysis history found for your account.")
                
            except Exception as e:
                st.error(f"Error loading database analytics: {str(e)}")
                
        else:
            st.warning("Database not available - using local file storage")
            st.info("Database features include: persistent user profiles, global leaderboards, achievement tracking, and advanced analytics.")
            
            # Show what would be available with database
            st.subheader("📈 Available with Database")
            st.write("- Persistent user profiles across sessions")
            st.write("- Global leaderboard with all users")
            st.write("- Achievement system with unlock tracking")
            st.write("- Advanced analytics and reporting")
            st.write("- Data export capabilities")
            st.write("- Multi-user collaboration features")

def display_refactor_suggestions(refactor_results):
    """Display AI-generated refactoring suggestions"""
    st.subheader("🤖 AI Refactoring Suggestions")
    
    # Improvement summary
    improvements = refactor_results.get('improvement_summary', [])
    if improvements:
        st.success("**Improvements Applied:**")
        for improvement in improvements:
            st.write(f"✅ {improvement}")
    
    # Before/After comparison
    st.subheader("📝 Optimized Code")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Before (Issues Highlighted):**")
        # Note: In a real implementation, you'd show the original code with issues highlighted
        st.info("Original code with inefficient patterns marked")
    
    with col2:
        st.write("**After (Optimized):**")
        optimized_code = refactor_results.get('optimized_full_code', 'No optimizations available')
        st.code(optimized_code, language='python')
    
    # Specific improvements
    specific_improvements = refactor_results.get('specific_improvements', {})
    if specific_improvements:
        st.subheader("🔧 Specific Optimizations")
        for improvement_id, suggestion in specific_improvements.items():
            with st.expander(f"Optimization: {improvement_id.replace('_', ' ').title()}"):
                st.code(suggestion, language='python')

if __name__ == "__main__":
    main()
