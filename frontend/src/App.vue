<script setup>
import { computed, onMounted, ref } from 'vue'
import { useInquiryWizard } from './composables/useInquiryWizard'
import { budgetOptions, timelineOptions, stageOptions } from './data/projectOptions'
import { checkApiHealth, submitInquiry as sendInquiry } from './services/api'

const {
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
} = useInquiryWizard()

const apiState = ref('checking')
const isSubmitting = ref(false)
const submitError = ref('')
const submission = ref(null)
const copied = ref(false)
const apiBaseUrl = (import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000').replace(/\/$/, '')
const progressStyle = computed(() => ({ width: `${progress.value}%` }))

onMounted(async () => {
  try {
    await checkApiHealth()
    apiState.value = 'connected'
  } catch {
    apiState.value = 'unavailable'
  }
})

function getIdempotencyKey() {
  const storageKey = 'cynbit-inquiry-idempotency-key'
  try {
    let key = window.sessionStorage.getItem(storageKey)
    if (!key) {
      key = window.crypto.randomUUID()
      window.sessionStorage.setItem(storageKey, key)
    }
    return key
  } catch {
    return window.crypto.randomUUID()
  }
}

async function submitInquiry() {
  if (!goNext()) return
  submitError.value = ''
  isSubmitting.value = true

  try {
    const result = await sendInquiry(
      {
        ...form,
        full_name: form.full_name.trim(),
        email: form.email.trim(),
        company_name: form.company_name.trim() || null,
        phone_number: form.phone_number.trim() || null,
        project_title: form.project_title.trim() || null,
        problem_statement: form.problem_statement.trim(),
        objective: form.objective.trim(),
        other_requirement: form.other_requirement.trim() || null,
      },
      getIdempotencyKey(),
    )
    submission.value = result
    window.sessionStorage.removeItem('cynbit-inquiry-idempotency-key')
  } catch (error) {
    submitError.value = error.message || 'We could not submit the inquiry. Your answers are still here; please try again.'
  } finally {
    isSubmitting.value = false
  }
}

async function copyBrief() {
  try {
    await navigator.clipboard.writeText(projectBrief.value)
    copied.value = true
    window.setTimeout(() => { copied.value = false }, 1800)
  } catch {
    copied.value = false
  }
}

function startAnotherInquiry() {
  submission.value = null
  submitError.value = ''
  resetForm()
}
</script>

<template>
  <div class="min-h-screen bg-slate-50 text-slate-900">
    <header class="border-b border-slate-200 bg-white">
      <div class="mx-auto flex max-w-6xl items-center justify-between px-5 py-5 sm:px-8">
        <a class="text-xl font-extrabold tracking-tight text-slate-950" href="#" aria-label="Cynbit project discovery">
          Cynbit<span class="text-teal-700">.</span>
        </a>
        <div class="flex items-center gap-2 text-xs font-medium text-slate-500" aria-live="polite">
          <span
            class="size-2 rounded-full"
            :class="apiState === 'connected' ? 'bg-emerald-500' : apiState === 'checking' ? 'bg-amber-400' : 'bg-slate-300'"
            aria-hidden="true"
          ></span>
          <span>{{ apiState === 'connected' ? 'API online' : apiState === 'checking' ? 'Checking API' : 'API offline' }}</span>
        </div>
      </div>
    </header>

    <main class="mx-auto max-w-6xl px-5 pb-14 pt-8 sm:px-8 sm:pt-12">
      <section v-if="submission" class="mx-auto max-w-2xl rounded-3xl border border-emerald-100 bg-white p-7 shadow-sm sm:p-10" aria-live="polite">
        <div class="mb-6 flex size-12 items-center justify-center rounded-full bg-emerald-50 text-2xl text-emerald-700" aria-hidden="true">✓</div>
        <p class="text-xs font-bold uppercase tracking-[0.18em] text-emerald-800">Inquiry received</p>
        <h1 class="mt-3 text-3xl font-extrabold tracking-tight text-slate-950">Thanks, {{ form.full_name.split(' ')[0] }}.</h1>
        <p class="mt-4 leading-7 text-slate-600">Your project details have been saved. Cynbit’s team can use this structured brief as a starting point for the next conversation.</p>
        <p v-if="submission.reference_id || submission.id" class="mt-6 rounded-xl bg-slate-50 px-4 py-3 text-sm text-slate-600">
          Reference: <span class="font-semibold text-slate-900">{{ submission.reference_id || submission.id }}</span>
        </p>
        <button class="mt-8 rounded-lg border border-slate-300 px-4 py-2.5 text-sm font-semibold hover:bg-slate-50" type="button" @click="startAnotherInquiry">
          Start another inquiry
        </button>
      </section>

      <template v-else>
        <section class="mb-8 grid gap-6 md:grid-cols-[1fr_auto] md:items-end">
          <div>
            <p class="mb-3 text-xs font-bold uppercase tracking-[0.2em] text-teal-800">Project discovery</p>
            <h1 class="max-w-3xl text-3xl font-extrabold tracking-tight text-slate-950 sm:text-5xl">A clearer starting point for your next build.</h1>
            <p class="mt-4 max-w-2xl leading-7 text-slate-600">Share your goals, requirements, and timing in a guided flow. This prototype complements Cynbit’s existing discovery process.</p>
          </div>
          <p class="rounded-xl border border-slate-200 bg-white px-4 py-3 text-sm font-medium text-slate-600">Usually takes <span class="font-bold text-slate-900">about 5 minutes</span></p>
        </section>

        <section class="overflow-hidden rounded-3xl border border-slate-200 bg-white shadow-sm">
          <div class="border-b border-slate-100 px-5 py-5 sm:px-8">
            <div class="mb-4 flex items-center justify-between gap-4">
              <div>
                <p class="text-xs font-bold uppercase tracking-[0.16em] text-slate-500">Step {{ currentStep + 1 }} of {{ steps.length }}</p>
                <h2 class="mt-1 text-xl font-bold text-slate-950">{{ steps[currentStep].title }}</h2>
              </div>
              <span class="text-right text-sm text-slate-500">{{ steps[currentStep].caption }}</span>
            </div>
            <div class="h-1.5 overflow-hidden rounded-full bg-slate-100" role="progressbar" :aria-valuenow="currentStep + 1" :aria-valuemin="1" :aria-valuemax="steps.length" :aria-label="`Step ${currentStep + 1} of ${steps.length}`">
              <div class="h-full rounded-full bg-teal-800 transition-all duration-300" :style="progressStyle"></div>
            </div>
            <nav class="mt-5 grid grid-cols-5 gap-2" aria-label="Inquiry steps">
              <button
                v-for="(step, index) in steps"
                :key="step.title"
                class="rounded-lg px-2 py-2 text-center text-xs font-semibold transition"
                :class="index === currentStep ? 'bg-teal-50 text-teal-900' : index < currentStep ? 'text-slate-700 hover:bg-slate-50' : 'cursor-default text-slate-400'"
                :aria-current="index === currentStep ? 'step' : undefined"
                :disabled="index >= currentStep"
                type="button"
                @click="editStep(index)"
              >
                <span class="hidden sm:inline">{{ step.title }}</span>
                <span class="sm:hidden">{{ index + 1 }}</span>
              </button>
            </nav>
          </div>

          <div class="px-5 py-7 sm:px-8 sm:py-9">
            <div v-if="currentStep === 0" class="max-w-3xl">
              <h3 class="text-lg font-bold text-slate-950">First, your contact details</h3>
              <p class="mt-1 text-sm text-slate-500">We’ll use these details to follow up about your project.</p>
              <div class="mt-7 grid gap-5 sm:grid-cols-2">
                <div>
                  <label class="field-label" for="full-name">Full name <span class="required-mark">*</span></label>
                  <input id="full-name" v-model.trim="form.full_name" class="field-input" :class="{ 'field-input-error': errors.full_name }" autocomplete="name" maxlength="100" :aria-invalid="Boolean(errors.full_name)" aria-describedby="full-name-error" @input="clearError('full_name')">
                  <p v-if="errors.full_name" id="full-name-error" class="field-error">{{ errors.full_name }}</p>
                </div>
                <div>
                  <label class="field-label" for="email">Email address <span class="required-mark">*</span></label>
                  <input id="email" v-model.trim="form.email" class="field-input" :class="{ 'field-input-error': errors.email }" type="email" autocomplete="email" maxlength="254" :aria-invalid="Boolean(errors.email)" aria-describedby="email-error" @input="clearError('email')">
                  <p v-if="errors.email" id="email-error" class="field-error">{{ errors.email }}</p>
                </div>
                <div>
                  <label class="field-label" for="company">Company <span class="optional-mark">Optional</span></label>
                  <input id="company" v-model.trim="form.company_name" class="field-input" autocomplete="organization" maxlength="120" :aria-invalid="Boolean(errors.company_name)" aria-describedby="company-error" @input="clearError('company_name')">
                  <p v-if="errors.company_name" id="company-error" class="field-error">{{ errors.company_name }}</p>
                </div>
                <div>
                  <label class="field-label" for="phone">Phone number <span class="optional-mark">Optional</span></label>
                  <input id="phone" v-model.trim="form.phone_number" class="field-input" type="tel" autocomplete="tel" maxlength="30" :aria-invalid="Boolean(errors.phone_number)" aria-describedby="phone-error" @input="clearError('phone_number')">
                  <p v-if="errors.phone_number" id="phone-error" class="field-error">{{ errors.phone_number }}</p>
                </div>
              </div>
            </div>

            <div v-else-if="currentStep === 1" class="max-w-4xl">
              <h3 class="text-lg font-bold text-slate-950">Tell us about the project</h3>
              <p class="mt-1 text-sm text-slate-500">Choose the closest service area, then describe the problem and outcome.</p>
              <fieldset class="mt-6">
                <legend class="field-label">Project category <span class="required-mark">*</span></legend>
                <div class="mt-3 grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
                  <button
                    v-for="category in categories"
                    :key="category.value"
                    class="rounded-xl border p-4 text-left transition hover:border-teal-700/50 hover:bg-teal-50/40"
                    :class="form.project_category === category.value ? 'border-teal-800 bg-teal-50 ring-1 ring-teal-800' : 'border-slate-200 bg-white'"
                    type="button"
                    :aria-pressed="form.project_category === category.value"
                    @click="chooseCategory(category.value)"
                  >
                    <span class="block text-sm font-bold text-slate-900">{{ category.label }}</span>
                    <span class="mt-1 block text-xs leading-5 text-slate-500">{{ category.description }}</span>
                  </button>
                </div>
                <p v-if="errors.project_category" class="field-error">{{ errors.project_category }}</p>
              </fieldset>
              <div class="mt-6 grid gap-5">
                <div>
                  <label class="field-label" for="project-title">Project title <span class="optional-mark">Optional</span></label>
                  <input id="project-title" v-model.trim="form.project_title" class="field-input" maxlength="120" :aria-invalid="Boolean(errors.project_title)" aria-describedby="project-title-error" @input="clearError('project_title')">
                  <p v-if="errors.project_title" id="project-title-error" class="field-error">{{ errors.project_title }}</p>
                </div>
                <div>
                  <label class="field-label" for="problem">What problem or opportunity are you addressing? <span class="required-mark">*</span></label>
                  <textarea id="problem" v-model.trim="form.problem_statement" class="field-input min-h-28 resize-y" maxlength="2000" placeholder="Describe the current challenge, who it affects, and any useful context." :aria-invalid="Boolean(errors.problem_statement)" aria-describedby="problem-help problem-error" @input="clearError('problem_statement')"></textarea>
                  <div class="mt-1 flex justify-between gap-3 text-xs text-slate-400"><span id="problem-help">At least 20 characters</span><span>{{ form.problem_statement.length }}/2000</span></div>
                  <p v-if="errors.problem_statement" id="problem-error" class="field-error">{{ errors.problem_statement }}</p>
                </div>
                <div>
                  <label class="field-label" for="objective">What would a successful outcome look like? <span class="required-mark">*</span></label>
                  <textarea id="objective" v-model.trim="form.objective" class="field-input min-h-24 resize-y" maxlength="600" placeholder="For example: help customers complete a task, reduce manual work, or launch a new service." :aria-invalid="Boolean(errors.objective)" aria-describedby="objective-error" @input="clearError('objective')"></textarea>
                  <p v-if="errors.objective" id="objective-error" class="field-error">{{ errors.objective }}</p>
                </div>
              </div>
            </div>

            <div v-else-if="currentStep === 2" class="max-w-4xl">
              <h3 class="text-lg font-bold text-slate-950">Choose the capabilities that matter</h3>
              <p class="mt-1 text-sm text-slate-500">Options are tailored to {{ selectedCategory?.label || 'your selected category' }}. Pick all that apply.</p>
              <fieldset class="mt-6">
                <legend class="sr-only">Project requirements</legend>
                <div class="grid gap-3 sm:grid-cols-2">
                  <label v-for="requirement in requirementOptions" :key="requirement" class="flex cursor-pointer items-start gap-3 rounded-xl border border-slate-200 p-4 transition hover:border-teal-700/50 hover:bg-teal-50/30 has-[:checked]:border-teal-800 has-[:checked]:bg-teal-50">
                    <input class="mt-0.5 size-4 accent-teal-800" type="checkbox" :checked="form.requirements.includes(requirement)" @change="toggleRequirement(requirement)">
                    <span class="text-sm font-medium leading-6 text-slate-800">{{ requirement }}</span>
                  </label>
                </div>
                <p v-if="errors.requirements" class="field-error">{{ errors.requirements }}</p>
              </fieldset>
              <div class="mt-6">
                <label class="field-label" for="other-requirement">Another requirement <span class="optional-mark">Optional</span></label>
                <textarea id="other-requirement" v-model.trim="form.other_requirement" class="field-input min-h-24 resize-y" maxlength="300" placeholder="Add a capability that is not listed." :aria-invalid="Boolean(errors.other_requirement)" aria-describedby="other-requirement-error" @input="clearError('other_requirement'); clearError('requirements')"></textarea>
                <p v-if="errors.other_requirement" id="other-requirement-error" class="field-error">{{ errors.other_requirement }}</p>
              </div>
            </div>

            <div v-else-if="currentStep === 3" class="max-w-3xl">
              <h3 class="text-lg font-bold text-slate-950">Set your planning expectations</h3>
              <p class="mt-1 text-sm text-slate-500">These are starting estimates to make the first discussion more useful.</p>
              <div class="mt-7 grid gap-5 sm:grid-cols-2">
                <div>
                  <label class="field-label" for="budget">Budget range <span class="required-mark">*</span></label>
                  <select id="budget" v-model="form.budget_range" class="field-input" :class="{ 'field-input-error': errors.budget_range }" :aria-invalid="Boolean(errors.budget_range)" @change="clearError('budget_range')">
                    <option value="" disabled>Select a range</option>
                    <option v-for="option in budgetOptions" :key="option" :value="option">{{ option }}</option>
                  </select>
                  <p v-if="errors.budget_range" class="field-error">{{ errors.budget_range }}</p>
                </div>
                <div>
                  <label class="field-label" for="timeline">Expected timeline <span class="required-mark">*</span></label>
                  <select id="timeline" v-model="form.expected_timeline" class="field-input" :class="{ 'field-input-error': errors.expected_timeline }" :aria-invalid="Boolean(errors.expected_timeline)" @change="clearError('expected_timeline')">
                    <option value="" disabled>Select a timeline</option>
                    <option v-for="option in timelineOptions" :key="option" :value="option">{{ option }}</option>
                  </select>
                  <p v-if="errors.expected_timeline" class="field-error">{{ errors.expected_timeline }}</p>
                </div>
                <div class="sm:col-span-2">
                  <label class="field-label" for="stage">Current project stage <span class="required-mark">*</span></label>
                  <select id="stage" v-model="form.project_stage" class="field-input" :class="{ 'field-input-error': errors.project_stage }" :aria-invalid="Boolean(errors.project_stage)" @change="clearError('project_stage')">
                    <option value="" disabled>Select the current stage</option>
                    <option v-for="option in stageOptions" :key="option" :value="option">{{ option }}</option>
                  </select>
                  <p v-if="errors.project_stage" class="field-error">{{ errors.project_stage }}</p>
                </div>
              </div>
            </div>

            <div v-else class="max-w-4xl">
              <h3 class="text-lg font-bold text-slate-950">Review your project brief</h3>
              <p class="mt-1 text-sm text-slate-500">Use Edit to return to any section and correct your answers before submitting.</p>
              <section class="mt-6 rounded-2xl bg-slate-950 p-5 text-white sm:p-6" aria-labelledby="brief-heading">
                <div class="flex flex-wrap items-center justify-between gap-3">
                  <div>
                    <p class="text-xs font-bold uppercase tracking-[0.16em] text-teal-300">Project brief</p>
                    <h4 id="brief-heading" class="mt-1 text-lg font-bold">{{ form.project_title || selectedCategory?.label }}</h4>
                  </div>
                  <button class="rounded-lg border border-white/20 px-3 py-2 text-xs font-semibold text-white hover:bg-white/10" type="button" @click="copyBrief">{{ copied ? 'Copied' : 'Copy brief' }}</button>
                </div>
                <pre class="mt-5 whitespace-pre-wrap break-words font-sans text-sm leading-6 text-slate-200">{{ projectBrief }}</pre>
                <p class="mt-4 text-xs text-slate-400">This summary is assembled from your answers using a fixed template.</p>
              </section>

              <div class="mt-5 grid gap-3 md:grid-cols-2">
                <section class="review-card">
                  <div class="review-heading"><h4>Contact</h4><button type="button" @click="editStep(0)">Edit</button></div>
                  <p>{{ form.full_name }} · {{ form.email }}</p>
                  <p v-if="form.company_name || form.phone_number" class="mt-1">{{ [form.company_name, form.phone_number].filter(Boolean).join(' · ') }}</p>
                </section>
                <section class="review-card">
                  <div class="review-heading"><h4>Project overview</h4><button type="button" @click="editStep(1)">Edit</button></div>
                  <p class="font-semibold">{{ form.project_title || selectedCategory?.label }} · {{ selectedCategory?.label }}</p>
                  <p class="mt-2"><span class="font-semibold text-slate-700">Problem:</span> {{ form.problem_statement }}</p>
                  <p class="mt-2"><span class="font-semibold text-slate-700">Outcome:</span> {{ form.objective }}</p>
                </section>
                <section class="review-card">
                  <div class="review-heading"><h4>Requirements</h4><button type="button" @click="editStep(2)">Edit</button></div>
                  <ul class="list-inside list-disc space-y-1">
                    <li v-for="item in [...form.requirements, ...(form.other_requirement ? [form.other_requirement] : [])]" :key="item">{{ item }}</li>
                  </ul>
                </section>
                <section class="review-card">
                  <div class="review-heading"><h4>Planning</h4><button type="button" @click="editStep(3)">Edit</button></div>
                  <p><span class="font-semibold text-slate-700">Budget:</span> {{ form.budget_range }}</p>
                  <p class="mt-1"><span class="font-semibold text-slate-700">Timeline:</span> {{ form.expected_timeline }}</p>
                  <p class="mt-1"><span class="font-semibold text-slate-700">Stage:</span> {{ form.project_stage }}</p>
                </section>
              </div>

              <p v-if="submitError" class="mt-5 rounded-xl border border-rose-200 bg-rose-50 px-4 py-3 text-sm text-rose-800" role="alert">{{ submitError }}</p>
            </div>
          </div>

          <div class="flex items-center justify-between gap-4 border-t border-slate-100 bg-slate-50/70 px-5 py-5 sm:px-8">
            <button class="rounded-lg px-4 py-2.5 text-sm font-semibold text-slate-600 hover:bg-slate-100 disabled:cursor-not-allowed disabled:opacity-40" type="button" :disabled="currentStep === 0 || isSubmitting" @click="goBack">Back</button>
            <button v-if="currentStep < steps.length - 1" class="rounded-lg bg-teal-800 px-5 py-2.5 text-sm font-semibold text-white shadow-sm transition hover:bg-teal-900 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-teal-800" type="button" @click="goNext">Continue <span aria-hidden="true">→</span></button>
            <button v-else class="rounded-lg bg-teal-800 px-5 py-2.5 text-sm font-semibold text-white shadow-sm transition hover:bg-teal-900 disabled:cursor-wait disabled:opacity-60" type="button" :disabled="isSubmitting" @click="submitInquiry">{{ isSubmitting ? 'Submitting…' : 'Submit inquiry' }}</button>
          </div>
        </section>

        <p class="mt-5 text-center text-xs leading-5 text-slate-500">Your project details are used to prepare an inquiry for Cynbit’s team. This is an independent assessment prototype.</p>
      </template>
    </main>
  </div>
</template>
