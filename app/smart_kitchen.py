"""
Recipe Assistant Bot - Smart Kitchen Device Integration
Author: RSK World (https://rskworld.in)
Founder: Molla Samser
Designer & Tester: Rima Khatun
Contact: help@rskworld.in, +91 93305 39277
Year: 2026
"""

import json
import requests
import asyncio
import websockets
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from enum import Enum

class DeviceType(Enum):
    """Smart kitchen device types."""
    OVEN = "oven"
    STOVE = "stove"
    MICROWAVE = "microwave"
    REFRIGERATOR = "refrigerator"
    DISHWASHER = "dishwasher"
    COFFEE_MAKER = "coffee_maker"
    AIR_FRYER = "air_fryer"
    INSTANT_POT = "instant_pot"
    SMART_SCALE = "smart_scale"
    THERMOMETER = "thermometer"

@dataclass
class SmartDevice:
    """Smart kitchen device model."""
    id: str
    name: str
    type: DeviceType
    brand: str
    model: str
    ip_address: str
    status: str
    capabilities: List[str]
    current_settings: Dict[str, Any]
    last_seen: str
    battery_level: Optional[float] = None
    
    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        result = asdict(self)
        result['type'] = self.type.value
        return result

@dataclass
class CookingSession:
    """Active cooking session."""
    id: str
    device_id: str
    recipe_name: str
    step_number: int
    target_temperature: float
    current_temperature: float
    remaining_time: int
    start_time: str
    status: str
    
    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return asdict(self)

