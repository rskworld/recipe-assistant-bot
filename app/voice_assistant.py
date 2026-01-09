"""
Recipe Assistant Bot - Voice Command Integration
Author: RSK World (https://rskworld.in)
Founder: Molla Samser
Designer & Tester: Rima Khatun
Contact: help@rskworld.in, +91 93305 39277
Year: 2026
"""

import speech_recognition as sr
import pyttsx3
import json
import re
import threading
import queue
import time
from typing import Dict, List, Optional, Callable, Any
from dataclasses import dataclass
from datetime import datetime

@dataclass
class VoiceCommand:
    """Voice command model."""
    command: str
    intent: str
    entities: Dict[str, Any]
    confidence: float
    timestamp: str

class VoiceAssistant:
    """Handles voice commands and text-to-speech."""
    
    def __init__(self):
        """Initialize voice assistant."""
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.tts_engine = pyttsx3.init()
        
        # Voice settings
        self.tts_engine.setProperty('rate', 150)  # Speed of speech
        self.tts_engine.setProperty('volume', 0.9)  # Volume level
        
        # Command patterns
        self.command_patterns = {
            'recipe_search': [
                r'find (?:a )?recipe (?:for|with) (.+)',
                r'search (?:for )?(.+?) recipe',
                r'look up (.+?) recipe',
                r'what can i make with (.+)'
            ],
            'ingredient_substitution': [
                r'what can i use instead of (.+)',
                r'substitute (.+)',
                r'replacement for (.+)'
            ],
            'cooking_time': [
                r'how long (?:do|i) (?:you|I) cook (.+)',
                r'cooking time for (.+)',
                r'(.+) cooking time'
            ],
            'temperature_conversion': [
                r'convert (\d+) degrees? (.+?) to (.+)',
                r'(\d+)°(.+?) to (.+)',
                r'what is (\d+) (.+?) in (.+)'
            ],
            'shopping_list': [
                r'add (.+?) to shopping list',
                r'put (.+?) on my list',
                r'shopping list add (.+)'
            ],
            'timer': [
                r'set timer for (\d+) (.+)',
                r'timer (\d+) (.+)',
                r'start timer (\d+) (.+)'
            ],
            'nutrition_info': [
                r'how many calories in (.+)',
                r'nutrition (?:info|information) (?:for|about) (.+)',
                r'(.+) nutrition'
            ],
            'step_by_step': [
                r'how to cook (.+)',
                r'step by step (.+)',
                r'guide me through (.+)'
            ],
            'meal_planning': [
                r'plan meals? for (.+)',
                r'meal plan for (.+)',
                r'what should i eat this week'
            ]
        }
        
        # Response templates
        self.responses = {
            'greeting': [
                "Hello! I'm your Recipe Assistant. How can I help you today?",
                "Hi there! Ready to help you with cooking. What would you like to make?",
                "Welcome! I'm here to assist with all your cooking needs."
            ],
            'confirmation': [
                "Got it! I'll help you with that.",
                "Understood! Let me take care of that for you.",
                "Perfect! I'm on it."
            ],
            'error': [
                "I didn't quite catch that. Could you repeat?",
                "Sorry, I'm having trouble understanding. Try again?",
                "I didn't get that. Could you say it differently?"
            ],
            'processing': [
                "Let me check that for you...",
                "Searching my recipe database...",
                "Looking that up for you..."
            ]
        }
        
        # Command queue for async processing
        self.command_queue = queue.Queue()
        self.is_listening = False
        self.current_recipe = None
        
    def start_listening(self, callback: Callable[[VoiceCommand], None]):
        """Start listening for voice commands."""
        self.is_listening = True
        self.callback = callback
        
        def listen_loop():
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                
            while self.is_listening:
                try:
                    with self.microphone as source:
                        audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
                    
                    # Recognize speech
                    text = self.recognizer.recognize_google(audio)
                    command = self._parse_command(text)
                    
                    if command:
                        self.command_queue.put(command)
                        
                except sr.WaitTimeoutError:
                    continue
                except sr.UnknownValueError:
                    continue
                except Exception as e:
                    print(f"Voice recognition error: {e}")
                    continue
        
        # Start listening in separate thread
        self.listening_thread = threading.Thread(target=listen_loop, daemon=True)
        self.listening_thread.start()
        
        # Process commands
        self._process_commands()
    
    def stop_listening(self):
        """Stop listening for voice commands."""
        self.is_listening = False
        if hasattr(self, 'listening_thread'):
            self.listening_thread.join(timeout=1)
    
    def speak(self, text: str):
        """Convert text to speech."""
        try:
            self.tts_engine.say(text)
            self.tts_engine.runAndWait()
        except Exception as e:
            print(f"TTS error: {e}")
    
    def _parse_command(self, text: str) -> Optional[VoiceCommand]:
        """Parse voice command text."""
        text = text.lower().strip()
        
        for intent, patterns in self.command_patterns.items():
            for pattern in patterns:
                match = re.search(pattern, text)
                if match:
                    entities = {}
                    
                    # Extract entities based on groups
                    if match.groups():
                        if intent == 'recipe_search':
                            entities['ingredients'] = match.group(1).strip()
                        elif intent == 'ingredient_substitution':
                            entities['ingredient'] = match.group(1).strip()
                        elif intent == 'cooking_time':
                            entities['food_item'] = match.group(1).strip()
                        elif intent == 'temperature_conversion':
                            entities['temperature'] = int(match.group(1))
                            entities['from_unit'] = match.group(2).strip()
                            entities['to_unit'] = match.group(3).strip()
                        elif intent == 'shopping_list':
                            entities['item'] = match.group(1).strip()
                        elif intent == 'timer':
                            entities['duration'] = int(match.group(1))
                            entities['unit'] = match.group(2).strip()
                        elif intent == 'nutrition_info':
                            entities['food_item'] = match.group(1).strip()
                        elif intent == 'step_by_step':
                            entities['recipe'] = match.group(1).strip()
                        elif intent == 'meal_planning':
                            entities['timeframe'] = match.group(1).strip() if match.group(1) else 'week'
                    
                    return VoiceCommand(
                        command=text,
                        intent=intent,
                        entities=entities,
                        confidence=0.8,  # Simplified confidence
                        timestamp=datetime.now().isoformat()
                    )
        
        return None
    
    def _process_commands(self):
        """Process queued commands."""
        while self.is_listening:
            try:
                if not self.command_queue.empty():
                    command = self.command_queue.get(timeout=0.1)
                    self._handle_command(command)
                    self.callback(command)
                else:
                    time.sleep(0.1)
            except queue.Empty:
                continue
            except Exception as e:
                print(f"Command processing error: {e}")
    
    def _handle_command(self, command: VoiceCommand):
        """Handle voice command with appropriate response."""
        if command.intent == 'recipe_search':
            self.speak("Searching for recipes with those ingredients...")
            
        elif command.intent == 'ingredient_substitution':
            self.speak(f"Looking for substitutes for {command.entities['ingredient']}...")
            
        elif command.intent == 'cooking_time':
            self.speak(f"Checking cooking time for {command.entities['food_item']}...")
            
        elif command.intent == 'temperature_conversion':
            temp = command.entities['temperature']
            from_unit = command.entities['from_unit']
            to_unit = command.entities['to_unit']
            self.speak(f"Converting {temp} degrees {from_unit} to {to_unit}...")
            
        elif command.intent == 'shopping_list':
            item = command.entities['item']
            self.speak(f"Adding {item} to your shopping list...")
            
        elif command.intent == 'timer':
            duration = command.entities['duration']
            unit = command.entities['unit']
            self.speak(f"Setting timer for {duration} {unit}...")
            
        elif command.intent == 'nutrition_info':
            self.speak(f"Getting nutrition information for {command.entities['food_item']}...")
            
        elif command.intent == 'step_by_step':
            self.speak(f"Getting step-by-step instructions for {command.entities['recipe']}...")
            
        elif command.intent == 'meal_planning':
            timeframe = command.entities['timeframe']
            self.speak(f"Creating meal plan for {timeframe}...")
    
    def get_voice_commands_history(self, limit: int = 10) -> List[Dict]:
        """Get history of voice commands (mock implementation)."""
        # In real implementation, this would store commands in database
        return [
            {
                'command': 'find recipe with chicken',
                'intent': 'recipe_search',
                'timestamp': datetime.now().isoformat(),
                'processed': True
            }
        ]
    
    def set_voice_settings(self, rate: int = None, volume: float = None, voice: str = None):
        """Update voice settings."""
        if rate is not None:
            self.tts_engine.setProperty('rate', rate)
        
        if volume is not None:
            self.tts_engine.setProperty('volume', volume)
        
        if voice is not None:
            voices = self.tts_engine.getProperty('voices')
            for v in voices:
                if voice.lower() in v.name.lower():
                    self.tts_engine.setProperty('voice', v.id)
                    break
    
    def get_available_voices(self) -> List[Dict]:
        """Get list of available TTS voices."""
        voices = self.tts_engine.getProperty('voices')
        return [
            {
                'id': voice.id,
                'name': voice.name,
                'languages': voice.languages,
                'gender': voice.gender
            }
            for voice in voices
        ]
    
    def test_microphone(self) -> Dict:
        """Test microphone functionality."""
        try:
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                audio = self.recognizer.listen(source, timeout=2, phrase_time_limit=3)
            
            text = self.recognizer.recognize_google(audio)
            return {
                'status': 'success',
                'recognized_text': text,
                'message': 'Microphone working correctly'
            }
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e),
                'message': 'Microphone test failed'
            }
    
    def create_custom_command(self, name: str, patterns: List[str], response_template: str):
        """Create custom voice command."""
        self.command_patterns[name] = patterns
        self.responses[name] = [response_template]
    
    def get_command_suggestions(self, partial_command: str) -> List[str]:
        """Get suggestions for partial voice commands."""
        suggestions = []
        
        for intent, patterns in self.command_patterns.items():
            for pattern in patterns:
                # Simple matching - in real app would use more sophisticated NLP
                if any(word in partial_command.lower() for word in pattern.split() if word.isalpha()):
                    suggestions.append(f"Try: {pattern}")
        
        return suggestions[:5]  # Return top 5 suggestions
