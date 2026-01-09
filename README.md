# Recipe Assistant Bot

![Recipe Assistant Bot](https://img.shields.io/badge/Version-1.0.0-blue.svg)
![Python](https://img.shields.io/badge/Python-3.8+-green.svg)
![Flask](https://img.shields.io/badge/Flask-2.3.3-red.svg)
![License](https://img.shields.io/badge/License-Educational-yellow.svg)

**Author:** RSK World (https://rskworld.in)  
**Founder:** Molla Samser  
**Designer & Tester:** Rima Khatun  
**Contact:** help@rskworld.in, +91 93305 39277  
**Year:** 2026  

## 🍳 Description

Recipe Assistant Bot is an AI-powered cooking chatbot that provides recipe suggestions, ingredient substitutions, cooking tips, and meal planning assistance. Perfect for food apps and cooking platforms, this beginner-friendly project demonstrates the integration of Python web development with natural language processing.

## ✨ Features

- 🍽️ **Recipe Suggestions** - Get personalized recipe recommendations
- 🔄 **Ingredient Substitutions** - Find alternatives for missing ingredients
- 💡 **Cooking Tips** - Learn professional cooking techniques
- 📋 **Meal Planning** - Plan your meals efficiently
- 🥗 **Dietary Restrictions** - Support for vegetarian, vegan, gluten-free, keto, and more
- 🌐 **Web Interface** - Modern, responsive chat interface
- 📱 **Mobile Friendly** - Works on all devices

## 🛠️ Technologies Used

- **Backend:** Python 3.8+, Flask 2.3.3
- **Frontend:** HTML5, CSS3, JavaScript, Bootstrap 5
- **APIs:** Recipe APIs, OpenAI API (optional)
- **Database:** SQLite (default), configurable for other databases
- **Additional:** Flask-CORS, Requests, Python-dotenv

## 📋 Requirements

- Python 3.8 or higher
- pip (Python package manager)
- Git (for cloning)

## 🚀 Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd recipe-assistant-bot
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env file with your configuration
   ```

5. **Run the application:**
   ```bash
   python run.py
   ```

6. **Open your browser and navigate to:**
   ```
   http://127.0.0.1:5000
   ```

## 📁 Project Structure

```
recipe-assistant-bot/
├── app/
│   ├── __init__.py          # Flask app factory
│   ├── routes.py            # Application routes
│   └── chatbot.py           # Core chatbot logic
├── static/
│   ├── css/
│   │   └── style.css        # Custom styles
│   ├── js/
│   │   └── chat.js          # Frontend JavaScript
│   └── images/              # Static images
├── templates/
│   └── index.html           # Main HTML template
├── config.py                # Configuration settings
├── run.py                   # Application runner
├── requirements.txt         # Python dependencies
├── .env.example            # Environment variables example
└── README.md               # This file
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file based on `.env.example`:

```bash
# Flask Configuration
FLASK_APP=run.py
FLASK_ENV=development
SECRET_KEY=your-secret-key-here

# API Keys (Optional)
SPOONACULAR_API_KEY=your-spoonacular-api-key
OPENAI_API_KEY=your-openai-api-key

# Server Configuration
HOST=127.0.0.1
PORT=5000
```

### Optional API Integration

For enhanced functionality, you can integrate with:

1. **Spoonacular API** (for real recipe data):
   - Sign up at https://spoonacular.com/food-api
   - Add your API key to `.env`

2. **OpenAI API** (for advanced AI responses):
   - Sign up at https://openai.com/
   - Add your API key to `.env`

## 📖 Usage

### Basic Chat

1. Open the web interface
2. Type your cooking-related question in the chat
3. Press Enter or click Send
4. Receive instant recipe suggestions, substitutions, or tips

### Example Queries

- "Give me a chicken recipe"
- "What can I substitute for eggs?"
- "Give me some baking tips"
- "Vegetarian pasta recipes"
- "How do I cook rice perfectly?"

### Quick Suggestions

Use the quick suggestion buttons for common queries:
- Chicken Recipe
- Egg Substitutes
- Baking Tips
- Vegetarian Options

## 🧪 Testing

Run the test suite:

```bash
# Install test dependencies
pip install pytest pytest-flask

# Run tests
pytest

# Run with coverage
pytest --cov=app
```

## 📚 API Endpoints

### Chat API
- **POST** `/api/chat` - Send message to chatbot
- **GET** `/api/recipes` - Get recipe suggestions
- **POST** `/api/substitutions` - Get ingredient substitutions
- **GET** `/api/tips` - Get cooking tips

### Request Examples

```javascript
// Chat endpoint
POST /api/chat
{
  "message": "Give me a chicken recipe"
}

// Substitutions endpoint
POST /api/substitutions
{
  "ingredient": "eggs"
}
```

## 🔒 Security Features

- CORS protection
- Input validation and sanitization
- Rate limiting (configurable)
- Secure session handling
- Environment variable configuration

## 🌟 Customization

### Adding New Recipes

Edit `app/chatbot.py` and add recipes to the `_load_recipes()` method:

```python
{
    'name': 'Your Recipe Name',
    'ingredients': ['ingredient1', 'ingredient2'],
    'instructions': 'Step-by-step instructions',
    'prep_time': '30 minutes',
    'difficulty': 'easy',
    'dietary': ['vegetarian']
}
```

### Adding New Substitutions

Edit the `_load_substitutions()` method:

```python
'your_ingredient': ['substitution1', 'substitution2', 'substitution3']
```

## 🚀 Deployment

### Production Deployment

1. **Set production environment:**
   ```bash
   export FLASK_ENV=production
   export FLASK_CONFIG=production
   ```

2. **Use a production server:**
   ```bash
   gunicorn -w 4 -b 0.0.0.0:5000 run:app
   ```

3. **Set up reverse proxy (nginx recommended)**

### Docker Deployment

```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "run:app"]
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is created for educational purposes by RSK World. Content used for educational purposes only.

## 📞 Support

- **Website:** https://rskworld.in
- **Email:** help@rskworld.in
- **Phone:** +91 93305 39277
- **Address:** Nutanhat, Mongolkote, Purba Burdwan, West Bengal, India - 713147

## 🙏 Acknowledgments

- **Founder:** Molla Samser
- **Designer & Tester:** Rima Khatun
- **RSK World** - Free Programming Resources & Source Code

---

**© 2026 RSK World. All rights reserved.**  
*Educational Purpose Project*
