from typing import Dict, List, Any

class GamificationEngine:
    """Handles user levels, achievements, and gamification features"""
    
    def __init__(self):
        self.levels = {
            1: {"name": "🌱 Green Seedling", "min_score": 0, "analyses_required": 1},
            2: {"name": "🌿 Code Gardener", "min_score": 40, "analyses_required": 3},
            3: {"name": "🌳 Eco Developer", "min_score": 60, "analyses_required": 5},
            4: {"name": "🏆 Green Champion", "min_score": 75, "analyses_required": 10},
            5: {"name": "⭐ Sustainability Master", "min_score": 85, "analyses_required": 15},
            6: {"name": "🌍 Green Code Hero", "min_score": 90, "analyses_required": 25}
        }
        
        self.achievements = {
            "first_analysis": {
                "name": "🎯 First Steps",
                "description": "Complete your first code analysis",
                "icon": "🎯"
            },
            "perfect_score": {
                "name": "💯 Perfectionist",
                "description": "Achieve a perfect 100/100 Green Score",
                "icon": "💯"
            },
            "consistent_improver": {
                "name": "📈 Consistent Improver",
                "description": "Show improvement in 5 consecutive analyses",
                "icon": "📈"
            },
            "code_optimizer": {
                "name": "⚡ Code Optimizer",
                "description": "Analyze code with 0 issues found",
                "icon": "⚡"
            },
            "eco_warrior": {
                "name": "🌿 Eco Warrior",
                "description": "Maintain average score above 80 for 10 analyses",
                "icon": "🌿"
            },
            "prolific_analyzer": {
                "name": "🔍 Prolific Analyzer",
                "description": "Complete 50 code analyses",
                "icon": "🔍"
            },
            "efficiency_expert": {
                "name": "🎓 Efficiency Expert",
                "description": "Achieve 5 scores above 95",
                "icon": "🎓"
            }
        }
    
    def calculate_user_level(self, user_stats: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate user's current level based on their statistics"""
        total_analyses = user_stats.get('total_analyses', 0)
        average_score = user_stats.get('average_score', 0)
        best_score = user_stats.get('best_score', 0)
        
        current_level = 1
        
        for level_num, level_info in self.levels.items():
            if (total_analyses >= level_info['analyses_required'] and 
                average_score >= level_info['min_score']):
                current_level = level_num
        
        # Get next level info
        next_level = current_level + 1 if current_level < max(self.levels.keys()) else None
        next_level_info = self.levels.get(next_level) if next_level else None
        
        # Calculate progress to next level
        progress = 0
        if next_level_info:
            score_progress = min(100, (average_score / next_level_info['min_score']) * 100) if next_level_info['min_score'] > 0 else 100
            analysis_progress = min(100, (total_analyses / next_level_info['analyses_required']) * 100)
            progress = min(score_progress, analysis_progress)
        
        return {
            'current_level': current_level,
            'level_name': self.levels[current_level]['name'],
            'next_level': next_level,
            'next_level_name': next_level_info['name'] if next_level_info else None,
            'progress_to_next': progress,
            'requirements_met': {
                'analyses': total_analyses,
                'required_analyses': next_level_info['analyses_required'] if next_level_info else 0,
                'average_score': average_score,
                'required_score': next_level_info['min_score'] if next_level_info else 0
            }
        }
    
    def check_achievements(self, user_history: List[Dict[str, Any]], user_stats: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Check which achievements the user has unlocked"""
        unlocked_achievements = []
        
        # First analysis
        if user_stats.get('total_analyses', 0) >= 1:
            unlocked_achievements.append(self.achievements['first_analysis'])
        
        # Perfect score
        if any(entry.get('green_score', 0) == 100 for entry in user_history):
            unlocked_achievements.append(self.achievements['perfect_score'])
        
        # Consistent improver (5 consecutive improvements)
        if len(user_history) >= 5:
            scores = [entry.get('green_score', 0) for entry in user_history[-5:]]
            if all(scores[i] <= scores[i+1] for i in range(len(scores)-1)):
                unlocked_achievements.append(self.achievements['consistent_improver'])
        
        # Code optimizer (0 issues)
        if any(entry.get('issues_count', 1) == 0 for entry in user_history):
            unlocked_achievements.append(self.achievements['code_optimizer'])
        
        # Eco warrior (average > 80 for 10 analyses)
        if (user_stats.get('total_analyses', 0) >= 10 and 
            user_stats.get('average_score', 0) > 80):
            unlocked_achievements.append(self.achievements['eco_warrior'])
        
        # Prolific analyzer
        if user_stats.get('total_analyses', 0) >= 50:
            unlocked_achievements.append(self.achievements['prolific_analyzer'])
        
        # Efficiency expert (5 scores above 95)
        high_scores = sum(1 for entry in user_history if entry.get('green_score', 0) > 95)
        if high_scores >= 5:
            unlocked_achievements.append(self.achievements['efficiency_expert'])
        
        return unlocked_achievements
    
    def generate_next_steps(self, level_info: Dict[str, Any], user_stats: Dict[str, Any]) -> List[str]:
        """Generate personalized next steps for improvement"""
        suggestions = []
        
        current_level = level_info['current_level']
        average_score = user_stats.get('average_score', 0)
        total_analyses = user_stats.get('total_analyses', 0)
        
        # Level-specific suggestions
        if current_level == 1:
            suggestions.extend([
                "🎯 Try analyzing different types of code to improve your average score",
                "📚 Focus on eliminating while loops and unused imports",
                "🔄 Analyze at least 3 different code samples to reach the next level"
            ])
        elif current_level == 2:
            suggestions.extend([
                "⚡ Aim for scores above 60 by optimizing loop patterns",
                "🧹 Clean up import statements in your code",
                "📈 Complete 5 total analyses to advance further"
            ])
        elif current_level >= 3:
            suggestions.extend([
                "🏆 Strive for consistency - maintain high scores across all analyses",
                "💡 Share your achievements on LinkedIn to inspire others",
                "🌟 Help others by sharing green coding best practices"
            ])
        
        # Score-based suggestions
        if average_score < 70:
            suggestions.append("🎯 Focus on basic optimizations: replace while loops with for loops")
        elif average_score < 85:
            suggestions.append("⚡ Advanced optimization: use list comprehensions and eliminate unused code")
        else:
            suggestions.append("🌟 You're doing great! Share your green coding expertise with the community")
        
        return suggestions[:4]  # Return top 4 suggestions
    
    def get_level_badge_text(self, level_info: Dict[str, Any], user_stats: Dict[str, Any]) -> str:
        """Generate text for sharing achievements"""
        level_name = level_info['level_name']
        best_score = user_stats.get('best_score', 0)
        total_analyses = user_stats.get('total_analyses', 0)
        
        badge_text = f"""🌿 Green Code Achievement Unlocked! 

{level_name}
🏆 Best Score: {best_score}/100
📊 Total Analyses: {total_analyses}

Promoting sustainable coding practices with Green Code Checker!
#GreenAI #SustainableCoding #CleanCode #TechForGood"""
        
        return badge_text
    
    def get_progress_message(self, level_info: Dict[str, Any]) -> str:
        """Get motivational progress message"""
        progress = level_info['progress_to_next']
        next_level_name = level_info.get('next_level_name')
        
        if not next_level_name:
            return "🌟 Congratulations! You've reached the highest level - Green Code Hero!"
        
        if progress >= 80:
            return f"🔥 Almost there! You're {100-progress:.0f}% away from becoming a {next_level_name}!"
        elif progress >= 50:
            return f"📈 Great progress! Halfway to {next_level_name} level!"
        else:
            return f"🌱 Keep growing! Working towards {next_level_name} level."