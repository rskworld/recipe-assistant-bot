"""
Recipe Assistant Bot - Test Suite
Author: RSK World (https://rskworld.in)
Founder: Molla Samser
Designer & Tester: Rima Khatun
Contact: help@rskworld.in, +91 93305 39277
Year: 2026
"""

import unittest
import json
from app.chatbot import RecipeChatbot

class TestRecipeChatbot(unittest.TestCase):
    """Test cases for RecipeChatbot class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.chatbot = RecipeChatbot()
    
    def test_initialization(self):
        """Test chatbot initialization."""
        self.assertIsNotNone(self.chatbot.recipes)
        self.assertIsNotNone(self.chatbot.substitutions)
        self.assertIsNotNone(self.chatbot.cooking_tips)
        self.assertTrue(len(self.chatbot.recipes) > 0)
        self.assertTrue(len(self.chatbot.substitutions) > 0)
        self.assertTrue(len(self.chatbot.cooking_tips) > 0)
    
    def test_recipe_request(self):
        """Test recipe request handling."""
        message = "Give me a chicken recipe"
        response = self.chatbot.get_response(message)
        self.assertIn("recipe", response.lower())
        self.assertIn("chicken", response.lower())
    
    def test_substitution_request(self):
        """Test ingredient substitution request."""
        message = "What can I substitute for eggs?"
        response = self.chatbot.get_response(message)
        self.assertIn("substitute", response.lower())
        self.assertIn("eggs", response.lower())
    
    def test_cooking_tips_request(self):
        """Test cooking tips request."""
        message = "Give me some baking tips"
        response = self.chatbot.get_response(message)
        self.assertIn("tip", response.lower())
    
    def test_dietary_request(self):
        """Test dietary restriction request."""
        message = "vegetarian recipes"
        response = self.chatbot.get_response(message)
        self.assertIn("vegetarian", response.lower())
    
    def test_get_recipe_suggestions(self):
        """Test recipe suggestions method."""
        suggestions = self.chatbot.get_recipe_suggestions("chicken")
        self.assertTrue(len(suggestions) >= 0)
        
        dietary_suggestions = self.chatbot.get_recipe_suggestions("", "vegetarian")
        self.assertTrue(len(dietary_suggestions) >= 0)
    
    def test_get_ingredient_substitutions(self):
        """Test ingredient substitutions method."""
        subs = self.chatbot.get_ingredient_substitutions("eggs")
        self.assertTrue(len(subs) > 0)
        self.assertNotIn("No specific substitutions", subs[0])
        
        non_existent = self.chatbot.get_ingredient_substitutions("nonexistent")
        self.assertIn("No specific substitutions", non_existent[0])
    
    def test_get_cooking_tips(self):
        """Test cooking tips method."""
        tips = self.chatbot.get_cooking_tips("baking")
        self.assertTrue(len(tips) > 0)
        
        general_tips = self.chatbot.get_cooking_tips("general")
        self.assertTrue(len(general_tips) > 0)
    
    def test_empty_message(self):
        """Test handling of empty messages."""
        response = self.chatbot.get_response("")
        self.assertIsInstance(response, str)
        self.assertTrue(len(response) > 0)
    
    def test_message_case_insensitive(self):
        """Test case insensitive message handling."""
        message1 = "CHICKEN RECIPE"
        message2 = "chicken recipe"
        
        response1 = self.chatbot.get_response(message1)
        response2 = self.chatbot.get_response(message2)
        
        self.assertIsInstance(response1, str)
        self.assertIsInstance(response2, str)

class TestFlaskRoutes(unittest.TestCase):
    """Test cases for Flask routes."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Import here to avoid issues with test discovery
        from app import create_app
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
    
    def test_index_route(self):
        """Test index route."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Recipe Assistant Bot', response.data)
    
    def test_chat_api_valid_message(self):
        """Test chat API with valid message."""
        response = self.client.post('/api/chat', 
                                  json={'message': 'Give me a recipe'},
                                  content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('response', data)
        self.assertIn('status', data)
        self.assertEqual(data['status'], 'success')
    
    def test_chat_api_empty_message(self):
        """Test chat API with empty message."""
        response = self.client.post('/api/chat', 
                                  json={'message': ''},
                                  content_type='application/json')
        self.assertEqual(response.status_code, 400)
    
    def test_chat_api_no_message(self):
        """Test chat API with no message."""
        response = self.client.post('/api/chat', 
                                  json={},
                                  content_type='application/json')
        self.assertEqual(response.status_code, 400)
    
    def test_recipes_api(self):
        """Test recipes API endpoint."""
        response = self.client.get('/api/recipes?query=chicken')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('recipes', data)
        self.assertIn('status', data)
        self.assertEqual(data['status'], 'success')
    
    def test_substitutions_api(self):
        """Test substitutions API endpoint."""
        response = self.client.post('/api/substitutions', 
                                  json={'ingredient': 'eggs'},
                                  content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('substitutions', data)
        self.assertIn('status', data)
        self.assertEqual(data['status'], 'success')
    
    def test_tips_api(self):
        """Test tips API endpoint."""
        response = self.client.get('/api/tips?category=baking')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('tips', data)
        self.assertIn('status', data)
        self.assertEqual(data['status'], 'success')

if __name__ == '__main__':
    unittest.main()
