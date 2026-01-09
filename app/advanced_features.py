"""
Recipe Assistant Bot - Advanced Features
Author: RSK World (https://rskworld.in)
Founder: Molla Samser
Designer & Tester: Rima Khatun
Contact: help@rskworld.in, +91 93305 39277
Year: 2026
"""

import json
import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from collections import defaultdict
from enum import Enum

class ChallengeType(Enum):
    """Types of cooking challenges."""
    WEEKLY_RECIPE = "weekly_recipe"
    TECHNIQUE_MASTER = "technique_master"
    CUISINE_EXPLORER = "cuisine_explorer"
    HEALTHY_EATING = "healthy_eating"
    MEAL_PREP = "meal_prep"
    SPEED_COOKING = "speed_cooking"

@dataclass
class IngredientInventory:
    """Ingredient inventory item."""
    name: str
    quantity: float
    unit: str
    expiry_date: Optional[str]
    location: str  # pantry, fridge, freezer
    category: str
    added_date: str
    notes: str
    
    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return asdict(self)

@dataclass
class RecipeCollection:
    """User recipe collection/cookbook."""
    id: str
    name: str
    description: str
    recipes: List[str]
    tags: List[str]
    created_date: str
    updated_date: str
    cover_image: Optional[str]
    is_public: bool
    
    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return asdict(self)

@dataclass
class CookingChallenge:
    """Cooking challenge/goal."""
    id: str
    user_id: str
    challenge_type: ChallengeType
    title: str
    description: str
    start_date: str
    end_date: str
    target_recipes: List[str]
    completed_recipes: List[str]
    progress_percentage: float
    rewards: List[str]
    difficulty: str
    is_active: bool
    
    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        result = asdict(self)
        result['challenge_type'] = self.challenge_type.value
        return result

@dataclass
class MealPrepPlan:
    """Meal prep planning session."""
    id: str
    user_id: str
    week_start: str
    recipes: List[Dict]
    batch_cooking_schedule: List[Dict]
    shopping_list: Dict
    prep_timeline: List[Dict]
    storage_instructions: Dict
    created_date: str
    
    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return asdict(self)

