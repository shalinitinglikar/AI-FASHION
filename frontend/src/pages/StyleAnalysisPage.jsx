import { useState } from 'react'
import { motion } from 'framer-motion'
import ImageUploader from '../components/ImageUploader'
import { apiService } from '../services/api'

export default function StyleAnalysisPage() {
  const [analysis, setAnalysis] = useState(null)
  const [loading, setLoading] = useState(false)

  const handleImageAnalyzed = async (data) => {
    setLoading(true)
    try {
      setAnalysis(data)
    } catch (error) {
      console.error('Failed to analyze image:', error)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="space-y-8">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="bg-gradient-to-r from-purple-600 to-pink-600 text-white rounded-lg p-8"
      >
        <h1 className="text-4xl font-bold mb-2">Style Analysis</h1>
        <p className="text-lg opacity-90">Upload an image to get instant AI-powered style insights</p>
      </motion.div>

      <div className="grid md:grid-cols-2 gap-8">
        {/* Upload Section */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="bg-white rounded-lg card-shadow p-8"
        >
          <h2 className="text-2xl font-bold text-gray-900 mb-6">Upload Your Image</h2>
          <ImageUploader
            onImageAnalyzed={handleImageAnalyzed}
            label="Upload a photo of yourself or an outfit"
          />
        </motion.div>

        {/* Analysis Results */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="bg-white rounded-lg card-shadow p-8"
        >
          <h2 className="text-2xl font-bold text-gray-900 mb-6">Analysis Results</h2>
          {loading ? (
            <p className="text-center text-gray-600">Analyzing your style...</p>
          ) : analysis ? (
            <div className="space-y-6">
              {analysis.dominant_colors && (
                <div>
                  <h3 className="font-semibold text-gray-800 mb-3">Dominant Colors</h3>
                  <div className="flex gap-2 flex-wrap">
                    {analysis.dominant_colors.map((color, idx) => (
                      <div
                        key={idx}
                        className="px-4 py-2 rounded-lg bg-gray-100 text-gray-800 text-sm"
                      >
                        {color}
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {analysis.style_suggestions && (
                <div>
                  <h3 className="font-semibold text-gray-800 mb-3">Style Suggestions</h3>
                  <ul className="space-y-2">
                    {analysis.style_suggestions.map((suggestion, idx) => (
                      <li key={idx} className="text-gray-700 flex items-start">
                        <span className="text-purple-600 mr-3">✓</span>
                        {suggestion}
                      </li>
                    ))}
                  </ul>
                </div>
              )}

              {analysis.body_shape_analysis && (
                <div>
                  <h3 className="font-semibold text-gray-800 mb-3">Body Shape Analysis</h3>
                  <p className="text-gray-700">{analysis.body_shape_analysis}</p>
                </div>
              )}

              {analysis.recommendations && (
                <div>
                  <h3 className="font-semibold text-gray-800 mb-3">Personalized Recommendations</h3>
                  <p className="text-gray-700">{analysis.recommendations}</p>
                </div>
              )}
            </div>
          ) : (
            <p className="text-center text-gray-600">Upload an image to see analysis results</p>
          )}
        </motion.div>
      </div>
    </div>
  )
}
