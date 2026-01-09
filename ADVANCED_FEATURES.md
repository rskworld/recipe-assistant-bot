# Advanced Features Documentation

## Overview
This document describes all the advanced features added to the Recipe Assistant Bot.

## 🎯 New Features Added

### 1. Recipe Scaling (`/api/recipe/scale`)
Scale any recipe to different serving sizes automatically.

**Features:**
- Adjust ingredient quantities proportionally
- Recalculate prep time
- Update nutritional information
- Maintain recipe quality at any serving size

**Example Request:**
```json
POST /api/recipe/scale
{
  "recipe_name": "Spaghetti Carbonara",
  "servings": 8
}
```

---

### 2. Recipe Variations Generator (`/api/recipe/variations`)
Generate creative variations of any recipe.

**Variation Types:**
- **Cuisine Variations**: Transform recipes into different cuisine styles (Italian, Mexican, Asian, Indian)
- **Dietary Variations**: Convert to vegan, gluten-free, keto, etc.
- **Spice Level Variations**: Adjust spice intensity (mild, medium, hot, extra hot)

**Example Request:**
```json
POST /api/recipe/variations
{
  "recipe_name": "Chicken Stir Fry",
  "variation_type": "all"
}
```

---

### 3. Leftover Recipe Suggestions (`/api/recipe/leftover-suggestions`)
Get recipe suggestions based on ingredients you have available.

**Features:**
- Match recipes to available ingredients
- Show completion percentage for each recipe
- List missing ingredients needed
- Prioritize recipes by ingredient match score

**Example Request:**
```json
POST /api/recipe/leftover-suggestions
{
  "ingredients": ["chicken", "tomatoes", "onion", "garlic"]
}
```

---

### 4. Ingredient Inventory Management

#### Get Inventory (`GET /api/inventory`)
View your complete ingredient inventory organized by location.

#### Add to Inventory (`POST /api/inventory/add`)
Add ingredients to your inventory with details.

**Features:**
- Track quantities and units
- Set expiry dates
- Organize by location (pantry, fridge, freezer)
- Add notes and categories

**Example Request:**
```json
POST /api/inventory/add
{
  "name": "Chicken Breast",
  "quantity": 1.5,
  "unit": "pounds",
  "expiry_date": "2026-01-15",
  "location": "fridge",
  "category": "proteins",
  "notes": "Organic"
}
```

#### Update Inventory (`PUT /api/inventory/update`)
Update existing inventory items.

#### Remove from Inventory (`DELETE /api/inventory/remove`)
Remove items from inventory.

#### Get Recipes from Inventory (`GET /api/inventory/recipes`)
Get recipe suggestions based on your current inventory.

**Special Features:**
- Expiring items alerts (7 days or less)
- Organized by storage location
- Category-based organization

---

### 5. Recipe Collections/Cookbooks

#### Create Collection (`POST /api/collections`)
Create your own recipe collections (cookbooks).

**Features:**
- Custom collection names and descriptions
- Add tags for easy organization
- Public or private collections
- Track creation and update dates

**Example Request:**
```json
POST /api/collections
{
  "name": "Weeknight Dinners",
  "description": "Quick and easy recipes for busy weeknights",
  "tags": ["quick", "easy", "dinner"],
  "is_public": false
}
```

#### Get Collections (`GET /api/collections`)
View all your recipe collections.

#### Add Recipe to Collection (`POST /api/collections/<collection_id>/recipes`)
Add recipes to your collections.

---

### 6. Cooking Challenges System

#### Create Challenge (`POST /api/challenges`)
Create personalized cooking challenges.

**Challenge Types:**
- **Weekly Recipe**: Cook new recipes each week
- **Technique Master**: Master specific cooking techniques
- **Cuisine Explorer**: Explore different cuisines
- **Healthy Eating**: Focus on healthy recipes
- **Meal Prep**: Complete meal prep challenges
- **Speed Cooking**: Quick cooking challenges

**Features:**
- Set target recipes
- Track progress percentage
- Earn rewards and badges
- Set difficulty levels
- Time-based challenges

**Example Request:**
```json
POST /api/challenges
{
  "challenge_type": "weekly_recipe",
  "title": "Mediterranean Week",
  "description": "Cook 5 Mediterranean recipes this week",
  "target_recipes": ["Greek Salad", "Hummus", "Tzatziki", "Baklava", "Moussaka"],
  "duration_days": 7,
  "difficulty": "medium"
}
```

#### Get Active Challenges (`GET /api/challenges`)
View all your active challenges.

