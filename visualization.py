import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import streamlit as st
from typing import Dict, Any, List

try:
    import numpy as np
except ImportError:
    # Fallback for numpy issues
    class MockNumpy:
        def polyfit(self, x, y, deg):
            return [0.5, 10]  # Simple linear approximation
        def poly1d(self, coeffs):
            return lambda x: coeffs[0] * x + coeffs[1]
    np = MockNumpy()

class CodeVisualization:
    """Generates interactive charts and visualizations for code analysis"""
    
    def __init__(self):
        self.colors = {
            'primary': '#2E8B57',  # Sea Green
            'secondary': '#90EE90',  # Light Green
            'warning': '#FFD700',   # Gold
            'danger': '#FF6347',    # Tomato
            'info': '#87CEEB'       # Sky Blue
        }
    
    def create_green_score_gauge(self, green_score: int) -> go.Figure:
        """Create a gauge chart for the green score"""
        fig = go.Figure(go.Indicator(
            mode = "gauge+number+delta",
            value = green_score,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "Green Score"},
            delta = {'reference': 70},
            gauge = {
                'axis': {'range': [None, 100]},
                'bar': {'color': self._get_score_color(green_score)},
                'steps': [
                    {'range': [0, 40], 'color': "#FFE4E1"},
                    {'range': [40, 70], 'color': "#FFF8DC"},
                    {'range': [70, 100], 'color': "#F0FFF0"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 70
                }
            }
        ))
        
        fig.update_layout(
            height=300,
            font={'color': "darkblue", 'family': "Arial"}
        )
        
        return fig
    
    def create_code_stats_chart(self, analysis_results: Dict[str, Any]) -> go.Figure:
        """Create a bar chart showing code statistics"""
        stats = {
            'Functions': analysis_results.get('function_count', 0),
            'For Loops': analysis_results.get('for_loop_count', 0),
            'While Loops': analysis_results.get('while_loop_count', 0),
            'Imports': analysis_results.get('import_count', 0),
            'Issues Found': len(analysis_results.get('issues', []))
        }
        
        colors = [
            self.colors['primary'] if v == 0 or k == 'Functions' else 
            self.colors['danger'] if k in ['While Loops', 'Issues Found'] else 
            self.colors['warning'] if k == 'Imports' else 
            self.colors['info']
            for k, v in stats.items()
        ]
        
        fig = go.Figure(data=[
            go.Bar(
                x=list(stats.keys()),
                y=list(stats.values()),
                marker_color=colors,
                text=list(stats.values()),
                textposition='auto',
            )
        ])
        
        fig.update_layout(
            title="Code Structure Analysis",
            xaxis_title="Metrics",
            yaxis_title="Count",
            height=400,
            showlegend=False
        )
        
        return fig
    
    def create_issues_pie_chart(self, analysis_results: Dict[str, Any]) -> go.Figure:
        """Create a pie chart showing distribution of issues"""
        issues = analysis_results.get('issues', [])
        
        if not issues:
            fig = go.Figure(data=[go.Pie(
                labels=['No Issues Found'],
                values=[1],
                marker_colors=[self.colors['primary']]
            )])
            fig.update_layout(title="Issues Distribution", height=300)
            return fig
        
        issue_counts = {}
        for issue in issues:
            issue_type = issue['type'].replace('_', ' ').title()
            issue_counts[issue_type] = issue_counts.get(issue_type, 0) + 1
        
        fig = go.Figure(data=[go.Pie(
            labels=list(issue_counts.keys()),
            values=list(issue_counts.values()),
            hole=.3,
            marker_colors=[self.colors['danger'], self.colors['warning'], self.colors['info']][:len(issue_counts)]
        )])
        
        fig.update_layout(
            title="Issues Distribution",
            height=300,
            showlegend=True
        )
        
        return fig
    
    def create_complexity_radar(self, analysis_results: Dict[str, Any]) -> go.Figure:
        """Create a radar chart for code complexity metrics"""
        # Normalize values to 0-10 scale for better visualization
        metrics = {
            'Code Lines': min(10, analysis_results.get('lines_of_code', 0) / 10),
            'Functions': min(10, analysis_results.get('function_count', 0)),
            'Complexity': min(10, analysis_results.get('complexity_score', 0) / 5),
            'Loop Count': min(10, (analysis_results.get('for_loop_count', 0) + analysis_results.get('while_loop_count', 0))),
            'Import Count': min(10, analysis_results.get('import_count', 0) / 2),
            'Issue Density': min(10, len(analysis_results.get('issues', [])))
        }
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatterpolar(
            r=list(metrics.values()),
            theta=list(metrics.keys()),
            fill='toself',
            name='Current Code',
            line_color=self.colors['primary']
        ))
        
        # Add ideal/target line
        ideal_values = [3, 5, 2, 2, 3, 0]  # Ideal values for each metric
        fig.add_trace(go.Scatterpolar(
            r=ideal_values,
            theta=list(metrics.keys()),
            fill='toself',
            name='Target',
            line_color=self.colors['secondary'],
            opacity=0.6
        ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 10]
                )),
            showlegend=True,
            title="Code Complexity Radar",
            height=400
        )
        
        return fig
    
    def create_score_history_chart(self, history_data: List[Dict]) -> go.Figure:
        """Create a line chart showing green score history"""
        if not history_data:
            # Create empty chart with placeholder
            fig = go.Figure()
            fig.add_annotation(
                text="No history data available yet.<br>Analyze some code to start tracking!",
                xref="paper", yref="paper",
                x=0.5, y=0.5, xanchor='center', yanchor='middle',
                showarrow=False,
                font=dict(size=16, color="gray")
            )
            fig.update_layout(
                title="Green Score History",
                height=300,
                xaxis=dict(showgrid=False, showticklabels=False),
                yaxis=dict(showgrid=False, showticklabels=False)
            )
            return fig
        
        df = pd.DataFrame(history_data)
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df['timestamp'],
            y=df['green_score'],
            mode='lines+markers',
            name='Green Score',
            line=dict(color=self.colors['primary'], width=3),
            marker=dict(size=8)
        ))
        
        # Add trend line
        if len(df) > 1:
            z = np.polyfit(range(len(df)), df['green_score'], 1)
            p = np.poly1d(z)
            fig.add_trace(go.Scatter(
                x=df['timestamp'],
                y=p(range(len(df))),
                mode='lines',
                name='Trend',
                line=dict(color=self.colors['warning'], width=2, dash='dash'),
                opacity=0.7
            ))
        
        fig.update_layout(
            title="Green Score Progress Over Time",
            xaxis_title="Analysis Date",
            yaxis_title="Green Score",
            height=300,
            yaxis=dict(range=[0, 100])
        )
        
        return fig
    
    def _get_score_color(self, score: int) -> str:
        """Get color based on score value"""
        if score >= 80:
            return self.colors['primary']
        elif score >= 60:
            return self.colors['warning']
        else:
            return self.colors['danger']
    
    def display_environmental_impact(self, analysis_results: Dict[str, Any], green_score: int):
        """Display environmental impact metrics"""
        # Calculate estimated environmental impact
        lines_of_code = analysis_results.get('lines_of_code', 0)
        issues_count = len(analysis_results.get('issues', []))
        
        # Mock calculations for environmental impact
        base_energy = lines_of_code * 0.1  # Base energy in micro-joules
        inefficiency_penalty = issues_count * 2.5  # Additional energy per issue
        total_energy = base_energy + inefficiency_penalty
        
        # Potential savings with optimizations
        potential_savings = inefficiency_penalty * 0.7  # 70% reduction possible
        co2_saved = potential_savings * 0.0001  # Convert to grams CO2
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                label="🔋 Estimated Energy Usage",
                value=f"{total_energy:.1f} μJ",
                delta=f"-{potential_savings:.1f} μJ potential savings"
            )
        
        with col2:
            st.metric(
                label="🌍 CO₂ Impact",
                value=f"{co2_saved:.3f} g",
                delta="Potential reduction",
                delta_color="inverse"
            )
        
        with col3:
            efficiency_rating = "A+" if green_score >= 90 else "A" if green_score >= 80 else "B" if green_score >= 70 else "C" if green_score >= 60 else "D"
            st.metric(
                label="⚡ Efficiency Rating",
                value=efficiency_rating,
                delta=f"Score: {green_score}/100"
            )