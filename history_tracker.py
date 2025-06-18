import json
import os
from datetime import datetime
from typing import List, Dict, Any
from database import DatabaseManager

class HistoryTracker:
    """Tracks and manages green score history with database persistence"""
    
    def __init__(self, use_database: bool = True):
        self.use_database = use_database
        self.db_manager = None
        
        if use_database:
            try:
                self.db_manager = DatabaseManager()
            except Exception as e:
                print(f"Database unavailable, falling back to file storage: {e}")
                self.use_database = False
        
        if not self.use_database:
            self.history_file = "green_score_history.json"
            self.history_data = self._load_history()
    
    def _load_history(self) -> List[Dict[str, Any]]:
        """Load history from JSON file"""
        try:
            if os.path.exists(self.history_file):
                with open(self.history_file, 'r') as f:
                    return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            pass
        return []
    
    def _save_history(self):
        """Save history to JSON file"""
        try:
            with open(self.history_file, 'w') as f:
                json.dump(self.history_data, f, indent=2, default=str)
        except Exception as e:
            print(f"Error saving history: {e}")
    
    def add_analysis(self, username: str, green_score: int, analysis_results: Dict[str, Any], 
                    code_snippet: str = "", security_score: int = 100, 
                    energy_consumption: float = 0.0, carbon_emissions: float = 0.0):
        """Add a new analysis to history"""
        if self.use_database and self.db_manager:
            return self.db_manager.save_analysis(
                username, green_score, analysis_results, security_score,
                energy_consumption, carbon_emissions, code_snippet
            )
        else:
            # Fallback to file storage
            entry = {
                'timestamp': datetime.now().isoformat(),
                'username': username,
                'green_score': green_score,
                'lines_of_code': analysis_results.get('lines_of_code', 0),
                'function_count': analysis_results.get('function_count', 0),
                'issues_count': len(analysis_results.get('issues', [])),
                'complexity_score': analysis_results.get('complexity_score', 0),
                'security_score': security_score,
                'energy_consumption': energy_consumption,
                'carbon_emissions': carbon_emissions,
                'code_preview': code_snippet[:100] + "..." if len(code_snippet) > 100 else code_snippet
            }
            
            self.history_data.append(entry)
            
            # Keep only last 50 entries to prevent file bloat
            if len(self.history_data) > 50:
                self.history_data = self.history_data[-50:]
            
            self._save_history()
            return True
    
    def get_history(self, username: str = None) -> List[Dict[str, Any]]:
        """Get history data, optionally filtered by username"""
        if self.use_database and self.db_manager:
            if username:
                return self.db_manager.get_user_history(username)
            else:
                # For admin purposes, could implement get_all_history
                return []
        else:
            if username:
                return [entry for entry in self.history_data if entry['username'] == username]
            return self.history_data
    
    def get_user_stats(self, username: str) -> Dict[str, Any]:
        """Get statistical summary for a specific user"""
        if self.use_database and self.db_manager:
            return self.db_manager.get_user_stats(username)
        else:
            user_history = self.get_history(username)
            
            if not user_history:
                return {
                    'total_analyses': 0,
                    'average_score': 0,
                    'best_score': 0,
                    'improvement_trend': 0,
                    'total_lines_analyzed': 0,
                    'recent_score': 0
                }
            
            scores = [entry['green_score'] for entry in user_history]
            
            # Calculate improvement trend (last 5 vs first 5 analyses)
            improvement_trend = 0
            if len(scores) >= 5:
                recent_avg = sum(scores[-5:]) / 5
                early_avg = sum(scores[:5]) / 5
                improvement_trend = recent_avg - early_avg
            
            return {
                'total_analyses': len(user_history),
                'average_score': sum(scores) / len(scores),
                'best_score': max(scores),
                'improvement_trend': improvement_trend,
                'total_lines_analyzed': sum(entry['lines_of_code'] for entry in user_history),
                'recent_score': scores[-1] if scores else 0
            }
    
    def get_leaderboard(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get top performers leaderboard"""
        if self.use_database and self.db_manager:
            return self.db_manager.get_leaderboard(limit)
        else:
            user_stats = {}
            
            for entry in self.history_data:
                username = entry['username']
                if username not in user_stats:
                    user_stats[username] = []
                user_stats[username].append(entry['green_score'])
            
            leaderboard = []
            for username, scores in user_stats.items():
                if scores:
                    avg_score = sum(scores) / len(scores)
                    best_score = max(scores)
                    total_analyses = len(scores)
                    
                    leaderboard.append({
                        'username': username,
                        'average_score': avg_score,
                        'best_score': best_score,
                        'total_analyses': total_analyses,
                        'composite_score': (avg_score * 0.7) + (best_score * 0.3)  # Weighted score
                    })
            
            # Sort by composite score
            leaderboard.sort(key=lambda x: x['composite_score'], reverse=True)
            return leaderboard[:limit]
    
    def clear_history(self):
        """Clear all history data"""
        self.history_data = []
        self._save_history()
    
    def export_history(self, username: str = None) -> str:
        """Export history as CSV format"""
        history = self.get_history(username)
        if not history:
            return "No history data available"
        
        csv_lines = ["Timestamp,Username,Green Score,Lines of Code,Functions,Issues,Complexity"]
        
        for entry in history:
            line = f"{entry['timestamp']},{entry['username']},{entry['green_score']}," \
                   f"{entry['lines_of_code']},{entry['function_count']},{entry['issues_count']}," \
                   f"{entry['complexity_score']}"
            csv_lines.append(line)
        
        return "\n".join(csv_lines)