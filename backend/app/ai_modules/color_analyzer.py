import numpy as np
from PIL import Image
from sklearn.cluster import KMeans
import io
import base64
from anthropic import Anthropic

class ColorAnalyzer:
    """Analyze colors in images for fashion recommendations"""
    
    def __init__(self):
        self.client = Anthropic()
    
    @staticmethod
    def extract_dominant_colors(image_path_or_bytes, num_colors=5):
        """Extract dominant colors from an image"""
        try:
            if isinstance(image_path_or_bytes, bytes):
                img = Image.open(io.BytesIO(image_path_or_bytes))
            else:
                img = Image.open(image_path_or_bytes)
            
            # Resize for faster processing
            img = img.resize((100, 100))
            img = img.convert('RGB')
            
            # Convert to array
            img_array = np.array(img).reshape(-1, 3)
            
            # Cluster colors
            kmeans = KMeans(n_clusters=num_colors, random_state=42)
            kmeans.fit(img_array)
            
            # Get dominant colors
            colors = kmeans.cluster_centers_.astype(int)
            
            # Convert RGB to hex
            hex_colors = ['#{:02x}{:02x}{:02x}'.format(int(c[0]), int(c[1]), int(c[2])) for c in colors]
            
            return {
                'dominant_colors': hex_colors,
                'color_names': ColorAnalyzer._color_names(colors),
                'rgb_values': colors.tolist()
            }
        except Exception as e:
            return {'error': str(e)}
    
    @staticmethod
    def _color_names(colors):
        """Map RGB values to color names"""
        color_names = []
        for color in colors:
            r, g, b = color
            
            # Simple color naming logic
            if r > 200 and g > 200 and b > 200:
                color_names.append('White')
            elif r < 50 and g < 50 and b < 50:
                color_names.append('Black')
            elif r > g and r > b:
                color_names.append('Red/Pink')
            elif g > r and g > b:
                color_names.append('Green')
            elif b > r and b > g:
                color_names.append('Blue')
            elif r > 150 and g > 100 and b < 100:
                color_names.append('Orange/Brown')
            else:
                color_names.append('Neutral')
        
        return color_names
    
    @staticmethod
    def analyze_color_harmony(colors):
        """Analyze color harmony for styling suggestions"""
        if len(colors) < 2:
            return {'harmony': 'monochromatic'}
        
        # Simple harmony detection
        rgb_colors = [np.array(c) for c in colors]
        distances = []
        for i in range(len(rgb_colors)):
            for j in range(i+1, len(rgb_colors)):
                dist = np.linalg.norm(rgb_colors[i] - rgb_colors[j])
                distances.append(dist)
        
        avg_distance = np.mean(distances) if distances else 0
        
        if avg_distance < 50:
            harmony = 'analogous'
        elif avg_distance < 150:
            harmony = 'complementary'
        else:
            harmony = 'triadic'
        
        return {'harmony': harmony, 'avg_color_distance': float(avg_distance)}
    
    def get_ai_color_recommendations(self, color_names, user_preferences):
        """Get AI-powered color recommendations based on dominant colors"""
        try:
            prompt = f"""Given these dominant colors from an outfit image: {', '.join(color_names)}
            and user style preferences: {user_preferences}
            
            Provide:
            1. Complementary colors that would work well
            2. How these colors match the user's style
            3. Seasonal recommendations
            4. Overall styling advice
            
            Keep response concise and actionable."""
            
            message = self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=500,
                messages=[{"role": "user", "content": prompt}]
            )
            
            return {'recommendations': message.content[0].text}
        except Exception as e:
            return {'recommendations': f'Color analysis complete. Try pairing with complementary colors for best results.'}
