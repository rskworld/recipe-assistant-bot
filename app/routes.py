"""
Recipe Assistant Bot - Routes
Author: RSK World (https://rskworld.in)
Founder: Molla Samser
Designer & Tester: Rima Khatun
Contact: help@rskworld.in, +91 93305 39277
Year: 2026
"""

from flask import Blueprint, request, jsonify, render_template, session
from werkzeug.utils import secure_filename
from .chatbot import RecipeChatbot
from .auth import AuthManager
from .image_recognition import ImageRecognition
from .shopping_nutrition import ShoppingListManager
from .rating_review import RatingReviewManager
from .voice_assistant import VoiceAssistant
from .smart_kitchen import SmartKitchenManager
from .cooking_assistant import AICookingAssistant
from .advanced_features import AdvancedFeaturesManager, ChallengeType, IngredientInventory
import json
import os
import datetime

main_bp = Blueprint('main', __name__)
chatbot = RecipeChatbot()
auth_manager = AuthManager()
image_recognition = ImageRecognition()
shopping_manager = ShoppingListManager()
rating_manager = RatingReviewManager()
voice_assistant = VoiceAssistant()
smart_kitchen = SmartKitchenManager()
cooking_assistant = AICookingAssistant()
advanced_features = AdvancedFeaturesManager()

@main_bp.route('/')
def index():
    """Render the main chat interface."""
    return render_template('index.html')

@main_bp.route('/api/chat', methods=['POST'])
def chat():
    """Handle chat requests."""
    try:
        data = request.get_json()
        user_message = data.get('message', '').strip()
        
        if not user_message:
            return jsonify({'error': 'Message cannot be empty'}), 400
        
        # Get chatbot response
        response = chatbot.get_response(user_message)
        
        return jsonify({
            'response': response,
            'status': 'success'
        })
    
    except Exception as e:
        return jsonify({
            'error': f'An error occurred: {str(e)}',
            'status': 'error'
        }), 500

@main_bp.route('/api/recipes', methods=['GET'])
def get_recipes():
    """Get recipe suggestions based on query parameters."""
    try:
        query = request.args.get('query', '')
        dietary = request.args.get('dietary', '')
        
        recipes = chatbot.get_recipe_suggestions(query, dietary)
        
        return jsonify({
            'recipes': recipes,
            'status': 'success'
        })
    
    except Exception as e:
        return jsonify({
            'error': f'An error occurred: {str(e)}',
            'status': 'error'
        }), 500

@main_bp.route('/api/substitutions', methods=['POST'])
def get_substitutions():
    """Get ingredient substitutions."""
    try:
        data = request.get_json()
        ingredient = data.get('ingredient', '').strip()
        
        if not ingredient:
            return jsonify({'error': 'Ingredient cannot be empty'}), 400
        
        substitutions = chatbot.get_ingredient_substitutions(ingredient)
        
        return jsonify({
            'substitutions': substitutions,
            'status': 'success'
        })
    
    except Exception as e:
        return jsonify({
            'error': f'An error occurred: {str(e)}',
            'status': 'error'
        }), 500

@main_bp.route('/api/tips', methods=['GET'])
def get_cooking_tips():
    """Get cooking tips based on category."""
    try:
        category = request.args.get('category', 'general')
        tips = chatbot.get_cooking_tips(category)
        
        return jsonify({
            'tips': tips,
            'status': 'success'
        })
    
    except Exception as e:
        return jsonify({
            'error': f'An error occurred: {str(e)}',
            'status': 'error'
        }), 500

@main_bp.route('/api/meal-plan', methods=['POST'])
def create_meal_plan():
    """Create a meal plan."""
    try:
        data = request.get_json()
        days = data.get('days', 7)
        dietary = data.get('dietary', '')
        
        meal_plan = chatbot.create_meal_plan(days, dietary)
        
        return jsonify({
            'meal_plan': meal_plan,
            'status': 'success'
        })
    
    except Exception as e:
        return jsonify({
            'error': f'An error occurred: {str(e)}',
            'status': 'error'
        }), 500

@main_bp.route('/api/nutrition/<recipe_name>', methods=['GET'])
def get_nutrition(recipe_name):
    """Get nutritional information for a recipe."""
    try:
        nutrition = chatbot.calculate_nutrition(recipe_name)
        
        if 'error' in nutrition:
            return jsonify({
                'error': nutrition['error'],
                'status': 'error'
            }), 404
        
        return jsonify({
            'nutrition': nutrition,
            'status': 'success'
        })
    
    except Exception as e:
        return jsonify({
            'error': f'An error occurred: {str(e)}',
            'status': 'error'
        }), 500

@main_bp.route('/api/cost/<recipe_name>', methods=['GET'])
def get_recipe_cost(recipe_name):
    """Get cost information for a recipe."""
    try:
        cost = chatbot.calculate_recipe_cost(recipe_name)
        
        if 'error' in cost:
            return jsonify({
                'error': cost['error'],
                'status': 'error'
            }), 404
        
        return jsonify({
            'cost': cost,
            'status': 'success'
        })
    
    except Exception as e:
        return jsonify({
            'error': f'An error occurred: {str(e)}',
            'status': 'error'
        }), 500

@main_bp.route('/api/shopping-list', methods=['POST'])
def generate_shopping_list():
    """Generate shopping list from recipes."""
    try:
        data = request.get_json()
        recipes = data.get('recipes', [])
        
        if not recipes:
            return jsonify({'error': 'Recipes list cannot be empty'}), 400
        
        shopping_list = chatbot.generate_shopping_list(recipes)
        
        return jsonify({
            'shopping_list': shopping_list,
            'status': 'success'
        })
    
    except Exception as e:
        return jsonify({
            'error': f'An error occurred: {str(e)}',
            'status': 'error'
        }), 500

@main_bp.route('/api/favorites', methods=['GET', 'POST'])
def manage_favorites():
    """Get or add favorite recipes."""
    try:
        if request.method == 'GET':
            favorites = chatbot.get_favorites()
            return jsonify({
                'favorites': favorites,
                'status': 'success'
            })
        
        elif request.method == 'POST':
            data = request.get_json()
            recipe_name = data.get('recipe_name', '').strip()
            
            if not recipe_name:
                return jsonify({'error': 'Recipe name cannot be empty'}), 400
            
            result = chatbot.add_to_favorites(recipe_name)
            
            return jsonify({
                'result': result,
                'status': 'success'
            })
    
    except Exception as e:
        return jsonify({
            'error': f'An error occurred: {str(e)}',
            'status': 'error'
        }), 500

@main_bp.route('/api/rate', methods=['POST'])
def rate_recipe():
    """Rate a recipe."""
    try:
        data = request.get_json()
        recipe_name = data.get('recipe_name', '').strip()
        rating = data.get('rating', 0)
        review = data.get('review', '')
        
        if not recipe_name:
            return jsonify({'error': 'Recipe name cannot be empty'}), 400
        
        if not isinstance(rating, int) or rating < 1 or rating > 5:
            return jsonify({'error': 'Rating must be an integer between 1 and 5'}), 400
        
        result = chatbot.rate_recipe(recipe_name, rating, review)
        
        return jsonify({
            'result': result,
            'status': 'success'
        })
    
    except Exception as e:
        return jsonify({
            'error': f'An error occurred: {str(e)}',
            'status': 'error'
        }), 500

@main_bp.route('/api/search', methods=['POST'])
def search_recipes():
    """Search recipes with filters."""
    try:
        data = request.get_json()
        query = data.get('query', '').strip()
        filters = data.get('filters', {})
        
        if not query:
            return jsonify({'error': 'Search query cannot be empty'}), 400
        
        results = chatbot.search_recipes(query, filters)
        
        return jsonify({
            'results': results,
            'total': len(results),
            'status': 'success'
        })
    
    except Exception as e:
        return jsonify({
            'error': f'An error occurred: {str(e)}',
            'status': 'error'
        }), 500

