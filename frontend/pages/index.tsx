/*
TROOPOD LANDING PAGE PERSONALISER - FRONTEND

To run this application:

1. Navigate to the frontend directory:
   cd frontend

2. Install dependencies:
   npm install

3. Start the development server:
   npm run dev

The app will be available at http://localhost:3000

Make sure the backend is running on http://localhost:8000
*/

'use client'

import { useState } from 'react'

interface Result {
  new_h1: string
  new_subhead: string
  new_cta: string
  reasoning: string
}

export default function Home() {
  const [adImageUrl, setAdImageUrl] = useState('')
  const [landingPageUrl, setLandingPageUrl] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [result, setResult] = useState<Result | null>(null)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError(null)
    setResult(null)
    setLoading(true)

    try {
      const response = await fetch('http://localhost:8000/enhance', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          ad_image_url: adImageUrl,
          landing_page_url: landingPageUrl,
        }),
      })

      if (!response.ok) {
        const errorData = await response.json()
        throw new Error(errorData.error || 'Failed to personalize page')
      }

      const data = await response.json()
      setResult(data)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-white">
      <div className="max-w-2xl mx-auto px-6 py-12">
        {/* Header */}
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold text-gray-900 mb-2">
            Landing Page Personaliser
          </h1>
          <p className="text-gray-600">
            Transform your landing page copy with AI-powered personalization
          </p>
        </div>

        {/* Form */}
        <form onSubmit={handleSubmit} className="mb-8">
          <div className="space-y-4 mb-6">
            {/* Ad Image URL Input */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Ad Image URL
              </label>
              <input
                type="text"
                value={adImageUrl}
                onChange={(e) => setAdImageUrl(e.target.value)}
                placeholder="https://example.com/ad.jpg"
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                required
              />
            </div>

            {/* Landing Page URL Input */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Landing Page URL
              </label>
              <input
                type="text"
                value={landingPageUrl}
                onChange={(e) => setLandingPageUrl(e.target.value)}
                placeholder="https://example.com/landing"
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                required
              />
            </div>
          </div>

          {/* Submit Button */}
          <button
            type="submit"
            disabled={loading}
            className="w-full bg-blue-600 text-white font-semibold py-3 px-4 rounded-lg hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors"
          >
            {loading ? 'Analysing...' : 'Personalise'}
          </button>
        </form>

        {/* Error Message */}
        {error && (
          <div className="text-red-600 text-sm mt-4 p-4 bg-red-50 rounded-lg border border-red-200">
            {error}
          </div>
        )}

        {/* Results Section */}
        {result && (
          <div className="grid grid-cols-2 gap-4 mt-8">
            {/* New Headline */}
            <div className="bg-gray-50 p-6 rounded-lg border border-gray-200">
              <label className="text-xs font-semibold text-gray-500 uppercase tracking-wide">
                New Headline
              </label>
              <p className="text-lg font-semibold text-gray-900 mt-2">
                {result.new_h1}
              </p>
            </div>

            {/* New Subheadline */}
            <div className="bg-gray-50 p-6 rounded-lg border border-gray-200">
              <label className="text-xs font-semibold text-gray-500 uppercase tracking-wide">
                New Subheadline
              </label>
              <p className="text-lg font-semibold text-gray-900 mt-2">
                {result.new_subhead}
              </p>
            </div>

            {/* New CTA */}
            <div className="bg-gray-50 p-6 rounded-lg border border-gray-200">
              <label className="text-xs font-semibold text-gray-500 uppercase tracking-wide">
                New CTA
              </label>
              <p className="text-lg font-semibold text-gray-900 mt-2">
                {result.new_cta}
              </p>
            </div>

            {/* Reasoning */}
            <div className="bg-gray-50 p-6 rounded-lg border border-gray-200">
              <label className="text-xs font-semibold text-gray-500 uppercase tracking-wide">
                Reasoning
              </label>
              <p className="text-lg font-semibold text-gray-900 mt-2">
                {result.reasoning}
              </p>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}
