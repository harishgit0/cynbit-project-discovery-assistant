import { computed, reactive, ref } from 'vue'
import { categories, requirementsByCategory } from '../data/projectOptions'

const createInitialForm = () => ({
  full_name: '',
  email: '',
  company_name: '',
  phone_number: '',
  project_category: '',
  project_title: '',
  problem_statement: '',
  objective: '',
  requirements: [],
  other_requirement: '',
  budget_range: '',
  expected_timeline: '',
  project_stage: '',
})

const steps = [
  { title: 'Contact', caption: 'How can we reach you?' },
  { title: 'Project', caption: 'What are you looking to build?' },
  { title: 'Requirements', caption: 'What should it include?' },
  { title: 'Planning', caption: 'What are your expectations?' },
  { title: 'Review', caption: 'Check your project brief' },
]

export function useInquiryWizard() {
  const currentStep = ref(0)
  const form = reactive(createInitialForm())
  const errors = ref({})

  const selectedCategory = computed(() => categories.find((item) => item.value === form.project_category))
  const requirementOptions = computed(() => requirementsByCategory[form.project_category] || [])
  const progress = computed(() => ((currentStep.value + 1) / steps.length) * 100)
  const projectBrief = computed(() => {
    const requirements = [...form.requirements]
    if (form.other_requirement.trim()) requirements.push(form.other_requirement.trim())

    return [
      `Project: ${form.project_title.trim() || selectedCategory.value?.label || 'Project inquiry'}`,
      `Category: ${selectedCategory.value?.label || 'Not selected'}`,
      `Problem: ${form.problem_statement.trim() || 'Not provided'}`,
      `Objective: ${form.objective.trim() || 'Not provided'}`,
      `Functional scope: ${requirements.length ? requirements.join('; ') : 'Not selected'}`,
      `Budget: ${form.budget_range || 'Not selected'}`,
      `Timeline: ${form.expected_timeline || 'Not selected'}`,
      `Project stage: ${form.project_stage || 'Not selected'}`,
      `Contact: ${form.full_name.trim() || 'Not provided'}${form.email ? ` (${form.email.trim()})` : ''}`,
    ].join('\n')
  })

  function clearError(field) {
    if (!errors.value[field]) return
    const nextErrors = { ...errors.value }
    delete nextErrors[field]
    errors.value = nextErrors
  }

  function chooseCategory(category) {
    if (form.project_category !== category) form.requirements = []
    form.project_category = category
    clearError('project_category')
    clearError('requirements')
  }

  function toggleRequirement(requirement) {
    const selected = new Set(form.requirements)
    if (selected.has(requirement)) selected.delete(requirement)
    else selected.add(requirement)
    form.requirements = [...selected]
    clearError('requirements')
  }

  function validateCurrentStep() {
    const nextErrors = {}
    const step = currentStep.value

    if (step === 0) {
      if (form.full_name.trim().length < 2) nextErrors.full_name = 'Enter your full name.'
      if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(form.email.trim())) nextErrors.email = 'Enter a valid email address.'
      if (form.company_name.length > 120) nextErrors.company_name = 'Keep the company name under 120 characters.'
      if (form.phone_number.length > 30) nextErrors.phone_number = 'Keep the phone number under 30 characters.'
    }

    if (step === 1) {
      if (!form.project_category) nextErrors.project_category = 'Choose a project category.'
      if (form.project_title.length > 120) nextErrors.project_title = 'Keep the project title under 120 characters.'
      if (form.problem_statement.trim().length < 20) nextErrors.problem_statement = 'Describe the problem in at least 20 characters.'
      if (form.problem_statement.length > 2000) nextErrors.problem_statement = 'Keep the description under 2,000 characters.'
      if (form.objective.trim().length < 10) nextErrors.objective = 'Describe the desired outcome in at least 10 characters.'
      if (form.objective.length > 600) nextErrors.objective = 'Keep the objective under 600 characters.'
    }

    if (step === 2) {
      if (form.requirements.length === 0 && !form.other_requirement.trim()) {
        nextErrors.requirements = 'Select at least one requirement or describe another one.'
      }
      if (form.other_requirement.length > 300) nextErrors.other_requirement = 'Keep this under 300 characters.'
    }

    if (step === 3) {
      if (!form.budget_range) nextErrors.budget_range = 'Choose a budget range.'
      if (!form.expected_timeline) nextErrors.expected_timeline = 'Choose an expected timeline.'
      if (!form.project_stage) nextErrors.project_stage = 'Choose the current project stage.'
    }

    errors.value = nextErrors
    return Object.keys(nextErrors).length === 0
  }

  function goNext() {
    if (!validateCurrentStep()) return false
    if (currentStep.value < steps.length - 1) currentStep.value += 1
    return true
  }

  function goBack() {
    if (currentStep.value > 0) currentStep.value -= 1
    errors.value = {}
  }

  function editStep(step) {
    if (step >= 0 && step < currentStep.value) {
      currentStep.value = step
      errors.value = {}
    }
  }

  function resetForm() {
    Object.assign(form, createInitialForm())
    errors.value = {}
    currentStep.value = 0
  }

  return {
    steps,
    categories,
    form,
    errors,
    currentStep,
    selectedCategory,
    requirementOptions,
    progress,
    projectBrief,
    clearError,
    chooseCategory,
    toggleRequirement,
    goNext,
    goBack,
    editStep,
    resetForm,
  }
}
