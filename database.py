import os
import json
from datetime import datetime, timezone
from typing import List, Dict, Any, Optional
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Float, Text, JSON, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import SQLAlchemyError
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    username = Column(String(255), unique=True, nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    total_analyses = Column(Integer, default=0)
    best_score = Column(Integer, default=0)
    average_score = Column(Float, default=0.0)
    current_level = Column(Integer, default=1)

class Analysis(Base):
    __tablename__ = 'analyses'
    
    id = Column(Integer, primary_key=True)
    username = Column(String(255), nullable=False, index=True)
    green_score = Column(Integer, nullable=False)
    lines_of_code = Column(Integer, nullable=False)
    function_count = Column(Integer, default=0)
    import_count = Column(Integer, default=0)
    while_loop_count = Column(Integer, default=0)
    for_loop_count = Column(Integer, default=0)
    issues_count = Column(Integer, default=0)
    complexity_score = Column(Integer, default=0)
    security_score = Column(Integer, default=100)
    energy_consumption = Column(Float, default=0.0)
    carbon_emissions = Column(Float, default=0.0)
    code_preview = Column(Text, nullable=True)
    analysis_data = Column(JSON, nullable=True)  # Store full analysis results
    created_at = Column(DateTime, default=datetime.utcnow, index=True)

class Achievement(Base):
    __tablename__ = 'achievements'
    
    id = Column(Integer, primary_key=True)
    username = Column(String(255), nullable=False, index=True)
    achievement_id = Column(String(100), nullable=False)
    achievement_name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    unlocked_at = Column(DateTime, default=datetime.utcnow)

class Leaderboard(Base):
    __tablename__ = 'leaderboard'
    
    id = Column(Integer, primary_key=True)
    username = Column(String(255), nullable=False, unique=True, index=True)
    best_score = Column(Integer, default=0)
    average_score = Column(Float, default=0.0)
    total_analyses = Column(Integer, default=0)
    current_level = Column(Integer, default=1)
    total_carbon_saved = Column(Float, default=0.0)
    last_updated = Column(DateTime, default=datetime.utcnow)

class DatabaseManager:
    """Manages database operations for Green Code Checker"""
    
    def __init__(self):
        self.database_url = os.getenv('DATABASE_URL')
        if not self.database_url:
            raise ValueError("DATABASE_URL environment variable not set")
        
        self.engine = create_engine(self.database_url)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        
        # Create tables
        self.create_tables()
    
    def create_tables(self):
        """Create all database tables"""
        try:
            Base.metadata.create_all(bind=self.engine)
            logger.info("Database tables created successfully")
        except SQLAlchemyError as e:
            logger.error(f"Error creating tables: {e}")
            raise
    
    def get_session(self) -> Session:
        """Get database session"""
        return self.SessionLocal()
    
    def add_user(self, username: str, email: str = None) -> bool:
        """Add a new user or update existing user info"""
        try:
            with self.get_session() as session:
                user = session.query(User).filter(User.username == username).first()
                
                if not user:
                    user = User(username=username, email=email)
                    session.add(user)
                    session.commit()
                    logger.info(f"New user created: {username}")
                    return True
                elif email and user.email != email:
                    user.email = email
                    session.commit()
                    logger.info(f"User email updated: {username}")
                
                return True
        except SQLAlchemyError as e:
            logger.error(f"Error adding user: {e}")
            return False
    
    def save_analysis(self, username: str, green_score: int, analysis_results: Dict[str, Any], 
                     security_score: int = 100, energy_consumption: float = 0.0, 
                     carbon_emissions: float = 0.0, code_snippet: str = "") -> bool:
        """Save analysis results to database"""
        try:
            with self.get_session() as session:
                # Ensure user exists
                self.add_user(username)
                
                # Create analysis record
                analysis = Analysis(
                    username=username,
                    green_score=green_score,
                    lines_of_code=analysis_results.get('lines_of_code', 0),
                    function_count=analysis_results.get('function_count', 0),
                    import_count=analysis_results.get('import_count', 0),
                    while_loop_count=analysis_results.get('while_loop_count', 0),
                    for_loop_count=analysis_results.get('for_loop_count', 0),
                    issues_count=len(analysis_results.get('issues', [])),
                    complexity_score=analysis_results.get('complexity_score', 0),
                    security_score=security_score,
                    energy_consumption=energy_consumption,
                    carbon_emissions=carbon_emissions,
                    code_preview=code_snippet[:500],  # Limit preview length
                    analysis_data=analysis_results
                )
                
                session.add(analysis)
                session.commit()
                
                # Update user statistics
                self._update_user_stats(session, username)
                
                logger.info(f"Analysis saved for user: {username}, score: {green_score}")
                return True
                
        except SQLAlchemyError as e:
            logger.error(f"Error saving analysis: {e}")
            return False
    
    def _update_user_stats(self, session: Session, username: str):
        """Update user statistics based on their analyses"""
        try:
            # Get user analyses
            analyses = session.query(Analysis).filter(Analysis.username == username).all()
            
            if not analyses:
                return
            
            total_analyses = len(analyses)
            scores = [a.green_score for a in analyses]
            best_score = max(scores)
            average_score = sum(scores) / len(scores)
            
            # Calculate level based on performance
            current_level = 1
            if total_analyses >= 25 and average_score >= 90:
                current_level = 6  # Green Code Hero
            elif total_analyses >= 15 and average_score >= 85:
                current_level = 5  # Sustainability Master
            elif total_analyses >= 10 and average_score >= 75:
                current_level = 4  # Green Champion
            elif total_analyses >= 5 and average_score >= 60:
                current_level = 3  # Eco Developer
            elif total_analyses >= 3 and average_score >= 40:
                current_level = 2  # Code Gardener
            
            # Update user record
            user = session.query(User).filter(User.username == username).first()
            if user:
                user.total_analyses = total_analyses
                user.best_score = best_score
                user.average_score = average_score
                user.current_level = current_level
                
                # Update leaderboard
                self._update_leaderboard(session, username, best_score, average_score, 
                                       total_analyses, current_level)
                
        except SQLAlchemyError as e:
            logger.error(f"Error updating user stats: {e}")
    
    def _update_leaderboard(self, session: Session, username: str, best_score: int, 
                          average_score: float, total_analyses: int, current_level: int):
        """Update leaderboard entry for user"""
        try:
            leaderboard_entry = session.query(Leaderboard).filter(
                Leaderboard.username == username
            ).first()
            
            if not leaderboard_entry:
                leaderboard_entry = Leaderboard(username=username)
                session.add(leaderboard_entry)
            
            leaderboard_entry.best_score = best_score
            leaderboard_entry.average_score = average_score
            leaderboard_entry.total_analyses = total_analyses
            leaderboard_entry.current_level = current_level
            leaderboard_entry.last_updated = datetime.utcnow()
            
        except SQLAlchemyError as e:
            logger.error(f"Error updating leaderboard: {e}")
    
    def get_user_history(self, username: str, limit: int = 50) -> List[Dict[str, Any]]:
        """Get user's analysis history"""
        try:
            with self.get_session() as session:
                analyses = session.query(Analysis).filter(
                    Analysis.username == username
                ).order_by(Analysis.created_at.desc()).limit(limit).all()
                
                return [{
                    'id': a.id,
                    'timestamp': a.created_at.isoformat(),
                    'green_score': a.green_score,
                    'lines_of_code': a.lines_of_code,
                    'function_count': a.function_count,
                    'issues_count': a.issues_count,
                    'complexity_score': a.complexity_score,
                    'security_score': a.security_score,
                    'energy_consumption': a.energy_consumption,
                    'carbon_emissions': a.carbon_emissions,
                    'code_preview': a.code_preview
                } for a in analyses]
                
        except SQLAlchemyError as e:
            logger.error(f"Error getting user history: {e}")
            return []
    
    def get_user_stats(self, username: str) -> Dict[str, Any]:
        """Get comprehensive user statistics"""
        try:
            with self.get_session() as session:
                user = session.query(User).filter(User.username == username).first()
                
                if not user:
                    return {
                        'total_analyses': 0,
                        'average_score': 0,
                        'best_score': 0,
                        'current_level': 1,
                        'improvement_trend': 0,
                        'total_lines_analyzed': 0,
                        'recent_score': 0
                    }
                
                # Get recent analyses for trend calculation
                recent_analyses = session.query(Analysis).filter(
                    Analysis.username == username
                ).order_by(Analysis.created_at.desc()).limit(10).all()
                
                improvement_trend = 0
                recent_score = 0
                total_lines = 0
                
                if recent_analyses:
                    recent_score = recent_analyses[0].green_score
                    total_lines = sum(a.lines_of_code for a in recent_analyses)
                    
                    if len(recent_analyses) >= 5:
                        recent_avg = sum(a.green_score for a in recent_analyses[:5]) / 5
                        older_avg = sum(a.green_score for a in recent_analyses[5:]) / len(recent_analyses[5:])
                        improvement_trend = recent_avg - older_avg
                
                return {
                    'total_analyses': user.total_analyses,
                    'average_score': user.average_score,
                    'best_score': user.best_score,
                    'current_level': user.current_level,
                    'improvement_trend': improvement_trend,
                    'total_lines_analyzed': total_lines,
                    'recent_score': recent_score
                }
                
        except SQLAlchemyError as e:
            logger.error(f"Error getting user stats: {e}")
            return {}
    
    def get_leaderboard(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get top performers leaderboard"""
        try:
            with self.get_session() as session:
                leaders = session.query(Leaderboard).order_by(
                    Leaderboard.average_score.desc(),
                    Leaderboard.best_score.desc(),
                    Leaderboard.total_analyses.desc()
                ).limit(limit).all()
                
                return [{
                    'username': leader.username,
                    'best_score': leader.best_score,
                    'average_score': leader.average_score,
                    'total_analyses': leader.total_analyses,
                    'current_level': leader.current_level,
                    'composite_score': (leader.average_score * 0.7) + (leader.best_score * 0.3)
                } for leader in leaders]
                
        except SQLAlchemyError as e:
            logger.error(f"Error getting leaderboard: {e}")
            return []
    
    def save_achievement(self, username: str, achievement_id: str, 
                        achievement_name: str, description: str = "") -> bool:
        """Save user achievement"""
        try:
            with self.get_session() as session:
                # Check if achievement already exists
                existing = session.query(Achievement).filter(
                    Achievement.username == username,
                    Achievement.achievement_id == achievement_id
                ).first()
                
                if existing:
                    return False  # Achievement already unlocked
                
                achievement = Achievement(
                    username=username,
                    achievement_id=achievement_id,
                    achievement_name=achievement_name,
                    description=description
                )
                
                session.add(achievement)
                session.commit()
                
                logger.info(f"Achievement unlocked: {username} - {achievement_name}")
                return True
                
        except SQLAlchemyError as e:
            logger.error(f"Error saving achievement: {e}")
            return False
    
    def get_user_achievements(self, username: str) -> List[Dict[str, Any]]:
        """Get user's unlocked achievements"""
        try:
            with self.get_session() as session:
                achievements = session.query(Achievement).filter(
                    Achievement.username == username
                ).order_by(Achievement.unlocked_at.desc()).all()
                
                return [{
                    'achievement_id': a.achievement_id,
                    'name': a.achievement_name,
                    'description': a.description,
                    'unlocked_at': a.unlocked_at.isoformat()
                } for a in achievements]
                
        except SQLAlchemyError as e:
            logger.error(f"Error getting achievements: {e}")
            return []
    
    def get_analytics_summary(self) -> Dict[str, Any]:
        """Get platform-wide analytics"""
        try:
            with self.get_session() as session:
                total_users = session.query(User).count()
                total_analyses = session.query(Analysis).count()
                
                if total_analyses > 0:
                    avg_platform_score = session.query(Analysis.green_score).all()
                    avg_score = sum(score[0] for score in avg_platform_score) / len(avg_platform_score)
                    
                    total_energy_saved = session.query(Analysis.energy_consumption).all()
                    energy_saved = sum(energy[0] for energy in total_energy_saved if energy[0])
                    
                    total_carbon_saved = session.query(Analysis.carbon_emissions).all()
                    carbon_saved = sum(carbon[0] for carbon in total_carbon_saved if carbon[0])
                else:
                    avg_score = 0
                    energy_saved = 0
                    carbon_saved = 0
                
                return {
                    'total_users': total_users,
                    'total_analyses': total_analyses,
                    'average_platform_score': avg_score,
                    'total_energy_saved': energy_saved,
                    'total_carbon_saved': carbon_saved
                }
                
        except SQLAlchemyError as e:
            logger.error(f"Error getting analytics: {e}")
            return {}
    
    def cleanup_old_data(self, days: int = 90):
        """Clean up old analysis data (keep only recent records)"""
        try:
            with self.get_session() as session:
                cutoff_date = datetime.utcnow() - timedelta(days=days)
                
                deleted = session.query(Analysis).filter(
                    Analysis.created_at < cutoff_date
                ).delete()
                
                session.commit()
                logger.info(f"Cleaned up {deleted} old analysis records")
                
        except SQLAlchemyError as e:
            logger.error(f"Error cleaning up data: {e}")