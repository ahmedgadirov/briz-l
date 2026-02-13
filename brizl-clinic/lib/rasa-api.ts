// Rasa REST API Client
// Connects to Vera AI bot at brizl.baysart.com

const RASA_URL = process.env.NEXT_PUBLIC_RASA_URL || 'https://brizl.baysart.com'

export interface RasaMessage {
  recipient_id: string
  text?: string
  buttons?: Array<{
    title: string
    payload: string
    type?: string
  }>
  image?: string
  attachment?: string
}

export interface RasaRequest {
  sender: string
  message: string
  metadata?: {
    platform?: string
    source?: string
    is_button_click?: boolean
    user_agent?: string
    device_type?: 'mobile' | 'desktop' | 'tablet'
  }
}

/**
 * Detect device type based on user agent
 */
function detectDeviceType(): 'mobile' | 'desktop' | 'tablet' {
  if (typeof window === 'undefined') return 'desktop'
  
  const ua = navigator.userAgent.toLowerCase()
  if (/tablet|ipad|playbook|silk/.test(ua)) return 'tablet'
  if (/mobile|android|iphone|ipod|blackberry|opera mini|iemobile/.test(ua)) return 'mobile'
  return 'desktop'
}

/**
 * Send a message to Rasa and get responses
 */
export async function sendMessageToRasa(
  sender: string,
  message: string,
  metadata?: RasaRequest['metadata']
): Promise<RasaMessage[]> {
  try {
    const response = await fetch(`${RASA_URL}/webhooks/rest/webhook`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        sender,
        message,
        metadata: {
          platform: 'web',
          source: 'website_chat',
          device_type: detectDeviceType(),
          user_agent: typeof window !== 'undefined' ? window.navigator.userAgent : undefined,
          ...metadata,
        },
      }),
    })

    if (!response.ok) {
      throw new Error(`Rasa API error: ${response.status}`)
    }

    const data = await response.json()
    return data as RasaMessage[]
  } catch (error) {
    console.error('Error sending message to Rasa:', error)
    throw error
  }
}

/**
 * Generate a unique session ID for the user
 */
export function generateSessionId(): string {
  return `web-${Date.now()}-${Math.random().toString(36).substring(2, 9)}`
}

/**
 * Surgery intent mapping - maps surgery IDs to Rasa intents
 */
export const surgeryIntents: Record<string, string> = {
  excimer: '/surgery_excimer',
  cataract: '/surgery_cataract',
  pteregium: '/surgery_opteregium',
  phacic: '/surgery_phacic',
  cesplik: '/surgery_cesplik',
  cross_linking: '/surgery_cross_linking',
  argon: '/surgery_argon',
  yag: '/surgery_yag',
  avastin: '/surgery_avastin',
  glaucoma: '/surgery_glaucoma',
}

/**
 * Doctor intent mapping - maps doctor IDs to Rasa intents
 */
export const doctorIntents: Record<string, string> = {
  iltifat: '/doctor_iltifat',
  emil: '/doctor_emil',
  sabina: '/doctor_sabina',
  seymur: '/doctor_seymur',
}

/**
 * Get surgery info message for Vera
 */
export function getSurgeryQuery(surgeryId: string): string {
  const queries: Record<string, string> = {
    excimer: 'Excimer laser haqqında ətraflı məlumat ver',
    cataract: 'Katarakta əməliyyatı haqqında ətraflı məlumat ver',
    pteregium: 'Pteregium əməliyyatı haqqında ətraflı məlumat ver',
    phacic: 'Phacic lens haqqında ətraflı məlumat ver',
    cesplik: 'Çəplik əməliyyatı haqqında ətraflı məlumat ver',
    cross_linking: 'Cross linking haqqında ətraflı məlumat ver',
    argon: 'Arqon laser haqqında ətraflı məlumat ver',
    yag: 'YAG laser haqqında ətraflı məlumat ver',
    avastin: 'Avastin müalicəsi haqqında ətraflı məlumat ver',
    glaucoma: 'Qlaukoma haqqında ətraflı məlumat ver',
  }
  return queries[surgeryId] || `${surgeryId} haqqında məlumat ver`
}

/**
 * Get doctor info message for Vera
 */
export function getDoctorQuery(doctorId: string): string {
  const queries: Record<string, string> = {
    iltifat: 'Dr. İltifat Şərif haqqında məlumat ver',
    emil: 'Dr. Emil Qafarlı haqqında məlumat ver',
    sabina: 'Dr. Səbinə Əbiyeva haqqında məlumat ver',
    seymur: 'Dr. Seymur Bayramov haqqında məlumat ver',
  }
  return queries[doctorId] || `${doctorId} haqqında məlumat ver`
}