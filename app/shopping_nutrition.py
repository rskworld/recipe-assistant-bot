"""
Recipe Assistant Bot - Shopping List and Nutrition Manager
Author: RSK World (https://rskworld.in)
Founder: Molla Samser
Designer & Tester: Rima Khatun
Contact: help@rskworld.in, +91 93305 39277
Year: 2026
"""

import json
import datetime
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from collections import defaultdict

@dataclass
class ShoppingItem:
    """Shopping item with price and store information."""
    name: str
    quantity: float
    unit: str
    estimated_price: float
    store_suggestions: List[str]
    category: str
    priority: str
    notes: str
    
    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return asdict(self)

@dataclass
class NutritionGoal:
    """User nutrition goals."""
    user_id: str
    daily_calories: int
    daily_protein: float
    daily_carbs: float
    daily_fat: float
    daily_fiber: float
    daily_sugar: float
    daily_sodium: int
    created_date: str
    active: bool
    
    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return asdict(self)

class ShoppingListManager:
    """Manages shopping lists with price estimation."""
    
    def __init__(self):
        """Initialize shopping list manager."""
        self.shopping_lists = {}  # user_id -> shopping_list
        self.price_database = self._load_price_database()
        self.store_data = self._load_store_data()
        self.nutrition_goals = {}  # user_id -> nutrition_goal
    
    def _load_price_database(self) -> Dict[str, Dict]:
        """Load ingredient price database."""
        return {
            'vegetables': {
                'tomato': {'avg_price': 2.49, 'unit': 'pound', 'stores': ['Walmart', 'Kroger', 'Whole Foods']},
                'onion': {'avg_price': 1.99, 'unit': 'pound', 'stores': ['Walmart', 'Kroger', 'Aldi']},
                'garlic': {'avg_price': 0.50, 'unit': 'bulb', 'stores': ['Walmart', 'Kroger', 'Trader Joe\'s']},
                'carrot': {'avg_price': 1.49, 'unit': 'pound', 'stores': ['Walmart', 'Kroger', 'Aldi']},
                'lettuce': {'avg_price': 2.49, 'unit': 'head', 'stores': ['Walmart', 'Kroger', 'Whole Foods']},
                'cucumber': {'avg_price': 1.99, 'unit': 'each', 'stores': ['Walmart', 'Kroger', 'Trader Joe\'s']},
                'pepper': {'avg_price': 3.99, 'unit': 'pound', 'stores': ['Walmart', 'Kroger', 'Whole Foods']},
                'broccoli': {'avg_price': 2.99, 'unit': 'pound', 'stores': ['Walmart', 'Kroger', 'Whole Foods']},
                'spinach': {'avg_price': 3.49, 'unit': 'bag', 'stores': ['Walmart', 'Kroger', 'Whole Foods']},
                'mushroom': {'avg_price': 4.99, 'unit': 'pound', 'stores': ['Walmart', 'Kroger', 'Whole Foods']}
            },
            'fruits': {
                'apple': {'avg_price': 2.99, 'unit': 'pound', 'stores': ['Walmart', 'Kroger', 'Whole Foods']},
                'banana': {'avg_price': 0.59, 'unit': 'pound', 'stores': ['Walmart', 'Kroger', 'Aldi']},
                'orange': {'avg_price': 1.99, 'unit': 'pound', 'stores': ['Walmart', 'Kroger', 'Whole Foods']},
                'lemon': {'avg_price': 1.99, 'unit': 'pound', 'stores': ['Walmart', 'Kroger', 'Trader Joe\'s']},
                'strawberry': {'avg_price': 4.99, 'unit': 'pound', 'stores': ['Walmart', 'Kroger', 'Whole Foods']},
                'blueberry': {'avg_price': 5.99, 'unit': 'pint', 'stores': ['Walmart', 'Kroger', 'Whole Foods']}
            },
            'proteins': {
                'chicken breast': {'avg_price': 3.99, 'unit': 'pound', 'stores': ['Walmart', 'Kroger', 'Costco']},
                'ground beef': {'avg_price': 4.99, 'unit': 'pound', 'stores': ['Walmart', 'Kroger', 'Costco']},
                'pork': {'avg_price': 3.49, 'unit': 'pound', 'stores': ['Walmart', 'Kroger', 'Costco']},
                'fish': {'avg_price': 8.99, 'unit': 'pound', 'stores': ['Walmart', 'Kroger', 'Whole Foods']},
                'salmon': {'avg_price': 12.99, 'unit': 'pound', 'stores': ['Walmart', 'Kroger', 'Whole Foods']},
                'egg': {'avg_price': 3.99, 'unit': 'dozen', 'stores': ['Walmart', 'Kroger', 'Trader Joe\'s']},
                'tofu': {'avg_price': 2.99, 'unit': 'block', 'stores': ['Walmart', 'Kroger', 'Whole Foods']},
                'beans': {'avg_price': 1.99, 'unit': 'can', 'stores': ['Walmart', 'Kroger', 'Aldi']},
                'lentil': {'avg_price': 2.99, 'unit': 'bag', 'stores': ['Walmart', 'Kroger', 'Trader Joe\'s']}
            },
            'grains': {
                'rice': {'avg_price': 2.99, 'unit': 'pound', 'stores': ['Walmart', 'Kroger', 'Aldi']},
                'pasta': {'avg_price': 1.99, 'unit': 'pound', 'stores': ['Walmart', 'Kroger', 'Aldi']},
                'bread': {'avg_price': 2.49, 'unit': 'loaf', 'stores': ['Walmart', 'Kroger', 'Whole Foods']},
                'flour': {'avg_price': 2.99, 'unit': 'pound', 'stores': ['Walmart', 'Kroger', 'Aldi']},
                'oat': {'avg_price': 3.99, 'unit': 'canister', 'stores': ['Walmart', 'Kroger', 'Whole Foods']},
                'quinoa': {'avg_price': 6.99, 'unit': 'pound', 'stores': ['Walmart', 'Kroger', 'Whole Foods']},
                'barley': {'avg_price': 3.99, 'unit': 'pound', 'stores': ['Walmart', 'Kroger', 'Trader Joe\'s']},
                'couscous': {'avg_price': 2.99, 'unit': 'box', 'stores': ['Walmart', 'Kroger', 'Trader Joe\'s']}
            },
            'dairy': {
                'cheese': {'avg_price': 5.99, 'unit': 'pound', 'stores': ['Walmart', 'Kroger', 'Whole Foods']},
                'milk': {'avg_price': 3.99, 'unit': 'gallon', 'stores': ['Walmart', 'Kroger', 'Aldi']},
                'butter': {'avg_price': 4.99, 'unit': 'pound', 'stores': ['Walmart', 'Kroger', 'Whole Foods']},
                'yogurt': {'avg_price': 1.99, 'unit': 'cup', 'stores': ['Walmart', 'Kroger', 'Whole Foods']},
                'cream': {'avg_price': 3.99, 'unit': 'pint', 'stores': ['Walmart', 'Kroger', 'Whole Foods']},
                'sour cream': {'avg_price': 3.99, 'unit': 'container', 'stores': ['Walmart', 'Kroger', 'Whole Foods']}
            },
            'pantry': {
                'olive oil': {'avg_price': 8.99, 'unit': 'liter', 'stores': ['Walmart', 'Kroger', 'Whole Foods']},
                'soy sauce': {'avg_price': 3.99, 'unit': 'bottle', 'stores': ['Walmart', 'Kroger', 'Trader Joe\'s']},
                'tomato sauce': {'avg_price': 1.99, 'unit': 'can', 'stores': ['Walmart', 'Kroger', 'Aldi']},
                'coconut milk': {'avg_price': 2.49, 'unit': 'can', 'stores': ['Walmart', 'Kroger', 'Trader Joe\'s']},
                'curry powder': {'avg_price': 4.99, 'unit': 'jar', 'stores': ['Walmart', 'Kroger', 'Trader Joe\'s']},
                'spice': {'avg_price': 3.99, 'unit': 'jar', 'stores': ['Walmart', 'Kroger', 'Whole Foods']}
            }
        }
    
    def _load_store_data(self) -> Dict[str, Dict]:
        """Load store information."""
        return {
            'Walmart': {
                'price_tier': 'budget',
                'quality_rating': 3.5,
                'specialties': ['groceries', 'household'],
                'hours': '6 AM - 11 PM',
                'delivery_available': True
            },
            'Kroger': {
                'price_tier': 'mid_range',
                'quality_rating': 4.0,
                'specialties': ['groceries', 'organic'],
                'hours': '6 AM - 10 PM',
                'delivery_available': True
            },
            'Whole Foods': {
                'price_tier': 'premium',
                'quality_rating': 4.5,
                'specialties': ['organic', 'natural'],
                'hours': '7 AM - 9 PM',
                'delivery_available': True
            },
            'Trader Joe\'s': {
                'price_tier': 'mid_range',
                'quality_rating': 4.2,
                'specialties': ['unique', 'organic'],
                'hours': '8 AM - 9 PM',
                'delivery_available': False
            },
            'Aldi': {
                'price_tier': 'budget',
                'quality_rating': 3.7,
                'specialties': ['budget', 'essentials'],
                'hours': '9 AM - 8 PM',
                'delivery_available': False
            },
            'Costco': {
                'price_tier': 'bulk',
                'quality_rating': 4.1,
                'specialties': ['bulk', 'warehouse'],
                'hours': '10 AM - 6 PM',
                'delivery_available': True
            }
        }
    
    def create_shopping_list(self, user_id: str, recipes: List[str], 
                          preferences: Dict = None) -> Dict:
        """Create shopping list from recipes with price estimation."""
        if preferences is None:
            preferences = {}
        
        shopping_items = []
        total_estimated_cost = 0
        ingredient_quantities = defaultdict(float)
        
        # Aggregate ingredients from all recipes
        for recipe_name in recipes:
            # This would normally fetch from recipe database
            recipe_ingredients = self._get_recipe_ingredients(recipe_name)
            
            for ingredient, quantity in recipe_ingredients.items():
                ingredient_quantities[ingredient] += quantity
        
        # Create shopping items
        for ingredient, total_quantity in ingredient_quantities.items():
            item = self._create_shopping_item(ingredient, total_quantity, preferences)
            shopping_items.append(item)
            total_estimated_cost += item.estimated_price
        
        # Sort by category and priority
        shopping_items.sort(key=lambda x: (x.category, x.priority))
        
        shopping_list = {
            'user_id': user_id,
            'items': shopping_items,
            'total_estimated_cost': round(total_estimated_cost, 2),
            'total_items': len(shopping_items),
            'created_date': datetime.datetime.now().isoformat(),
            'recipes': recipes,
            'preferences': preferences
        }
        
        # Save shopping list
        self.shopping_lists[user_id] = shopping_list
        
        return shopping_list
    
    def _get_recipe_ingredients(self, recipe_name: str) -> Dict[str, float]:
        """Get ingredients for a recipe (mock implementation)."""
        # Mock recipe ingredients - in real app, this would query database
        recipe_ingredients = {
            'Spaghetti Carbonara': {
                'spaghetti': 0.5,  # pounds
                'egg': 4,  # count
                'bacon': 0.25,  # pounds
                'parmesan cheese': 0.25,  # pounds
                'black pepper': 0.05  # pounds
            },
            'Chicken Stir Fry': {
                'chicken breast': 1.5,  # pounds
                'mixed vegetables': 2,  # pounds
                'soy sauce': 0.25,  # liters
                'garlic': 0.1,  # pounds
                'ginger': 0.1  # pounds
            },
            'Greek Salad': {
                'tomato': 1,  # pounds
                'cucumber': 1,  # count
                'red onion': 0.5,  # pounds
                'feta cheese': 0.25,  # pounds
                'olives': 0.25,  # pounds
                'olive oil': 0.1  # liters
            }
        }
        
        return recipe_ingredients.get(recipe_name, {})
    
    def _create_shopping_item(self, ingredient: str, quantity: float, 
                           preferences: Dict) -> ShoppingItem:
        """Create a shopping item with price estimation."""
        # Find ingredient in price database
        price_info = self._find_ingredient_price(ingredient)
        
        if price_info:
            estimated_price = price_info['avg_price'] * quantity
            store_suggestions = price_info['stores']
            category = self._get_ingredient_category(ingredient)
        else:
            # Default values for unknown ingredients
            estimated_price = quantity * 3.99  # Default price
            store_suggestions = ['Walmart', 'Kroger']
            category = 'other'
        
        # Determine priority based on preferences
        priority = self._determine_priority(ingredient, preferences)
        
        # Generate notes
        notes = self._generate_item_notes(ingredient, quantity, preferences)
        
        return ShoppingItem(
            name=ingredient,
            quantity=quantity,
            unit=price_info['unit'] if price_info else 'item',
            estimated_price=round(estimated_price, 2),
            store_suggestions=store_suggestions,
            category=category,
            priority=priority,
            notes=notes
        )
    
    def _find_ingredient_price(self, ingredient: str) -> Optional[Dict]:
        """Find ingredient price in database."""
        ingredient_lower = ingredient.lower()
        
        for category, items in self.price_database.items():
            for item_name, price_info in items.items():
                if item_name in ingredient_lower or ingredient_lower in item_name:
                    return price_info
        
        return None
    
    def _get_ingredient_category(self, ingredient: str) -> str:
        """Get category for ingredient."""
        ingredient_lower = ingredient.lower()
        
        for category, items in self.price_database.items():
            for item_name in items.keys():
                if item_name in ingredient_lower or ingredient_lower in item_name:
                    return category
        
        return 'other'
    
    def _determine_priority(self, ingredient: str, preferences: Dict) -> str:
        """Determine shopping priority based on preferences."""
        # Check if ingredient is in dietary restrictions
        dietary_restrictions = preferences.get('dietary_restrictions', [])
        allergies = preferences.get('allergies', [])
        
        if any(allergy.lower() in ingredient.lower() for allergy in allergies):
            return 'avoid'
        
        # Check if ingredient is preferred
        preferred_ingredients = preferences.get('preferred_ingredients', [])
        if any(pref.lower() in ingredient.lower() for pref in preferred_ingredients):
            return 'high'
        
        # Default priority
        return 'medium'
    
    def _generate_item_notes(self, ingredient: str, quantity: float, 
                           preferences: Dict) -> str:
        """Generate notes for shopping item."""
        notes = []
        
        # Add dietary notes
        if 'organic' in preferences.get('preferences', []):
            notes.append('Consider organic option')
        
        if 'local' in preferences.get('preferences', []):
            notes.append('Look for local produce')
        
        # Add quantity notes
        if quantity > 1:
            notes.append(f'Buy in bulk for savings')
        
        # Add storage notes
        if 'tomato' in ingredient.lower():
            notes.append('Store at room temperature')
        elif 'leaf' in ingredient.lower() or 'lettuce' in ingredient.lower():
            notes.append('Refrigerate immediately')
        
        return '; '.join(notes) if notes else ''
    
    def get_shopping_list(self, user_id: str) -> Optional[Dict]:
        """Get user's shopping list."""
        return self.shopping_lists.get(user_id)
    
    def update_shopping_list(self, user_id: str, updates: Dict) -> Dict:
        """Update shopping list."""
        if user_id not in self.shopping_lists:
            return {'error': 'Shopping list not found'}
        
        shopping_list = self.shopping_lists[user_id]
        
        # Update items
        if 'items' in updates:
            for item_update in updates['items']:
                item_name = item_update.get('name')
                for i, item in enumerate(shopping_list['items']):
                    if item['name'] == item_name:
                        shopping_list['items'][i].update(item_update)
                        break
        
        # Recalculate total cost
        total_cost = sum(item['estimated_price'] for item in shopping_list['items'])
        shopping_list['total_estimated_cost'] = round(total_cost, 2)
        shopping_list['updated_date'] = datetime.datetime.now().isoformat()
        
        return shopping_list
    
    def compare_store_prices(self, user_id: str) -> Dict:
        """Compare prices across different stores."""
        shopping_list = self.get_shopping_list(user_id)
        
        if not shopping_list:
            return {'error': 'Shopping list not found'}
        
        store_prices = defaultdict(float)
        store_item_counts = defaultdict(int)
        
        for item in shopping_list['items']:
            price_info = self._find_ingredient_price(item['name'])
            
            if price_info:
                for store in price_info['stores']:
                    # Adjust price based on store tier
                    store_data = self.store_data.get(store, {})
                    price_multiplier = self._get_price_multiplier(store_data.get('price_tier', 'mid_range'))
                    
                    adjusted_price = price_info['avg_price'] * item['quantity'] * price_multiplier
                    store_prices[store] += adjusted_price
                    store_item_counts[store] += 1
        
        # Sort stores by total price
        sorted_stores = sorted(store_prices.items(), key=lambda x: x[1])
        
        return {
            'store_comparison': [
                {
                    'store': store,
                    'estimated_total': round(price, 2),
                    'item_count': store_item_counts[store],
                    'store_info': self.store_data.get(store, {})
                }
                for store, price in sorted_stores
            ],
            'cheapest_store': sorted_stores[0][0] if sorted_stores else None,
            'potential_savings': round(sorted_stores[-1][1] - sorted_stores[0][1], 2) if len(sorted_stores) > 1 else 0
        }
    
    def _get_price_multiplier(self, price_tier: str) -> float:
        """Get price multiplier based on store tier."""
        multipliers = {
            'budget': 0.9,
            'mid_range': 1.0,
            'premium': 1.3,
            'bulk': 0.8
        }
        return multipliers.get(price_tier, 1.0)
    
    def set_nutrition_goals(self, user_id: str, goals: Dict) -> Dict:
        """Set user nutrition goals."""
        nutrition_goal = NutritionGoal(
            user_id=user_id,
            daily_calories=goals.get('daily_calories', 2000),
            daily_protein=goals.get('daily_protein', 50),
            daily_carbs=goals.get('daily_carbs', 300),
            daily_fat=goals.get('daily_fat', 65),
            daily_fiber=goals.get('daily_fiber', 25),
            daily_sugar=goals.get('daily_sugar', 50),
            daily_sodium=goals.get('daily_sodium', 2300),
            created_date=datetime.datetime.now().isoformat(),
            active=goals.get('active', True)
        )
        
        self.nutrition_goals[user_id] = nutrition_goal
        
        return {
            'message': 'Nutrition goals set successfully',
            'goals': nutrition_goal.to_dict()
        }
    
    def track_daily_nutrition(self, user_id: str, meals: List[Dict]) -> Dict:
        """Track daily nutrition against goals."""
        if user_id not in self.nutrition_goals:
            return {'error': 'No nutrition goals set'}
        
        goals = self.nutrition_goals[user_id]
        
        # Calculate daily totals
        daily_totals = {
            'calories': sum(meal.get('calories', 0) for meal in meals),
            'protein': sum(meal.get('protein', 0) for meal in meals),
            'carbs': sum(meal.get('carbs', 0) for meal in meals),
            'fat': sum(meal.get('fat', 0) for meal in meals),
            'fiber': sum(meal.get('fiber', 0) for meal in meals),
            'sugar': sum(meal.get('sugar', 0) for meal in meals),
            'sodium': sum(meal.get('sodium', 0) for meal in meals)
        }
        
        # Calculate progress towards goals
        progress = {}
        for nutrient in daily_totals:
            goal_value = getattr(goals, f'daily_{nutrient}')
            current_value = daily_totals[nutrient]
            
            progress[nutrient] = {
                'current': current_value,
                'goal': goal_value,
                'percentage': round((current_value / goal_value) * 100, 1) if goal_value > 0 else 0,
                'status': self._get_nutrition_status(current_value, goal_value, nutrient)
            }
        
        return {
            'date': datetime.datetime.now().strftime('%Y-%m-%d'),
            'daily_totals': daily_totals,
            'goals': goals.to_dict(),
            'progress': progress,
            'overall_score': self._calculate_nutrition_score(progress)
        }
    
    def _get_nutrition_status(self, current: float, goal: float, nutrient: str) -> str:
        """Get nutrition status based on current vs goal."""
        if nutrient == 'sodium':
            # For sodium, lower is better
            if current <= goal:
                return 'excellent'
            elif current <= goal * 1.2:
                return 'good'
            else:
                return 'high'
        else:
            # For other nutrients, aim for goal range
            percentage = (current / goal) * 100 if goal > 0 else 0
            
            if 90 <= percentage <= 110:
                return 'excellent'
            elif 80 <= percentage <= 120:
                return 'good'
            elif percentage < 80:
                return 'low'
            else:
                return 'high'
    
    def _calculate_nutrition_score(self, progress: Dict) -> float:
        """Calculate overall nutrition score."""
        scores = []
        
        for nutrient_data in progress.values():
            status = nutrient_data['status']
            
            if status == 'excellent':
                scores.append(100)
            elif status == 'good':
                scores.append(80)
            elif status == 'low':
                scores.append(60)
            else:  # high
                scores.append(40)
        
        return round(sum(scores) / len(scores), 1) if scores else 0
