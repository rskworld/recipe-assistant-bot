"""
Recipe Assistant Bot - User Authentication
Author: RSK World (https://rskworld.in)
Founder: Molla Samser
Designer & Tester: Rima Khatun
Contact: help@rskworld.in, +91 93305 39277
Year: 2026
"""

import hashlib
import secrets
import json
from typing import Dict, Optional, List
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta

@dataclass
class User:
    """User model for authentication and profiles."""
    id: str
    username: str
    email: str
    password_hash: str
    created_at: str
    last_login: str
    preferences: Dict
    favorites: List[str]
    dietary_restrictions: List[str]
    allergies: List[str]
    skill_level: str
    family_size: int
    budget_range: str
    cuisine_preferences: List[str]
    
    def to_dict(self) -> Dict:
        """Convert user to dictionary."""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'User':
        """Create user from dictionary."""
        return cls(**data)

class AuthManager:
    """Handles user authentication and profile management."""
    
    def __init__(self):
        """Initialize authentication manager."""
        self.users = {}  # In-memory storage (use database in production)
        self.sessions = {}  # Active sessions
        self.session_duration = timedelta(days=7)  # Sessions expire after 7 days
    
    def hash_password(self, password: str) -> str:
        """Hash password using SHA-256 with salt."""
        salt = secrets.token_hex(16)
        password_hash = hashlib.sha256((password + salt).encode()).hexdigest()
        return f"{salt}:{password_hash}"
    
    def verify_password(self, password: str, stored_hash: str) -> bool:
        """Verify password against stored hash."""
        try:
            salt, password_hash = stored_hash.split(':')
            computed_hash = hashlib.sha256((password + salt).encode()).hexdigest()
            return computed_hash == password_hash
        except ValueError:
            return False
    
    def register_user(self, username: str, email: str, password: str, 
                    preferences: Dict = None) -> Dict:
        """Register a new user."""
        # Check if user already exists
        for user in self.users.values():
            if user.username == username or user.email == email:
                return {'error': 'Username or email already exists'}
        
        # Validate input
        if len(password) < 6:
            return {'error': 'Password must be at least 6 characters long'}
        
        if '@' not in email or '.' not in email:
            return {'error': 'Invalid email address'}
        
        # Create new user
        user_id = secrets.token_hex(8)
        password_hash = self.hash_password(password)
        
        user = User(
            id=user_id,
            username=username,
            email=email,
            password_hash=password_hash,
            created_at=datetime.now().isoformat(),
            last_login=datetime.now().isoformat(),
            preferences=preferences or {},
            favorites=[],
            dietary_restrictions=[],
            allergies=[],
            skill_level='beginner',
            family_size=1,
            budget_range='medium',
            cuisine_preferences=[]
        )
        
        self.users[user_id] = user
        
        return {
            'user_id': user_id,
            'username': username,
            'email': email,
            'message': 'User registered successfully'
        }
    
    def login_user(self, username: str, password: str) -> Dict:
        """Authenticate user and create session."""
        # Find user by username or email
        user = None
        for u in self.users.values():
            if u.username == username or u.email == username:
                user = u
                break
        
        if not user:
            return {'error': 'Invalid username or password'}
        
        if not self.verify_password(password, user.password_hash):
            return {'error': 'Invalid username or password'}
        
        # Create session
        session_token = secrets.token_hex(32)
        expires_at = datetime.now() + self.session_duration
        
        self.sessions[session_token] = {
            'user_id': user.id,
            'expires_at': expires_at.isoformat()
        }
        
        # Update last login
        user.last_login = datetime.now().isoformat()
        
        return {
            'session_token': session_token,
            'user_id': user.id,
            'username': user.username,
            'expires_at': expires_at.isoformat(),
            'message': 'Login successful'
        }
    
    def logout_user(self, session_token: str) -> Dict:
        """Logout user by removing session."""
        if session_token in self.sessions:
            del self.sessions[session_token]
            return {'message': 'Logout successful'}
        
        return {'error': 'Invalid session token'}
    
    def get_user_by_session(self, session_token: str) -> Optional[User]:
        """Get user from session token."""
        if session_token not in self.sessions:
            return None
        
        session = self.sessions[session_token]
        expires_at = datetime.fromisoformat(session['expires_at'])
        
        if datetime.now() > expires_at:
            del self.sessions[session_token]
            return None
        
        user_id = session['user_id']
        return self.users.get(user_id)
    
    def update_user_profile(self, user_id: str, updates: Dict) -> Dict:
        """Update user profile."""
        if user_id not in self.users:
            return {'error': 'User not found'}
        
        user = self.users[user_id]
        
        # Update allowed fields
        allowed_fields = [
            'preferences', 'favorites', 'dietary_restrictions', 'allergies',
            'skill_level', 'family_size', 'budget_range', 'cuisine_preferences'
        ]
        
        for field, value in updates.items():
            if field in allowed_fields:
                setattr(user, field, value)
        
        return {
            'message': 'Profile updated successfully',
            'user': user.to_dict()
        }
    
    def get_user_preferences(self, user_id: str) -> Dict:
        """Get user preferences."""
        if user_id not in self.users:
            return {'error': 'User not found'}
        
        user = self.users[user_id]
        return {
            'preferences': user.preferences,
            'dietary_restrictions': user.dietary_restrictions,
            'allergies': user.allergies,
            'skill_level': user.skill_level,
            'family_size': user.family_size,
            'budget_range': user.budget_range,
            'cuisine_preferences': user.cuisine_preferences,
            'favorites': user.favorites
        }
    
    def add_favorite_recipe(self, user_id: str, recipe_name: str) -> Dict:
        """Add recipe to user favorites."""
        if user_id not in self.users:
            return {'error': 'User not found'}
        
        user = self.users[user_id]
        if recipe_name not in user.favorites:
            user.favorites.append(recipe_name)
        
        return {
            'message': 'Recipe added to favorites',
            'favorites': user.favorites
        }
    
    def remove_favorite_recipe(self, user_id: str, recipe_name: str) -> Dict:
        """Remove recipe from user favorites."""
        if user_id not in self.users:
            return {'error': 'User not found'}
        
        user = self.users[user_id]
        if recipe_name in user.favorites:
            user.favorites.remove(recipe_name)
        
        return {
            'message': 'Recipe removed from favorites',
            'favorites': user.favorites
        }
    
    def get_user_stats(self, user_id: str) -> Dict:
        """Get user statistics."""
        if user_id not in self.users:
            return {'error': 'User not found'}
        
        user = self.users[user_id]
        
        # Calculate account age
        created_date = datetime.fromisoformat(user.created_at)
        account_age = datetime.now() - created_date
        
        return {
            'username': user.username,
            'member_since': user.created_at,
            'account_age_days': account_age.days,
            'total_favorites': len(user.favorites),
            'dietary_restrictions': len(user.dietary_restrictions),
            'allergies': len(user.allergies),
            'skill_level': user.skill_level,
            'family_size': user.family_size,
            'budget_range': user.budget_range,
            'cuisine_preferences': len(user.cuisine_preferences)
        }
