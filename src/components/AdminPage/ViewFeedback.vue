<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'

interface Feedback {
  id: number
  user_email: string
  profile_image?: string
  rating: number
  comment: string
  created_at: string
}

const feedbacks = ref<Feedback[]>([])
const backend = import.meta.env.VITE_BACKEND_URL || ''

const averageRating = computed(() => {
  if (!feedbacks.value.length) return 0
  const sum = feedbacks.value.reduce((acc, f) => acc + f.rating, 0)
  return +(sum / feedbacks.value.length).toFixed(1)
})

const fetchFeedbacks = async () => {
  try {
    const res = await axios.get<Feedback[]>(`${backend}/users/feedbacks`, { withCredentials: true })
    feedbacks.value = res.data
  } catch (err) {
    console.error(err)
  }
}

onMounted(() => fetchFeedbacks())
</script>

<template>
  <div class="bg-gray-900 text-white p-6 mb-5 rounded-xl shadow-md relative space-y-4 max-h-screen overflow-auto">
    <!-- Average Rating -->
    <div class="bg-gray-800/50 backdrop-blur-xl p-4 rounded-3xl shadow-2xl border border-gray-500 flex items-center gap-4">
      <span class="text-xl font-bold text-sky-500">Average Rating:</span>
      <span class="text-yellow-400 text-2xl">★ {{ averageRating }}</span>
      <span class="text-gray-300">({{ feedbacks.length }} reviews)</span>
    </div>

    <!-- Feedback List -->
    <div class="space-y-6">
      <h3 class="text-3xl font-bold text-gray-200 mb-5 flex items-center gap-2">
        <i class="fa-solid fa-comments text-sky-400"></i> Customer Feedback
      </h3>

      <div v-if="feedbacks.length === 0" class="text-gray-500 flex items-center gap-2">
        <i class="fa-solid fa-circle-exclamation text-yellow-500"></i> No feedback yet.
      </div>

      <div v-for="fb in feedbacks" :key="fb.id"
        class="relative bg-gray-800/50 backdrop-blur-xl p-6 rounded-3xl shadow-sm border border-gray-500 flex flex-col md:flex-row gap-6 hover:shadow-md transition-all">
        
        <!-- Left: profile + email + date -->
        <div class="flex flex-col items-center w-28 flex-shrink-0 gap-2 text-center">
          <img
            :src="fb.profile_image || 'https://via.placeholder.com/150'"
            alt="Profile"
            class="w-16 h-16 md:w-20 md:h-20 rounded-full border-4 border-sky-200 object-cover shadow-sm"
          />
          <span class="text-gray-200 text-xs truncate w-full">{{ fb.user_email }}</span>
          <span class="text-gray-400 text-xs w-full">{{ new Date(fb.created_at).toLocaleDateString() }}</span>
        </div>

        <!-- Middle: comment -->
        <div class="flex-1 text-gray-200 text-sm md:text-base break-words">
          <p>{{ fb.comment }}</p>
        </div>

        <!-- Right: stars -->
        <div class="flex-shrink-0 text-yellow-400 text-lg flex items-center gap-0.5">
          <span v-for="n in 5" :key="n" :class="n <= fb.rating ? '' : 'text-gray-400'">★</span>
        </div>
      </div>
    </div>
  </div>
</template>
