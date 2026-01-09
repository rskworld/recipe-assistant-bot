"""
Recipe Assistant Bot - Image Recognition
Author: RSK World (https://rskworld.in)
Founder: Molla Samser
Designer & Tester: Rima Khatun
Contact: help@rskworld.in, +91 93305 39277
Year: 2026
"""

import os
import json
import base64
from typing import Dict, List, Optional, Tuple
from werkzeug.utils import secure_filename
from PIL import Image
import io
import re

class ImageRecognition:
    """Handles image upload and recipe recognition."""
    
    def __init__(self):
        """Initialize image recognition system."""
        self.allowed_extensions = {'png', 'jpg', 'jpeg', 'gif', 'bmp'}
        self.upload_folder = 'uploads'
        self.max_file_size = 16 * 1024 * 1024  # 16MB
        
        # Create upload folder if it doesn't exist
        os.makedirs(self.upload_folder, exist_ok=True)
        
        # Ingredient recognition patterns (simplified)
        self.ingredient_patterns = {
            'vegetables': [
                r'tomato', r'carrot', r'onion', r'potato', r'garlic', r'pepper',
                r'lettuce', r'cucumber', r'broccoli', r'spinach', r'mushroom'
            ],
            'fruits': [
                r'apple', r'banana', r'orange', r'lemon', r'lime', r'berry',
                r'strawberry', r'blueberry', r'grape', r'watermelon'
            ],
            'proteins': [
                r'chicken', r'beef', r'pork', r'fish', r'salmon', r'tuna',
                r'egg', r'tofu', r'beans', r'lentil'
            ],
            'grains': [
                r'rice', r'pasta', r'bread', r'flour', r'oat', r'quinoa',
                r'barley', r'couscous'
            ],
            'dairy': [
                r'cheese', r'milk', r'butter', r'yogurt', r'cream', r'sour cream'
            ],
            'herbs_spices': [
                r'basil', r'oregano', r'thyme', r'rosemary', r'parsley',
                r'cinnamon', r'cumin', r'paprika', r'pepper', r'salt'
            ]
        }
        
        # Recipe recognition based on ingredient combinations
        self.recipe_signatures = {
            'Spaghetti Carbonara': {
                'required': ['pasta', 'egg', 'cheese'],
                'optional': ['pepper', 'bacon'],
                'confidence_threshold': 0.7
            },
            'Chicken Stir Fry': {
                'required': ['chicken', 'vegetable'],
                'optional': ['rice', 'soy sauce', 'garlic', 'ginger'],
                'confidence_threshold': 0.6
            },
            'Greek Salad': {
                'required': ['tomato', 'cucumber', 'cheese'],
                'optional': ['olive', 'onion', 'pepper'],
                'confidence_threshold': 0.7
            },
            'Beef Tacos': {
                'required': ['beef', 'taco'],
                'optional': ['lettuce', 'tomato', 'cheese', 'sour cream'],
                'confidence_threshold': 0.6
            },
            'Vegetable Curry': {
                'required': ['vegetable', 'curry'],
                'optional': ['coconut', 'onion', 'garlic'],
                'confidence_threshold': 0.6
            }
        }
    
    def allowed_file(self, filename: str) -> bool:
        """Check if file extension is allowed."""
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in self.allowed_extensions
    
    def save_uploaded_file(self, file, filename: str = None) -> Tuple[bool, str, Dict]:
        """Save uploaded file and return status."""
        try:
            if filename is None:
                filename = secure_filename(file.filename)
            
            if not self.allowed_file(filename):
                return False, '', {'error': 'File type not allowed'}
            
            # Check file size
            file.seek(0, os.SEEK_END)
            file_size = file.tell()
            file.seek(0)
            
            if file_size > self.max_file_size:
                return False, '', {'error': 'File too large'}
            
            # Save file
            filepath = os.path.join(self.upload_folder, filename)
            file.save(filepath)
            
            return True, filepath, {'message': 'File saved successfully'}
        
        except Exception as e:
            return False, '', {'error': f'Failed to save file: {str(e)}'}
    
    def analyze_image(self, image_path: str) -> Dict:
        """Analyze image and detect ingredients."""
        try:
            # Open and process image
            with Image.open(image_path) as img:
                # Convert to RGB if necessary
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                
                # Get image info
                width, height = img.size
                format_type = img.format
                
                # Simulate ingredient detection (in real app, use ML model)
                detected_ingredients = self._simulate_ingredient_detection(img)
                
                # Analyze image properties
                image_analysis = {
                    'width': width,
                    'height': height,
                    'format': format_type,
                    'size_mb': round(os.path.getsize(image_path) / (1024 * 1024), 2),
                    'dominant_colors': self._get_dominant_colors(img),
                    'brightness': self._calculate_brightness(img),
                    'contrast': self._calculate_contrast(img)
                }
                
                return {
                    'status': 'success',
                    'detected_ingredients': detected_ingredients,
                    'image_analysis': image_analysis,
                    'confidence_scores': self._calculate_confidence_scores(detected_ingredients)
                }
        
        except Exception as e:
            return {
                'status': 'error',
                'error': f'Failed to analyze image: {str(e)}'
            }
    
    def recognize_recipe(self, detected_ingredients: List[str]) -> Dict:
        """Recognize recipe based on detected ingredients."""
        recipe_matches = []
        
        for recipe_name, signature in self.recipe_signatures.items():
            match_score = self._calculate_recipe_match(
                detected_ingredients, signature
            )
            
            if match_score >= signature['confidence_threshold']:
                recipe_matches.append({
                    'recipe_name': recipe_name,
                    'confidence': match_score,
                    'matched_ingredients': self._get_matched_ingredients(
                        detected_ingredients, signature
                    ),
                    'missing_ingredients': self._get_missing_ingredients(
                        detected_ingredients, signature
                    )
                })
        
        # Sort by confidence
        recipe_matches.sort(key=lambda x: x['confidence'], reverse=True)
        
        return {
            'status': 'success',
            'recipe_matches': recipe_matches,
            'top_match': recipe_matches[0] if recipe_matches else None,
            'total_matches': len(recipe_matches)
        }
    
    def _simulate_ingredient_detection(self, img: Image.Image) -> List[str]:
        """Simulate ingredient detection (placeholder for ML model)."""
        # In a real implementation, this would use a trained ML model
        # For demo purposes, we'll return some common ingredients based on image properties
        
        detected = []
        
        # Simulate detection based on image properties
        brightness = self._calculate_brightness(img)
        
        if brightness > 0.6:
            detected.extend(['tomato', 'pepper', 'carrot'])
        elif brightness > 0.4:
            detected.extend(['onion', 'garlic', 'mushroom'])
        else:
            detected.extend(['beef', 'soy sauce', 'dark sauce'])
        
        # Add some random ingredients for variety
        import random
        possible_ingredients = [
            'chicken', 'pasta', 'rice', 'cheese', 'lettuce',
            'cucumber', 'olive', 'basil', 'oregano', 'thyme'
        ]
        
        additional = random.sample(possible_ingredients, min(3, len(possible_ingredients)))
        detected.extend(additional)
        
        return list(set(detected))  # Remove duplicates
    
    def _get_dominant_colors(self, img: Image.Image) -> List[str]:
        """Get dominant colors from image."""
        # Simplified color detection
        colors = []
        
        # Convert to RGB if needed
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Sample pixels
        pixels = list(img.getdata())
        sample_pixels = pixels[::len(pixels)//1000]  # Sample 1000 pixels
        
        # Analyze color distribution
        red_count = sum(1 for r, g, b in sample_pixels if r > g and r > b)
        green_count = sum(1 for r, g, b in sample_pixels if g > r and g > b)
        blue_count = sum(1 for r, g, b in sample_pixels if b > r and b > g)
        
        total = len(sample_pixels)
        
        if red_count / total > 0.3:
            colors.append('red')
        if green_count / total > 0.3:
            colors.append('green')
        if blue_count / total > 0.3:
            colors.append('blue')
        
        if not colors:
            colors.append('neutral')
        
        return colors
    
    def _calculate_brightness(self, img: Image.Image) -> float:
        """Calculate average brightness of image."""
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        pixels = list(img.getdata())
        brightness = sum((r + g + b) / 3 for r, g, b in pixels) / len(pixels)
        return brightness / 255.0
    
    def _calculate_contrast(self, img: Image.Image) -> float:
        """Calculate image contrast."""
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        pixels = list(img.getdata())
        gray_values = [(r + g + b) / 3 for r, g, b in pixels]
        
        if len(gray_values) == 0:
            return 0.0
        
        mean_gray = sum(gray_values) / len(gray_values)
        variance = sum((x - mean_gray) ** 2 for x in gray_values) / len(gray_values)
        
        return variance / (255.0 ** 2)  # Normalize to 0-1
    
    def _calculate_confidence_scores(self, ingredients: List[str]) -> Dict[str, float]:
        """Calculate confidence scores for detected ingredients."""
        scores = {}
        
        for ingredient in ingredients:
            # Simulate confidence based on ingredient complexity
            base_confidence = 0.7
            
            # Higher confidence for common ingredients
            common_ingredients = ['tomato', 'onion', 'garlic', 'chicken', 'rice', 'pasta']
            if ingredient.lower() in common_ingredients:
                base_confidence += 0.2
            
            # Add some randomness
            import random
            base_confidence += random.uniform(-0.1, 0.1)
            
            scores[ingredient] = min(1.0, max(0.0, base_confidence))
        
        return scores
    
    def _calculate_recipe_match(self, ingredients: List[str], signature: Dict) -> float:
        """Calculate how well ingredients match a recipe signature."""
        required = signature['required']
        optional = signature['optional']
        
        # Check required ingredients
        required_match = sum(1 for req in required 
                           if any(req.lower() in ing.lower() for ing in ingredients))
        required_score = required_match / len(required) if required else 0
        
        # Check optional ingredients
        optional_match = sum(1 for opt in optional 
                           if any(opt.lower() in ing.lower() for ing in ingredients))
        optional_score = optional_match / len(optional) if optional else 0
        
        # Weighted score (required ingredients are more important)
        total_score = (required_score * 0.7) + (optional_score * 0.3)
        
        return total_score
    
    def _get_matched_ingredients(self, ingredients: List[str], signature: Dict) -> List[str]:
        """Get ingredients that match the recipe signature."""
        matched = []
        all_signature_ingredients = signature['required'] + signature['optional']
        
        for sig_ingredient in all_signature_ingredients:
            for ingredient in ingredients:
                if sig_ingredient.lower() in ingredient.lower():
                    matched.append(ingredient)
                    break
        
        return matched
    
    def _get_missing_ingredients(self, ingredients: List[str], signature: Dict) -> List[str]:
        """Get required ingredients that are missing."""
        missing = []
        
        for required in signature['required']:
            if not any(required.lower() in ing.lower() for ing in ingredients):
                missing.append(required)
        
        return missing
    
    def generate_recipe_from_image(self, image_path: str) -> Dict:
        """Generate complete recipe analysis from image."""
        # Analyze image
        analysis = self.analyze_image(image_path)
        
        if analysis['status'] != 'success':
            return analysis
        
        # Recognize recipe
        recipe_recognition = self.recognize_recipe(
            analysis['detected_ingredients']
        )
        
        # Combine results
        result = {
            'status': 'success',
            'image_analysis': analysis['image_analysis'],
            'detected_ingredients': analysis['detected_ingredients'],
            'confidence_scores': analysis['confidence_scores'],
            'recipe_recognition': recipe_recognition
        }
        
        # Add recipe suggestions if no strong match
        if not recipe_recognition['top_match'] or recipe_recognition['top_match']['confidence'] < 0.7:
            result['suggestions'] = self._generate_recipe_suggestions(
                analysis['detected_ingredients']
            )
        
        return result
    
    def _generate_recipe_suggestions(self, ingredients: List[str]) -> List[Dict]:
        """Generate recipe suggestions based on available ingredients."""
        suggestions = []
        
        # Simple ingredient-based suggestions
        if 'chicken' in ingredients:
            suggestions.append({
                'name': 'Grilled Chicken',
                'reason': 'You have chicken available',
                'additional_needed': ['oil', 'spices'],
                'confidence': 0.8
            })
        
        if 'pasta' in ingredients:
            suggestions.append({
                'name': 'Pasta with Vegetables',
                'reason': 'You have pasta and vegetables',
                'additional_needed': ['sauce', 'cheese'],
                'confidence': 0.7
            })
        
        if 'tomato' in ingredients and 'onion' in ingredients:
            suggestions.append({
                'name': 'Fresh Salad',
                'reason': 'You have fresh vegetables',
                'additional_needed': ['lettuce', 'dressing'],
                'confidence': 0.6
            })
        
        return suggestions
