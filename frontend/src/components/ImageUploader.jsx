import { useState } from 'react'
import { useDropzone } from 'react-dropzone'
import { motion } from 'framer-motion'
import { apiService } from '../services/api'

export default function ImageUploader({ onImageAnalyzed, label = 'Upload Image' }) {
  const [preview, setPreview] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const onDrop = async (acceptedFiles) => {
    if (acceptedFiles.length === 0) return

    const file = acceptedFiles[0]
    const reader = new FileReader()

    reader.onload = () => {
      setPreview(reader.result)
    }

    reader.readAsDataURL(file)

    // Upload and analyze image
    const formData = new FormData()
    formData.append('image', file)

    setLoading(true)
    setError(null)

    try {
      const response = await apiService.analyzeImage(formData)
      onImageAnalyzed(response.data)
    } catch (err) {
      setError('Failed to analyze image. Please try again.')
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: { 'image/*': ['.jpeg', '.jpg', '.png', '.gif'] }
  })

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="w-full"
    >
      <div
        {...getRootProps()}
        className={`border-2 border-dashed rounded-lg p-8 text-center cursor-pointer transition ${
          isDragActive
            ? 'border-purple-600 bg-purple-50'
            : 'border-gray-300 hover:border-purple-400'
        }`}
      >
        <input {...getInputProps()} />
        {preview ? (
          <div className="space-y-4">
            <img src={preview} alt="preview" className="max-h-64 mx-auto rounded-lg" />
            <p className="text-sm text-gray-600">{isDragActive ? 'Drop the image here' : 'Click or drag another image'}</p>
          </div>
        ) : (
          <div>
            <p className="text-lg font-semibold text-gray-700">{label}</p>
            <p className="text-sm text-gray-600 mt-2">
              {isDragActive
                ? 'Drop the image here'
                : 'Drag and drop your image here, or click to select'}
            </p>
          </div>
        )}
      </div>
      {loading && <p className="text-center mt-4 text-purple-600">Analyzing image...</p>}
      {error && <p className="text-center mt-4 text-red-600">{error}</p>}
    </motion.div>
  )
}
