# 🌱 Green Code Checker

A comprehensive Python code analyzer that evaluates code for sustainability, efficiency, and environmental impact. This tool promotes eco-conscious coding practices by providing actionable insights to write more efficient, secure, and environmentally-friendly code.

![Green Code Checker](https://img.shields.io/badge/Status-Active-green)
![Python](https://img.shields.io/badge/Python-3.11-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red)
![License](https://img.shields.io/badge/License-MIT-yellow)


## 🚀 Key Features

- ♻️ **Green Score** (0–100) based on code efficiency and sustainability
- 🔒 **Security Analysis** (detects `eval`, `exec`, hardcoded credentials, injections)
- 🧠 **AI-Powered Suggestions** for performance and optimization
- 📊 **Interactive Dashboard** with real-time Plotly visualizations
- 🌍 **Carbon Footprint Estimation** (energy, CO₂, real-world equivalents)
- 🏆 **Gamification** with user levels, badges, and global leaderboard
- 🧾 **Downloadable Reports** for professional insights and sharing

---

## 🎥All  Demo cases included:

▶️ [Watch Demo](https://drive.google.com/file/d/13RmLPfjQ0lXe3h6fbQI9l6x9AapQvmAJ/view?usp=drivesdk)

## Example Output for High Carbon Cost Code (Heavy Looping)
![2025-06-19 (1)](https://github.com/user-attachments/assets/cd71574d-b382-4a46-b4eb-32d84a7faac4)
![2025-06-19 (2)](https://github.com/user-attachments/assets/2b46bfe4-a91b-45f0-b012-7110ee5e38fa)
![2025-06-19 (4)](https://github.com/user-attachments/assets/946ac045-ad8d-4ebe-89c1-e6e9b7b0bfbd)
![2025-06-19 (5)](https://github.com/user-attachments/assets/b63414d8-47f8-4af8-affb-69d0390c4920)


---

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

| Layer       | Tools/Frameworks                    |
|-------------|-------------------------------------|
| Frontend    | Streamlit, Plotly                   |
| Backend     | Python (AST), AI logic, Refactoring |
| Database    | PostgreSQL, SQLAlchemy              |
| Analytics   | Custom carbon model + visual stats  |

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


### Quick Start
1. **Clone or access the project**
2. **Run the application**:
   ```bash
   streamlit run streamlit_app.py --server.port 5000
   ```
3. **Access the web interface** at `http://localhost:5000`


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



## 🌍 Environmental Impact

### Carbon Footprint Calculation
- **Energy Consumption**: Estimated microjoules based on code complexity
- **Carbon Emissions**: CO2 equivalent calculations
- **Efficiency Ratings**: A+ to F scale classification
- **Real-world Equivalents**: Smartphone charges, car miles, etc.


## 🚀 Deployment

This application is designed for deployment on Replit:

1. **Environment**: Nix-based with automatic dependency management
2. **Database**: Built-in PostgreSQL integration
3. **Hosting**: Autoscale deployment with public access
4. **Configuration**: Streamlit server on port 5000

## 🤝 Contribution Welcome!
Contributions are welcome! Feel free to fork the repo and submit a pull request.

**Let's build together 💚!**  
Make sure to check our [guidelines](#guidelines) before you start.

<details id="guidelines">
  <summary>Development Guidelines</summary>

- Follow PEP 8 Python style guidelines  
- Add comprehensive docstrings and comments  
- Include unit tests for new features  
- Update documentation for API changes  

</details>

 
### Feature Requests
- Environmental impact enhancements
- Additional programming language support
- Advanced AI optimization algorithms
- Extended gamification mechanics

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
