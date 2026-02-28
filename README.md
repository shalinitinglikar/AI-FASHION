# AI-FASHION: Generative AI Fashion Recommendation Platform

A comprehensive AI-powered fashion recommendation platform that provides personalized styling advice, outfit suggestions, image-based analysis, trend-aware insights, and an interactive UI.

## 🌟 Features

### Personalized Styling Advice
- Tailored recommendations based on user preferences, body type, and climate
- Expert styling tips for different occasions and seasons
- Color analysis and fashion trend insights

### Outfit Recommendations
- Smart outfit suggestions based on style preferences
- Occasion-based recommendations (casual, formal, business, party, gym)
- Season-aware outfit curation
- Save and manage favorite outfits

### Image-Based Analysis
- Upload photos for instant AI analysis
- Color dominance detection
- Body shape analysis
- Style suggestions based on uploaded images
- Clothing item identification

### Trend-Aware Suggestions
- Stay updated with the latest fashion trends
- AI-generated recommendations aligned with current trends
- Personalized trend insights based on user preferences

### Interactive UI
- Beautiful, responsive React frontend
- Smooth animations and transitions
- Real-time image analysis
- Intuitive user dashboard
- Profile management

## 🏗️ Architecture

### Backend
- **Framework**: Flask with SQLAlchemy ORM
- **Authentication**: JWT-based auth
- **Database**: SQLite (development)
- **AI Integration**: Claude API for intelligent recommendations
- **Image Processing**: OpenCV and PIL

### Frontend
- **Framework**: React 18 with Vite
- **State Management**: Zustand
- **Styling**: Tailwind CSS
- **Animations**: Framer Motion
- **HTTP Client**: Axios

## 📁 Project Structure

```
AI-FASHION/
├── backend/
│   ├── run.py                 # Flask app entry point
│   ├── requirements.txt       # Python dependencies
│   └── app/
│       ├── __init__.py        # Flask app factory
│       ├── models/            # Database models
│       │   ├── user.py
│       │   ├── recommendation.py
│       │   ├── saved_outfit.py
│       │   └── style_image.py
│       ├── routes/            # API endpoints
│       │   ├── auth_routes.py
│       │   ├── recommendation_routes.py
│       │   ├── user_routes.py
│       │   └── image_routes.py
│       └── ai_modules/        # AI processing
│           ├── color_analyzer.py
│           ├── image_analyzer.py
│           └── recommendation_engine.py
│
└── frontend/
	├── index.html
	├── package.json
	├── vite.config.js
	├── tailwind.config.js
	└── src/
		├── main.jsx
		├── App.jsx
		├── index.css
		├── components/
		│   ├── Layout.jsx
		│   ├── ImageUploader.jsx
		│   └── OutfitCard.jsx
		├── pages/
		│   ├── HomePage.jsx
		│   ├── LoginPage.jsx
		│   ├── RegisterPage.jsx
		│   ├── DashboardPage.jsx
		│   ├── RecommendationsPage.jsx
		│   ├── StyleAnalysisPage.jsx
		│   └── ProfilePage.jsx
		├── services/
		│   └── api.js
		└── store/
			└── authStore.js
```

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- Node.js 16+
- npm or yarn

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env and add your Anthropic API key
```

4. Run the Flask server:
```bash
python run.py
```

The backend will be available at `http://localhost:5000`

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install Node dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm run dev
```

The frontend will be available at `http://localhost:3000`

## 📚 API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login user

### User Profile
- `GET /api/users/profile` - Get user profile
- `PUT /api/users/profile` - Update user profile
- `PUT /api/users/preferences` - Update style preferences
- `GET /api/users/outfits` - Get saved outfits

### Recommendations
- `GET /api/recommendations` - Get outfit recommendations
- `POST /api/recommendations/generate` - Generate new recommendations

### Image Analysis
- `POST /api/images/analyze` - Analyze uploaded image
- `POST /api/images/upload-style` - Upload style reference image

## 🤖 AI Features

### Color Analyzer
- Analyzes dominant colors in images
- Suggests complementary color palettes
- Identifies seasonal color trends

### Image Analyzer
- Detects clothing items and styles
- Analyzes fit and styling
- Provides styling recommendations

### Recommendation Engine
- Generates personalized outfit suggestions
- Considers user preferences and body type
- Adapts recommendations based on occasion and season

## 🔐 Security

- JWT-based authentication
- Password hashing with SHA-256
- CORS enabled for frontend-backend communication
- Environment variables for sensitive data

## 🎨 Customization

### Adding New Style Preferences
Edit the style preferences in `RegisterPage.jsx` and the database model `User` in `user.py`

### Modifying Recommendation Logic
Update the recommendation engine in `backend/app/ai_modules/recommendation_engine.py`

### Styling Changes
Customize colors and styles in:
- `frontend/tailwind.config.js` - Color schemes
- `frontend/src/index.css` - Global styles

## 📦 Dependencies

### Backend
- Flask 3.0.0
- Flask-CORS 4.0.0
- Flask-SQLAlchemy 3.1.1
- Flask-JWT-Extended 4.5.3
- Pillow 12.1.0+
- numpy 2.3.0+
- opencv-python-headless
- scikit-learn
- anthropic

### Frontend
- react 18.2.0
- react-router-dom 6.20.0
- axios 1.6.2
- zustand 4.4.0
- tailwindcss 3.4.0
- framer-motion 10.16.0

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Troubleshooting

### Backend won't start
- Check if port 5000 is available
- Ensure all dependencies are installed: `pip install -r requirements.txt`
- Check environment variables in `.env`

### Frontend won't connect to backend
- Ensure backend is running on `http://localhost:5000`
- Check CORS configuration in `backend/app/__init__.py`
- Clear browser cache and restart dev server

### Images not uploading
- Check file size limits
- Ensure proper file format (JPEG, PNG, GIF)
- Check backend file upload configuration

## 📞 Support

For issues and questions, please create an issue in the repository.

---

**Built with ❤️ using Flask, React, and Claude AI**