"""
Recipe Assistant Bot - Rating and Review System
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
class Review:
    """Recipe review model."""
    id: str
    recipe_name: str
    user_id: str
    username: str
    rating: int  # 1-5
    title: str
    comment: str
    pros: List[str]
    cons: List[str]
    would_make_again: bool
    difficulty_rating: int  # 1-5
    value_rating: int  # 1-5
    taste_rating: int  # 1-5
    created_date: str
    helpful_count: int
    verified_purchase: bool
    
    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return asdict(self)

@dataclass
class RecipeStats:
    """Recipe statistics."""
    recipe_name: str
    total_reviews: int
    average_rating: float
    rating_distribution: Dict[int, int]  # rating -> count
    average_difficulty: float
    average_value: float
    average_taste: float
    would_make_again_percentage: float
    verified_purchase_percentage: float
    top_pros: List[str]
    top_cons: List[str]
    
    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return asdict(self)

class RatingReviewManager:
    """Manages recipe ratings and reviews."""
    
    def __init__(self):
        """Initialize rating and review manager."""
        self.reviews = {}  # review_id -> review
        self.recipe_reviews = defaultdict(list)  # recipe_name -> list of review_ids
        self.user_reviews = defaultdict(list)  # user_id -> list of review_ids
        self.helpful_votes = defaultdict(set)  # review_id -> set of user_ids who voted
        self.recipe_stats = {}  # recipe_name -> RecipeStats
    
    def add_review(self, recipe_name: str, user_id: str, username: str,
                  rating: int, title: str, comment: str, pros: List[str] = None,
                  cons: List[str] = None, would_make_again: bool = True,
                  difficulty_rating: int = 3, value_rating: int = 3,
                  taste_rating: int = 3, verified_purchase: bool = False) -> Dict:
        """Add a new review for a recipe."""
        
        # Validate rating
        if not (1 <= rating <= 5):
            return {'error': 'Rating must be between 1 and 5'}
        
        # Check if user already reviewed this recipe
        user_review_ids = self.user_reviews.get(user_id, [])
        for review_id in user_review_ids:
            review = self.reviews.get(review_id)
            if review and review.recipe_name == recipe_name:
                return {'error': 'You have already reviewed this recipe'}
        
        # Create review
        review_id = f"review_{len(self.reviews) + 1}"
        review = Review(
            id=review_id,
            recipe_name=recipe_name,
            user_id=user_id,
            username=username,
            rating=rating,
            title=title,
            comment=comment,
            pros=pros or [],
            cons=cons or [],
            would_make_again=would_make_again,
            difficulty_rating=difficulty_rating,
            value_rating=value_rating,
            taste_rating=taste_rating,
            created_date=datetime.datetime.now().isoformat(),
            helpful_count=0,
            verified_purchase=verified_purchase
        )
        
        # Store review
        self.reviews[review_id] = review
        self.recipe_reviews[recipe_name].append(review_id)
        self.user_reviews[user_id].append(review_id)
        
        # Update recipe statistics
        self._update_recipe_stats(recipe_name)
        
        return {
            'review_id': review_id,
            'message': 'Review added successfully',
            'recipe_stats': self.recipe_stats.get(recipe_name)
        }
    
    def update_review(self, review_id: str, user_id: str, updates: Dict) -> Dict:
        """Update an existing review."""
        review = self.reviews.get(review_id)
        
        if not review:
            return {'error': 'Review not found'}
        
        if review.user_id != user_id:
            return {'error': 'You can only update your own reviews'}
        
        # Update allowed fields
        allowed_fields = [
            'rating', 'title', 'comment', 'pros', 'cons', 
            'would_make_again', 'difficulty_rating', 'value_rating', 'taste_rating'
        ]
        
        for field, value in updates.items():
            if field in allowed_fields:
                setattr(review, field, value)
        
        # Update recipe statistics
        self._update_recipe_stats(review.recipe_name)
        
        return {
            'review_id': review_id,
            'message': 'Review updated successfully',
            'recipe_stats': self.recipe_stats.get(review.recipe_name)
        }
    
    def delete_review(self, review_id: str, user_id: str) -> Dict:
        """Delete a review."""
        review = self.reviews.get(review_id)
        
        if not review:
            return {'error': 'Review not found'}
        
        if review.user_id != user_id:
            return {'error': 'You can only delete your own reviews'}
        
        # Remove from all data structures
        recipe_name = review.recipe_name
        
        del self.reviews[review_id]
        self.recipe_reviews[recipe_name].remove(review_id)
        self.user_reviews[user_id].remove(review_id)
        
        # Remove helpful votes
        if review_id in self.helpful_votes:
            del self.helpful_votes[review_id]
        
        # Update recipe statistics
        self._update_recipe_stats(recipe_name)
        
        return {
            'message': 'Review deleted successfully',
            'recipe_stats': self.recipe_stats.get(recipe_name)
        }
    
    def get_recipe_reviews(self, recipe_name: str, sort_by: str = 'newest',
                         page: int = 1, per_page: int = 10) -> Dict:
        """Get reviews for a recipe."""
        review_ids = self.recipe_reviews.get(recipe_name, [])
        
        if not review_ids:
            return {
                'reviews': [],
                'total_count': 0,
                'page': page,
                'per_page': per_page,
                'total_pages': 0
            }
        
        # Get reviews
        reviews = [self.reviews[rid] for rid in review_ids]
        
        # Sort reviews
        if sort_by == 'newest':
            reviews.sort(key=lambda x: x.created_date, reverse=True)
        elif sort_by == 'oldest':
            reviews.sort(key=lambda x: x.created_date)
        elif sort_by == 'highest_rating':
            reviews.sort(key=lambda x: x.rating, reverse=True)
        elif sort_by == 'lowest_rating':
            reviews.sort(key=lambda x: x.rating)
        elif sort_by == 'most_helpful':
            reviews.sort(key=lambda x: x.helpful_count, reverse=True)
        
        # Paginate
        total_count = len(reviews)
        total_pages = (total_count + per_page - 1) // per_page
        start_idx = (page - 1) * per_page
        end_idx = start_idx + per_page
        
        paginated_reviews = reviews[start_idx:end_idx]
        
        return {
            'reviews': [review.to_dict() for review in paginated_reviews],
            'total_count': total_count,
            'page': page,
            'per_page': per_page,
            'total_pages': total_pages
        }
    
    def get_user_reviews(self, user_id: str, page: int = 1, per_page: int = 10) -> Dict:
        """Get reviews by a user."""
        review_ids = self.user_reviews.get(user_id, [])
        
        if not review_ids:
            return {
                'reviews': [],
                'total_count': 0,
                'page': page,
                'per_page': per_page,
                'total_pages': 0
            }
        
        # Get reviews
        reviews = [self.reviews[rid] for rid in review_ids]
        reviews.sort(key=lambda x: x.created_date, reverse=True)
        
        # Paginate
        total_count = len(reviews)
        total_pages = (total_count + per_page - 1) // per_page
        start_idx = (page - 1) * per_page
        end_idx = start_idx + per_page
        
        paginated_reviews = reviews[start_idx:end_idx]
        
        return {
            'reviews': [review.to_dict() for review in paginated_reviews],
            'total_count': total_count,
            'page': page,
            'per_page': per_page,
            'total_pages': total_pages
        }
    
    def mark_review_helpful(self, review_id: str, user_id: str) -> Dict:
        """Mark a review as helpful."""
        review = self.reviews.get(review_id)
        
        if not review:
            return {'error': 'Review not found'}
        
        if review.user_id == user_id:
            return {'error': 'You cannot mark your own review as helpful'}
        
        # Toggle helpful vote
        if user_id in self.helpful_votes[review_id]:
            self.helpful_votes[review_id].remove(user_id)
            review.helpful_count -= 1
            action = 'removed'
        else:
            self.helpful_votes[review_id].add(user_id)
            review.helpful_count += 1
            action = 'added'
        
        return {
            'review_id': review_id,
            'helpful_count': review.helpful_count,
            'action': action,
            'message': f'Helpful vote {action} successfully'
        }
    
    def get_recipe_stats(self, recipe_name: str) -> Optional[RecipeStats]:
        """Get statistics for a recipe."""
        return self.recipe_stats.get(recipe_name)
    
    def get_top_recipes(self, limit: int = 10, min_reviews: int = 5) -> List[Dict]:
        """Get top rated recipes."""
        qualified_recipes = [
            (recipe_name, stats) for recipe_name, stats in self.recipe_stats.items()
            if stats.total_reviews >= min_reviews
        ]
        
        # Sort by average rating
        qualified_recipes.sort(key=lambda x: x[1].average_rating, reverse=True)
        
        return [
            {
                'recipe_name': recipe_name,
                'stats': stats.to_dict()
            }
            for recipe_name, stats in qualified_recipes[:limit]
        ]
    
    def get_user_rating_summary(self, user_id: str) -> Dict:
        """Get user's rating summary."""
        review_ids = self.user_reviews.get(user_id, [])
        
        if not review_ids:
            return {
                'total_reviews': 0,
                'average_rating': 0,
                'rating_distribution': {},
                'most_reviewed_recipes': []
            }
        
        reviews = [self.reviews[rid] for rid in review_ids]
        
        # Calculate statistics
        total_reviews = len(reviews)
        average_rating = sum(review.rating for review in reviews) / total_reviews
        
        # Rating distribution
        rating_distribution = defaultdict(int)
        for review in reviews:
            rating_distribution[review.rating] += 1
        
        # Most reviewed recipes
        recipe_counts = defaultdict(int)
        for review in reviews:
            recipe_counts[review.recipe_name] += 1
        
        most_reviewed = sorted(
            recipe_counts.items(), 
            key=lambda x: x[1], 
            reverse=True
        )[:5]
        
        return {
            'total_reviews': total_reviews,
            'average_rating': round(average_rating, 1),
            'rating_distribution': dict(rating_distribution),
            'most_reviewed_recipes': [
                {'recipe_name': recipe, 'review_count': count}
                for recipe, count in most_reviewed
            ]
        }
    
    def _update_recipe_stats(self, recipe_name: str) -> None:
        """Update statistics for a recipe."""
        review_ids = self.recipe_reviews.get(recipe_name, [])
        
        if not review_ids:
            return
        
        reviews = [self.reviews[rid] for rid in review_ids]
        
        # Calculate basic statistics
        total_reviews = len(reviews)
        average_rating = sum(review.rating for review in reviews) / total_reviews
        
        # Rating distribution
        rating_distribution = defaultdict(int)
        for review in reviews:
            rating_distribution[review.rating] += 1
        
        # Average sub-ratings
        average_difficulty = sum(review.difficulty_rating for review in reviews) / total_reviews
        average_value = sum(review.value_rating for review in reviews) / total_reviews
        average_taste = sum(review.taste_rating for review in reviews) / total_reviews
        
        # Would make again percentage
        would_make_again_count = sum(1 for review in reviews if review.would_make_again)
        would_make_again_percentage = (would_make_again_count / total_reviews) * 100
        
        # Verified purchase percentage
        verified_count = sum(1 for review in reviews if review.verified_purchase)
        verified_purchase_percentage = (verified_count / total_reviews) * 100
        
        # Top pros and cons
        all_pros = []
        all_cons = []
        
        for review in reviews:
            all_pros.extend(review.pros)
            all_cons.extend(review.cons)
        
        # Count frequency of pros and cons
        pro_counts = defaultdict(int)
        con_counts = defaultdict(int)
        
        for pro in all_pros:
            pro_counts[pro] += 1
        
        for con in all_cons:
            con_counts[con] += 1
        
        # Get top 5 pros and cons
        top_pros = sorted(pro_counts.items(), key=lambda x: x[1], reverse=True)[:5]
        top_cons = sorted(con_counts.items(), key=lambda x: x[1], reverse=True)[:5]
        
        # Create stats object
        stats = RecipeStats(
            recipe_name=recipe_name,
            total_reviews=total_reviews,
            average_rating=round(average_rating, 1),
            rating_distribution=dict(rating_distribution),
            average_difficulty=round(average_difficulty, 1),
            average_value=round(average_value, 1),
            average_taste=round(average_taste, 1),
            would_make_again_percentage=round(would_make_again_percentage, 1),
            verified_purchase_percentage=round(verified_purchase_percentage, 1),
            top_pros=[pro for pro, count in top_pros],
            top_cons=[con for con, count in top_cons]
        )
        
        self.recipe_stats[recipe_name] = stats
    
    def search_reviews(self, query: str, recipe_name: str = None, 
                    rating_filter: int = None, page: int = 1, 
                    per_page: int = 10) -> Dict:
        """Search reviews."""
        query_lower = query.lower()
        matching_reviews = []
        
        for review in self.reviews.values():
            # Filter by recipe name if specified
            if recipe_name and review.recipe_name != recipe_name:
                continue
            
            # Filter by rating if specified
            if rating_filter and review.rating != rating_filter:
                continue
            
            # Search in title, comment, pros, and cons
            searchable_text = f"{review.title} {review.comment} {' '.join(review.pros)} {' '.join(review.cons)}"
            
            if query_lower in searchable_text.lower():
                matching_reviews.append(review)
        
        # Sort by newest
        matching_reviews.sort(key=lambda x: x.created_date, reverse=True)
        
        # Paginate
        total_count = len(matching_reviews)
        total_pages = (total_count + per_page - 1) // per_page
        start_idx = (page - 1) * per_page
        end_idx = start_idx + per_page
        
        paginated_reviews = matching_reviews[start_idx:end_idx]
        
        return {
            'reviews': [review.to_dict() for review in paginated_reviews],
            'total_count': total_count,
            'page': page,
            'per_page': per_page,
            'total_pages': total_pages,
            'query': query,
            'recipe_name': recipe_name,
            'rating_filter': rating_filter
        }