@main_bp.route('/api/share/<recipe_name>', methods=['GET'])
def share_recipe(recipe_name):
    """Get shareable recipe information."""
    try:
        recipe = next((r for r in chatbot.recipes if r['name'].lower() == recipe_name.lower()), None)
        
        if not recipe:
            return jsonify({
                'error': 'Recipe not found',
                'status': 'error'
            }), 404
        
        # Create shareable content
        share_content = {
            'recipe': recipe,
            'share_url': f'{request.host_url}recipe/{recipe_name.lower().replace(" ", "-")}',
            'share_text': f"Check out this amazing {recipe['name']} recipe!",
            'nutrition': chatbot.calculate_nutrition(recipe_name),
            'cost': chatbot.calculate_recipe_cost(recipe_name)
        }
        
        return jsonify({
            'share_content': share_content,
            'status': 'success'
        })
    
    except Exception as e:
        return jsonify({
            'error': f'An error occurred: {str(e)}',
            'status': 'error'
        }), 500

# Authentication Routes

@main_bp.route('/api/auth/register', methods=['POST'])
def register():
    """Register a new user."""
    try:
        data = request.get_json()
        username = data.get('username', '').strip()
        email = data.get('email', '').strip()
        password = data.get('password', '')
        preferences = data.get('preferences', {})
        
        if not username or not email or not password:
            return jsonify({'error': 'Username, email, and password are required'}), 400
        
        result = auth_manager.register_user(username, email, password, preferences)
        
        if 'error' in result:
            return jsonify(result), 400
        
        return jsonify(result), 201
    
    except Exception as e:
        return jsonify({
            'error': f'Registration failed: {str(e)}',
            'status': 'error'
        }), 500

@main_bp.route('/api/auth/login', methods=['POST'])
def login():
    """Authenticate user."""
    try:
        data = request.get_json()
        username = data.get('username', '').strip()
        password = data.get('password', '')
        
        if not username or not password:
            return jsonify({'error': 'Username and password are required'}), 400
        
        result = auth_manager.login_user(username, password)
        
        if 'error' in result:
            return jsonify(result), 401
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({
            'error': f'Login failed: {str(e)}',
            'status': 'error'
        }), 500

@main_bp.route('/api/auth/logout', methods=['POST'])
def logout():
    """Logout user."""
    try:
        session_token = request.headers.get('Authorization', '').replace('Bearer ', '')
        
        if not session_token:
            return jsonify({'error': 'Session token required'}), 400
        
        result = auth_manager.logout_user(session_token)
        
        if 'error' in result:
            return jsonify(result), 400
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({
            'error': f'Logout failed: {str(e)}',
            'status': 'error'
        }), 500

@main_bp.route('/api/auth/profile', methods=['GET', 'PUT'])
def profile():
    """Get or update user profile."""
    try:
        session_token = request.headers.get('Authorization', '').replace('Bearer ', '')
        
        if not session_token:
            return jsonify({'error': 'Session token required'}), 400
        
        user = auth_manager.get_user_by_session(session_token)
        
        if not user:
            return jsonify({'error': 'Invalid or expired session'}), 401
        
        if request.method == 'GET':
            return jsonify({
                'user': user.to_dict(),
                'status': 'success'
            })
        
        elif request.method == 'PUT':
            data = request.get_json()
            result = auth_manager.update_user_profile(user.id, data)
            
            if 'error' in result:
                return jsonify(result), 400
            
            return jsonify(result)
    
    except Exception as e:
        return jsonify({
            'error': f'Profile operation failed: {str(e)}',
            'status': 'error'
        }), 500

@main_bp.route('/api/auth/preferences', methods=['GET'])
def get_preferences():
    """Get user preferences."""
    try:
        session_token = request.headers.get('Authorization', '').replace('Bearer ', '')
        
        if not session_token:
            return jsonify({'error': 'Session token required'}), 400
        
        user = auth_manager.get_user_by_session(session_token)
        
        if not user:
            return jsonify({'error': 'Invalid or expired session'}), 401
        
        preferences = auth_manager.get_user_preferences(user.id)
        
        return jsonify({
            'preferences': preferences,
            'status': 'success'
        })
    
    except Exception as e:
        return jsonify({
            'error': f'Failed to get preferences: {str(e)}',
            'status': 'error'
        }), 500

@main_bp.route('/api/auth/favorites', methods=['POST', 'DELETE'])
def manage_auth_favorites():
    """Add or remove favorite recipes."""
    try:
        session_token = request.headers.get('Authorization', '').replace('Bearer ', '')
        
        if not session_token:
            return jsonify({'error': 'Session token required'}), 400
        
        user = auth_manager.get_user_by_session(session_token)
        
        if not user:
            return jsonify({'error': 'Invalid or expired session'}), 401
        
        data = request.get_json()
        recipe_name = data.get('recipe_name', '').strip()
        
        if not recipe_name:
            return jsonify({'error': 'Recipe name is required'}), 400
        
        if request.method == 'POST':
            result = auth_manager.add_favorite_recipe(user.id, recipe_name)
        else:  # DELETE
            result = auth_manager.remove_favorite_recipe(user.id, recipe_name)
        
        if 'error' in result:
            return jsonify(result), 400
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({
            'error': f'Favorites operation failed: {str(e)}',
            'status': 'error'
        }), 500

@main_bp.route('/api/auth/stats', methods=['GET'])
def get_user_stats():
    """Get user statistics."""
    try:
        session_token = request.headers.get('Authorization', '').replace('Bearer ', '')
        
        if not session_token:
            return jsonify({'error': 'Session token required'}), 400
        
        user = auth_manager.get_user_by_session(session_token)
        
        if not user:
            return jsonify({'error': 'Invalid or expired session'}), 401
        
        stats = auth_manager.get_user_stats(user.id)
        
        return jsonify({
            'stats': stats,
            'status': 'success'
        })
    
    except Exception as e:
        return jsonify({
            'error': f'Failed to get user stats: {str(e)}',
            'status': 'error'
        }), 500

@main_bp.route('/api/personalized-meal-plan', methods=['POST'])
def personalized_meal_plan():
    """Generate personalized meal plan based on user preferences."""
    try:
        session_token = request.headers.get('Authorization', '').replace('Bearer ', '')
        
        user = None
        if session_token:
            user = auth_manager.get_user_by_session(session_token)
        
        data = request.get_json()
        days = data.get('days', 7)
        
        # Get user preferences if authenticated
        preferences = {}
        if user:
            preferences = {
                'dietary': user.dietary_restrictions,
                'cuisine': user.cuisine_preferences,
                'difficulty': user.skill_level,
                'allergies': user.allergies,
                'family_size': user.family_size,
                'budget': user.budget_range
            }
        
        # Override with request data if provided
        preferences.update(data.get('preferences', {}))
        
        meal_plan = chatbot.get_personalized_meal_plan(
            days=days,
            dietary=preferences.get('dietary', ''),
            preferences=preferences
        )
        
        return jsonify({
            'meal_plan': meal_plan,
            'personalized': user is not None,
            'status': 'success'
        })
    
    except Exception as e:
        return jsonify({
            'error': f'Failed to generate meal plan: {str(e)}',
            'status': 'error'
        }), 500

# Image Upload and Recognition Routes

@main_bp.route('/api/upload-image', methods=['POST'])
def upload_image():
    """Handle image upload for recipe recognition."""
    try:
        # Check if file is in request
        if 'image' not in request.files:
            return jsonify({'error': 'No image file provided'}), 400
        
        file = request.files['image']
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Save uploaded file
        success, filepath, result = image_recognition.save_uploaded_file(file)
        
        if not success:
            return jsonify(result), 400
        
        # Analyze image for recipe recognition
        analysis = image_recognition.generate_recipe_from_image(filepath)
        
        return jsonify({
            'file_info': {
                'filename': os.path.basename(filepath),
                'size': os.path.getsize(filepath),
                'path': filepath
            },
            'analysis': analysis,
            'status': 'success'
        })
    
    except Exception as e:
        return jsonify({
            'error': f'Image upload failed: {str(e)}',
            'status': 'error'
        }), 500

@main_bp.route('/api/analyze-image', methods=['POST'])
def analyze_image():
    """Analyze uploaded image for ingredients."""
    try:
        data = request.get_json()
        image_path = data.get('image_path', '')
        
        if not image_path or not os.path.exists(image_path):
            return jsonify({'error': 'Invalid image path'}), 400
        
        # Analyze image
        analysis = image_recognition.analyze_image(image_path)
        
        return jsonify({
            'analysis': analysis,
            'status': 'success'
        })
    
    except Exception as e:
        return jsonify({
            'error': f'Image analysis failed: {str(e)}',
            'status': 'error'
        }), 500

