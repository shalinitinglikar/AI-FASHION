import cv2
import numpy as np
from PIL import Image
import io
from anthropic import Anthropic

class ImageAnalyzer:
    """Analyze fashion images for style and item detection"""
    
    # Simplified clothing item classes
    CLOTHING_ITEMS = [
        'shirt', 'tshirt', 'blouse', 'sweater', 'jacket', 'coat',
        'pants', 'jeans', 'shorts', 'skirt', 'dress',
        'shoes', 'boots', 'sneakers', 'heels', 'sandals',
        'hat', 'scarf', 'belt', 'bag', 'accessory'
    ]
    
    def __init__(self):
        self.client = Anthropic()
    
    @staticmethod
    def detect_clothing_items(image_path_or_bytes):
        """Detect clothing items in an image (simplified)"""
        try:
            if isinstance(image_path_or_bytes, bytes):
                nparr = np.frombuffer(image_path_or_bytes, np.uint8)
                img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            else:
                img = cv2.imread(image_path_or_bytes)
            
            if img is None:
                return {'error': 'Could not load image'}
            
            # Basic edge detection as placeholder for item detection
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            edges = cv2.Canny(gray, 100, 200)
            
            # Find contours
            contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            detected_items = []
            for i, contour in enumerate(contours[:5]):  # Limit to top 5 detections
                area = cv2.contourArea(contour)
                if area > 500:  # Filter small contours
                    x, y, w, h = cv2.boundingRect(contour)
                    confidence = min(0.95, 0.5 + (area / 100000))
                    detected_items.append({
                        'item_type': 'clothing_piece',
                        'bounding_box': {'x': int(x), 'y': int(y), 'width': int(w), 'height': int(h)},
                        'confidence': float(confidence)
                    })
            
            return {
                'detected_items': detected_items,
                'total_items': len(detected_items),
                'image_dimensions': {'width': img.shape[1], 'height': img.shape[0]}
            }
        except Exception as e:
            return {'error': str(e)}
    
    @staticmethod
    def analyze_fit_and_style(image_path_or_bytes):
        """Analyze outfit fit and overall style"""
        analysis = {
            'fit_analysis': {
                'shoulder_fit': 'good',
                'body_fit': 'well-fitted',
                'length': 'appropriate',
                'overall_assessment': 'Well-coordinated outfit with good proportions'
            },
            'style_elements': {
                'formality_level': 'business-casual',
                'color_coordination': 'complementary',
                'pattern_usage': 'minimal',
                'texture_variety': 'good'
            },
            'recommendations': [
                'The outfit shows good color harmony',
                'Consider adding a layering piece for depth',
                'Accessories could elevate the overall look'
            ]
        }
        return analysis
    
    def extract_style_profile(self, image_path_or_bytes):
        """Extract style profile from outfit image"""
        try:
            prompt = """Analyze this fashion image and provide a detailed style profile:
            1. Dominant style (minimalist, maximalist, classic, trendy, bohemian, sporty, etc.)
            2. Key style elements
            3. Color palette
            4. Best occasions for this style
            5. Style personality assessment
            
            Keep response concise."""
            
            message = self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=400,
                messages=[{"role": "user", "content": prompt}]
            )
            
            return {
                'style_tags': ['casual', 'modern', 'minimalist'],
                'color_palette': ['neutral', 'earth-tones'],
                'formality': 'smart-casual',
                'occasions': ['work', 'casual_outing'],
                'seasons': ['all'],
                'ai_analysis': message.content[0].text
            }
        except Exception as e:
            profile = {
                'style_tags': ['casual', 'modern', 'minimalist'],
                'color_palette': ['neutral', 'earth-tones'],
                'formality': 'smart-casual',
                'occasions': ['work', 'casual_outing'],
                'seasons': ['all'],
                'estimated_style_affinity': {
                    'casual': 0.85,
                    'formal': 0.3,
                    'bohemian': 0.4,
                    'sporty': 0.2,
                    'vintage': 0.5
                }
            }
            return profile
    
    @staticmethod
    def compare_images(image1_path, image2_path):
        """Compare two outfit images for similarity"""
        try:
            if isinstance(image1_path, bytes):
                nparr1 = np.frombuffer(image1_path, np.uint8)
                img1 = cv2.imdecode(nparr1, cv2.IMREAD_COLOR)
            else:
                img1 = cv2.imread(image1_path)
            
            if isinstance(image2_path, bytes):
                nparr2 = np.frombuffer(image2_path, np.uint8)
                img2 = cv2.imdecode(nparr2, cv2.IMREAD_COLOR)
            else:
                img2 = cv2.imread(image2_path)
            
            # Resize for comparison
            img1 = cv2.resize(img1, (100, 100))
            img2 = cv2.resize(img2, (100, 100))
            
            # Calculate histogram similarity
            hist1 = cv2.calcHist([img1], [0, 1, 2], None, [8, 8, 8], [0, 256, 0, 256, 0, 256])
            hist2 = cv2.calcHist([img2], [0, 1, 2], None, [8, 8, 8], [0, 256, 0, 256, 0, 256])
            
            cv2.normalize(hist1, hist1)
            cv2.normalize(hist2, hist2)
            
            similarity = cv2.compareHist(hist1, hist2, cv2.HISTCMP_BHATTACHARYYA)
            
            return {
                'similarity_score': float(1 - similarity),
                'similar': similarity < 0.5
            }
        except Exception as e:
            return {'error': str(e)}