#### Complete Challenge Recipe (`POST /api/challenges/<challenge_id>/complete`)
Mark recipes as completed in challenges.

**Rewards System:**
- Badge achievements
- Progress tracking
- Completion rewards

---

### 7. Meal Prep Planning (`/api/meal-prep/create`)
Create comprehensive meal prep plans.

**Features:**
- Batch cooking schedule
- Prep timeline with task breakdown
- Storage instructions (fridge/freezer)
- Shopping list integration
- Time estimation

**Example Request:**
```json
POST /api/meal-prep/create
{
  "recipes": [
    {"name": "Chicken Stir Fry", "servings": 4, "prep_time": "25 minutes"},
    {"name": "Greek Salad", "servings": 4, "prep_time": "15 minutes"}
  ],
  "week_start": "2026-01-09"
}
```

**Includes:**
- Batch cooking recommendations
- Step-by-step prep timeline
- Storage guidelines (temperature, duration)
- Container recommendations
- Thawing instructions

---

### 8. Cooking Statistics & Tracking

#### Track Recipe Cooked (`POST /api/stats/track-recipe`)
Track when you cook recipes.

#### Get Cooking Stats (`GET /api/stats/cooking`)
View comprehensive cooking statistics.

**Stats Include:**
- Total recipes cooked
- Favorite cuisine
- Most cooked recipe
- Cooking streak (consecutive days)
- Total cooking time
- Recent recipe history

---

## 🔧 Technical Implementation

### New Modules
- `app/advanced_features.py` - Advanced features manager
- Enhanced `app/chatbot.py` - Recipe scaling and variations
- Updated `app/routes.py` - New API endpoints

### Data Models
- `IngredientInventory` - Inventory item tracking
- `RecipeCollection` - User recipe collections
- `CookingChallenge` - Challenge/goal tracking
- `MealPrepPlan` - Meal prep planning

### Features Architecture
All advanced features are managed through the `AdvancedFeaturesManager` class, which provides:
- In-memory data storage (can be migrated to database)
- User-specific data isolation
- Comprehensive error handling
- Extensible design for future enhancements

---

## 📊 API Endpoint Summary

### Recipe Operations
- `POST /api/recipe/scale` - Scale recipe servings
- `POST /api/recipe/variations` - Get recipe variations
- `POST /api/recipe/leftover-suggestions` - Leftover ingredient recipes

### Inventory Management
- `GET /api/inventory` - Get inventory
- `POST /api/inventory/add` - Add item
- `PUT /api/inventory/update` - Update item
- `DELETE /api/inventory/remove` - Remove item
- `GET /api/inventory/recipes` - Get recipes from inventory

### Collections
- `GET /api/collections` - Get collections
- `POST /api/collections` - Create collection
- `POST /api/collections/<id>/recipes` - Add recipe

### Challenges
- `GET /api/challenges` - Get challenges
- `POST /api/challenges` - Create challenge
- `POST /api/challenges/<id>/complete` - Complete recipe

### Meal Prep
- `POST /api/meal-prep/create` - Create meal prep plan

### Statistics
- `GET /api/stats/cooking` - Get cooking stats
- `POST /api/stats/track-recipe` - Track recipe

---

## 🚀 Usage Examples

### Complete Workflow Example

1. **Add ingredients to inventory**
```bash
POST /api/inventory/add
```

2. **Get recipe suggestions from inventory**
```bash
GET /api/inventory/recipes
```

3. **Scale recipe for family size**
```bash
POST /api/recipe/scale
```

4. **Create meal prep plan**
```bash
POST /api/meal-prep/create
```

5. **Track cooking progress**
```bash
POST /api/stats/track-recipe
```

6. **View cooking statistics**
```bash
GET /api/stats/cooking
```

---

## 🎨 Future Enhancement Ideas

1. **Smart Shopping Route Optimization** - Optimize grocery shopping routes
2. **Recipe Cost Calculator** - Track recipe costs over time
3. **Nutritional Goal Tracking** - Set and track nutritional goals
4. **Social Sharing** - Share recipes and collections
5. **Recipe Video Integration** - Link to cooking videos
6. **AI-Powered Recipe Generation** - Generate new recipes from ingredients
7. **Equipment Recommendations** - Suggest kitchen tools needed
8. **Seasonal Recipe Suggestions** - Time-based recipe recommendations

---

## 📝 Notes

- All endpoints require authentication (Bearer token)
- Data is stored in-memory (can be migrated to database)
- All timestamps use ISO format
- Error responses follow consistent format
- Most endpoints support pagination

---

**Created by:** RSK World  
**Version:** 2.0.0  
**Last Updated:** 2026