@main_bp.route('/api/recognize-recipe', methods=['POST'])
def recognize_recipe():
    """Recognize recipe from detected ingredients."""
    try:
        data = request.get_json()
        ingredients = data.get('ingredients', [])
        
        if not ingredients:
            return jsonify({'error': 'No ingredients provided'}), 400
        
        # Recognize recipe
        recognition = image_recognition.recognize_recipe(ingredients)
        
        return jsonify({
            'recognition': recognition,
            'status': 'success'
        })
    
    except Exception as e:
        return jsonify({
            'error': f'Recipe recognition failed: {str(e)}',
            'status': 'error'
        }), 500

@main_bp.route('/api/image-to-recipe', methods=['POST'])
def image_to_recipe():
    """Complete image to recipe conversion."""
    try:
        # Get user session for personalization
        session_token = request.headers.get('Authorization', '').replace('Bearer ', '')
        user = None
        if session_token:
            user = auth_manager.get_user_by_session(session_token)
        
        # Handle file upload or base64 image
        if 'image' in request.files:
            file = request.files['image']
            success, filepath, result = image_recognition.save_uploaded_file(file)
            
            if not success:
                return jsonify(result), 400
        
        elif request.is_json:
            data = request.get_json()
            image_data = data.get('image_data', '')  # Base64 encoded image
            
            if image_data:
                # Decode base64 and save
                import base64
                image_bytes = base64.b64decode(image_data.split(',')[1])
                filename = f"upload_{os.urandom(8).hex()}.jpg"
                filepath = os.path.join(image_recognition.upload_folder, filename)
                
                with open(filepath, 'wb') as f:
                    f.write(image_bytes)
            else:
                return jsonify({'error': 'No image data provided'}), 400
        else:
            return jsonify({'error': 'No image provided'}), 400
        
        # Generate complete recipe analysis
        result = image_recognition.generate_recipe_from_image(filepath)
        
        # Get user preferences for personalization
        user_preferences = {}
        if user:
            user_preferences = {
                'dietary_restrictions': user.dietary_restrictions,
                'allergies': user.allergies,
                'skill_level': user.skill_level,
                'cuisine_preferences': user.cuisine_preferences
            }
        
        # Add personalized suggestions
        if result.get('suggestions'):
            for suggestion in result['suggestions']:
                # Filter suggestions based on user preferences
                if user_preferences.get('dietary_restrictions'):
                    # Simple filtering - in real app, would be more sophisticated
                    pass
        
        return jsonify({
            'result': result,
            'user_preferences': user_preferences,
            'personalized': user is not None,
            'status': 'success'
        })
    
    except Exception as e:
        return jsonify({
            'error': f'Image to recipe conversion failed: {str(e)}',
            'status': 'error'
        }), 500

@main_bp.route('/api/recipe-from-ingredients', methods=['POST'])
def recipe_from_ingredients():
    """Generate recipe suggestions from ingredient list."""
    try:
        data = request.get_json()
        ingredients = data.get('ingredients', [])
        preferences = data.get('preferences', {})
        
        if not ingredients:
            return jsonify({'error': 'No ingredients provided'}), 400
        
        # Get matching recipes
        matching_recipes = []
        for recipe in chatbot.recipes:
            match_score = 0
            matched_ingredients = []
            
            for ingredient in ingredients:
                for recipe_ingredient in recipe['ingredients']:
                    if ingredient.lower() in recipe_ingredient.lower():
                        match_score += 1
                        matched_ingredients.append(ingredient)
                        break
            
            if match_score > 0:
                recipe_copy = recipe.copy()
                recipe_copy['match_score'] = match_score
                recipe_copy['matched_ingredients'] = matched_ingredients
                recipe_copy['match_percentage'] = (match_score / len(recipe['ingredients'])) * 100
                matching_recipes.append(recipe_copy)
        
        # Sort by match score
        matching_recipes.sort(key=lambda x: x['match_score'], reverse=True)
        
        # Apply preferences
        if preferences.get('dietary'):
            matching_recipes = [
                r for r in matching_recipes 
                if preferences['dietary'] in r.get('dietary', [])
            ]
        
        return jsonify({
            'matching_recipes': matching_recipes[:10],  # Top 10 matches
            'total_matches': len(matching_recipes),
            'input_ingredients': ingredients,
            'status': 'success'
        })
    
    except Exception as e:
        return jsonify({
            'error': f'Recipe generation failed: {str(e)}',
            'status': 'error'
        }), 500

# Shopping List and Nutrition Routes

@main_bp.route('/api/shopping-list/create', methods=['POST'])
def create_shopping_list():
    """Create shopping list from recipes."""
    try:
        session_token = request.headers.get('Authorization', '').replace('Bearer ', '')
        user = auth_manager.get_user_by_session(session_token)
        
        if not user:
            return jsonify({'error': 'Authentication required'}), 401
        
        data = request.get_json()
        recipes = data.get('recipes', [])
        preferences = data.get('preferences', {})
        
        if not recipes:
            return jsonify({'error': 'No recipes provided'}), 400
        
        # Get user preferences
        user_preferences = {
            'dietary_restrictions': user.dietary_restrictions,
            'allergies': user.allergies,
            'budget_range': user.budget_range,
            'preferred_ingredients': user.cuisine_preferences
        }
        user_preferences.update(preferences)
        
        # Create shopping list
        shopping_list = shopping_manager.create_shopping_list(
            user.id, recipes, user_preferences
        )
        
        return jsonify({
            'shopping_list': shopping_list,
            'status': 'success'
        })
    
    except Exception as e:
        return jsonify({
            'error': f'Failed to create shopping list: {str(e)}',
            'status': 'error'
        }), 500

@main_bp.route('/api/shopping-list', methods=['GET'])
def get_shopping_list():
    """Get user's shopping list."""
    try:
        session_token = request.headers.get('Authorization', '').replace('Bearer ', '')
        user = auth_manager.get_user_by_session(session_token)
        
        if not user:
            return jsonify({'error': 'Authentication required'}), 401
        
        shopping_list = shopping_manager.get_shopping_list(user.id)
        
        if not shopping_list:
            return jsonify({'error': 'No shopping list found'}), 404
        
        return jsonify({
            'shopping_list': shopping_list,
            'status': 'success'
        })
    
    except Exception as e:
        return jsonify({
            'error': f'Failed to get shopping list: {str(e)}',
            'status': 'error'
        }), 500

@main_bp.route('/api/shopping-list/update', methods=['PUT'])
def update_shopping_list():
    """Update shopping list."""
    try:
        session_token = request.headers.get('Authorization', '').replace('Bearer ', '')
        user = auth_manager.get_user_by_session(session_token)
        
        if not user:
            return jsonify({'error': 'Authentication required'}), 401
        
        data = request.get_json()
        updates = data.get('updates', {})
        
        if not updates:
            return jsonify({'error': 'No updates provided'}), 400
        
        shopping_list = shopping_manager.update_shopping_list(user.id, updates)
        
        return jsonify({
            'shopping_list': shopping_list,
            'status': 'success'
        })
    
    except Exception as e:
        return jsonify({
            'error': f'Failed to update shopping list: {str(e)}',
            'status': 'error'
        }), 500

@main_bp.route('/api/shopping-list/compare-prices', methods=['GET'])
def compare_store_prices():
    """Compare prices across stores."""
    try:
        session_token = request.headers.get('Authorization', '').replace('Bearer ', '')
        user = auth_manager.get_user_by_session(session_token)
        
        if not user:
            return jsonify({'error': 'Authentication required'}), 401
        
        comparison = shopping_manager.compare_store_prices(user.id)
        
        return jsonify({
            'price_comparison': comparison,
            'status': 'success'
        })
    
    except Exception as e:
        return jsonify({
            'error': f'Failed to compare prices: {str(e)}',
            'status': 'error'
        }), 500

