"""
Recipe Assistant Bot - AI Cooking Assistant
Author: RSK World (https://rskworld.in)
Founder: Molla Samser
Designer & Tester: Rima Khatun
Contact: help@rskworld.in, +91 93305 39277
Year: 2026
"""

import json
import time
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from enum import Enum

class CookingStepType(Enum):
    """Types of cooking steps."""
    PREPARATION = "preparation"
    COOKING = "cooking"
    SEASONING = "seasoning"
    PLATING = "plating"
    RESTING = "resting"
    CLEANUP = "cleanup"

class DifficultyLevel(Enum):
    """Cooking difficulty levels."""
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    EXPERT = "expert"

@dataclass
class CookingStep:
    """Individual cooking step."""
    id: str
    step_number: int
    title: str
    description: str
    step_type: CookingStepType
    duration_minutes: int
    temperature: Optional[float]
    equipment_needed: List[str]
    ingredients_needed: List[str]
    tips: List[str]
    warnings: List[str]
    completion_criteria: List[str]
    
    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        result = asdict(self)
        result['step_type'] = self.step_type.value
        return result

@dataclass
class CookingSession:
    """Active cooking session with AI guidance."""
    id: str
    recipe_name: str
    user_id: str
    current_step: int
    total_steps: int
    start_time: str
    estimated_completion_time: str
    difficulty_level: DifficultyLevel
    skill_adjustments: Dict[str, Any]
    progress_percentage: float
    paused: bool
    completed_steps: List[str]
    notes: List[str]
    
    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        result = asdict(self)
        result['difficulty_level'] = self.difficulty_level.value
        return result

