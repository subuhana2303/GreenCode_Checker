# 🌱 Green Code Checker

A comprehensive Python code analyzer that evaluates code for sustainability, efficiency, and environmental impact. This tool promotes eco-conscious coding practices by providing actionable insights to write more efficient, secure, and environmentally-friendly code.

![Green Code Checker](https://img.shields.io/badge/Status-Active-green)
![Python](https://img.shields.io/badge/Python-3.11-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red)
![License](https://img.shields.io/badge/License-MIT-yellow)

## 🚀 Features

### Core Analysis
- **Green Score (0-100)**: Comprehensive sustainability rating for your Python code
- **Security Analysis**: Detects vulnerabilities and security anti-patterns
- **Performance Optimization**: Identifies inefficient coding patterns
- **Carbon Footprint Calculation**: Estimates energy consumption and environmental impact

### Advanced Features
- **Interactive Dashboard**: Real-time visualizations with Plotly charts
- **AI-Powered Refactoring**: Intelligent code optimization suggestions
- **Gamification System**: User levels, achievements, and progress tracking
- **Global Leaderboards**: Compare your coding efficiency with others
- **LinkedIn Integration**: Share your achievements professionally
- **History Tracking**: Monitor improvement over time
- **Report Generation**: Download comprehensive analysis reports

### Multi-Tab Interface
1. **Dashboard**: Overview with green score gauge and key metrics
2. **Details**: In-depth analysis with specific issue breakdowns
3. **Security**: Vulnerability detection and security recommendations
4. **Achievements**: Gamification, levels, and sharing capabilities
5. **History**: Score progression and analysis timeline
6. **Carbon Impact**: Environmental footprint and efficiency ratings
7. **Database**: Platform statistics and global leaderboards

## 📁 Project Structure

```
green-code-checker/
├── streamlit_app.py          # Main Streamlit application
├── analyzer.py               # Core code analysis engine
├── suggestions.py            # Improvement recommendations
├── security_checker.py       # Security vulnerability detection
├── carbon_calculator.py      # Environmental impact calculations
├── ai_refactor.py           # AI-powered code optimization
├── gamification.py          # User levels and achievements
├── visualization.py         # Interactive charts and graphs
├── database.py              # PostgreSQL database operations
├── history_tracker.py       # Analysis history management
├── report_generator.py      # Report creation utilities
├── sample_code.py           # Sample code for testing
├── test_guide.md            # Comprehensive testing guide
├── replit.md                # Project documentation and preferences
└── README.md                # This file
```

## 🏗️ Architecture

### Frontend (Streamlit)
- **Framework**: Streamlit for rapid web application development
- **Layout**: Multi-tab interface with sidebar configuration
- **Visualizations**: Interactive charts using Plotly
- **User Experience**: Real-time analysis with progress indicators

### Backend Components
- **Analysis Engine**: AST-based Python code parsing and pattern detection
- **Database Layer**: PostgreSQL for user data and analytics
- **Security Module**: Pattern-based vulnerability detection
- **Carbon Calculator**: Energy consumption and environmental impact modeling

### Data Flow
1. **Input**: Python code via web interface
2. **Validation**: Syntax checking and AST parsing
3. **Analysis**: Multi-dimensional code evaluation
4. **Scoring**: Green score calculation (0-100)
5. **Enhancement**: AI-powered optimization suggestions
6. **Storage**: Database persistence for tracking
7. **Visualization**: Interactive dashboard presentation

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.11+
- PostgreSQL database (provided by Replit)
- Required packages (automatically installed)

### Dependencies
```python
streamlit>=1.28.0
plotly>=5.0.0
pandas>=1.5.0
numpy>=1.20.0
psycopg2-binary>=2.9.0
sqlalchemy>=2.0.0
matplotlib>=3.5.0
```

### Quick Start
1. **Clone or access the project**
2. **Run the application**:
   ```bash
   streamlit run streamlit_app.py --server.port 5000
   ```
3. **Access the web interface** at `http://localhost:5000`

## 📊 Usage Guide

### Basic Analysis
1. Enter your Python code in the main text area
2. Click "Analyze Code" to get instant feedback
3. Review your Green Score and detailed recommendations
4. Explore different tabs for comprehensive insights

### Advanced Features
- **Sample Code**: Use the sidebar dropdown to load test examples
- **User Profiles**: Enter a username to track progress over time
- **AI Refactoring**: Click the AI suggestions button for optimization
- **Achievement Tracking**: Complete analyses to unlock badges and levels
- **LinkedIn Sharing**: Share your coding achievements professionally

### Testing Examples

#### Basic Inefficient Code
```python
import os
import sys
import unused_module

def inefficient_function():
    data = []
    for i in range(len([1,2,3,4,5])):
        data.append(i * 2)
    
    counter = 0
    while counter < 10:
        print(f"Count: {counter}")
        counter += 1
    
    return data
```

#### Security Vulnerable Code
```python
import subprocess
password = "hardcoded123"
user_input = input("Enter command: ")
subprocess.call(user_input, shell=True)
eval("print('dangerous')")
```

## 🏆 Scoring System

### Green Score Components
- **Code Efficiency (40%)**: Loop optimization, built-in usage
- **Resource Management (25%)**: Memory and CPU efficiency patterns
- **Code Quality (20%)**: Structure, readability, best practices
- **Security Considerations (15%)**: Vulnerability detection

### Score Ranges
- **90-100**: Excellent - Highly optimized and secure
- **70-89**: Good - Minor improvements possible
- **50-69**: Average - Several optimization opportunities
- **30-49**: Below Average - Significant improvements needed
- **0-29**: Poor - Major refactoring required

## 🔒 Security Analysis

The security checker detects:
- Hardcoded credentials and secrets
- Command injection vulnerabilities
- Unsafe deserialization patterns
- SQL injection risks
- Path traversal vulnerabilities
- Use of dangerous functions (eval, exec)

## 🌍 Environmental Impact

### Carbon Footprint Calculation
- **Energy Consumption**: Estimated microjoules based on code complexity
- **Carbon Emissions**: CO2 equivalent calculations
- **Efficiency Ratings**: A+ to F scale classification
- **Real-world Equivalents**: Smartphone charges, car miles, etc.

## 🎯 Gamification System

### User Levels
1. **Eco Newbie** (0-99 points): Just starting your green coding journey
2. **Code Gardener** (100-299 points): Growing your sustainable coding skills
3. **Efficiency Expert** (300-599 points): Mastering optimization techniques
4. **Green Guru** (600-999 points): Leading by example in eco-coding
5. **Sustainability Champion** (1000+ points): Inspiring others to code green

### Achievement Types
- **Score-based**: Perfect scores, consistency achievements
- **Analysis-based**: Frequency milestones, improvement tracking
- **Special**: Security mastery, carbon reduction goals

## 📈 Analytics & Tracking

### Personal Analytics
- Score progression over time
- Improvement trends and patterns
- Achievement unlock timeline
- Carbon footprint reduction tracking

### Global Statistics
- Platform-wide usage metrics
- Community leaderboards
- Aggregate improvement trends
- Environmental impact summaries

## 🚀 Deployment

This application is designed for deployment on Replit:

1. **Environment**: Nix-based with automatic dependency management
2. **Database**: Built-in PostgreSQL integration
3. **Hosting**: Autoscale deployment with public access
4. **Configuration**: Streamlit server on port 5000

### Production Considerations
- Database connection pooling for scalability
- Error handling and graceful degradation
- User data privacy and security
- Performance optimization for larger codebases

## 🤝 Contributing

### Development Guidelines
- Follow PEP 8 Python style guidelines
- Add comprehensive docstrings and comments
- Include unit tests for new features
- Update documentation for API changes

### Feature Requests
- Environmental impact enhancements
- Additional programming language support
- Advanced AI optimization algorithms
- Extended gamification mechanics

## 📞 Support & Contact

For questions, suggestions, or contributions:
- Create an issue in the project repository
- Reach out through Replit community forums
- Share your achievements on LinkedIn using the built-in feature

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **Streamlit**: For the amazing web framework
- **Plotly**: For interactive visualization capabilities
- **Python AST**: For code analysis foundation
- **PostgreSQL**: For robust data persistence
- **Green AI Community**: For inspiration and best practices

---

**Made with 💚 for sustainable coding practices**

*Green Code Checker - Helping developers write more efficient, secure, and environmentally-conscious code, one analysis at a time.*