@main_bp.route('/api/nutrition/goals', methods=['POST', 'GET'])
def manage_nutrition_goals():
    """Set or get nutrition goals."""
    try:
        session_token = request.headers.get('Authorization', '').replace('Bearer ', '')
        user = auth_manager.get_user_by_session(session_token)
        
        if not user:
            return jsonify({'error': 'Authentication required'}), 401
        
        if request.method == 'POST':
            data = request.get_json()
            goals = data.get('goals', {})
            
            if not goals:
                return jsonify({'error': 'No goals provided'}), 400
            
            result = shopping_manager.set_nutrition_goals(user.id, goals)
            
            return jsonify({
                'result': result,
                'status': 'success'
            })
        
        else:  # GET
            # Get current goals (would need to implement this in manager)
            return jsonify({
                'message': 'Nutrition goals retrieval not implemented yet',
                'status': 'pending'
            })
    
    except Exception as e:
        return jsonify({
            'error': f'Nutrition goals operation failed: {str(e)}',
            'status': 'error'
        }), 500

@main_bp.route('/api/nutrition/track', methods=['POST'])
def track_daily_nutrition():
    """Track daily nutrition intake."""
    try:
        session_token = request.headers.get('Authorization', '').replace('Bearer ', '')
        user = auth_manager.get_user_by_session(session_token)
        
        if not user:
            return jsonify({'error': 'Authentication required'}), 401
        
        data = request.get_json()
        meals = data.get('meals', [])
        
        if not meals:
            return jsonify({'error': 'No meals provided'}), 400
        
        tracking = shopping_manager.track_daily_nutrition(user.id, meals)
        
        return jsonify({
            'nutrition_tracking': tracking,
            'status': 'success'
        })
    
    except Exception as e:
        return jsonify({
            'error': f'Nutrition tracking failed: {str(e)}',
            'status': 'error'
        }), 500

@main_bp.route('/api/nutrition/recipe-analysis', methods=['POST'])
def analyze_recipe_nutrition():
    """Analyze nutrition for a recipe."""
    try:
        data = request.get_json()
        recipe_name = data.get('recipe_name', '')
        
        if not recipe_name:
            return jsonify({'error': 'Recipe name required'}), 400
        
        nutrition = chatbot.calculate_nutrition(recipe_name)
        
        if 'error' in nutrition:
            return jsonify(nutrition), 404
        
        return jsonify({
            'nutrition_analysis': nutrition,
            'status': 'success'
        })
    
    except Exception as e:
        return jsonify({
            'error': f'Nutrition analysis failed: {str(e)}',
            'status': 'error'
        }), 500

@main_bp.route('/api/nutrition/meal-plan-analysis', methods=['POST'])
def analyze_meal_plan_nutrition():
    """Analyze nutrition for a meal plan."""
    try:
        data = request.get_json()
        meal_plan = data.get('meal_plan', {})
        
        if not meal_plan:
            return jsonify({'error': 'Meal plan required'}), 400
        
        # Calculate nutrition for entire meal plan
        total_nutrition = {
            'calories': 0,
            'protein': 0,
            'carbs': 0,
            'fat': 0,
            'fiber': 0,
            'sugar': 0,
            'sodium': 0
        }
        
        daily_nutrition = {}
        
        for day, meals in meal_plan.items():
            daily_total = {
                'calories': 0,
                'protein': 0,
                'carbs': 0,
                'fat': 0,
                'fiber': 0,
                'sugar': 0,
                'sodium': 0
            }
            
            for meal_type, meal in meals.items():
                if isinstance(meal, dict):
                    nutrition = chatbot.calculate_nutrition(meal.get('name', ''))
                    if 'error' not in nutrition:
                        per_serving = nutrition.get('per_serving', {})
                        servings = meal.get('servings', 1)
                        
                        for nutrient in daily_total:
                            daily_total[nutrient] += per_serving.get(nutrient, 0) * servings
            
            daily_nutrition[day] = daily_total
            
            # Add to totals
            for nutrient in total_nutrition:
                total_nutrition[nutrient] += daily_total[nutrient]
        
        # Calculate averages
        days_count = len(meal_plan)
        average_daily = {
            nutrient: round(total / days_count, 1) 
            for nutrient, total in total_nutrition.items()
        }
        
        return jsonify({
            'total_nutrition': total_nutrition,
            'daily_nutrition': daily_nutrition,
            'average_daily': average_daily,
            'days_analyzed': days_count,
            'status': 'success'
        })
    
    except Exception as e:
        return jsonify({
            'error': f'Meal plan nutrition analysis failed: {str(e)}',
            'status': 'error'
        }), 500

# Rating and Review System Routes

@main_bp.route('/api/reviews/add', methods=['POST'])
def add_review():
    """Add a new review for a recipe."""
    try:
        session_token = request.headers.get('Authorization', '').replace('Bearer ', '')
        user = auth_manager.get_user_by_session(session_token)
        
        if not user:
            return jsonify({'error': 'Authentication required'}), 401
        
        data = request.get_json()
        recipe_name = data.get('recipe_name', '').strip()
        rating = data.get('rating', 0)
        title = data.get('title', '').strip()
        comment = data.get('comment', '').strip()
        
        if not recipe_name:
            return jsonify({'error': 'Recipe name is required'}), 400
        
        if not (1 <= rating <= 5):
            return jsonify({'error': 'Rating must be between 1 and 5'}), 400
        
        if not title:
            return jsonify({'error': 'Review title is required'}), 400
        
        # Optional fields
        pros = data.get('pros', [])
        cons = data.get('cons', [])
        would_make_again = data.get('would_make_again', True)
        difficulty_rating = data.get('difficulty_rating', 3)
        value_rating = data.get('value_rating', 3)
        taste_rating = data.get('taste_rating', 3)
        verified_purchase = data.get('verified_purchase', False)
        
        result = rating_manager.add_review(
            recipe_name=recipe_name,
            user_id=user.id,
            username=user.username,
            rating=rating,
            title=title,
            comment=comment,
            pros=pros,
            cons=cons,
            would_make_again=would_make_again,
            difficulty_rating=difficulty_rating,
            value_rating=value_rating,
            taste_rating=taste_rating,
            verified_purchase=verified_purchase
        )
        
        if 'error' in result:
            return jsonify(result), 400
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({
            'error': f'Failed to add review: {str(e)}',
            'status': 'error'
        }), 500

@main_bp.route('/api/reviews/update', methods=['PUT'])
def update_review():
    """Update an existing review."""
    try:
        session_token = request.headers.get('Authorization', '').replace('Bearer ', '')
        user = auth_manager.get_user_by_session(session_token)
        
        if not user:
            return jsonify({'error': 'Authentication required'}), 401
        
        data = request.get_json()
        review_id = data.get('review_id', '').strip()
        updates = data.get('updates', {})
        
        if not review_id:
            return jsonify({'error': 'Review ID is required'}), 400
        
        if not updates:
            return jsonify({'error': 'No updates provided'}), 400
        
        result = rating_manager.update_review(review_id, user.id, updates)
        
        if 'error' in result:
            return jsonify(result), 400
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({
            'error': f'Failed to update review: {str(e)}',
            'status': 'error'
        }), 500

@main_bp.route('/api/reviews/delete', methods=['DELETE'])
def delete_review():
    """Delete a review."""
    try:
        session_token = request.headers.get('Authorization', '').replace('Bearer ', '')
        user = auth_manager.get_user_by_session(session_token)
        
        if not user:
            return jsonify({'error': 'Authentication required'}), 401
        
        data = request.get_json()
        review_id = data.get('review_id', '').strip()
        
        if not review_id:
            return jsonify({'error': 'Review ID is required'}), 400
        
        result = rating_manager.delete_review(review_id, user.id)
        
        if 'error' in result:
            return jsonify(result), 400
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({
            'error': f'Failed to delete review: {str(e)}',
            'status': 'error'
        }), 500

@main_bp.route('/api/reviews/recipe/<recipe_name>', methods=['GET'])
def get_recipe_reviews(recipe_name: str):
    """Get reviews for a specific recipe."""
    try:
        sort_by = request.args.get('sort_by', 'newest')
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 10))
        
        result = rating_manager.get_recipe_reviews(
            recipe_name=recipe_name,
            sort_by=sort_by,
            page=page,
            per_page=per_page
        )
        
        return jsonify({
            'reviews': result,
            'status': 'success'
        })
    
    except Exception as e:
        return jsonify({
            'error': f'Failed to get reviews: {str(e)}',
            'status': 'error'
        }), 500

