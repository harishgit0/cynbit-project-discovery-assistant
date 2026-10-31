const API_BASE_URL = (import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000').replace(/\/$/, '')

export async function checkApiHealth() {
  const response = await fetch(`${API_BASE_URL}/api/health`)
  if (!response.ok) throw new Error(`Health check failed (${response.status})`)
  return response.json()
}

export async function submitInquiry(payload, idempotencyKey) {
  let response
  try {
    response = await fetch(`${API_BASE_URL}/api/inquiries`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Idempotency-Key': idempotencyKey,
      },
      body: JSON.stringify(payload),
    })
  } catch {
    throw new Error('Could not reach the API. Your answers are still here; please try again when the service is available.')
  }

  const result = await response.json().catch(() => ({}))
  if (!response.ok) {
    const detail = typeof result.detail === 'string' ? result.detail : 'Please review the form and try again.'
    throw new Error(detail)
  }
  return result
}
