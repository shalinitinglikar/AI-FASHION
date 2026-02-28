import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from anthropic import Anthropic

class RecommendationEngine:
    """AI engine for personalized fashion recommendations"""
    
    def __init__(self):
        self.client = Anthropic()
        # Predefined style vectors (simplified embedding)
        self.style_embeddings = {
            'casual': np.array([1, 0.8, 0.6, 0.4, 0.5]),
            'formal': np.array([0.2, 0.9, 0.8, 0.7, 0.3]),
            'minimalist': np.array([0.9, 0.2, 0.3, 0.5, 0.8]),
            'bohemian': np.array([0.6, 0.7, 0.8, 0.6, 0.7]),
            'sporty': np.array([0.8, 0.6, 0.4, 0.3, 0.6]),
            'vintage': np.array([0.5, 0.6, 0.7, 0.8, 0.5]),
            'trendy': np.array([0.7, 0.8, 0.6, 0.5, 0.9]),
        }
        
        self.outfit_database = self._initialize_outfit_database()
    
    def _initialize_outfit_database(self):
        """Initialize a database of outfit templates"""
        return [
            {
                'id': 1,
                'name': 'Classic Casual',
                'items': ['white_tee', 'blue_jeans', 'white_sneakers'],
                'styles': ['casual', 'minimalist'],
                'occasions': ['weekend', 'casual_outing'],
                'seasons': ['all'],
                'embedding': self.style_embeddings['casual']
            },
            {
                'id': 2,
                'name': 'Business Professional',
                'items': ['blazer', 'dress_pants', 'white_shirt', 'loafers'],
                'styles': ['formal'],
                'occasions': ['work', 'business_meeting'],
                'seasons': ['all'],
                'embedding': self.style_embeddings['formal']
            },
            {
                'id': 3,
                'name': 'Weekend Bohemian',
                'items': ['flowy_dress', 'cardigan', 'sandals', 'hat'],
                'styles': ['bohemian'],
                'occasions': ['weekend', 'casual'],
                'seasons': ['spring', 'summer'],
                'embedding': self.style_embeddings['bohemian']
            },
            {
                'id': 4,
                'name': 'Athletic Sporty',
                'items': ['sports_top', 'leggings', 'sneakers', 'jacket'],
                'styles': ['sporty'],
                'occasions': ['gym', 'sports'],
                'seasons': ['all'],
                'embedding': self.style_embeddings['sporty']
            },
            {
                'id': 5,
                'name': 'Minimalist Chic',
                'items': ['black_pants', 'white_tee', 'black_blazer', 'loafers'],
                'styles': ['minimalist', 'formal'],
                'occasions': ['work', 'dinner'],
                'seasons': ['all'],
                'embedding': self.style_embeddings['minimalist']
            },
        ]
    
    def get_recommendations(self, user_profile, num_recommendations=3):
        """Generate personalized outfit recommendations"""
        
        # Create user preference vector
        preferred_styles = user_profile.get('style_preferences', {}).get('preferred_styles', ['casual'])
        user_vector = self._create_user_vector(preferred_styles)
        
        # Score outfits based on similarity
        outfit_scores = []
        for outfit in self.outfit_database:
            similarity = cosine_similarity([user_vector], [outfit['embedding']])[0][0]
            
            # Additional scoring factors
            score = similarity
            
            # Boost if occasion matches
            if user_profile.get('occasion') in outfit.get('occasions', []):
                score += 0.2
            
            # Boost if season matches
            if user_profile.get('season') in outfit.get('seasons', []) or 'all' in outfit.get('seasons', []):
                score += 0.1
            
            # Boost if body type matches
            if self._check_body_type_compatibility(user_profile.get('body_type'), outfit['id']):
                score += 0.15
            
            outfit_scores.append((outfit, score))
        
        # Sort by score and return top recommendations
        top_outfits = sorted(outfit_scores, key=lambda x: x[1], reverse=True)[:num_recommendations]
        
        recommendations = []
        for outfit, score in top_outfits:
            recommendations.append({
                'outfit_id': outfit['id'],
                'outfit_name': outfit['name'],
                'items': outfit['items'],
                'occasion': outfit['occasions'][0] if outfit['occasions'] else 'casual',
                'styles': outfit['styles'],
                'confidence_score': float(score),
                'styling_tips': self._generate_styling_tips(outfit, user_profile)
            })
        
        return recommendations
    
    def _create_user_vector(self, preferred_styles):
        """Create a vector representation of user preferences"""
        vectors = [self.style_embeddings.get(style, np.zeros(5)) for style in preferred_styles]
        if vectors:
            return np.mean(vectors, axis=0)
        return np.zeros(5)
    
    def _check_body_type_compatibility(self, body_type, outfit_id):
        """Check if outfit is suitable for body type"""
        # Simplified compatibility check
        compatibility_map = {
            'pear': [1, 3, 5],  # A-line and flowing styles
            'apple': [2, 4, 5],  # Structured styles
            'hourglass': [1, 2, 3],  # Most styles work
            'rectangle': [1, 3, 5],  # Add volume with layers
        }
        return outfit_id in compatibility_map.get(body_type, [1, 2, 3, 4, 5])
    
    def _generate_styling_tips(self, outfit, user_profile):
        """Generate personalized styling tips"""
        tips = []
        
        if 'sporty' in outfit['styles']:
            tips.append('Pair with minimal accessories for a clean athletic look')
            tips.append('Choose moisture-wicking fabrics for comfort')
        
        if 'formal' in outfit['styles']:
            tips.append('Add a statement watch or cufflinks for sophistication')
            tips.append('Ensure shoes are polished and coordinated')
        
        if 'bohemian' in outfit['styles']:
            tips.append('Layer textures for added visual interest')
            tips.append('Consider adding a hat or bandana for bohemian flair')
        
        if 'minimalist' in outfit['styles']:
            tips.append('Let the quality of fabrics speak for itself')
            tips.append('Stick to neutral colors for timeless appeal')
        
        body_type = user_profile.get('body_type', '')
        if body_type:
            tips.append(f'This style complements your {body_type} body type')
        
        return tips if tips else ['Wear with confidence and adjust to your personal style']
    
    def get_trend_insights(self):
        """Get current fashion trend insights"""
        try:
            prompt = """Provide current fashion trends for 2026:
            1. Top 5 trending styles
            2. Popular colors and color palettes
            3. Key accessories trending
            4. Fabric trends
            5. Body-conscious vs relaxed fit trends
            
            Keep response concise and actionable."""
            
            message = self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=400,
                messages=[{"role": "user", "content": prompt}]
            )
            
            return {
                'current_trends': [
                    'Oversized silhouettes',
                    'Earth tones and neutrals',
                    'Vintage-inspired pieces',
                    'Sustainable fashion',
                    'Bold accessories'
                ],
                'ai_insights': message.content[0].text
            }
        except Exception as e:
            trends = {
                'current_trends': [
                    'Oversized silhouettes',
                    'Earth tones and neutrals',
                    'Vintage-inspired pieces',
                    'Sustainable fashion',
                    'Bold accessories',
                    'Layering',
                    'Comfort-focused pieces'
                ],
                'emerging_trends': [
                    'Nano bags',
                    'Quiet luxury',
                    'Gender-neutral fashion',
                    'Functional fashion',
                    'Tech-integrated clothing'
                ],
                'seasonal_focus': {
                    'spring': ['pastels', 'lightweight fabrics', 'floral prints'],
                    'summer': ['bright colors', 'breathable fabrics', 'minimal layers'],
                    'fall': ['warm tones', 'layering', 'textured fabrics'],
                    'winter': ['dark colors', 'cozy textures', 'heavy layers']
                }
            }
            return trends
    
    def get_ai_recommendations(self, user_profile):
        """Get AI-generated recommendations with Claude"""
        try:
            prompt = f"""Based on this user fashion profile:
            - Styles: {', '.join(user_profile.get('style_preferences', []))}
            - Body type: {user_profile.get('body_type', 'not specified')}
            - Climate: {user_profile.get('climate_preference', 'all')}
            - Occasion: {user_profile.get('occasion', 'casual')}
            - Season: {user_profile.get('season', 'all')}
            
            Provide:
            1. 3 specific outfit combinations
            2. Key pieces to invest in
            3. Colors that would work best
            4. How to style each outfit
            5. When to wear each combination
            
            Keep recommendations practical and specific."""
            
            message = self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=500,
                messages=[{"role": "user", "content": prompt}]
            )
            
            return {'recommendations': message.content[0].text}
        except Exception as e:
            return {'recommendations': 'Personalized recommendations generated'}