@main_bp.route('/api/reviews/user', methods=['GET'])
def get_user_reviews():
    """Get reviews by the current user."""
    try:
        session_token = request.headers.get('Authorization', '').replace('Bearer ', '')
        user = auth_manager.get_user_by_session(session_token)
        
        if not user:
            return jsonify({'error': 'Authentication required'}), 401
        
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 10))
        
        result = rating_manager.get_user_reviews(
            user_id=user.id,
            page=page,
            per_page=per_page
        )
        
        return jsonify({
            'reviews': result,
            'status': 'success'
        })
    
    except Exception as e:
        return jsonify({
            'error': f'Failed to get user reviews: {str(e)}',
            'status': 'error'
        }), 500

@main_bp.route('/api/reviews/helpful', methods=['POST'])
def mark_review_helpful():
    """Mark a review as helpful."""
    try:
        session_token = request.headers.get('Authorization', '').replace('Bearer ', '')
        user = auth_manager.get_user_by_session(session_token)
        
        if not user:
            return jsonify({'error': 'Authentication required'}), 401
        
        data = request.get_json()
        review_id = data.get('review_id', '').strip()
        
        if not review_id:
            return jsonify({'error': 'Review ID is required'}), 400
        
        result = rating_manager.mark_review_helpful(review_id, user.id)
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({
            'error': f'Failed to mark review helpful: {str(e)}',
            'status': 'error'
        }), 500

@main_bp.route('/api/reviews/stats/<recipe_name>', methods=['GET'])
def get_recipe_stats(recipe_name: str):
    """Get statistics for a recipe."""
    try:
        stats = rating_manager.get_recipe_stats(recipe_name)
        
        if not stats:
            return jsonify({'error': 'Recipe statistics not found'}), 404
        
        return jsonify({
            'stats': stats.to_dict(),
            'status': 'success'
        })
    
    except Exception as e:
        return jsonify({
            'error': f'Failed to get recipe stats: {str(e)}',
            'status': 'error'
        }), 500

@main_bp.route('/api/reviews/top-recipes', methods=['GET'])
def get_top_recipes():
    """Get top rated recipes."""
    try:
        limit = int(request.args.get('limit', 10))
        min_reviews = int(request.args.get('min_reviews', 5))
        
        top_recipes = rating_manager.get_top_recipes(
            limit=limit,
            min_reviews=min_reviews
        )
        
        return jsonify({
            'top_recipes': top_recipes,
            'status': 'success'
        })
    
    except Exception as e:
        return jsonify({
            'error': f'Failed to get top recipes: {str(e)}',
            'status': 'error'
        }), 500

@main_bp.route('/api/reviews/search', methods=['POST'])
def search_reviews():
    """Search reviews."""
    try:
        data = request.get_json()
        query = data.get('query', '').strip()
        recipe_name = data.get('recipe_name', '')
        rating_filter = data.get('rating_filter')
        page = int(data.get('page', 1))
        per_page = int(data.get('per_page', 10))
        
        if not query:
            return jsonify({'error': 'Search query is required'}), 400
        
        result = rating_manager.search_reviews(
            query=query,
            recipe_name=recipe_name,
            rating_filter=rating_filter,
            page=page,
            per_page=per_page
        )
        
        return jsonify({
            'search_results': result,
            'status': 'success'
        })
    
    except Exception as e:
        return jsonify({
            'error': f'Failed to search reviews: {str(e)}',
            'status': 'error'
        }), 500

@main_bp.route('/api/reviews/user-summary', methods=['GET'])
def get_user_rating_summary():
    """Get user's rating summary."""
    try:
        session_token = request.headers.get('Authorization', '').replace('Bearer ', '')
        user = auth_manager.get_user_by_session(session_token)
        
        if not user:
            return jsonify({'error': 'Authentication required'}), 401
        
        summary = rating_manager.get_user_rating_summary(user.id)
        
        return jsonify({
            'summary': summary,
            'status': 'success'
        })
    
    except Exception as e:
        return jsonify({
            'error': f'Failed to get user rating summary: {str(e)}',
            'status': 'error'
        }), 500

# Social Sharing and Community Features

@main_bp.route('/api/share/recipe', methods=['POST'])
def share_recipe():
    """Share a recipe to social platforms."""
    try:
        data = request.get_json()
        recipe_name = data.get('recipe_name', '').strip()
        platform = data.get('platform', '').strip()
        custom_message = data.get('message', '')
        
        if not recipe_name:
            return jsonify({'error': 'Recipe name is required'}), 400
        
        if not platform:
            return jsonify({'error': 'Platform is required'}), 400
        
        # Get recipe details
        recipe = next((r for r in chatbot.recipes if r['name'] == recipe_name), None)
        
        if not recipe:
            return jsonify({'error': 'Recipe not found'}), 404
        
        # Generate shareable content
        share_content = {
            'title': f"Check out this amazing {recipe_name} recipe!",
            'description': f"Delicious {recipe_name} - {recipe.get('prep_time', 'Quick')} to make!",
            'url': f"https://yourapp.com/recipe/{recipe_name.lower().replace(' ', '-')}",
            'image': f"https://yourapp.com/images/recipes/{recipe_name.lower().replace(' ', '-')}.jpg",
            'hashtags': ['#RecipeAssistant', '#Cooking', '#Foodie', recipe_name.replace(' ', '')],
            'platform': platform
        }
        
        # Platform-specific formatting
        if platform == 'twitter':
            share_content['text'] = f"{share_content['title']} {share_content['url']} {' '.join(share_content['hashtags'][:3])}"
        elif platform == 'facebook':
            share_content['text'] = f"{share_content['title']}\n\n{share_content['description']}\n\n{share_content['url']}"
        elif platform == 'instagram':
            share_content['text'] = f"{share_content['title']}\n\n{share_content['description']}\n\n{' '.join(share_content['hashtags'][:5])}"
        elif platform == 'pinterest':
            share_content['text'] = f"{share_content['title']}\n\n{share_content['description']}"
        
        # Add custom message if provided
        if custom_message:
            share_content['text'] = f"{custom_message}\n\n{share_content['text']}"
        
        return jsonify({
            'share_content': share_content,
            'message': 'Recipe shared successfully',
            'status': 'success'
        })
    
    except Exception as e:
        return jsonify({
            'error': f'Failed to share recipe: {str(e)}',
            'status': 'error'
        }), 500

@main_bp.route('/api/community/trending-recipes', methods=['GET'])
def get_trending_recipes():
    """Get trending recipes in the community."""
    try:
        # Mock trending data - in real app, would analyze actual usage patterns
        trending_recipes = [
            {
                'recipe_name': 'Spaghetti Carbonara',
                'trend_score': 95,
                'recent_reviews': 12,
                'average_rating': 4.7,
                'category': 'Italian'
            },
            {
                'recipe_name': 'Chicken Stir Fry',
                'trend_score': 88,
                'recent_reviews': 8,
                'average_rating': 4.5,
                'category': 'Asian'
            },
            {
                'recipe_name': 'Greek Salad',
                'trend_score': 82,
                'recent_reviews': 6,
                'average_rating': 4.6,
                'category': 'Mediterranean'
            }
        ]
        
        return jsonify({
            'trending_recipes': trending_recipes,
            'updated_date': datetime.datetime.now().isoformat(),
            'status': 'success'
        })
    
    except Exception as e:
        return jsonify({
            'error': f'Failed to get trending recipes: {str(e)}',
            'status': 'error'
        }), 500

@main_bp.route('/api/community/recent-activity', methods=['GET'])
def get_recent_activity():
    """Get recent community activity."""
    try:
        # Mock activity data - in real app, would fetch from database
        recent_activity = [
            {
                'type': 'review',
                'user': 'John Doe',
                'action': 'reviewed',
                'target': 'Spaghetti Carbonara',
                'rating': 5,
                'timestamp': datetime.datetime.now().isoformat()
            },
            {
                'type': 'favorite',
                'user': 'Jane Smith',
                'action': 'favorited',
                'target': 'Greek Salad',
                'timestamp': (datetime.datetime.now() - datetime.timedelta(hours=2)).isoformat()
            },
            {
                'type': 'share',
                'user': 'Mike Johnson',
                'action': 'shared',
                'target': 'Chicken Stir Fry',
                'platform': 'Facebook',
                'timestamp': (datetime.datetime.now() - datetime.timedelta(hours=4)).isoformat()
            }
        ]
        
        return jsonify({
            'recent_activity': recent_activity,
            'status': 'success'
        })
    
    except Exception as e:
        return jsonify({
            'error': f'Failed to get recent activity: {str(e)}',
            'status': 'error'
        }), 500