class SmartKitchenManager:
    """Manages smart kitchen devices and automation."""
    
    def __init__(self):
        """Initialize smart kitchen manager."""
        self.devices = {}  # device_id -> SmartDevice
        self.cooking_sessions = {}  # session_id -> CookingSession
        self.device_apis = {}  # device_type -> API handler
        self.automation_rules = []  # List of automation rules
        
        # Initialize device APIs
        self._initialize_device_apis()
        
        # Load mock devices for demo
        self._load_mock_devices()
    
    def _initialize_device_apis(self):
        """Initialize device API handlers."""
        self.device_apis = {
            DeviceType.OVEN: self._handle_oven_api,
            DeviceType.STOVE: self._handle_stove_api,
            DeviceType.MICROWAVE: self._handle_microwave_api,
            DeviceType.REFRIGERATOR: self._handle_refrigerator_api,
            DeviceType.AIR_FRYER: self._handle_air_fryer_api,
            DeviceType.INSTANT_POT: self._handle_instant_pot_api,
            DeviceType.SMART_SCALE: self._handle_smart_scale_api,
            DeviceType.THERMOMETER: self._handle_thermometer_api
        }
    
    def _load_mock_devices(self):
        """Load mock smart devices for demonstration."""
        mock_devices = [
            SmartDevice(
                id="oven_001",
                name="Kitchen Oven",
                type=DeviceType.OVEN,
                brand="SmartOven",
                model="SO-2000",
                ip_address="192.168.1.100",
                status="online",
                capabilities=["bake", "broil", "convection", "preheat", "timer"],
                current_settings={"temperature": 350, "mode": "bake"},
                last_seen=datetime.now().isoformat()
            ),
            SmartDevice(
                id="scale_001",
                name="Kitchen Scale",
                type=DeviceType.SMART_SCALE,
                brand="SmartScale",
                model="SS-100",
                ip_address="192.168.1.101",
                status="online",
                capabilities=["weigh", "tare", "nutrition_estimate"],
                current_settings={"unit": "grams", "weight": 0},
                last_seen=datetime.now().isoformat(),
                battery_level=85.0
            ),
            SmartDevice(
                id="thermometer_001",
                name="Meat Thermometer",
                type=DeviceType.THERMOMETER,
                brand="ThermoPro",
                model="TP-500",
                ip_address="192.168.1.102",
                status="online",
                capabilities=["temperature", "alerts", "presets"],
                current_settings={"temperature": 72.0, "unit": "fahrenheit"},
                last_seen=datetime.now().isoformat(),
                battery_level=92.0
            )
        ]
        
        for device in mock_devices:
            self.devices[device.id] = device
    
    def discover_devices(self) -> List[SmartDevice]:
        """Discover smart kitchen devices on network."""
        discovered_devices = []
        
        # Mock discovery - in real implementation would scan network
        for device in self.devices.values():
            if device.status == "online":
                discovered_devices.append(device)
        
        return discovered_devices
    
    def add_device(self, device: SmartDevice) -> Dict:
        """Add a new smart device."""
        try:
            # Test device connection
            if self._test_device_connection(device):
                self.devices[device.id] = device
                return {
                    'status': 'success',
                    'message': f'Device {device.name} added successfully',
                    'device_id': device.id
                }
            else:
                return {
                    'status': 'error',
                    'message': 'Failed to connect to device'
                }
        except Exception as e:
            return {
                'status': 'error',
                'message': f'Failed to add device: {str(e)}'
            }
    
    def remove_device(self, device_id: str) -> Dict:
        """Remove a smart device."""
        if device_id in self.devices:
            device_name = self.devices[device_id].name
            del self.devices[device_id]
            
            # Stop any active sessions
            sessions_to_remove = [
                session_id for session_id, session in self.cooking_sessions.items()
                if session.device_id == device_id
            ]
            
            for session_id in sessions_to_remove:
                del self.cooking_sessions[session_id]
            
            return {
                'status': 'success',
                'message': f'Device {device_name} removed successfully'
            }
        else:
            return {
                'status': 'error',
                'message': 'Device not found'
            }
    
    def get_device_status(self, device_id: str) -> Optional[Dict]:
        """Get current status of a device."""
        if device_id not in self.devices:
            return None
        
        device = self.devices[device_id]
        
        # Get real-time status from device
        try:
            api_handler = self.device_apis.get(device.type)
            if api_handler:
                current_status = api_handler(device, "status")
                device.current_settings.update(current_status)
                device.last_seen = datetime.now().isoformat()
        except Exception as e:
            print(f"Failed to get device status: {e}")
        
        return device.to_dict()
    
    def control_device(self, device_id: str, command: str, parameters: Dict = None) -> Dict:
        """Send control command to device."""
        if device_id not in self.devices:
            return {'status': 'error', 'message': 'Device not found'}
        
        device = self.devices[device_id]
        
        try:
            api_handler = self.device_apis.get(device.type)
            if api_handler:
                result = api_handler(device, command, parameters or {})
                
                if result.get('success'):
                    device.current_settings.update(result.get('settings', {}))
                    device.last_seen = datetime.now().isoformat()
                
                return result
            else:
                return {'status': 'error', 'message': 'Device type not supported'}
        
        except Exception as e:
            return {'status': 'error', 'message': f'Command failed: {str(e)}'}
    
    def start_cooking_session(self, device_id: str, recipe_name: str, 
                           target_temperature: float, estimated_time: int) -> Dict:
        """Start a cooking session on a device."""
        if device_id not in self.devices:
            return {'status': 'error', 'message': 'Device not found'}
        
        device = self.devices[device_id]
        session_id = f"session_{len(self.cooking_sessions) + 1}"
        
        session = CookingSession(
            id=session_id,
            device_id=device_id,
            recipe_name=recipe_name,
            step_number=1,
            target_temperature=target_temperature,
            current_temperature=device.current_settings.get('temperature', 70),
            remaining_time=estimated_time,
            start_time=datetime.now().isoformat(),
            status="active"
        )
        
        self.cooking_sessions[session_id] = session
        
        # Start preheating if it's an oven
        if device.type == DeviceType.OVEN:
            self.control_device(device_id, "preheat", {"temperature": target_temperature})
        
        return {
            'status': 'success',
            'session_id': session_id,
            'message': f'Cooking session started for {recipe_name}'
        }
    
    def update_cooking_session(self, session_id: str, step_number: int = None,
                            temperature: float = None, time_remaining: int = None) -> Dict:
        """Update cooking session progress."""
        if session_id not in self.cooking_sessions:
            return {'status': 'error', 'message': 'Session not found'}
        
        session = self.cooking_sessions[session_id]
        
        if step_number is not None:
            session.step_number = step_number
        
        if temperature is not None:
            session.current_temperature = temperature
        
        if time_remaining is not None:
            session.remaining_time = time_remaining
        
        # Check if session is complete
        if session.remaining_time <= 0:
            session.status = "completed"
        
        return {
            'status': 'success',
            'session': session.to_dict()
        }
    
    def get_active_sessions(self) -> List[CookingSession]:
        """Get all active cooking sessions."""
        return [
            session for session in self.cooking_sessions.values()
            if session.status == "active"
        ]
    
    def create_automation_rule(self, name: str, trigger: Dict, action: Dict) -> Dict:
        """Create automation rule for smart devices."""
        rule = {
            'id': f"rule_{len(self.automation_rules) + 1}",
            'name': name,
            'trigger': trigger,
            'action': action,
            'enabled': True,
            'created_at': datetime.now().isoformat()
        }
        
        self.automation_rules.append(rule)
        
        return {
            'status': 'success',
            'rule_id': rule['id'],
            'message': f'Automation rule "{name}" created successfully'
        }
    
    def execute_automation_rules(self):
        """Execute automation rules based on current conditions."""
        for rule in self.automation_rules:
            if not rule['enabled']:
                continue
            
            trigger = rule['trigger']
            action = rule['action']
            
            # Check trigger conditions
            if self._evaluate_trigger(trigger):
                self._execute_action(action)
    
    def _evaluate_trigger(self, trigger: Dict) -> bool:
        """Evaluate if trigger conditions are met."""
        trigger_type = trigger.get('type')
        
        if trigger_type == 'temperature':
            device_id = trigger.get('device_id')
            threshold = trigger.get('threshold')
            operator = trigger.get('operator', '>')
            
            device_status = self.get_device_status(device_id)
            if device_status:
                current_temp = device_status['current_settings'].get('temperature', 0)
                
                if operator == '>':
                    return current_temp > threshold
                elif operator == '<':
                    return current_temp < threshold
                elif operator == '=':
                    return current_temp == threshold
        
        elif trigger_type == 'time':
            trigger_time = trigger.get('time')
            current_time = datetime.now().strftime('%H:%M')
            return current_time == trigger_time
        
        elif trigger_type == 'device_status':
            device_id = trigger.get('device_id')
            expected_status = trigger.get('status')
            
            device_status = self.get_device_status(device_id)
            if device_status:
                return device_status['status'] == expected_status
        
        return False
    
    def _execute_action(self, action: Dict):
        """Execute automation action."""
        action_type = action.get('type')
        
        if action_type == 'device_command':
            device_id = action.get('device_id')
            command = action.get('command')
            parameters = action.get('parameters', {})
            
            self.control_device(device_id, command, parameters)
        
        elif action_type == 'notification':
            message = action.get('message')
            # Send notification (would integrate with notification system)
            print(f"Automation notification: {message}")
        
        elif action_type == 'session_update':
            session_id = action.get('session_id')
            updates = action.get('updates', {})
            
            self.update_cooking_session(session_id, **updates)
    
    def _test_device_connection(self, device: SmartDevice) -> bool:
        """Test connection to a device."""
        try:
            # Mock connection test - in real implementation would ping device
            return True
        except:
            return False
    
    # Device API handlers (mock implementations)
    def _handle_oven_api(self, device: SmartDevice, command: str, parameters: Dict = None) -> Dict:
        """Handle oven device commands."""
        if command == "preheat":
            temp = parameters.get('temperature', 350)
            device.current_settings['temperature'] = temp
            device.current_settings['mode'] = 'preheating'
            return {'success': True, 'settings': device.current_settings}
        
        elif command == "bake":
            temp = parameters.get('temperature', 350)
            device.current_settings['temperature'] = temp
            device.current_settings['mode'] = 'bake'
            return {'success': True, 'settings': device.current_settings}
        
        elif command == "status":
            return {'success': True, 'settings': device.current_settings}
        
        return {'success': False, 'message': 'Unknown command'}
    
    def _handle_stove_api(self, device: SmartDevice, command: str, parameters: Dict = None) -> Dict:
        """Handle stove device commands."""
        if command == "set_burner":
            burner = parameters.get('burner', 1)
            level = parameters.get('level', 5)
            device.current_settings[f'burner_{burner}'] = level
            return {'success': True, 'settings': device.current_settings}
        
        return {'success': False, 'message': 'Unknown command'}
    
    def _handle_microwave_api(self, device: SmartDevice, command: str, parameters: Dict = None) -> Dict:
        """Handle microwave device commands."""
        if command == "cook":
            time = parameters.get('time', 60)
            power = parameters.get('power', 100)
            device.current_settings['time'] = time
            device.current_settings['power'] = power
            return {'success': True, 'settings': device.current_settings}
        
        return {'success': False, 'message': 'Unknown command'}
    
    def _handle_refrigerator_api(self, device: SmartDevice, command: str, parameters: Dict = None) -> Dict:
        """Handle refrigerator device commands."""
        if command == "set_temperature":
            temp = parameters.get('temperature', 37)
            device.current_settings['temperature'] = temp
            return {'success': True, 'settings': device.current_settings}
        
        return {'success': False, 'message': 'Unknown command'}
    
    def _handle_air_fryer_api(self, device: SmartDevice, command: str, parameters: Dict = None) -> Dict:
        """Handle air fryer device commands."""
        if command == "fry":
            temp = parameters.get('temperature', 400)
            time = parameters.get('time', 15)
            device.current_settings['temperature'] = temp
            device.current_settings['time'] = time
            return {'success': True, 'settings': device.current_settings}
        
        return {'success': False, 'message': 'Unknown command'}
    
    def _handle_instant_pot_api(self, device: SmartDevice, command: str, parameters: Dict = None) -> Dict:
        """Handle Instant Pot device commands."""
        if command == "pressure_cook":
            time = parameters.get('time', 30)
            pressure = parameters.get('pressure', 'high')
            device.current_settings['time'] = time
            device.current_settings['pressure'] = pressure
            return {'success': True, 'settings': device.current_settings}
        
        return {'success': False, 'message': 'Unknown command'}
    
    def _handle_smart_scale_api(self, device: SmartDevice, command: str, parameters: Dict = None) -> Dict:
        """Handle smart scale device commands."""
        if command == "weigh":
            # Mock weight reading
            weight = parameters.get('expected_weight', 0)
            device.current_settings['weight'] = weight
            return {'success': True, 'settings': device.current_settings}
        
        elif command == "tare":
            device.current_settings['weight'] = 0
            return {'success': True, 'settings': device.current_settings}
        
        return {'success': False, 'message': 'Unknown command'}
    
    def _handle_thermometer_api(self, device: SmartDevice, command: str, parameters: Dict = None) -> Dict:
        """Handle thermometer device commands."""
        if command == "measure":
            # Mock temperature reading
            temp = parameters.get('expected_temp', 72.0)
            device.current_settings['temperature'] = temp
            return {'success': True, 'settings': device.current_settings}
        
        return {'success': False, 'message': 'Unknown command'}
    
    def get_device_analytics(self, device_id: str, days: int = 30) -> Dict:
        """Get analytics for device usage."""
        if device_id not in self.devices:
            return {'error': 'Device not found'}
        
        # Mock analytics data
        return {
            'device_id': device_id,
            'period_days': days,
            'total_usage_hours': 45.5,
            'average_daily_usage': 1.52,
            'most_used_function': 'bake',
            'energy_consumption_kwh': 12.3,
            'maintenance_alerts': 0,
            'efficiency_score': 8.7
        }