class AICookingAssistant:
    """AI-powered cooking assistant with step-by-step guidance."""
    
    def __init__(self):
        """Initialize AI cooking assistant."""
        self.active_sessions = {}  # session_id -> CookingSession
        self.recipe_steps = {}  # recipe_name -> List[CookingStep]
        self.cooking_tips = self._load_cooking_tips()
        self.technique_guides = self._load_technique_guides()
        self.troubleshooting_guide = self._load_troubleshooting_guide()
        
        # Load detailed recipe steps
        self._load_recipe_steps()
    
    def _load_cooking_tips(self) -> Dict[str, List[str]]:
        """Load cooking tips by category."""
        return {
            'knife_skills': [
                "Keep your knives sharp for safer, more efficient cutting",
                "Use the proper knife for each task - chef's knife for general work, paring knife for detail work",
                "Practice the claw grip to protect your fingers while cutting",
                "Cut on a stable surface and keep your cutting board from sliding"
            ],
            'temperature_control': [
                "Let meat come to room temperature before cooking for even results",
                "Preheat your pan properly to prevent sticking",
                "Use a thermometer to ensure accurate cooking temperatures",
                "Allow cooked meat to rest before cutting to retain juices"
            ],
            'seasoning': [
                "Season in layers - salt at each stage of cooking",
                "Taste and adjust seasoning throughout the cooking process",
                "Use fresh herbs at the end to preserve their flavor",
                "Remember that salt enhances flavor, other spices add character"
            ],
            'timing': [
                "Read the entire recipe before starting to plan your timing",
                "Prep all ingredients before you begin cooking (mise en place)",
                "Clean as you go to maintain an organized workspace",
                "Set timers for each cooking step to prevent overcooking"
            ],
            'safety': [
                "Always keep a fire extinguisher in the kitchen",
                "Turn pot handles inward to prevent accidental spills",
                "Use dry oven mitts to handle hot pans",
                "Never leave cooking food unattended"
            ]
        }
    
    def _load_technique_guides(self) -> Dict[str, Dict]:
        """Load detailed cooking technique guides."""
        return {
            'sautéing': {
                'description': 'Cooking quickly in a small amount of fat over relatively high heat',
                'key_points': [
                    'Use a wide, shallow pan for best results',
                    'Don\'t overcrowd the pan - cook in batches if needed',
                    'Keep the food moving to ensure even cooking',
                    'Listen for the sizzle to know the pan is hot enough'
                ],
                'common_mistakes': [
                    'Pan not hot enough - food steams instead of browns',
                    'Overcrowding the pan lowers the temperature',
                    'Adding cold food to hot oil causes splattering'
                ]
            },
            'braising': {
                'description': 'Cooking food slowly in liquid after browning',
                'key_points': [
                    'Brown the meat first for better flavor',
                    'Use enough liquid to come about halfway up the food',
                    'Keep the liquid at a gentle simmer, not boiling',
                    'Cover the pot to retain moisture'
                ],
                'common_mistakes': [
                    'Not browning the meat first',
                    'Using too much liquid',
                    'Cooking at too high temperature'
                ]
            },
            'roasting': {
                'description': 'Cooking with dry heat in an oven',
                'key_points': [
                    'Preheat the oven thoroughly',
                    'Use a roasting rack for air circulation',
                    'Rotate the pan halfway through cooking',
                    'Let meat rest before carving'
                ],
                'common_mistakes': [
                    'Oven not fully preheated',
                    'Overcrowding the pan',
                    'Not using a meat thermometer'
                ]
            }
        }
    
    def _load_troubleshooting_guide(self) -> Dict[str, Dict]:
        """Load troubleshooting guide for common cooking problems."""
        return {
            'meat_tough': {
                'symptoms': ['Meat is hard to chew', 'Dry texture', 'Difficult to cut'],
                'causes': ['Overcooked', 'Wrong cut of meat', 'Not enough fat', 'Cooked at too high temperature'],
                'solutions': [
                    'Use a meat thermometer to avoid overcooking',
                    'Choose appropriate cuts for your cooking method',
                    'Consider marinating tougher cuts',
                    'Cook at lower temperatures for longer periods'
                ]
            },
            'sauce_broken': {
                'symptoms': ['Oil separated', 'Curled appearance', 'Grainy texture'],
                'causes': ['Temperature too high', 'Added ingredients too quickly', 'Too much fat', 'Not enough emulsifier'],
                'solutions': [
                    'Remove from heat and whisk vigorously',
                    'Add a small amount of mustard or egg yolk',
                    'Gradually add liquid while whisking',
                    'Keep sauce warm but not hot'
                ]
            },
            'vegetables_mushy': {
                'symptoms': ['Soft texture', 'Loss of color', 'Mushy consistency'],
                'causes': ['Overcooked', 'Cooked too long', 'Too much water', 'Cut too small'],
                'solutions': [
                    'Cook vegetables briefly (blanch or steam)',
                    'Use ice bath to stop cooking process',
                    'Cut vegetables uniformly for even cooking',
                    'Don\'t overcrowd the pan'
                ]
            }
        }
    
    def _load_recipe_steps(self):
        """Load detailed steps for common recipes."""
        self.recipe_steps = {
            'Spaghetti Carbonara': [
                CookingStep(
                    id="step_1",
                    step_number=1,
                    title="Prepare Ingredients",
                    description="Gather and prepare all ingredients. Cut pancetta into small cubes, grate Parmesan cheese, and crack eggs into a bowl.",
                    step_type=CookingStepType.PREPARATION,
                    duration_minutes=10,
                    temperature=None,
                    equipment_needed=["cutting board", "knife", "grater", "mixing bowl"],
                    ingredients_needed=["spaghetti", "eggs", "pancetta", "parmesan", "black pepper"],
                    tips=["Use room temperature eggs for better mixing", "Grate cheese finely for smooth sauce"],
                    warnings=["Keep eggs separate until ready to use"],
                    completion_criteria=["All ingredients prepped and ready", "Water boiling for pasta"]
                ),
                CookingStep(
                    id="step_2",
                    step_number=2,
                    title="Cook Pasta",
                    description="Add spaghetti to boiling salted water and cook according to package directions until al dente.",
                    step_type=CookingStepType.COOKING,
                    duration_minutes=8,
                    temperature=212,
                    equipment_needed=["large pot", "colander"],
                    ingredients_needed=["spaghetti", "salt"],
                    tips=["Save pasta water for sauce", "Stir occasionally to prevent sticking"],
                    warnings=["Water will be hot - handle carefully"],
                    completion_criteria=["Pasta is al dente", "Pasta water reserved"]
                ),
                CookingStep(
                    id="step_3",
                    step_number=3,
                    title="Cook Pancetta",
                    description="Cook pancetta in a large skillet until crisp and golden brown.",
                    step_type=CookingStepType.COOKING,
                    duration_minutes=5,
                    temperature=350,
                    equipment_needed=["large skillet", "spatula"],
                    ingredients_needed=["pancetta"],
                    tips=["Don't overcrowd the pan", "Render fat slowly for best flavor"],
                    warnings=["Fat will be hot", "Don't burn the pancetta"],
                    completion_criteria=["Pancetta is crispy", "Fat is rendered"]
                ),
                CookingStep(
                    id="step_4",
                    step_number=4,
                    title="Mix Sauce",
                    description="Beat eggs with grated Parmesan and black pepper. Add hot pasta and toss quickly.",
                    step_type=CookingStepType.SEASONING,
                    duration_minutes=2,
                    temperature=None,
                    equipment_needed=["mixing bowl", "whisk", "tongs"],
                    ingredients_needed=["eggs", "parmesan", "black pepper", "cooked pasta"],
                    tips=["Work quickly to avoid scrambling eggs", "Use pasta water to adjust consistency"],
                    warnings=["Eggs should not be fully cooked", "Remove from heat if needed"],
                    completion_criteria=["Sauce is creamy", "Pasta is well coated"]
                )
            ],
            'Chicken Stir Fry': [
                CookingStep(
                    id="step_1",
                    step_number=1,
                    title="Prepare Ingredients",
                    description="Cut chicken into bite-sized pieces and chop vegetables. Mix sauce ingredients.",
                    step_type=CookingStepType.PREPARATION,
                    duration_minutes=15,
                    temperature=None,
                    equipment_needed=["cutting board", "knife", "mixing bowls"],
                    ingredients_needed=["chicken", "vegetables", "soy sauce", "garlic", "ginger"],
                    tips=["Cut vegetables uniformly for even cooking", "Pat chicken dry for better browning"],
                    warnings=["Keep raw chicken separate from vegetables"],
                    completion_criteria=["All ingredients prepped", "Sauce mixed and ready"]
                ),
                CookingStep(
                    id="step_2",
                    step_number=2,
                    title="Cook Chicken",
                    description="Heat oil in wok or large skillet and cook chicken until golden and cooked through.",
                    step_type=CookingStepType.COOKING,
                    duration_minutes=6,
                    temperature=375,
                    equipment_needed=["wok or skillet", "spatula"],
                    ingredients_needed=["chicken", "oil"],
                    tips=["Don't overcrowd the pan", "Cook in batches if needed"],
                    warnings=["Oil will be very hot", "Chicken must reach 165°F internal temperature"],
                    completion_criteria=["Chicken is golden brown", "Internal temperature is 165°F"]
                ),
                CookingStep(
                    id="step_3",
                    step_number=3,
                    title="Stir Fry Vegetables",
                    description="Add vegetables to hot wok and stir-fry until crisp-tender.",
                    step_type=CookingStepType.COOKING,
                    duration_minutes=4,
                    temperature=400,
                    equipment_needed=["wok", "spatula"],
                    ingredients_needed=["vegetables", "garlic", "ginger"],
                    tips=["Keep vegetables moving", "Add harder vegetables first"],
                    warnings=["Vegetables cook quickly", "Don't overcook"],
                    completion_criteria=["Vegetables are crisp-tender", "Aromatics are fragrant"]
                ),
                CookingStep(
                    id="step_4",
                    step_number=4,
                    title="Combine and Sauce",
                    description="Return chicken to wok, add sauce, and toss until everything is coated.",
                    step_type=CookingStepType.SEASONING,
                    duration_minutes=2,
                    temperature=None,
                    equipment_needed=["wok", "spatula"],
                    ingredients_needed=["cooked chicken", "cooked vegetables", "sauce"],
                    tips=["Toss quickly to combine", "Taste and adjust seasoning"],
                    warnings=["Sauce will thicken quickly", "Be careful of steam"],
                    completion_criteria=["Everything is well coated", "Sauce is thickened"]
                )
            ]
        }
    
    def start_cooking_session(self, recipe_name: str, user_id: str, 
                            skill_level: DifficultyLevel = DifficultyLevel.BEGINNER,
                            dietary_preferences: List[str] = None) -> Dict:
        """Start a new cooking session with AI guidance."""
        if recipe_name not in self.recipe_steps:
            return {'error': 'Recipe steps not available'}
        
        session_id = f"cooking_session_{len(self.active_sessions) + 1}"
        steps = self.recipe_steps[recipe_name]
        
        # Calculate total time and difficulty adjustments
        total_time = sum(step.duration_minutes for step in steps)
        skill_adjustments = self._calculate_skill_adjustments(skill_level, steps)
        
        session = CookingSession(
            id=session_id,
            recipe_name=recipe_name,
            user_id=user_id,
            current_step=1,
            total_steps=len(steps),
            start_time=datetime.now().isoformat(),
            estimated_completion_time=(
                datetime.now() + timedelta(minutes=total_time)
            ).isoformat(),
            difficulty_level=skill_level,
            skill_adjustments=skill_adjustments,
            progress_percentage=0.0,
            paused=False,
            completed_steps=[],
            notes=[]
        )
        
        self.active_sessions[session_id] = session
        
        return {
            'session_id': session_id,
            'current_step': self.get_current_step(session_id),
            'total_steps': len(steps),
            'estimated_time': total_time,
            'skill_adjustments': skill_adjustments,
            'message': f'Cooking session started for {recipe_name}'
        }
    
    def get_current_step(self, session_id: str) -> Optional[CookingStep]:
        """Get current cooking step for a session."""
        if session_id not in self.active_sessions:
            return None
        
        session = self.active_sessions[session_id]
        recipe_name = session.recipe_name
        steps = self.recipe_steps[recipe_name]
        
        if session.current_step <= len(steps):
            return steps[session.current_step - 1]
        
        return None
    
    def advance_to_next_step(self, session_id: str, notes: str = None) -> Dict:
        """Advance to the next cooking step."""
        if session_id not in self.active_sessions:
            return {'error': 'Session not found'}
        
        session = self.active_sessions[session_id]
        current_step = self.get_current_step(session_id)
        
        if not current_step:
            return {'error': 'No more steps available'}
        
        # Mark current step as completed
        session.completed_steps.append(current_step.id)
        session.current_step += 1
        
        # Update progress
        session.progress_percentage = (session.current_step - 1) / session.total_steps * 100
        
        # Add notes if provided
        if notes:
            session.notes.append({
                'step': current_step.id,
                'note': notes,
                'timestamp': datetime.now().isoformat()
            })
        
        next_step = self.get_current_step(session_id)
        
        if next_step:
            return {
                'session_id': session_id,
                'previous_step': current_step.to_dict(),
                'current_step': next_step.to_dict(),
                'progress': session.progress_percentage,
                'message': f'Moved to step {session.current_step}: {next_step.title}'
            }
        else:
            # Cooking completed
            session.progress_percentage = 100.0
            return {
                'session_id': session_id,
                'completed': True,
                'final_step': current_step.to_dict(),
                'total_time': self._calculate_session_time(session),
                'message': 'Cooking session completed successfully!'
            }
    
    def get_step_guidance(self, session_id: str, guidance_type: str = 'detailed') -> Dict:
        """Get detailed guidance for current step."""
        if session_id not in self.active_sessions:
            return {'error': 'Session not found'}
        
        current_step = self.get_current_step(session_id)
        if not current_step:
            return {'error': 'No current step'}
        
        guidance = {
            'step': current_step.to_dict(),
            'basic_tips': current_step.tips,
            'warnings': current_step.warnings
        }
        
        if guidance_type == 'detailed':
            # Add technique-specific guidance
            technique_tips = self._get_technique_tips(current_step)
            guidance['technique_guide'] = technique_tips
            
            # Add skill-level adjustments
            session = self.active_sessions[session_id]
            skill_guidance = self._get_skill_level_guidance(
                current_step, session.difficulty_level
            )
            guidance['skill_guidance'] = skill_guidance
        
        elif guidance_type == 'troubleshooting':
            # Add troubleshooting tips
            troubleshooting = self._get_troubleshooting_tips(current_step)
            guidance['troubleshooting'] = troubleshooting
        
        return guidance
    
    def pause_session(self, session_id: str, reason: str = None) -> Dict:
        """Pause a cooking session."""
        if session_id not in self.active_sessions:
            return {'error': 'Session not found'}
        
        session = self.active_sessions[session_id]
        session.paused = True
        
        return {
            'session_id': session_id,
            'paused': True,
            'reason': reason,
            'message': 'Cooking session paused'
        }
    
    def resume_session(self, session_id: str) -> Dict:
        """Resume a paused cooking session."""
        if session_id not in self.active_sessions:
            return {'error': 'Session not found'}
        
        session = self.active_sessions[session_id]
        session.paused = False
        
        current_step = self.get_current_step(session_id)
        
        return {
            'session_id': session_id,
            'resumed': True,
            'current_step': current_step.to_dict() if current_step else None,
            'message': 'Cooking session resumed'
        }
    
    def _calculate_skill_adjustments(self, skill_level: DifficultyLevel, 
                                 steps: List[CookingStep]) -> Dict[str, Any]:
        """Calculate time and complexity adjustments based on skill level."""
        adjustments = {
            'time_multiplier': 1.0,
            'additional_tips': [],
            'simplified_steps': False,
            'extra_warnings': []
        }
        
        if skill_level == DifficultyLevel.BEGINNER:
            adjustments['time_multiplier'] = 1.5
            adjustments['additional_tips'] = [
                "Take your time with each step",
                "Don't worry about perfection - practice makes perfect",
                "Read each step completely before starting"
            ]
            adjustments['extra_warnings'] = [
                "Be careful with hot surfaces",
                "Ask for help if unsure about any step"
            ]
        
        elif skill_level == DifficultyLevel.INTERMEDIATE:
            adjustments['time_multiplier'] = 1.2
            adjustments['additional_tips'] = [
                "Focus on technique and timing",
                "Trust your instincts on seasoning"
            ]
        
        elif skill_level == DifficultyLevel.ADVANCED:
            adjustments['time_multiplier'] = 1.0
            adjustments['additional_tips'] = [
                "Experiment with flavors and techniques",
                "Consider presentation and garnishes"
            ]
        
        elif skill_level == DifficultyLevel.EXPERT:
            adjustments['time_multiplier'] = 0.8
            adjustments['additional_tips'] = [
                "Focus on precision and refinement",
                "Consider creative variations"
            ]
        
        return adjustments
    
    def _get_technique_tips(self, step: CookingStep) -> Dict:
        """Get technique-specific tips for a cooking step."""
        # Analyze step description to determine technique
        description = step.description.lower()
        
        if 'sauté' in description or 'fry' in description:
            return self.technique_guides.get('sautéing', {})
        elif 'braise' in description:
            return self.technique_guides.get('braising', {})
        elif 'roast' in description or 'oven' in description:
            return self.technique_guides.get('roasting', {})
        
        return {}
    
    def _get_skill_level_guidance(self, step: CookingStep, 
                               skill_level: DifficultyLevel) -> Dict:
        """Get skill-level specific guidance."""
        guidance = {
            'beginner_focus': [],
            'intermediate_tips': [],
            'advanced_techniques': []
        }
        
        if skill_level == DifficultyLevel.BEGINNER:
            guidance['beginner_focus'] = [
                "Focus on safety and basic techniques",
                "Don't rush through steps",
                "Ask questions if anything is unclear"
            ]
        elif skill_level == DifficultyLevel.INTERMEDIATE:
            guidance['intermediate_tips'] = [
                "Work on timing and multitasking",
                "Practice knife skills",
                "Learn to adjust seasoning by taste"
            ]
        elif skill_level in [DifficultyLevel.ADVANCED, DifficultyLevel.EXPERT]:
            guidance['advanced_techniques'] = [
                "Focus on precision and consistency",
                "Experiment with flavor combinations",
                "Consider presentation and plating"
            ]
        
        return guidance
    
    def _get_troubleshooting_tips(self, step: CookingStep) -> List[Dict]:
        """Get troubleshooting tips for current step."""
        # Analyze step to identify potential issues
        tips = []
        
        if 'meat' in step.description.lower() or 'chicken' in step.description.lower():
            tips.append(self.troubleshooting_guide['meat_tough'])
        
        if 'sauce' in step.description.lower():
            tips.append(self.troubleshooting_guide['sauce_broken'])
        
        if 'vegetable' in step.description.lower():
            tips.append(self.troubleshooting_guide['vegetables_mushy'])
        
        return tips
    
    def _calculate_session_time(self, session: CookingSession) -> Dict:
        """Calculate time spent in cooking session."""
        start_time = datetime.fromisoformat(session.start_time)
        current_time = datetime.now()
        
        total_time = current_time - start_time
        
        return {
            'total_minutes': int(total_time.total_seconds() / 60),
            'formatted_time': str(total_time).split('.')[0],
            'estimated_vs_actual': {
                'estimated': session.estimated_completion_time,
                'actual': current_time.isoformat()
            }
        }
    
    def get_session_summary(self, session_id: str) -> Dict:
        """Get complete summary of a cooking session."""
        if session_id not in self.active_sessions:
            return {'error': 'Session not found'}
        
        session = self.active_sessions[session_id]
        time_info = self._calculate_session_time(session)
        
        return {
            'session': session.to_dict(),
            'time_info': time_info,
            'completed_steps': len(session.completed_steps),
            'total_steps': session.total_steps,
            'notes': session.notes,
            'achievements': self._calculate_achievements(session)
        }
    
    def _calculate_achievements(self, session: CookingSession) -> List[str]:
        """Calculate achievements earned during cooking session."""
        achievements = []
        
        if session.progress_percentage == 100:
            achievements.append("Recipe Master - Completed full recipe")
        
        if len(session.notes) == 0:
            achievements.append("Confident Cook - No notes needed")
        
        if session.difficulty_level in [DifficultyLevel.ADVANCED, DifficultyLevel.EXPERT]:
            achievements.append("Brave Chef - Attempted advanced recipe")
        
        time_info = self._calculate_session_time(session)
        if time_info['total_minutes'] < 30:
            achievements.append("Speed Cooker - Finished in under 30 minutes")
        
        return achievements
