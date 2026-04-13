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

import { useState, useEffect } from 'react'

interface Result {
  original_h1: string
  new_h1: string
  original_subhead: string
  new_subhead: string
  original_cta: string
  new_cta: string
  reasoning: string
}

const PROGRESS_STEPS = [
  'Scraping landing page...',
  'Analysing ad creative...',
  'Generating personalised copy...',
]

export default function Home() {
  const [adImageUrl, setAdImageUrl] = useState('')
  const [adImageBase64, setAdImageBase64] = useState<string | null>(null)
  const [landingPageUrl, setLandingPageUrl] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [result, setResult] = useState<Result | null>(null)
  const [currentStep, setCurrentStep] = useState(0)

  // Get API URL from environment or use default
  const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

  // Cycle through progress steps every 2 seconds during loading
  useEffect(() => {
    if (!loading) return

    const interval = setInterval(() => {
      setCurrentStep((prev) => (prev + 1) % PROGRESS_STEPS.length)
    }, 2000)

    return () => clearInterval(interval)
  }, [loading])

  const handleFileUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (!file) return

    const reader = new FileReader()
    reader.onload = (event) => {
      const base64String = event.target?.result as string
      setAdImageBase64(base64String)
      setAdImageUrl('') // Clear URL if file is selected
    }
    reader.readAsDataURL(file)
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError(null)
    setResult(null)
    setCurrentStep(0)
    setLoading(true)

    try {
      const imageSource = adImageBase64 || adImageUrl
      if (!imageSource) {
        throw new Error('Please provide an ad image URL or upload a file')
      }

      const response = await fetch(`${API_URL}/enhance`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          ad_image_url: imageSource,
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

  const handleRetry = async (e: React.FormEvent) => {
    e.preventDefault()
    await handleSubmit(e)
  }

  const handleStartOver = () => {
    setAdImageUrl('')
    setAdImageBase64(null)
    setLandingPageUrl('')
    setError(null)
    setResult(null)
    setCurrentStep(0)
  }

  return (
    <div className="min-h-screen bg-white">
      <div className="max-w-6xl mx-auto px-6 py-12">
        {/* Header */}
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold text-gray-900 mb-2">
            Landing Page Personaliser
          </h1>
          <p className="text-gray-600">
            Transform your landing page copy with AI-powered personalization
          </p>
        </div>

        {/* Main Content */}
        {!result ? (
          <>
            {/* Form */}
            <form onSubmit={handleSubmit} className="mb-8">
              <div className="space-y-4 mb-6">
                {/* Ad Image URL or File Upload */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Ad Image
                  </label>
                  <div className="flex gap-2">
                    <input
                      type="text"
                      value={adImageUrl}
                      onChange={(e) => {
                        setAdImageUrl(e.target.value)
                        if (e.target.value) setAdImageBase64(null)
                      }}
                      placeholder="https://example.com/ad.jpg"
                      className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                      disabled={!!adImageBase64}
                    />
                    <label className="px-4 py-2 bg-gray-100 border border-gray-300 rounded-lg cursor-pointer hover:bg-gray-200 transition-colors">
                      Upload
                      <input
                        type="file"
                        accept="image/*"
                        onChange={handleFileUpload}
                        className="hidden"
                      />
                    </label>
                  </div>
                  {adImageBase64 && (
                    <p className="text-sm text-green-600 mt-1">✓ Image uploaded</p>
                  )}
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
                {loading ? 'Personalising...' : 'Personalise'}
              </button>
            </form>

            {/* Loading State with Progress Indicator */}
            {loading && (
              <div className="mb-8 p-6 bg-blue-50 rounded-lg border border-blue-200">
                <div className="flex items-center gap-3">
                  <div className="animate-spin rounded-full h-5 w-5 border-2 border-blue-600 border-t-transparent"></div>
                  <div>
                    <p className="text-blue-900 font-medium">
                      {PROGRESS_STEPS[currentStep]}
                    </p>
                    <div className="flex gap-2 mt-2">
                      {PROGRESS_STEPS.map((_, index) => (
                        <div
                          key={index}
                          className={`h-2 w-2 rounded-full transition-colors ${
                            index === currentStep
                              ? 'bg-blue-600'
                              : index < currentStep
                              ? 'bg-blue-400'
                              : 'bg-gray-300'
                          }`}
                        ></div>
                      ))}
                    </div>
                  </div>
                </div>
              </div>
            )}

            {/* Error Message */}
            {error && (
              <div className="mb-8 p-4 bg-red-50 rounded-lg border border-red-200">
                <p className="text-red-700 mb-3">{error}</p>
                <button
                  onClick={handleRetry}
                  className="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors"
                >
                  Retry
                </button>
              </div>
            )}
          </>
        ) : (
          <>
            {/* Results Section - Side by Side Before/After */}
            <div className="mb-8">
              <div className="grid grid-cols-2 gap-8">
                {/* Original Page Column */}
                <div>
                  <h2 className="text-xl font-bold text-gray-700 mb-6">
                    Original page
                  </h2>
                  <div className="space-y-6">
                    {/* Original H1 */}
                    <div className="p-6 bg-gray-50 rounded-lg border border-gray-200">
                      <label className="text-xs font-semibold text-gray-500 uppercase tracking-wide block mb-2">
                        Headline
                      </label>
                      <p className="text-base text-gray-600">
                        {result.original_h1}
                      </p>
                    </div>

                    {/* Original Subhead */}
                    <div className="p-6 bg-gray-50 rounded-lg border border-gray-200">
                      <label className="text-xs font-semibold text-gray-500 uppercase tracking-wide block mb-2">
                        Subheadline
                      </label>
                      <p className="text-base text-gray-600">
                        {result.original_subhead}
                      </p>
                    </div>

                    {/* Original CTA */}
                    <div className="p-6 bg-gray-50 rounded-lg border border-gray-200">
                      <label className="text-xs font-semibold text-gray-500 uppercase tracking-wide block mb-2">
                        CTA button
                      </label>
                      <p className="text-base text-gray-600">
                        {result.original_cta}
                      </p>
                    </div>
                  </div>
                </div>

                {/* Personalised Page Column */}
                <div>
                  <h2 className="text-xl font-bold text-gray-900 mb-6">
                    Personalised page
                  </h2>
                  <div className="space-y-6">
                    {/* New H1 */}
                    <div className="p-6 bg-white rounded-lg border-l-4 border-green-500 border border-gray-200">
                      <label className="text-xs font-semibold text-gray-700 uppercase tracking-wide block mb-2">
                        Headline
                      </label>
                      <p className="text-base font-semibold text-gray-900">
                        {result.new_h1}
                      </p>
                    </div>

                    {/* New Subhead */}
                    <div className="p-6 bg-white rounded-lg border-l-4 border-green-500 border border-gray-200">
                      <label className="text-xs font-semibold text-gray-700 uppercase tracking-wide block mb-2">
                        Subheadline
                      </label>
                      <p className="text-base font-semibold text-gray-900">
                        {result.new_subhead}
                      </p>
                    </div>

                    {/* New CTA */}
                    <div className="p-6 bg-white rounded-lg border-l-4 border-green-500 border border-gray-200">
                      <label className="text-xs font-semibold text-gray-700 uppercase tracking-wide block mb-2">
                        CTA button
                      </label>
                      <p className="text-base font-semibold text-gray-900">
                        {result.new_cta}
                      </p>
                    </div>
                  </div>
                </div>
              </div>

              {/* Reasoning Card - Full Width */}
              <div className="mt-8 p-6 bg-yellow-50 rounded-lg border border-yellow-200">
                <label className="text-xs font-semibold text-gray-700 uppercase tracking-wide block mb-2">
                  Why these changes
                </label>
                <p className="text-base text-gray-900">
                  {result.reasoning}
                </p>
              </div>
            </div>

            {/* Action Buttons */}
            <div className="flex gap-4">
              <button
                onClick={handleStartOver}
                className="flex-1 px-4 py-3 bg-gray-200 text-gray-900 font-semibold rounded-lg hover:bg-gray-300 transition-colors"
              >
                Start over
              </button>
              <button
                onClick={() => window.location.reload()}
                className="flex-1 px-4 py-3 bg-blue-600 text-white font-semibold rounded-lg hover:bg-blue-700 transition-colors"
              >
                Try another page
              </button>
            </div>
          </>
        )}
      </div>
    </div>
  )
}