class AdvancedFeaturesManager:
    """Manages advanced features like inventory, collections, challenges."""
    
    def __init__(self):
        """Initialize advanced features manager."""
        self.inventories = {}  # user_id -> List[IngredientInventory]
        self.collections = {}  # user_id -> List[RecipeCollection]
        self.challenges = {}  # user_id -> List[CookingChallenge]
        self.meal_prep_plans = {}  # user_id -> List[MealPrepPlan]
        self.user_recipe_history = defaultdict(list)  # user_id -> List[recipe_name]
        self.cooking_stats = defaultdict(dict)  # user_id -> stats
    
    # Ingredient Inventory Management
    def add_to_inventory(self, user_id: str, ingredient: IngredientInventory) -> Dict:
        """Add ingredient to user's inventory."""
        if user_id not in self.inventories:
            self.inventories[user_id] = []
        
        self.inventories[user_id].append(ingredient)
        
        return {
            'status': 'success',
            'message': f'Added {ingredient.name} to inventory',
            'inventory': [item.to_dict() for item in self.inventories[user_id]]
        }
    
    def get_inventory(self, user_id: str) -> Dict:
        """Get user's ingredient inventory."""
        inventory = self.inventories.get(user_id, [])
        
        # Organize by location
        organized = {
            'pantry': [],
            'fridge': [],
            'freezer': []
        }
        
        for item in inventory:
            organized[item.location].append(item.to_dict())
        
        return {
            'inventory': organized,
            'total_items': len(inventory),
            'expiring_soon': self._get_expiring_items(inventory)
        }
    
    def update_inventory_item(self, user_id: str, item_name: str, updates: Dict) -> Dict:
        """Update inventory item."""
        if user_id not in self.inventories:
            return {'error': 'Inventory not found'}
        
        for item in self.inventories[user_id]:
            if item.name.lower() == item_name.lower():
                for key, value in updates.items():
                    if hasattr(item, key):
                        setattr(item, key, value)
                
                return {
                    'status': 'success',
                    'message': f'Updated {item_name}',
                    'item': item.to_dict()
                }
        
        return {'error': 'Item not found in inventory'}
    
    def remove_from_inventory(self, user_id: str, item_name: str) -> Dict:
        """Remove item from inventory."""
        if user_id not in self.inventories:
            return {'error': 'Inventory not found'}
        
        for i, item in enumerate(self.inventories[user_id]):
            if item.name.lower() == item_name.lower():
                removed = self.inventories[user_id].pop(i)
                return {
                    'status': 'success',
                    'message': f'Removed {item_name} from inventory',
                    'removed_item': removed.to_dict()
                }
        
        return {'error': 'Item not found'}
    
    def get_recipes_from_inventory(self, user_id: str) -> Dict:
        """Get recipe suggestions based on inventory."""
        inventory = self.inventories.get(user_id, [])
        available_ingredients = [item.name for item in inventory]
        
        return {
            'available_ingredients': available_ingredients,
            'message': 'Use leftover_recipes endpoint with these ingredients'
        }
    
    def _get_expiring_items(self, inventory: List[IngredientInventory]) -> List[Dict]:
        """Get items expiring soon."""
        expiring = []
        today = datetime.date.today()
        
        for item in inventory:
            if item.expiry_date:
                try:
                    expiry = datetime.datetime.fromisoformat(item.expiry_date).date()
                    days_until_expiry = (expiry - today).days
                    
                    if 0 <= days_until_expiry <= 7:
                        expiring.append({
                            'item': item.to_dict(),
                            'days_until_expiry': days_until_expiry
                        })
                except:
                    pass
        
        return expiring
    
    # Recipe Collections/Cookbooks
    def create_collection(self, user_id: str, name: str, description: str = '', 
                         tags: List[str] = None, is_public: bool = False) -> Dict:
        """Create a new recipe collection."""
        if user_id not in self.collections:
            self.collections[user_id] = []
        
        collection_id = f"collection_{len(self.collections[user_id]) + 1}"
        collection = RecipeCollection(
            id=collection_id,
            name=name,
            description=description,
            recipes=[],
            tags=tags or [],
            created_date=datetime.datetime.now().isoformat(),
            updated_date=datetime.datetime.now().isoformat(),
            cover_image=None,
            is_public=is_public
        )
        
        self.collections[user_id].append(collection)
        
        return {
            'status': 'success',
            'collection': collection.to_dict(),
            'message': f'Collection "{name}" created successfully'
        }
    
    def add_recipe_to_collection(self, user_id: str, collection_id: str, 
                                recipe_name: str) -> Dict:
        """Add recipe to collection."""
        collection = self._get_collection(user_id, collection_id)
        if not collection:
            return {'error': 'Collection not found'}
        
        if recipe_name not in collection.recipes:
            collection.recipes.append(recipe_name)
            collection.updated_date = datetime.datetime.now().isoformat()
        
        return {
            'status': 'success',
            'collection': collection.to_dict(),
            'message': f'Added {recipe_name} to collection'
        }
    
    def get_collections(self, user_id: str) -> Dict:
        """Get user's recipe collections."""
        collections = self.collections.get(user_id, [])
        return {
            'collections': [c.to_dict() for c in collections],
            'total': len(collections)
        }
    
    def _get_collection(self, user_id: str, collection_id: str) -> Optional[RecipeCollection]:
        """Get collection by ID."""
        collections = self.collections.get(user_id, [])
        for collection in collections:
            if collection.id == collection_id:
                return collection
        return None
    
    # Cooking Challenges
    def create_challenge(self, user_id: str, challenge_type: ChallengeType, 
                        title: str, description: str, target_recipes: List[str],
                        duration_days: int = 7, difficulty: str = 'medium') -> Dict:
        """Create a new cooking challenge."""
        if user_id not in self.challenges:
            self.challenges[user_id] = []
        
        challenge_id = f"challenge_{len(self.challenges[user_id]) + 1}"
        start_date = datetime.datetime.now()
        end_date = start_date + datetime.timedelta(days=duration_days)
        
        challenge = CookingChallenge(
            id=challenge_id,
            user_id=user_id,
            challenge_type=challenge_type,
            title=title,
            description=description,
            start_date=start_date.isoformat(),
            end_date=end_date.isoformat(),
            target_recipes=target_recipes,
            completed_recipes=[],
            progress_percentage=0.0,
            rewards=self._generate_challenge_rewards(challenge_type),
            difficulty=difficulty,
            is_active=True
        )
        
        self.challenges[user_id].append(challenge)
        
        return {
            'status': 'success',
            'challenge': challenge.to_dict(),
            'message': f'Challenge "{title}" created successfully'
        }
    
    def complete_challenge_recipe(self, user_id: str, challenge_id: str, 
                                 recipe_name: str) -> Dict:
        """Mark a recipe as completed in a challenge."""
        challenge = self._get_challenge(user_id, challenge_id)
        if not challenge:
            return {'error': 'Challenge not found'}
        
        if recipe_name not in challenge.completed_recipes:
            challenge.completed_recipes.append(recipe_name)
            challenge.progress_percentage = (
                len(challenge.completed_recipes) / len(challenge.target_recipes) * 100
            )
        
        # Check if challenge is completed
        is_completed = challenge.progress_percentage >= 100
        
        return {
            'status': 'success',
            'challenge': challenge.to_dict(),
            'completed': is_completed,
            'message': f'Completed {recipe_name}!' + 
                      (' Challenge completed!' if is_completed else '')
        }
    
    def get_active_challenges(self, user_id: str) -> Dict:
        """Get active challenges for user."""
        challenges = self.challenges.get(user_id, [])
        active = [c for c in challenges if c.is_active]
        
        return {
            'challenges': [c.to_dict() for c in active],
            'total': len(active)
        }
    
    def _get_challenge(self, user_id: str, challenge_id: str) -> Optional[CookingChallenge]:
        """Get challenge by ID."""
        challenges = self.challenges.get(user_id, [])
        for challenge in challenges:
            if challenge.id == challenge_id:
                return challenge
        return None
    
    def _generate_challenge_rewards(self, challenge_type: ChallengeType) -> List[str]:
        """Generate rewards for completing challenge."""
        rewards_map = {
            ChallengeType.WEEKLY_RECIPE: ['Chef Badge', 'Recipe Explorer'],
            ChallengeType.TECHNIQUE_MASTER: ['Technique Master Badge', 'Skill Level Up'],
            ChallengeType.CUISINE_EXPLORER: ['World Traveler Badge', 'Cuisine Expert'],
            ChallengeType.HEALTHY_EATING: ['Health Champion Badge', 'Wellness Warrior'],
            ChallengeType.MEAL_PREP: ['Meal Prep Pro Badge', 'Organization Master'],
            ChallengeType.SPEED_COOKING: ['Speed Chef Badge', 'Time Saver']
        }
        return rewards_map.get(challenge_type, ['Achievement Unlocked'])
    
    # Meal Prep Planning
    def create_meal_prep_plan(self, user_id: str, recipes: List[Dict], 
                            week_start: str) -> Dict:
        """Create a meal prep plan for the week."""
        plan_id = f"mealprep_{len(self.meal_prep_plans.get(user_id, [])) + 1}"
        
        # Generate batch cooking schedule
        batch_schedule = self._generate_batch_schedule(recipes)
        
        # Generate prep timeline
        prep_timeline = self._generate_prep_timeline(recipes)
        
        # Generate storage instructions
        storage_instructions = self._generate_storage_instructions(recipes)
        
        plan = MealPrepPlan(
            id=plan_id,
            user_id=user_id,
            week_start=week_start,
            recipes=recipes,
            batch_cooking_schedule=batch_schedule,
            shopping_list={},  # Would be generated separately
            prep_timeline=prep_timeline,
            storage_instructions=storage_instructions,
            created_date=datetime.datetime.now().isoformat()
        )
        
        if user_id not in self.meal_prep_plans:
            self.meal_prep_plans[user_id] = []
        self.meal_prep_plans[user_id].append(plan)
        
        return {
            'status': 'success',
            'meal_prep_plan': plan.to_dict(),
            'message': 'Meal prep plan created successfully'
        }
    
    def _generate_batch_schedule(self, recipes: List[Dict]) -> List[Dict]:
        """Generate batch cooking schedule."""
        schedule = []
        day = 1
        
        for recipe in recipes[:5]:  # Limit to 5 recipes
            schedule.append({
                'day': day,
                'recipe': recipe.get('name', 'Unknown'),
                'prep_time': recipe.get('prep_time', '30 minutes'),
                'batch_size': recipe.get('servings', 4),
                'notes': f"Batch cook {recipe.get('name', 'recipe')} for the week"
            })
            day += 1
        
        return schedule
    
    def _generate_prep_timeline(self, recipes: List[Dict]) -> List[Dict]:
        """Generate prep timeline with tasks."""
        timeline = []
        total_time = 0
        
        # Prep tasks
        prep_tasks = ['Chop vegetables', 'Cook proteins', 'Prepare sauces', 
                     'Cook grains', 'Assemble containers']
        
        for i, task in enumerate(prep_tasks[:len(recipes)]):
            timeline.append({
                'task': task,
                'estimated_time': '30 minutes',
                'order': i + 1,
                'description': f'Complete {task} for meal prep'
            })
            total_time += 30
        
        timeline.append({
            'task': 'Total Prep Time',
            'estimated_time': f'{total_time} minutes',
            'order': len(timeline) + 1,
            'description': 'Total time needed for meal prep'
        })
        
        return timeline
    
    def _generate_storage_instructions(self, recipes: List[Dict]) -> Dict:
        """Generate storage instructions."""
        return {
            'containers': 'Use airtight containers',
            'fridge': {
                'duration': '3-5 days',
                'temperature': '40°F or below',
                'items': ['Cooked meals', 'Prepared ingredients']
            },
            'freezer': {
                'duration': '2-3 months',
                'temperature': '0°F or below',
                'items': ['Soups', 'Stews', 'Baked goods']
            },
            'tips': [
                'Label containers with date and contents',
                'Cool food before storing',
                'Use freezer-safe containers for frozen meals',
                'Thaw in fridge overnight before reheating'
            ]
        }
    
    # Recipe History and Stats
    def track_recipe_cooked(self, user_id: str, recipe_name: str) -> Dict:
        """Track that user cooked a recipe."""
        self.user_recipe_history[user_id].append({
            'recipe_name': recipe_name,
            'date': datetime.datetime.now().isoformat()
        })
        
        # Update stats
        self._update_cooking_stats(user_id, recipe_name)
        
        return {
            'status': 'success',
            'message': f'Tracked {recipe_name}',
            'total_recipes_cooked': len(self.user_recipe_history[user_id])
        }
    
    def get_cooking_stats(self, user_id: str) -> Dict:
        """Get user's cooking statistics."""
        stats = self.cooking_stats.get(user_id, {})
        history = self.user_recipe_history.get(user_id, [])
        
        # Calculate stats
        if not stats:
            stats = {
                'total_recipes_cooked': len(history),
                'favorite_cuisine': self._get_favorite_cuisine(user_id),
                'most_cooked_recipe': self._get_most_cooked_recipe(user_id),
                'cooking_streak': self._calculate_cooking_streak(history),
                'total_cooking_time': self._calculate_total_time(history)
            }
            self.cooking_stats[user_id] = stats
        
        return {
            'stats': stats,
            'recent_recipes': history[-10:]  # Last 10 recipes
        }
    
    def _update_cooking_stats(self, user_id: str, recipe_name: str):
        """Update cooking statistics."""
        # This would update various stats
        pass
    
    def _get_favorite_cuisine(self, user_id: str) -> str:
        """Get user's favorite cuisine based on cooking history."""
        # Simplified - would analyze recipe history
        return 'Italian'
    
    def _get_most_cooked_recipe(self, user_id: str) -> str:
        """Get most cooked recipe."""
        history = self.user_recipe_history.get(user_id, [])
        if not history:
            return 'None'
        
        recipe_counts = defaultdict(int)
        for entry in history:
            recipe_counts[entry['recipe_name']] += 1
        
        if recipe_counts:
            return max(recipe_counts.items(), key=lambda x: x[1])[0]
        return 'None'
    
    def _calculate_cooking_streak(self, history: List[Dict]) -> int:
        """Calculate consecutive days cooking streak."""
        if not history:
            return 0
        
        # Simplified calculation
        return min(len(history), 30)
    
    def _calculate_total_time(self, history: List[Dict]) -> str:
        """Calculate total cooking time."""
        # Simplified - would sum actual prep times
        total_minutes = len(history) * 30
        hours = total_minutes // 60
        minutes = total_minutes % 60
        return f"{hours} hours {minutes} minutes"