# Voice Assistant Routes

@main_bp.route('/api/voice/start', methods=['POST'])
def start_voice_assistant():
    """Start voice assistant listening."""
    try:
        session_token = request.headers.get('Authorization', '').replace('Bearer ', '')
        user = auth_manager.get_user_by_session(session_token)
        
        if not user:
            return jsonify({'error': 'Authentication required'}), 401
        
        # Start listening (mock implementation)
        return jsonify({
            'status': 'listening',
            'message': 'Voice assistant started',
            'available_commands': list(voice_assistant.command_patterns.keys())
        })
    
    except Exception as e:
        return jsonify({
            'error': f'Failed to start voice assistant: {str(e)}',
            'status': 'error'
        }), 500

@main_bp.route('/api/voice/stop', methods=['POST'])
def stop_voice_assistant():
    """Stop voice assistant listening."""
    try:
        voice_assistant.stop_listening()
        
        return jsonify({
            'status': 'stopped',
            'message': 'Voice assistant stopped'
        })
    
    except Exception as e:
        return jsonify({
            'error': f'Failed to stop voice assistant: {str(e)}',
            'status': 'error'
        }), 500

@main_bp.route('/api/voice/speak', methods=['POST'])
def speak_text():
    """Convert text to speech."""
    try:
        data = request.get_json()
        text = data.get('text', '').strip()
        
        if not text:
            return jsonify({'error': 'Text is required'}), 400
        
        voice_assistant.speak(text)
        
        return jsonify({
            'message': 'Text spoken successfully',
            'text': text
        })
    
    except Exception as e:
        return jsonify({
            'error': f'Failed to speak text: {str(e)}',
            'status': 'error'
        }), 500

@main_bp.route('/api/voice/commands', methods=['GET'])
def get_voice_commands():
    """Get available voice commands."""
    try:
        return jsonify({
            'commands': voice_assistant.command_patterns,
            'status': 'success'
        })
    
    except Exception as e:
        return jsonify({
            'error': f'Failed to get voice commands: {str(e)}',
            'status': 'error'
        }), 500

@main_bp.route('/api/voice/settings', methods=['POST'])
def update_voice_settings():
    """Update voice assistant settings."""
    try:
        data = request.get_json()
        rate = data.get('rate')
        volume = data.get('volume')
        voice = data.get('voice')
        
        voice_assistant.set_voice_settings(rate, volume, voice)
        
        return jsonify({
            'message': 'Voice settings updated',
            'settings': {
                'rate': rate,
                'volume': volume,
                'voice': voice
            }
        })
    
    except Exception as e:
        return jsonify({
            'error': f'Failed to update voice settings: {str(e)}',
            'status': 'error'
        }), 500

# Smart Kitchen Routes

@main_bp.route('/api/smart-kitchen/devices', methods=['GET'])
def get_smart_devices():
    """Get all smart kitchen devices."""
    try:
        session_token = request.headers.get('Authorization', '').replace('Bearer ', '')
        user = auth_manager.get_user_by_session(session_token)
        
        if not user:
            return jsonify({'error': 'Authentication required'}), 401
        
        devices = smart_kitchen.discover_devices()
        
        return jsonify({
            'devices': [device.to_dict() for device in devices],
            'status': 'success'
        })
    
    except Exception as e:
        return jsonify({
            'error': f'Failed to get devices: {str(e)}',
            'status': 'error'
        }), 500

@main_bp.route('/api/smart-kitchen/devices', methods=['POST'])
def add_smart_device():
    """Add a new smart device."""
    try:
        session_token = request.headers.get('Authorization', '').replace('Bearer ', '')
        user = auth_manager.get_user_by_session(session_token)
        
        if not user:
            return jsonify({'error': 'Authentication required'}), 401
        
        data = request.get_json()
        
        # Create device object (simplified)
        from .smart_kitchen import SmartDevice, DeviceType
        
        device = SmartDevice(
            id=data.get('id'),
            name=data.get('name'),
            type=DeviceType(data.get('type')),
            brand=data.get('brand'),
            model=data.get('model'),
            ip_address=data.get('ip_address'),
            status='offline',
            capabilities=data.get('capabilities', []),
            current_settings={},
            last_seen=datetime.datetime.now().isoformat()
        )
        
        result = smart_kitchen.add_device(device)
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({
            'error': f'Failed to add device: {str(e)}',
            'status': 'error'
        }), 500

@main_bp.route('/api/smart-kitchen/devices/<device_id>/control', methods=['POST'])
def control_smart_device(device_id: str):
    """Control a smart device."""
    try:
        session_token = request.headers.get('Authorization', '').replace('Bearer ', '')
        user = auth_manager.get_user_by_session(session_token)
        
        if not user:
            return jsonify({'error': 'Authentication required'}), 401
        
        data = request.get_json()
        command = data.get('command')
        parameters = data.get('parameters', {})
        
        result = smart_kitchen.control_device(device_id, command, parameters)
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({
            'error': f'Failed to control device: {str(e)}',
            'status': 'error'
        }), 500

@main_bp.route('/api/smart-kitchen/devices/<device_id>/status', methods=['GET'])
def get_device_status(device_id: str):
    """Get device status."""
    try:
        session_token = request.headers.get('Authorization', '').replace('Bearer ', '')
        user = auth_manager.get_user_by_session(session_token)
        
        if not user:
            return jsonify({'error': 'Authentication required'}), 401
        
        status = smart_kitchen.get_device_status(device_id)
        
        if not status:
            return jsonify({'error': 'Device not found'}), 404
        
        return jsonify({
            'device_status': status,
            'status': 'success'
        })
    
    except Exception as e:
        return jsonify({
            'error': f'Failed to get device status: {str(e)}',
            'status': 'error'
        }), 500

@main_bp.route('/api/smart-kitchen/cooking-sessions', methods=['POST'])
def start_cooking_session():
    """Start cooking session on smart device."""
    try:
        session_token = request.headers.get('Authorization', '').replace('Bearer ', '')
        user = auth_manager.get_user_by_session(session_token)
        
        if not user:
            return jsonify({'error': 'Authentication required'}), 401
        
        data = request.get_json()
        device_id = data.get('device_id')
        recipe_name = data.get('recipe_name')
        target_temperature = data.get('target_temperature', 350)
        estimated_time = data.get('estimated_time', 30)
        
        result = smart_kitchen.start_cooking_session(
            device_id, recipe_name, target_temperature, estimated_time
        )
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({
            'error': f'Failed to start cooking session: {str(e)}',
            'status': 'error'
        }), 500

@main_bp.route('/api/smart-kitchen/cooking-sessions', methods=['GET'])
def get_active_sessions():
    """Get active cooking sessions."""
    try:
        session_token = request.headers.get('Authorization', '').replace('Bearer ', '')
        user = auth_manager.get_user_by_session(session_token)
        
        if not user:
            return jsonify({'error': 'Authentication required'}), 401
        
        sessions = smart_kitchen.get_active_sessions()
        
        return jsonify({
            'active_sessions': [session.to_dict() for session in sessions],
            'status': 'success'
        })
    
    except Exception as e:
        return jsonify({
            'error': f'Failed to get active sessions: {str(e)}',
            'status': 'error'
        }), 500

# AI Cooking Assistant Routes

@main_bp.route('/api/cooking-assistant/start', methods=['POST'])
def start_ai_cooking_session():
    """Start AI cooking assistant session."""
    try:
        session_token = request.headers.get('Authorization', '').replace('Bearer ', '')
        user = auth_manager.get_user_by_session(session_token)
        
        if not user:
            return jsonify({'error': 'Authentication required'}), 401
        
        data = request.get_json()
        recipe_name = data.get('recipe_name')
        skill_level = data.get('skill_level', 'beginner')
        dietary_preferences = data.get('dietary_preferences', [])
        
        from .cooking_assistant import DifficultyLevel
        difficulty = DifficultyLevel(skill_level)
        
        result = cooking_assistant.start_cooking_session(
            recipe_name, user.id, difficulty, dietary_preferences
        )
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({
            'error': f'Failed to start cooking session: {str(e)}',
            'status': 'error'
        }), 500

