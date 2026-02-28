import { motion } from 'framer-motion'

export default function OutfitCard({ outfit, onSave, onDelete }) {
  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.9 }}
      animate={{ opacity: 1, scale: 1 }}
      whileHover={{ y: -5 }}
      className="bg-white rounded-lg overflow-hidden card-shadow"
    >
      <div className="aspect-video bg-gradient-to-br from-purple-200 to-pink-200 flex items-center justify-center">
        {outfit.image_url ? (
          <img src={outfit.image_url} alt={outfit.name} className="w-full h-full object-cover" />
        ) : (
          <div className="text-center">
            <p className="text-gray-500">No image</p>
          </div>
        )}
      </div>

      <div className="p-4">
        <h3 className="text-lg font-semibold text-gray-800 mb-2">{outfit.name}</h3>
        <p className="text-sm text-gray-600 mb-4">{outfit.description}</p>

        <div className="space-y-2 mb-4">
          <p className="text-xs text-gray-500"><strong>Occasion:</strong> {outfit.occasion}</p>
          <p className="text-xs text-gray-500"><strong>Season:</strong> {outfit.season}</p>
          <p className="text-xs text-gray-500"><strong>Colors:</strong> {outfit.colors?.join(', ')}</p>
        </div>

        <div className="flex gap-2">
          {onSave && (
            <button
              onClick={() => onSave(outfit)}
              className="flex-1 bg-gradient-to-r from-purple-600 to-pink-600 text-white py-2 rounded-lg hover:shadow-lg transition"
            >
              Save
            </button>
          )}
          {onDelete && (
            <button
              onClick={() => onDelete(outfit.id)}
              className="flex-1 bg-red-500 text-white py-2 rounded-lg hover:bg-red-600 transition"
            >
              Delete
            </button>
          )}
        </div>
      </div>
    </motion.div>
  )
}
