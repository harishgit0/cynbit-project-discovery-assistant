export const categories = [
  { value: 'ai_automation', label: 'AI & Automation', description: 'Agents, LLM features, and workflow automation' },
  { value: 'web_mobile', label: 'Web & Mobile Application', description: 'Websites, mobile apps, and digital products' },
  { value: 'saas_platform', label: 'SaaS Platform', description: 'Subscription software and business platforms' },
  { value: 'backend_cloud', label: 'Backend & Cloud Infrastructure', description: 'APIs, databases, cloud, and integrations' },
  { value: 'digital_marketing_crm', label: 'Digital Marketing & CRM', description: 'SEO, campaigns, funnels, and CRM workflows' },
  { value: 'other_custom', label: 'Other / Custom Solution', description: 'A tailored solution across multiple areas' },
]

export const requirementsByCategory = {
  ai_automation: [
    'AI chatbot or virtual assistant',
    'LLM integration',
    'Document processing',
    'Workflow automation',
    'Voice AI agent',
    'CRM integration',
    'Analytics dashboard',
    'Admin panel',
  ],
  web_mobile: [
    'Responsive web application',
    'iOS or Android application',
    'User accounts and authentication',
    'Admin dashboard',
    'Online payments',
    'Notifications',
    'Third-party integrations',
    'Analytics and reporting',
  ],
  saas_platform: [
    'Multiple organizations or workspaces',
    'Subscription and billing management',
    'Role-based access',
    'Customer onboarding',
    'Usage analytics',
    'Admin dashboard',
    'API and webhooks',
    'Notifications',
  ],
  backend_cloud: [
    'API development',
    'Cloud infrastructure setup',
    'Database design or migration',
    'Legacy system migration',
    'Third-party integrations',
    'Security and access controls',
    'Monitoring and logging',
    'CI/CD deployment pipeline',
  ],
  digital_marketing_crm: [
    'CRM setup or customization',
    'Lead capture and funnel setup',
    'Email or WhatsApp automation',
    'Campaign analytics',
    'Technical SEO improvements',
    'Conversion-focused landing pages',
    'Advertising conversion tracking',
    'Marketing performance dashboard',
  ],
  other_custom: [
    'Customer or partner portal',
    'Business workflow automation',
    'Data dashboard or reporting',
    'Third-party system integration',
    'AI capability',
    'Cloud or infrastructure work',
    'Not sure yet — discuss during discovery',
  ],
}

export const budgetOptions = [
  'Below ₹25,000',
  '₹25,000–₹50,000',
  '₹50,000–₹1,00,000',
  '₹1,00,000–₹3,00,000',
  'Above ₹3,00,000',
  'Not decided yet',
]

export const timelineOptions = [
  'Less than 1 month',
  '1–2 months',
  '2–3 months',
  '3–6 months',
  'More than 6 months',
  'Flexible / Not decided',
]

export const stageOptions = [
  'Idea stage',
  'Planning / Research',
  'Design completed',
  'Development in progress',
  'Existing product / improvement',
]