@main_bp.route('/api/cooking-assistant/<session_id>/current-step', methods=['GET'])
def get_current_cooking_step(session_id: str):
    """Get current cooking step."""
    try:
        session_token = request.headers.get('Authorization', '').replace('Bearer ', '')
        user = auth_manager.get_user_by_session(session_token)
        
        if not user:
            return jsonify({'error': 'Authentication required'}), 401
        
        current_step = cooking_assistant.get_current_step(session_id)
        
        if not current_step:
            return jsonify({'error': 'No current step found'}), 404
        
        return jsonify({
            'current_step': current_step.to_dict(),
            'status': 'success'
        })
    
    except Exception as e:
        return jsonify({
            'error': f'Failed to get current step: {str(e)}',
            'status': 'error'
        }), 500

@main_bp.route('/api/cooking-assistant/<session_id>/next-step', methods=['POST'])
def advance_to_next_step(session_id: str):
    """Advance to next cooking step."""
    try:
        session_token = request.headers.get('Authorization', '').replace('Bearer ', '')
        user = auth_manager.get_user_by_session(session_token)
        
        if not user:
            return jsonify({'error': 'Authentication required'}), 401
        
        data = request.get_json()
        notes = data.get('notes', '')
        
        result = cooking_assistant.advance_to_next_step(session_id, notes)
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({
            'error': f'Failed to advance step: {str(e)}',
            'status': 'error'
        }), 500

@main_bp.route('/api/cooking-assistant/<session_id>/guidance', methods=['GET'])
def get_step_guidance(session_id: str):
    """Get detailed guidance for current step."""
    try:
        session_token = request.headers.get('Authorization', '').replace('Bearer ', '')
        user = auth_manager.get_user_by_session(session_token)
        
        if not user:
            return jsonify({'error': 'Authentication required'}), 401
        
        guidance_type = request.args.get('type', 'detailed')
        
        guidance = cooking_assistant.get_step_guidance(session_id, guidance_type)
        
        return jsonify({
            'guidance': guidance,
            'status': 'success'
        })
    
    except Exception as e:
        return jsonify({
            'error': f'Failed to get step guidance: {str(e)}',
            'status': 'error'
        }), 500

@main_bp.route('/api/cooking-assistant/<session_id>/pause', methods=['POST'])
def pause_cooking_session(session_id: str):
    """Pause cooking session."""
    try:
        session_token = request.headers.get('Authorization', '').replace('Bearer ', '')
        user = auth_manager.get_user_by_session(session_token)
        
        if not user:
            return jsonify({'error': 'Authentication required'}), 401
        
        data = request.get_json()
        reason = data.get('reason', '')
        
        result = cooking_assistant.pause_session(session_id, reason)
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({
            'error': f'Failed to pause session: {str(e)}',
            'status': 'error'
        }), 500

@main_bp.route('/api/cooking-assistant/<session_id>/resume', methods=['POST'])
def resume_cooking_session(session_id: str):
    """Resume cooking session."""
    try:
        session_token = request.headers.get('Authorization', '').replace('Bearer ', '')
        user = auth_manager.get_user_by_session(session_token)
        
        if not user:
            return jsonify({'error': 'Authentication required'}), 401
        
        result = cooking_assistant.resume_session(session_id)
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({
            'error': f'Failed to resume session: {str(e)}',
            'status': 'error'
        }), 500

@main_bp.route('/api/cooking-assistant/<session_id>/summary', methods=['GET'])
def get_cooking_session_summary(session_id: str):
    """Get cooking session summary."""
    try:
        session_token = request.headers.get('Authorization', '').replace('Bearer ', '')
        user = auth_manager.get_user_by_session(session_token)
        
        if not user:
            return jsonify({'error': 'Authentication required'}), 401
        
        summary = cooking_assistant.get_session_summary(session_id)
        
        return jsonify({
            'session_summary': summary,
            'status': 'success'
        })
    
    except Exception as e:
        return jsonify({
            'error': f'Failed to get session summary: {str(e)}',
            'status': 'error'
        }), 500

# Advanced Features Routes - Recipe Scaling and Variations

@main_bp.route('/api/recipe/scale', methods=['POST'])
def scale_recipe():
    """Scale recipe to different serving size."""
    try:
        data = request.get_json()
        recipe_name = data.get('recipe_name', '').strip()
        servings = data.get('servings', 4)
        
        if not recipe_name:
            return jsonify({'error': 'Recipe name is required'}), 400
        
        if servings < 1:
            return jsonify({'error': 'Servings must be at least 1'}), 400
        
        result = chatbot.scale_recipe(recipe_name, servings)
        
        if 'error' in result:
            return jsonify(result), 404
        
        return jsonify({
            'result': result,
            'status': 'success'
        })
    
    except Exception as e:
        return jsonify({
            'error': f'Failed to scale recipe: {str(e)}',
            'status': 'error'
        }), 500

@main_bp.route('/api/recipe/variations', methods=['POST'])
def get_recipe_variations():
    """Get recipe variations."""
    try:
        data = request.get_json()
        recipe_name = data.get('recipe_name', '').strip()
        variation_type = data.get('variation_type', 'all')
        
        if not recipe_name:
            return jsonify({'error': 'Recipe name is required'}), 400
        
        result = chatbot.generate_recipe_variations(recipe_name, variation_type)
        
        if 'error' in result:
            return jsonify(result), 404
        
        return jsonify({
            'result': result,
            'status': 'success'
        })
    
    except Exception as e:
        return jsonify({
            'error': f'Failed to generate variations: {str(e)}',
            'status': 'error'
        }), 500

@main_bp.route('/api/recipe/leftover-suggestions', methods=['POST'])
def get_leftover_suggestions():
    """Get recipe suggestions based on leftover ingredients."""
    try:
        data = request.get_json()
        ingredients = data.get('ingredients', [])
        
        if not ingredients:
            return jsonify({'error': 'Ingredients list is required'}), 400
        
        result = chatbot.suggest_leftover_recipes(ingredients)
        
        return jsonify({
            'result': result,
            'status': 'success'
        })
    
    except Exception as e:
        return jsonify({
            'error': f'Failed to get leftover suggestions: {str(e)}',
            'status': 'error'
        }), 500

# Advanced Features Routes - Ingredient Inventory

@main_bp.route('/api/inventory', methods=['GET'])
def get_inventory():
    """Get user's ingredient inventory."""
    try:
        session_token = request.headers.get('Authorization', '').replace('Bearer ', '')
        user = auth_manager.get_user_by_session(session_token)
        
        if not user:
            return jsonify({'error': 'Authentication required'}), 401
        
        result = advanced_features.get_inventory(user.id)
        
        return jsonify({
            'inventory': result,
            'status': 'success'
        })
    
    except Exception as e:
        return jsonify({
            'error': f'Failed to get inventory: {str(e)}',
            'status': 'error'
        }), 500

@main_bp.route('/api/inventory/add', methods=['POST'])
def add_to_inventory():
    """Add item to inventory."""
    try:
        session_token = request.headers.get('Authorization', '').replace('Bearer ', '')
        user = auth_manager.get_user_by_session(session_token)
        
        if not user:
            return jsonify({'error': 'Authentication required'}), 401
        
        data = request.get_json()
        ingredient = IngredientInventory(
            name=data.get('name', '').strip(),
            quantity=float(data.get('quantity', 1)),
            unit=data.get('unit', 'item'),
            expiry_date=data.get('expiry_date'),
            location=data.get('location', 'pantry'),
            category=data.get('category', 'other'),
            added_date=datetime.datetime.now().isoformat(),
            notes=data.get('notes', '')
        )
        
        if not ingredient.name:
            return jsonify({'error': 'Item name is required'}), 400
        
        result = advanced_features.add_to_inventory(user.id, ingredient)
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({
            'error': f'Failed to add to inventory: {str(e)}',
            'status': 'error'
        }), 500

@main_bp.route('/api/inventory/update', methods=['PUT'])
def update_inventory_item():
    """Update inventory item."""
    try:
        session_token = request.headers.get('Authorization', '').replace('Bearer ', '')
        user = auth_manager.get_user_by_session(session_token)
        
        if not user:
            return jsonify({'error': 'Authentication required'}), 401
        
        data = request.get_json()
        item_name = data.get('item_name', '').strip()
        updates = data.get('updates', {})
        
        if not item_name:
            return jsonify({'error': 'Item name is required'}), 400
        
        result = advanced_features.update_inventory_item(user.id, item_name, updates)
        
        if 'error' in result:
            return jsonify(result), 400
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({
            'error': f'Failed to update inventory: {str(e)}',
            'status': 'error'
        }), 500

