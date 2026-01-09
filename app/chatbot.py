"""
Recipe Assistant Bot - Core Chatbot Logic
Author: RSK World (https://rskworld.in)
Founder: Molla Samser
Designer & Tester: Rima Khatun
Contact: help@rskworld.in, +91 93305 39277
Year: 2026
"""

import json
import random
import re
import datetime
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from collections import defaultdict

class RecipeChatbot:
    """Main chatbot class for recipe assistance."""
    
    def __init__(self):
        """Initialize the chatbot with recipe data."""
        self.recipes = self._load_recipes()
        self.substitutions = self._load_substitutions()
        self.cooking_tips = self._load_cooking_tips()
        self.dietary_options = ['vegetarian', 'vegan', 'gluten-free', 'dairy-free', 'keto', 'paleo']
        self.nutritional_data = self._load_nutritional_data()
        self.ingredient_costs = self._load_ingredient_costs()
        self.meal_plans = {}  # Store meal plans by user/session
        self.shopping_lists = {}  # Store shopping lists
        self.favorites = set()  # Store favorite recipes
        self.ratings = {}  # Store recipe ratings
        self.user_preferences = {}  # Store user preferences
        self.meal_history = defaultdict(list)  # Track meal history
        self.seasonal_ingredients = self._load_seasonal_ingredients()
        self.cuisine_types = ['italian', 'mexican', 'asian', 'indian', 'mediterranean', 'american', 'french', 'thai']
    
    def _load_recipes(self) -> List[Dict]:
        """Load recipe data."""
        return [
            {
                'name': 'Spaghetti Carbonara',
                'ingredients': ['spaghetti', 'eggs', 'bacon', 'parmesan cheese', 'black pepper'],
                'instructions': 'Cook pasta. Fry bacon. Mix eggs and cheese. Combine all ingredients.',
                'prep_time': '20 minutes',
                'difficulty': 'easy',
                'dietary': ['vegetarian']
            },
            {
                'name': 'Chicken Stir Fry',
                'ingredients': ['chicken breast', 'mixed vegetables', 'soy sauce', 'garlic', 'ginger'],
                'instructions': 'Cut chicken into pieces. Stir-fry vegetables. Add chicken and sauce.',
                'prep_time': '25 minutes',
                'difficulty': 'easy',
                'dietary': ['gluten-free']
            },
            {
                'name': 'Vegetable Curry',
                'ingredients': ['mixed vegetables', 'coconut milk', 'curry powder', 'onion', 'garlic'],
                'instructions': 'Sauté onions and garlic. Add vegetables and curry powder. Simmer with coconut milk.',
                'prep_time': '30 minutes',
                'difficulty': 'medium',
                'dietary': ['vegan', 'gluten-free']
            },
            {
                'name': 'Greek Salad',
                'ingredients': ['tomatoes', 'cucumber', 'red onion', 'feta cheese', 'olives', 'olive oil'],
                'instructions': 'Chop all vegetables. Mix with olive oil and seasonings. Add feta and olives.',
                'prep_time': '15 minutes',
                'difficulty': 'easy',
                'dietary': ['vegetarian', 'gluten-free']
            },
            {
                'name': 'Beef Tacos',
                'ingredients': ['ground beef', 'taco shells', 'lettuce', 'tomatoes', 'cheese', 'sour cream'],
                'instructions': 'Brown ground beef with spices. Warm taco shells. Fill with beef and toppings.',
                'prep_time': '20 minutes',
                'difficulty': 'easy',
                'dietary': ['keto'],
                'cuisine': 'mexican',
                'calories': 350,
                'protein': 25,
                'carbs': 15,
                'fat': 22
            },
            {
                'name': 'Margherita Pizza',
                'ingredients': ['pizza dough', 'tomato sauce', 'mozzarella', 'fresh basil', 'olive oil'],
                'instructions': 'Roll out dough. Add sauce and cheese. Bake at 475°F for 12-15 minutes. Top with basil.',
                'prep_time': '30 minutes',
                'difficulty': 'medium',
                'dietary': ['vegetarian'],
                'cuisine': 'italian',
                'calories': 280,
                'protein': 12,
                'carbs': 35,
                'fat': 10
            },
            {
                'name': 'Chicken Tikka Masala',
                'ingredients': ['chicken breast', 'yogurt', 'tikka masala spice', 'cream', 'rice', 'onion', 'garlic'],
                'instructions': 'Marinate chicken in yogurt and spices. Grill and add to creamy tomato sauce. Serve with rice.',
                'prep_time': '45 minutes',
                'difficulty': 'medium',
                'dietary': ['gluten-free'],
                'cuisine': 'indian',
                'calories': 420,
                'protein': 32,
                'carbs': 28,
                'fat': 18
            },
            {
                'name': 'Thai Green Curry',
                'ingredients': ['coconut milk', 'green curry paste', 'vegetables', 'tofu', 'basil', 'jasmine rice'],
                'instructions': 'Fry curry paste. Add coconut milk and vegetables. Simmer with tofu. Serve over rice.',
                'prep_time': '35 minutes',
                'difficulty': 'medium',
                'dietary': ['vegan', 'gluten-free'],
                'cuisine': 'thai',
                'calories': 320,
                'protein': 15,
                'carbs': 38,
                'fat': 14
            },
            {
                'name': 'Mediterranean Quinoa Bowl',
                'ingredients': ['quinoa', 'chickpeas', 'cucumber', 'tomatoes', 'feta', 'olives', 'lemon', 'tahini'],
                'instructions': 'Cook quinoa. Roast chickpeas. Chop vegetables. Assemble bowl with tahini dressing.',
                'prep_time': '25 minutes',
                'difficulty': 'easy',
                'dietary': ['vegetarian', 'gluten-free'],
                'cuisine': 'mediterranean',
                'calories': 380,
                'protein': 18,
                'carbs': 45,
                'fat': 16
            }
        ]
    
    def _load_substitutions(self) -> Dict[str, List[str]]:
        """Load ingredient substitution data."""
        return {
            'eggs': ['flax eggs (1 tbsp ground flax + 3 tbsp water)', 'applesauce (1/4 cup per egg)', 'banana (1/2 mashed banana per egg)'],
            'butter': ['coconut oil', 'olive oil', 'applesauce (for baking)', 'ghee'],
            'milk': ['almond milk', 'soy milk', 'coconut milk', 'oat milk', 'water (in some recipes)'],
            'flour': ['almond flour', 'coconut flour', 'oat flour', 'gluten-free flour blend'],
            'sugar': ['honey', 'maple syrup', 'stevia', 'coconut sugar', 'dates'],
            'cheese': ['nutritional yeast', 'cashew cheese', 'dairy-free cheese alternatives'],
            'sour cream': ['coconut cream', 'cashew cream', 'Greek yogurt', 'dairy-free sour cream'],
            'mayonnaise': ['Greek yogurt', 'avocado', 'hummus', 'vegan mayonnaise']
        }
    
    def _load_seasonal_ingredients(self) -> Dict[str, List[str]]:
        """Load seasonal ingredient data."""
        return {
            'spring': ['asparagus', 'artichokes', 'peas', 'rhubarb', 'strawberries', 'spinach', 'leeks'],
            'summer': ['tomatoes', 'zucchini', 'corn', 'berries', 'peppers', 'eggplant', 'watermelon'],
            'fall': ['pumpkin', 'squash', 'apples', 'pears', 'brussels sprouts', 'sweet potatoes', 'cranberries'],
            'winter': ['citrus', 'kale', 'cabbage', 'carrots', 'potatoes', 'onions', 'winter squash']
        }
    
    def _load_nutritional_data(self) -> Dict[str, Dict]:
        """Load nutritional data for ingredients."""
        return {
            'chicken breast': {'calories': 165, 'protein': 31, 'carbs': 0, 'fat': 3.6},
            'eggs': {'calories': 155, 'protein': 13, 'carbs': 1.1, 'fat': 11},
            'rice': {'calories': 130, 'protein': 2.7, 'carbs': 28, 'fat': 0.3},
            'quinoa': {'calories': 120, 'protein': 4.4, 'carbs': 21, 'fat': 1.9},
            'vegetables': {'calories': 50, 'protein': 2, 'carbs': 10, 'fat': 0.5}
        }
    
    def _load_ingredient_costs(self) -> Dict[str, float]:
        """Load ingredient cost data."""
        return {
            'chicken breast': 3.50,
            'eggs': 0.25,
            'rice': 0.10,
            'vegetables': 0.80,
            'cheese': 2.00,
            'pasta': 0.30
        }
    
    def _load_cooking_tips(self) -> Dict[str, List[str]]:
        """Load cooking tips by category."""
        return {
            'general': [
                'Always read the entire recipe before starting to cook.',
                'Prep all ingredients before you start cooking (mise en place).',
                'Taste your food as you cook and adjust seasonings.',
                'Let meat rest after cooking to retain juices.',
                'Use a sharp knife - it\'s safer and more efficient.'
            ],
            'baking': [
                'Measure ingredients precisely - baking is chemistry.',
                'Room temperature ingredients mix better.',
                'Don\'t overmix batter - it can make baked goods tough.',
                'Preheat your oven for consistent results.',
                'Use an oven thermometer for accuracy.'
            ],
            'knife_skills': [
                'Keep fingers curled under when chopping.',
                'Use the claw grip for safety.',
                'Sharpen knives regularly for better control.',
                'Cut on a stable surface.',
                'Clean knives immediately after use.'
            ],
            'food_storage': [
                'Store herbs like flowers in water.',
                'Keep tomatoes at room temperature for best flavor.',
                'Store mushrooms in paper bags.',
                'Freeze ginger for easy grating.',
                'Revive limp lettuce in ice water.'
            ]
        }
    
    def get_response(self, message: str) -> str:
        """Generate response to user message."""
        message_lower = message.lower()
        
        # Check for meal planning requests
        if any(word in message_lower for word in ['meal plan', 'meal planning', 'weekly meals', 'daily meals']):
            return self._handle_meal_plan_request(message)
        
        # Check for nutrition requests
        if any(word in message_lower for word in ['nutrition', 'calories', 'protein', 'carbs', 'fat']):
            return self._handle_nutrition_request(message)
        
        # Check for cost requests
        if any(word in message_lower for word in ['cost', 'price', 'how much', 'budget']):
            return self._handle_cost_request(message)
        
        # Check for shopping list requests
        if any(word in message_lower for word in ['shopping list', 'grocery list', 'buy ingredients']):
            return self._handle_shopping_list_request(message)
        
        # Check for rating requests
        if any(word in message_lower for word in ['rate', 'rating', 'review', 'score']):
            return self._handle_rating_request(message)
        
        # Check for favorites requests
        if any(word in message_lower for word in ['favorite', 'favourite', 'save', 'bookmark']):
            return self._handle_favorites_request(message)
        
        # Check for search requests
        if any(word in message_lower for word in ['search', 'find', 'looking for', 'filter']):
            return self._handle_search_request(message)
        
        # Check for timer requests
        if any(word in message_lower for word in ['timer', 'set timer', 'alarm', 'reminder']):
            return self._handle_timer_request(message)
        
        # Check for recipe requests
        if any(word in message_lower for word in ['recipe', 'cook', 'make', 'how to']):
            return self._handle_recipe_request(message)
        
        # Check for substitution requests
        if any(word in message_lower for word in ['substitute', 'replace', 'instead of', 'alternative']):
            return self._handle_substitution_request(message)
        
        # Check for cooking tips
        if any(word in message_lower for word in ['tip', 'help', 'advice', 'how do']):
            return self._handle_tips_request(message)
        
        # Check for dietary restrictions
        if any(diet in message_lower for diet in self.dietary_options):
            return self._handle_dietary_request(message)
        
        # Check for AI-powered recommendations
        if any(word in message_lower for word in ['recommend', 'suggest', 'what should', 'feel like', 'craving']):
            return self._handle_ai_recommendation_request(message)
        
        # Check for seasonal requests
        if any(word in message_lower for word in ['seasonal', 'fresh', 'available now']):
            return self._handle_seasonal_request(message)
        
        # Check for cuisine preferences
        if any(cuisine in message_lower for cuisine in self.cuisine_types):
            return self._handle_cuisine_request(message)
        
        # Default response
        return self._get_default_response()
    
    def _handle_recipe_request(self, message: str) -> str:
        """Handle recipe-related requests."""
        message_lower = message.lower()
        
        # Find matching recipes based on ingredients mentioned
        matching_recipes = []
        for recipe in self.recipes:
            if any(ingredient in message_lower for ingredient in recipe['ingredients']):
                matching_recipes.append(recipe)
        
        if matching_recipes:
            recipe = random.choice(matching_recipes)
            return f"Here's a great recipe for {recipe['name']}!\n\nIngredients: {', '.join(recipe['ingredients'])}\n\nInstructions: {recipe['instructions']}\n\nPrep time: {recipe['prep_time']}\nDifficulty: {recipe['difficulty']}"
        
        # If no specific ingredients mentioned, suggest a random recipe
        recipe = random.choice(self.recipes)
        return f"How about trying {recipe['name']}?\n\nIngredients: {', '.join(recipe['ingredients'])}\n\nInstructions: {recipe['instructions']}\n\nPrep time: {recipe['prep_time']}\nDifficulty: {recipe['difficulty']}"
    
    def _handle_substitution_request(self, message: str) -> str:
        """Handle ingredient substitution requests."""
        message_lower = message.lower()
        
        for ingredient in self.substitutions:
            if ingredient in message_lower:
                subs = self.substitutions[ingredient]
                return f"Great substitutes for {ingredient}:\n" + "\n".join(f"• {sub}" for sub in subs)
        
        return "I can help with substitutions! What ingredient would you like to replace?"
    
    def _handle_tips_request(self, message: str) -> str:
        """Handle cooking tips requests."""
        message_lower = message.lower()
        
        for category in self.cooking_tips:
            if category in message_lower:
                tips = self.cooking_tips[category]
                return f"Here are some {category} cooking tips:\n" + "\n".join(f"• {tip}" for tip in tips[:3])
        
        # Give a random general tip
        tip = random.choice(self.cooking_tips['general'])
        return f"Here's a helpful cooking tip: {tip}"
    
    def _handle_dietary_request(self, message: str) -> str:
        """Handle dietary restriction requests."""
        message_lower = message.lower()
        
        for diet in self.dietary_options:
            if diet in message_lower:
                matching_recipes = [r for r in self.recipes if diet in r['dietary']]
                if matching_recipes:
                    recipe = random.choice(matching_recipes)
                    return f"Here's a {diet} recipe for {recipe['name']}!\n\nIngredients: {', '.join(recipe['ingredients'])}\n\nInstructions: {recipe['instructions']}"
                else:
                    return f"I don't have specific {diet} recipes right now, but I can help you modify recipes to be {diet}!"
        
        return "I can help with various dietary restrictions including vegetarian, vegan, gluten-free, dairy-free, keto, and paleo options!"
    
    def _get_default_response(self) -> str:
        """Get default response when no specific intent is detected."""
        responses = [
            "I'm here to help with recipes, meal planning, nutrition info, shopping lists, and cooking tips! What would you like to know?",
            "I can suggest recipes, create meal plans, calculate nutrition, generate shopping lists, and share cooking tips. What can I help you with today?",
            "Whether you need recipe ideas, meal planning, nutritional information, or cooking advice, I'm here to help! What's on your mind?"
        ]
        return random.choice(responses)
    
    def _handle_meal_plan_request(self, message: str) -> str:
        """Handle meal planning requests."""
        message_lower = message.lower()
        
        # Extract number of days
        days = 7  # default
        if 'week' in message_lower:
            days = 7
        elif '3 day' in message_lower or 'three day' in message_lower:
            days = 3
        elif '5 day' in message_lower or 'five day' in message_lower:
            days = 5
        elif '10 day' in message_lower or 'ten day' in message_lower:
            days = 10
        
        # Check for dietary restrictions
        dietary = ''
        for diet in self.dietary_options:
            if diet in message_lower:
                dietary = diet
                break
        
        meal_plan = self.create_meal_plan(days, dietary)
        
        response = f"Here's your {days}-day meal plan"
        if dietary:
            response += f" ({dietary})"
        response += ":\n\n"
        
        for day, meals in meal_plan['meal_plan'].items():
            response += f"**{day}**\n"
            for meal_type, meal_info in meals.items():
                response += f"  • {meal_type.capitalize()}: {meal_info['recipe']} ({meal_info['prep_time']})\n"
            response += "\n"
        
        return response
    
    def _handle_nutrition_request(self, message: str) -> str:
        """Handle nutrition information requests."""
        message_lower = message.lower()
        
        # Try to extract recipe name
        for recipe in self.recipes:
            if recipe['name'].lower() in message_lower:
                nutrition = self.calculate_nutrition(recipe['name'])
                if 'error' not in nutrition:
                    per_serving = nutrition['per_serving']
                    return f"Nutritional information for {recipe['name']} (per serving):\n" + \
                           f"• Calories: {per_serving['calories']} kcal\n" + \
                           f"• Protein: {per_serving['protein']}g\n" + \
                           f"• Carbohydrates: {per_serving['carbs']}g\n" + \
                           f"• Fat: {per_serving['fat']}g\n" + \
                           f"• Servings: {nutrition['servings']}"
        
        return "I can provide nutritional information for any recipe! Just ask 'What's the nutrition for [recipe name]?'"
    
    def _handle_cost_request(self, message: str) -> str:
        """Handle cost calculation requests."""
        message_lower = message.lower()
        
        # Try to extract recipe name
        for recipe in self.recipes:
            if recipe['name'].lower() in message_lower:
                cost = self.calculate_recipe_cost(recipe['name'])
                if 'error' not in cost:
                    return f"Cost breakdown for {recipe['name']}:\n" + \
                           f"• Total estimated cost: ${cost['total_cost']}\n" + \
                           f"• Cost per serving: ${cost['cost_per_serving']}\n" + \
                           f"• Servings: {cost['servings']}\n" + \
                           f"*Prices are estimates and may vary by location*"
        
        return "I can calculate the cost of any recipe! Just ask 'How much does [recipe name] cost?'"
    
    def _handle_shopping_list_request(self, message: str) -> str:
        """Handle shopping list generation requests."""
        # For simplicity, generate shopping list for a few popular recipes
        sample_recipes = ['Spaghetti Carbonara', 'Chicken Stir Fry', 'Greek Salad']
        shopping_list = self.generate_shopping_list(sample_recipes)
        
        response = f"Shopping list for {len(sample_recipes)} recipes:\n\n"
        for ingredient, info in shopping_list['shopping_list'].items():
            response += f"• {ingredient.capitalize()}\n"
        
        response += f"\nEstimated total cost: ${shopping_list['estimated_cost']}\n"
        response += "*Quantities may vary based on recipe requirements*"
        
        return response
    
    def _handle_rating_request(self, message: str) -> str:
        """Handle recipe rating requests."""
        return "You can rate any recipe from 1-5 stars! Just say 'Rate [recipe name] [1-5] stars' and I'll record your rating."
    
    def _handle_favorites_request(self, message: str) -> str:
        """Handle favorites requests."""
        message_lower = message.lower()
        
        # Try to extract recipe name for adding to favorites
        for recipe in self.recipes:
            if recipe['name'].lower() in message_lower:
                result = self.add_to_favorites(recipe['name'])
                return f"✅ {recipe['name']} has been added to your favorites! You now have {result['total_favorites']} favorite recipes."
        
        # Show current favorites
        favorites = self.get_favorites()
        if favorites:
            return f"Your favorite recipes:\n" + "\n".join(f"• {fav}" for fav in favorites)
        else:
            return "You don't have any favorite recipes yet! Say 'Add [recipe name] to favorites' to get started."
    
    def _handle_search_request(self, message: str) -> str:
        """Handle recipe search requests."""
        message_lower = message.lower()
        
        # Extract search query
        query = message_lower.replace('search', '').replace('find', '').replace('looking for', '').strip()
        
        if not query:
            return "What would you like me to search for? You can search by recipe name, ingredient, or cuisine type."
        
        # Apply basic filters
        filters = {}
        for diet in self.dietary_options:
            if diet in message_lower:
                filters['dietary'] = diet
        
        if 'easy' in message_lower:
            filters['difficulty'] = 'easy'
        elif 'medium' in message_lower:
            filters['difficulty'] = 'medium'
        
        results = self.search_recipes(query, filters)
        
        if results:
            response = f"Found {len(results)} recipes matching '{query}':\n\n"
            for recipe in results[:5]:  # Show top 5
                rating_info = ""
                if 'average_rating' in recipe:
                    rating_info = f" (⭐ {recipe['average_rating']}/5)"
                response += f"• {recipe['name']}{rating_info}\n"
                response += f"  {recipe['prep_time']} • {recipe['difficulty']}\n"
            return response
        else:
            return f"No recipes found matching '{query}'. Try different keywords!"
    
    def _handle_timer_request(self, message: str) -> str:
        """Handle cooking timer requests."""
        message_lower = message.lower()
        
        # Extract time
        import re
        time_match = re.search(r'(\d+)\s*(minutes?|hours?)', message_lower)
        
        if time_match:
            amount = int(time_match.group(1))
            unit = time_match.group(2)
            
            if 'hour' in unit:
                minutes = amount * 60
                time_str = f"{amount} hour{'s' if amount > 1 else ''}"
            else:
                minutes = amount
                time_str = f"{amount} minute{'s' if amount > 1 else ''}"
            
            return f"⏰ Timer set for {time_str}! I'll remind you when it's time to check your cooking.\n\n*Note: This is a simulated timer. In a real app, you'd get an actual notification.*"
        
        return "I can set a cooking timer for you! Just say 'Set timer for [number] minutes/hours'."
    
    def get_recipe_suggestions(self, query: str = '', dietary: str = '') -> List[Dict]:
        """Get recipe suggestions based on query and dietary restrictions."""
        suggestions = self.recipes
        
        if dietary:
            suggestions = [r for r in suggestions if dietary in r['dietary']]
        
        if query:
            query_lower = query.lower()
            suggestions = [r for r in suggestions if 
                          any(query_lower in ingredient.lower() for ingredient in r['ingredients']) or
                          query_lower in r['name'].lower()]
        
        return suggestions[:5]  # Return max 5 suggestions
    
    def get_ingredient_substitutions(self, ingredient: str) -> List[str]:
        """Get substitutions for a specific ingredient."""
        ingredient_lower = ingredient.lower()
        
        for key, subs in self.substitutions.items():
            if key in ingredient_lower or ingredient_lower in key:
                return subs
        
        return ["No specific substitutions found for this ingredient."]
    
    def get_cooking_tips(self, category: str = 'general') -> List[str]:
        """Get cooking tips by category."""
        if category in self.cooking_tips:
            return self.cooking_tips[category]
        return self.cooking_tips['general']
    
    def _load_nutritional_data(self) -> Dict[str, Dict]:
        """Load nutritional information for ingredients."""
        return {
            'eggs': {'calories': 155, 'protein': 13, 'carbs': 1, 'fat': 11, 'unit': '2 large eggs'},
            'chicken breast': {'calories': 165, 'protein': 31, 'carbs': 0, 'fat': 3.6, 'unit': '100g'},
            'rice': {'calories': 130, 'protein': 2.7, 'carbs': 28, 'fat': 0.3, 'unit': '100g cooked'},
            'pasta': {'calories': 131, 'protein': 5, 'carbs': 25, 'fat': 1.1, 'unit': '100g'},
            'tomatoes': {'calories': 18, 'protein': 0.9, 'carbs': 3.9, 'fat': 0.2, 'unit': '100g'},
            'onions': {'calories': 40, 'protein': 1.1, 'carbs': 9.3, 'fat': 0.1, 'unit': '100g'},
            'garlic': {'calories': 149, 'protein': 6.4, 'carbs': 33, 'fat': 0.5, 'unit': '100g'},
            'olive oil': {'calories': 884, 'protein': 0, 'carbs': 0, 'fat': 100, 'unit': '100ml'},
            'cheese': {'calories': 402, 'protein': 25, 'carbs': 1.3, 'fat': 33, 'unit': '100g'},
            'vegetables': {'calories': 35, 'protein': 2, 'carbs': 7, 'fat': 0.2, 'unit': '100g mixed'}
        }
    
    def _load_ingredient_costs(self) -> Dict[str, float]:
        """Load approximate ingredient costs in USD."""
        return {
            'eggs': 0.25,  # per egg
            'chicken breast': 3.99,  # per pound
            'rice': 2.99,  # per pound
            'pasta': 1.99,  # per pound
            'tomatoes': 2.49,  # per pound
            'onions': 1.99,  # per pound
            'garlic': 0.50,  # per bulb
            'olive oil': 8.99,  # per liter
            'cheese': 5.99,  # per pound
            'vegetables': 3.49,  # per pound mixed
            'bacon': 6.99,  # per pound
            'parmesan cheese': 8.99,  # per pound
            'coconut milk': 2.49,  # per can
            'curry powder': 3.99,  # per jar
            'soy sauce': 2.99,  # per bottle
            'ginger': 2.99,  # per pound
            'feta cheese': 6.99,  # per pound
            'olives': 4.99,  # per jar
            'ground beef': 4.99,  # per pound
            'taco shells': 2.99,  # per package
            'lettuce': 2.49,  # per head
            'sour cream': 3.99,  # per container
            'taco seasoning': 1.99,  # per packet
            'salsa': 3.49  # per jar
        }
    
    def calculate_nutrition(self, recipe_name: str) -> Dict:
        """Calculate nutritional information for a recipe."""
        recipe = next((r for r in self.recipes if r['name'].lower() == recipe_name.lower()), None)
        if not recipe:
            return {'error': 'Recipe not found'}
        
        total_nutrition = {'calories': 0, 'protein': 0, 'carbs': 0, 'fat': 0}
        ingredient_details = []
        
        for ingredient in recipe['ingredients']:
            # Find matching nutritional data
            nutrition_key = None
            for key in self.nutritional_data:
                if key in ingredient.lower():
                    nutrition_key = key
                    break
            
            if nutrition_key:
                nutrition = self.nutritional_data[nutrition_key]
                total_nutrition['calories'] += nutrition['calories']
                total_nutrition['protein'] += nutrition['protein']
                total_nutrition['carbs'] += nutrition['carbs']
                total_nutrition['fat'] += nutrition['fat']
                ingredient_details.append({
                    'ingredient': ingredient,
                    'nutrition': nutrition
                })
        
        # Per serving calculation
        servings = recipe.get('servings', 4)
        per_serving = {
            'calories': round(total_nutrition['calories'] / servings, 1),
            'protein': round(total_nutrition['protein'] / servings, 1),
            'carbs': round(total_nutrition['carbs'] / servings, 1),
            'fat': round(total_nutrition['fat'] / servings, 1)
        }
        
        return {
            'recipe': recipe_name,
            'total': total_nutrition,
            'per_serving': per_serving,
            'servings': servings,
            'ingredients': ingredient_details
        }
    
    def calculate_recipe_cost(self, recipe_name: str) -> Dict:
        """Calculate approximate cost for a recipe."""
        recipe = next((r for r in self.recipes if r['name'].lower() == recipe_name.lower()), None)
        if not recipe:
            return {'error': 'Recipe not found'}
        
        total_cost = 0
        ingredient_costs = []
        
        for ingredient in recipe['ingredients']:
            # Find matching cost data
            cost_key = None
            for key in self.ingredient_costs:
                if key in ingredient.lower():
                    cost_key = key
                    break
            
            if cost_key:
                cost = self.ingredient_costs[cost_key]
                total_cost += cost
                ingredient_costs.append({
                    'ingredient': ingredient,
                    'estimated_cost': cost
                })
        
        servings = recipe.get('servings', 4)
        cost_per_serving = round(total_cost / servings, 2)
        
        return {
            'recipe': recipe_name,
            'total_cost': round(total_cost, 2),
            'cost_per_serving': cost_per_serving,
            'servings': servings,
            'currency': 'USD',
            'ingredients': ingredient_costs
        }
    
    def create_meal_plan(self, days: int = 7, dietary: str = '') -> Dict:
        """Create a meal plan for specified number of days."""
        available_recipes = self.recipes
        
        if dietary:
            available_recipes = [r for r in available_recipes if dietary in r.get('dietary', [])]
        
        meal_plan = {}
        meal_types = ['breakfast', 'lunch', 'dinner']
        
        for day in range(1, days + 1):
            meal_plan[f'Day {day}'] = {}
            for meal_type in meal_types:
                # Select a random recipe for each meal
                recipe = random.choice(available_recipes)
                meal_plan[f'Day {day}'][meal_type] = {
                    'recipe': recipe['name'],
                    'prep_time': recipe['prep_time'],
                    'difficulty': recipe['difficulty']
                }
        
        return {
            'meal_plan': meal_plan,
            'days': days,
            'dietary': dietary if dietary else 'none',
            'created_date': '2026-01-09'
        }
    
    def generate_shopping_list(self, recipes: List[str]) -> Dict:
        """Generate shopping list from recipe list."""
        shopping_list = {}
        total_estimated_cost = 0
        
        for recipe_name in recipes:
            recipe = next((r for r in self.recipes if r['name'].lower() == recipe_name.lower()), None)
            if recipe:
                for ingredient in recipe['ingredients']:
                    # Clean ingredient name
                    clean_ingredient = ingredient.lower().replace(',', '').strip()
                    
                    # Add to shopping list
                    if clean_ingredient not in shopping_list:
                        shopping_list[clean_ingredient] = {
                            'quantity': '1',
                            'unit': 'item',
                            'recipes': [recipe_name]
                        }
                    else:
                        shopping_list[clean_ingredient]['recipes'].append(recipe_name)
                    
                    # Estimate cost
                    for cost_key, cost in self.ingredient_costs.items():
                        if cost_key in clean_ingredient:
                            total_estimated_cost += cost
                            break
        
        return {
            'shopping_list': shopping_list,
            'total_recipes': len(recipes),
            'estimated_cost': round(total_estimated_cost, 2),
            'currency': 'USD'
        }
    
    def rate_recipe(self, recipe_name: str, rating: int, review: str = '') -> Dict:
        """Rate and review a recipe."""
        if rating < 1 or rating > 5:
            return {'error': 'Rating must be between 1 and 5'}
        
        if recipe_name not in self.ratings:
            self.ratings[recipe_name] = []
        
        self.ratings[recipe_name].append({
            'rating': rating,
            'review': review,
            'date': '2026-01-09'
        })
        
        # Calculate average rating
        ratings = self.ratings[recipe_name]
        avg_rating = sum(r['rating'] for r in ratings) / len(ratings)
        
        return {
            'recipe': recipe_name,
            'rating': rating,
            'review': review,
            'date': '2026-01-09',
            'average_rating': round(avg_rating, 1),
            'total_ratings': len(ratings),
            'status': 'success'
        }
    
    def _handle_ai_recommendation_request(self, message: str) -> str:
        """Handle AI-powered recipe recommendations."""
        message_lower = message.lower()
        
        # Analyze user preferences from message
        preferences = self._extract_preferences(message)
        
        # Get current season
        current_season = self._get_current_season()
        seasonal_ingredients = self.seasonal_ingredients.get(current_season, [])
        
        # Filter recipes based on preferences and seasonality
        recommended_recipes = []
        for recipe in self.recipes:
            score = 0
            
            # Check dietary preferences
            if 'dietary' in preferences:
                for diet in preferences['dietary']:
                    if diet in recipe.get('dietary', []):
                        score += 3
            
            # Check cuisine preferences
            if 'cuisine' in preferences and recipe.get('cuisine') == preferences['cuisine']:
                score += 2
            
            # Check for seasonal ingredients
            for ingredient in recipe['ingredients']:
                if any(seasonal in ingredient.lower() for seasonal in seasonal_ingredients):
                    score += 1
            
            # Check difficulty preference
            if 'difficulty' in preferences and recipe.get('difficulty') == preferences['difficulty']:
                score += 1
            
            # Check time preference
            if 'max_time' in preferences:
                recipe_time = int(recipe.get('prep_time', '0').split()[0])
                if recipe_time <= preferences['max_time']:
                    score += 1
            
            if score > 0:
                recipe['recommendation_score'] = score
                recommended_recipes.append(recipe)
        
        # Sort by recommendation score
        recommended_recipes.sort(key=lambda x: x.get('recommendation_score', 0), reverse=True)
        
        if recommended_recipes:
            best_recipe = recommended_recipes[0]
            return f"🍽️ **AI Recommendation:** {best_recipe['name']}\\n\\n**Why you'll love it:** This recipe matches your preferences perfectly!\\n\\n**Ingredients:** {', '.join(best_recipe['ingredients'])}\\n**Instructions:** {best_recipe['instructions']}\\n**Prep time:** {best_recipe['prep_time']}\\n**Difficulty:** {best_recipe['difficulty']}\\n**Cuisine:** {best_recipe.get('cuisine', 'International')}\\n**Calories:** {best_recipe.get('calories', 'N/A')}\\n\\nWould you like more suggestions or details about any aspect?"
        else:
            return "I'd be happy to recommend something! Could you tell me more about your preferences? For example:\\n- Any dietary restrictions?\\n- Preferred cuisine type?\\n- How much time do you have?\\n- Difficulty level?"
    
    def _handle_seasonal_request(self, message: str) -> str:
        """Handle seasonal recipe requests."""
        current_season = self._get_current_season()
        seasonal_ingredients = self.seasonal_ingredients.get(current_season, [])
        
        seasonal_recipes = []
        for recipe in self.recipes:
            for ingredient in recipe['ingredients']:
                if any(seasonal in ingredient.lower() for seasonal in seasonal_ingredients):
                    seasonal_recipes.append(recipe)
                    break
        
        if seasonal_recipes:
            recipe = random.choice(seasonal_recipes)
            return f"🌱 **Seasonal Special for {current_season.title()}:** {recipe['name']}\\n\\nPerfect for this time of year! Using fresh, seasonal ingredients.\\n\\n**Ingredients:** {', '.join(recipe['ingredients'])}\\n**Instructions:** {recipe['instructions']}\\n**Prep time:** {recipe['prep_time']}\\n**Difficulty:** {recipe['difficulty']}"
        else:
            return f"It's currently {current_season}, and I'd recommend using ingredients like {', '.join(seasonal_ingredients[:5])}. Would you like me to suggest recipes using any of these seasonal ingredients?"
    
    def _handle_cuisine_request(self, message: str) -> str:
        """Handle cuisine-specific requests."""
        message_lower = message.lower()
        
        for cuisine in self.cuisine_types:
            if cuisine in message_lower:
                cuisine_recipes = [r for r in self.recipes if r.get('cuisine') == cuisine]
                if cuisine_recipes:
                    recipe = random.choice(cuisine_recipes)
                    return f"🍴 **{cuisine.title()} Cuisine:** {recipe['name']}\\n\\nAuthentic flavors from {cuisine.title()}!\\n\\n**Ingredients:** {', '.join(recipe['ingredients'])}\\n**Instructions:** {recipe['instructions']}\\n**Prep time:** {recipe['prep_time']}\\n**Difficulty:** {recipe['difficulty']}\\n**Calories:** {recipe.get('calories', 'N/A')}"
                else:
                    return f"I don't have any {cuisine} recipes at the moment, but I can suggest similar alternatives. Would you like me to recommend something else?"
        
        return "Which cuisine type are you interested in? I can suggest recipes from Italian, Mexican, Asian, Indian, Mediterranean, American, French, or Thai cuisine!"
    
    def _extract_preferences(self, message: str) -> Dict:
        """Extract user preferences from message."""
        preferences = {}
        message_lower = message.lower()
        
        # Dietary preferences
        for diet in self.dietary_options:
            if diet in message_lower:
                preferences.setdefault('dietary', []).append(diet)
        
        # Cuisine preferences
        for cuisine in self.cuisine_types:
            if cuisine in message_lower:
                preferences['cuisine'] = cuisine
        
        # Time preferences
        time_patterns = [
            (r'(\\d+)\\s*minutes?', lambda m: int(m.group(1))),
            (r'(\\d+)\\s*hours?', lambda m: int(m.group(1)) * 60),
            (r'quick', lambda m: 20),
            (r'fast', lambda m: 20),
            (r'slow', lambda m: 60)
        ]
        
        for pattern, extractor in time_patterns:
            match = re.search(pattern, message_lower)
            if match:
                preferences['max_time'] = extractor(match)
                break
        
        # Difficulty preferences
        if 'easy' in message_lower:
            preferences['difficulty'] = 'easy'
        elif 'medium' in message_lower:
            preferences['difficulty'] = 'medium'
        elif 'hard' in message_lower or 'difficult' in message_lower:
            preferences['difficulty'] = 'hard'
        
        return preferences
    
    def _get_current_season(self) -> str:
        """Get current season based on date."""
        month = datetime.datetime.now().month
        if month in [3, 4, 5]:
            return 'spring'
        elif month in [6, 7, 8]:
            return 'summer'
        elif month in [9, 10, 11]:
            return 'fall'
        else:
            return 'winter'
    
    def get_personalized_meal_plan(self, days: int = 7, dietary: str = '', preferences: Dict = None) -> Dict:
        """Generate personalized meal plan using AI."""
        if preferences is None:
            preferences = {}
        
        meal_plan = {}
        used_recipes = set()
        
        for day in range(days):
            daily_meals = {}
            
            for meal_type in ['breakfast', 'lunch', 'dinner']:
                # Filter recipes based on dietary restrictions and preferences
                available_recipes = []
                for recipe in self.recipes:
                    if recipe['name'] in used_recipes:
                        continue
                    
                    # Check dietary restrictions
                    if dietary and dietary not in recipe.get('dietary', []):
                        continue
                    
                    # Check meal type appropriateness (simplified)
                    if meal_type == 'breakfast' and any(ing in recipe['name'].lower() for ing in ['pizza', 'taco']):
                        continue
                    
                    available_recipes.append(recipe)
                
                if available_recipes:
                    # Select recipe based on preferences
                    selected_recipe = self._select_best_recipe(available_recipes, preferences)
                    daily_meals[meal_type] = selected_recipe
                    used_recipes.add(selected_recipe['name'])
            
            meal_plan[f'Day {day + 1}'] = daily_meals
        
        return {
            'meal_plan': meal_plan,
            'shopping_list': self.generate_shopping_list(list(used_recipes)),
            'total_calories_per_day': self._calculate_daily_calories(meal_plan),
            'dietary_info': dietary or 'None specified'
        }
    
    def _select_best_recipe(self, recipes: List[Dict], preferences: Dict) -> Dict:
        """Select best recipe based on preferences using AI scoring."""
        if not recipes:
            return {}
        
        scored_recipes = []
        for recipe in recipes:
            score = 0
            
            # Score based on cuisine preference
            if 'cuisine' in preferences and recipe.get('cuisine') == preferences['cuisine']:
                score += 3
            
            # Score based on difficulty preference
            if 'difficulty' in preferences and recipe.get('difficulty') == preferences['difficulty']:
                score += 2
            
            # Score based on time preference
            if 'max_time' in preferences:
                recipe_time = int(recipe.get('prep_time', '0').split()[0])
                if recipe_time <= preferences['max_time']:
                    score += 2
            
            # Add some randomness for variety
            score += random.randint(0, 2)
            
            scored_recipes.append((recipe, score))
        
        # Return recipe with highest score
        return max(scored_recipes, key=lambda x: x[1])[0]
    
    def _calculate_daily_calories(self, meal_plan: Dict) -> Dict:
        """Calculate total calories per day."""
        daily_calories = {}
        
        for day, meals in meal_plan.items():
            total_calories = 0
            for meal in meals.values():
                if isinstance(meal, dict) and meal.get('calories'):
                    total_calories += meal['calories']
            daily_calories[day] = total_calories
        
        return daily_calories
    
    def add_to_favorites(self, recipe_name: str) -> Dict:
        """Add recipe to favorites."""
        self.favorites.add(recipe_name)
        return {
            'recipe': recipe_name,
            'message': 'Added to favorites',
            'total_favorites': len(self.favorites)
        }
    
    def get_favorites(self) -> List[str]:
        """Get list of favorite recipes."""
        return list(self.favorites)
    
    def search_recipes(self, query: str, filters: Dict = None) -> List[Dict]:
        """Search recipes with advanced filters."""
        results = []
        query_lower = query.lower()
        
        for recipe in self.recipes:
            # Text search
            matches_query = (
                query_lower in recipe['name'].lower() or
                any(query_lower in ingredient.lower() for ingredient in recipe['ingredients']) or
                query_lower in recipe.get('category', '').lower()
            )
            
            if not matches_query:
                continue
            
            # Apply filters
            if filters:
                # Dietary filter
                if 'dietary' in filters and filters['dietary']:
                    if filters['dietary'] not in recipe.get('dietary', []):
                        continue
                
                # Difficulty filter
                if 'difficulty' in filters and filters['difficulty']:
                    if recipe['difficulty'] != filters['difficulty']:
                        continue
                
                # Max prep time filter
                if 'max_prep_time' in filters:
                    prep_time = int(recipe['prep_time'].split()[0])
                    if prep_time > filters['max_prep_time']:
                        continue
            
            # Add rating info if available
            recipe_copy = recipe.copy()
            if recipe['name'] in self.ratings:
                ratings = self.ratings[recipe['name']]
                avg_rating = sum(r['rating'] for r in ratings) / len(ratings)
                recipe_copy['average_rating'] = round(avg_rating, 1)
                recipe_copy['total_ratings'] = len(ratings)
            
            results.append(recipe_copy)
        
        return results
    
    def scale_recipe(self, recipe_name: str, new_servings: int) -> Dict:
        """Scale recipe to different serving size."""
        recipe = next((r for r in self.recipes if r['name'].lower() == recipe_name.lower()), None)
        if not recipe:
            return {'error': 'Recipe not found'}
        
        original_servings = recipe.get('servings', 4)
        if original_servings == 0:
            original_servings = 4
        
        scale_factor = new_servings / original_servings
        
        scaled_recipe = recipe.copy()
        scaled_recipe['name'] = f"{recipe['name']} (Serves {new_servings})"
        scaled_recipe['servings'] = new_servings
        scaled_recipe['original_servings'] = original_servings
        scaled_recipe['scale_factor'] = round(scale_factor, 2)
        
        # Scale ingredients (simplified - in real app would parse quantities)
        scaled_ingredients = []
        for ingredient in recipe['ingredients']:
            # Try to detect quantities and scale them
            scaled_ingredients.append(ingredient)  # In real app, would parse and scale quantities
        
        scaled_recipe['ingredients'] = scaled_ingredients
        
        # Scale prep time (approximate - cooking time might not scale linearly)
        if 'prep_time' in recipe:
            original_time = int(recipe['prep_time'].split()[0])
            # Prep time scales, but cooking time less so
            scaled_prep = int(original_time * (0.7 + 0.3 * scale_factor))
            scaled_recipe['prep_time'] = f"{scaled_prep} minutes"
        
        # Recalculate nutrition if available
        if 'calories' in recipe:
            scaled_recipe['calories'] = int(recipe['calories'] * scale_factor)
            scaled_recipe['protein'] = round(recipe.get('protein', 0) * scale_factor, 1)
            scaled_recipe['carbs'] = round(recipe.get('carbs', 0) * scale_factor, 1)
            scaled_recipe['fat'] = round(recipe.get('fat', 0) * scale_factor, 1)
        
        return {
            'original_recipe': recipe['name'],
            'scaled_recipe': scaled_recipe,
            'servings': new_servings,
            'scale_factor': round(scale_factor, 2)
        }
    
    def generate_recipe_variations(self, recipe_name: str, variation_type: str = 'all') -> Dict:
        """Generate variations of a recipe."""
        recipe = next((r for r in self.recipes if r['name'].lower() == recipe_name.lower()), None)
        if not recipe:
            return {'error': 'Recipe not found'}
        
        variations = []
        
        # Cuisine variations
        if variation_type in ['all', 'cuisine']:
            cuisine_variations = {
                'italian': {'substitutions': {'soy sauce': 'balsamic vinegar', 'ginger': 'basil'}},
                'mexican': {'substitutions': {'basil': 'cilantro', 'parmesan': 'queso fresco'}},
                'asian': {'substitutions': {'basil': 'cilantro', 'olive oil': 'sesame oil'}},
                'indian': {'substitutions': {'basil': 'curry leaves', 'garlic': 'ginger-garlic paste'}}
            }
            
            for cuisine, changes in cuisine_variations.items():
                if cuisine != recipe.get('cuisine'):
                    variation = recipe.copy()
                    variation['name'] = f"{recipe['name']} ({cuisine.title()} Style)"
                    variation['cuisine'] = cuisine
                    variation['variation_type'] = 'cuisine'
                    variation['changes'] = changes
                    variations.append(variation)
        
        # Dietary variations
        if variation_type in ['all', 'dietary']:
            dietary_variations = {
                'vegan': {
                    'substitutions': {
                        'eggs': 'flax eggs',
                        'cheese': 'nutritional yeast',
                        'milk': 'plant milk',
                        'butter': 'coconut oil'
                    },
                    'remove': ['chicken', 'beef', 'pork', 'fish']
                },
                'gluten-free': {
                    'substitutions': {
                        'pasta': 'gluten-free pasta',
                        'flour': 'almond flour',
                        'bread': 'gluten-free bread'
                    }
                },
                'keto': {
                    'substitutions': {
                        'pasta': 'zucchini noodles',
                        'rice': 'cauliflower rice',
                        'sugar': 'stevia'
                    },
                    'remove': ['bread', 'pasta', 'rice']
                }
            }
            
            current_dietary = set(recipe.get('dietary', []))
            for diet, changes in dietary_variations.items():
                if diet not in current_dietary:
                    variation = recipe.copy()
                    variation['name'] = f"{recipe['name']} ({diet.title()})"
                    variation['dietary'] = list(current_dietary) + [diet]
                    variation['variation_type'] = 'dietary'
                    variation['changes'] = changes
                    variations.append(variation)
        
        # Spice level variations
        if variation_type in ['all', 'spice']:
            spice_levels = ['mild', 'medium', 'hot', 'extra hot']
            for level in spice_levels:
                variation = recipe.copy()
                variation['name'] = f"{recipe['name']} ({level.title()} Spice)"
                variation['spice_level'] = level
                variation['variation_type'] = 'spice'
                variations.append(variation)
        
        return {
            'original_recipe': recipe['name'],
            'variations': variations[:10],  # Limit to 10 variations
            'total_variations': len(variations)
        }
    
    def suggest_leftover_recipes(self, available_ingredients: List[str]) -> Dict:
        """Suggest recipes based on leftover/available ingredients."""
        matching_recipes = []
        
        for recipe in self.recipes:
            match_score = 0
            matched_ingredients = []
            missing_ingredients = []
            
            for ingredient in recipe['ingredients']:
                # Check if ingredient is available (simplified matching)
                ingredient_lower = ingredient.lower()
                matched = False
                
                for available in available_ingredients:
                    if available.lower() in ingredient_lower or ingredient_lower in available.lower():
                        match_score += 1
                        matched_ingredients.append(ingredient)
                        matched = True
                        break
                
                if not matched:
                    missing_ingredients.append(ingredient)
            
            if match_score > 0:
                completion_percentage = (match_score / len(recipe['ingredients'])) * 100
                recipe_copy = recipe.copy()
                recipe_copy['match_score'] = match_score
                recipe_copy['matched_ingredients'] = matched_ingredients
                recipe_copy['missing_ingredients'] = missing_ingredients
                recipe_copy['completion_percentage'] = round(completion_percentage, 1)
                matching_recipes.append(recipe_copy)
        
        # Sort by match score and completion percentage
        matching_recipes.sort(key=lambda x: (x['match_score'], x['completion_percentage']), reverse=True)
        
        return {
            'available_ingredients': available_ingredients,
            'suggested_recipes': matching_recipes[:10],
            'total_matches': len(matching_recipes)
        }