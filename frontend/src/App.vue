<script setup>
import { onMounted, ref } from 'vue'

const apiState = ref('checking')
const apiBaseUrl = (import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000').replace(/\/$/, '')

onMounted(async () => {
  try {
    const response = await fetch(`${apiBaseUrl}/api/health`)
    if (!response.ok) throw new Error(`API returned ${response.status}`)
    apiState.value = 'connected'
  } catch {
    apiState.value = 'unavailable'
  }
})
</script>

<template>
  <main class="mx-auto flex min-h-screen max-w-5xl flex-col px-6 py-8 sm:px-10">
    <header class="flex items-center justify-between border-b border-slate-200 pb-6">
      <span class="text-lg font-extrabold tracking-tight text-slate-950">Cynbit</span>
      <span class="text-sm font-medium text-slate-500">Website improvement prototype</span>
    </header>

    <section class="my-auto grid gap-12 py-16 md:grid-cols-[1.3fr_0.7fr] md:items-center">
      <div>
        <p class="mb-4 text-xs font-bold uppercase tracking-[0.2em] text-teal-800">Project discovery</p>
        <h1 class="max-w-2xl text-4xl font-extrabold tracking-tight text-slate-950 sm:text-6xl">
          A clearer starting point for your next build.
        </h1>
        <p class="mt-6 max-w-xl text-lg leading-8 text-slate-600">
          Share your goals, requirements, and timing in a guided flow. This prototype complements
          Cynbit’s existing discovery process.
        </p>
        <p class="mt-8 inline-flex rounded-lg border border-teal-800/20 bg-white px-4 py-3 text-sm font-semibold text-teal-900">
          Five-step guided inquiry — setup in progress
        </p>
      </div>

      <aside class="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm" aria-live="polite">
        <p class="text-sm font-semibold text-slate-900">Local setup check</p>
        <p v-if="apiState === 'checking'" class="mt-3 text-sm text-slate-600">Checking the API…</p>
        <p v-else-if="apiState === 'connected'" class="mt-3 flex items-center gap-2 text-sm text-emerald-700">
          <span class="size-2 rounded-full bg-emerald-500" aria-hidden="true"></span>
          API connected
        </p>
        <p v-else class="mt-3 flex items-center gap-2 text-sm text-amber-700">
          <span class="size-2 rounded-full bg-amber-500" aria-hidden="true"></span>
          API unavailable — start the backend to verify the connection.
        </p>
        <p class="mt-4 break-all text-xs text-slate-400">{{ apiBaseUrl }}</p>
      </aside>
    </section>

    <footer class="border-t border-slate-200 pt-5 text-xs text-slate-500">
      Independent prototype inspired by Cynbit’s publicly presented services.
    </footer>
  </main>
</template>