@main_bp.route('/api/inventory/remove', methods=['DELETE'])
def remove_from_inventory():
    """Remove item from inventory."""
    try:
        session_token = request.headers.get('Authorization', '').replace('Bearer ', '')
        user = auth_manager.get_user_by_session(session_token)
        
        if not user:
            return jsonify({'error': 'Authentication required'}), 401
        
        data = request.get_json()
        item_name = data.get('item_name', '').strip()
        
        if not item_name:
            return jsonify({'error': 'Item name is required'}), 400
        
        result = advanced_features.remove_from_inventory(user.id, item_name)
        
        if 'error' in result:
            return jsonify(result), 400
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({
            'error': f'Failed to remove from inventory: {str(e)}',
            'status': 'error'
        }), 500

@main_bp.route('/api/inventory/recipes', methods=['GET'])
def get_recipes_from_inventory():
    """Get recipe suggestions from inventory."""
    try:
        session_token = request.headers.get('Authorization', '').replace('Bearer ', '')
        user = auth_manager.get_user_by_session(session_token)
        
        if not user:
            return jsonify({'error': 'Authentication required'}), 401
        
        inventory_info = advanced_features.get_recipes_from_inventory(user.id)
        ingredients = inventory_info.get('available_ingredients', [])
        
        if not ingredients:
            return jsonify({
                'message': 'No ingredients in inventory',
                'suggestions': []
            })
        
        result = chatbot.suggest_leftover_recipes(ingredients)
        
        return jsonify({
            'result': result,
            'status': 'success'
        })
    
    except Exception as e:
        return jsonify({
            'error': f'Failed to get recipes: {str(e)}',
            'status': 'error'
        }), 500

# Advanced Features Routes - Recipe Collections

@main_bp.route('/api/collections', methods=['GET', 'POST'])
def manage_collections():
    """Get or create recipe collections."""
    try:
        session_token = request.headers.get('Authorization', '').replace('Bearer ', '')
        user = auth_manager.get_user_by_session(session_token)
        
        if not user:
            return jsonify({'error': 'Authentication required'}), 401
        
        if request.method == 'GET':
            result = advanced_features.get_collections(user.id)
            return jsonify(result)
        
        elif request.method == 'POST':
            data = request.get_json()
            name = data.get('name', '').strip()
            description = data.get('description', '')
            tags = data.get('tags', [])
            is_public = data.get('is_public', False)
            
            if not name:
                return jsonify({'error': 'Collection name is required'}), 400
            
            result = advanced_features.create_collection(
                user.id, name, description, tags, is_public
            )
            
            return jsonify(result)
    
    except Exception as e:
        return jsonify({
            'error': f'Collection operation failed: {str(e)}',
            'status': 'error'
        }), 500

@main_bp.route('/api/collections/<collection_id>/recipes', methods=['POST'])
def add_recipe_to_collection(collection_id: str):
    """Add recipe to collection."""
    try:
        session_token = request.headers.get('Authorization', '').replace('Bearer ', '')
        user = auth_manager.get_user_by_session(session_token)
        
        if not user:
            return jsonify({'error': 'Authentication required'}), 401
        
        data = request.get_json()
        recipe_name = data.get('recipe_name', '').strip()
        
        if not recipe_name:
            return jsonify({'error': 'Recipe name is required'}), 400
        
        result = advanced_features.add_recipe_to_collection(
            user.id, collection_id, recipe_name
        )
        
        if 'error' in result:
            return jsonify(result), 400
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({
            'error': f'Failed to add recipe: {str(e)}',
            'status': 'error'
        }), 500

# Advanced Features Routes - Cooking Challenges

@main_bp.route('/api/challenges', methods=['GET', 'POST'])
def manage_challenges():
    """Get or create cooking challenges."""
    try:
        session_token = request.headers.get('Authorization', '').replace('Bearer ', '')
        user = auth_manager.get_user_by_session(session_token)
        
        if not user:
            return jsonify({'error': 'Authentication required'}), 401
        
        if request.method == 'GET':
            result = advanced_features.get_active_challenges(user.id)
            return jsonify(result)
        
        elif request.method == 'POST':
            data = request.get_json()
            challenge_type_str = data.get('challenge_type', 'weekly_recipe')
            title = data.get('title', '').strip()
            description = data.get('description', '')
            target_recipes = data.get('target_recipes', [])
            duration_days = data.get('duration_days', 7)
            difficulty = data.get('difficulty', 'medium')
            
            if not title:
                return jsonify({'error': 'Challenge title is required'}), 400
            
            try:
                challenge_type = ChallengeType(challenge_type_str)
            except ValueError:
                return jsonify({'error': 'Invalid challenge type'}), 400
            
            result = advanced_features.create_challenge(
                user.id, challenge_type, title, description,
                target_recipes, duration_days, difficulty
            )
            
            return jsonify(result)
    
    except Exception as e:
        return jsonify({
            'error': f'Challenge operation failed: {str(e)}',
            'status': 'error'
        }), 500

@main_bp.route('/api/challenges/<challenge_id>/complete', methods=['POST'])
def complete_challenge_recipe(challenge_id: str):
    """Complete a recipe in a challenge."""
    try:
        session_token = request.headers.get('Authorization', '').replace('Bearer ', '')
        user = auth_manager.get_user_by_session(session_token)
        
        if not user:
            return jsonify({'error': 'Authentication required'}), 401
        
        data = request.get_json()
        recipe_name = data.get('recipe_name', '').strip()
        
        if not recipe_name:
            return jsonify({'error': 'Recipe name is required'}), 400
        
        result = advanced_features.complete_challenge_recipe(
            user.id, challenge_id, recipe_name
        )
        
        if 'error' in result:
            return jsonify(result), 400
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({
            'error': f'Failed to complete recipe: {str(e)}',
            'status': 'error'
        }), 500

# Advanced Features Routes - Meal Prep Planning

@main_bp.route('/api/meal-prep/create', methods=['POST'])
def create_meal_prep_plan():
    """Create a meal prep plan."""
    try:
        session_token = request.headers.get('Authorization', '').replace('Bearer ', '')
        user = auth_manager.get_user_by_session(session_token)
        
        if not user:
            return jsonify({'error': 'Authentication required'}), 401
        
        data = request.get_json()
        recipes = data.get('recipes', [])
        week_start = data.get('week_start', datetime.datetime.now().isoformat())
        
        if not recipes:
            return jsonify({'error': 'Recipes are required'}), 400
        
        result = advanced_features.create_meal_prep_plan(
            user.id, recipes, week_start
        )
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({
            'error': f'Failed to create meal prep plan: {str(e)}',
            'status': 'error'
        }), 500

# Advanced Features Routes - Cooking Stats

@main_bp.route('/api/stats/cooking', methods=['GET'])
def get_cooking_stats():
    """Get user's cooking statistics."""
    try:
        session_token = request.headers.get('Authorization', '').replace('Bearer ', '')
        user = auth_manager.get_user_by_session(session_token)
        
        if not user:
            return jsonify({'error': 'Authentication required'}), 401
        
        result = advanced_features.get_cooking_stats(user.id)
        
        return jsonify({
            'stats': result,
            'status': 'success'
        })
    
    except Exception as e:
        return jsonify({
            'error': f'Failed to get stats: {str(e)}',
            'status': 'error'
        }), 500

@main_bp.route('/api/stats/track-recipe', methods=['POST'])
def track_recipe_cooked():
    """Track that user cooked a recipe."""
    try:
        session_token = request.headers.get('Authorization', '').replace('Bearer ', '')
        user = auth_manager.get_user_by_session(session_token)
        
        if not user:
            return jsonify({'error': 'Authentication required'}), 401
        
        data = request.get_json()
        recipe_name = data.get('recipe_name', '').strip()
        
        if not recipe_name:
            return jsonify({'error': 'Recipe name is required'}), 400
        
        result = advanced_features.track_recipe_cooked(user.id, recipe_name)
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({
            'error': f'Failed to track recipe: {str(e)}',
            'status': 'error'
        }), 500
