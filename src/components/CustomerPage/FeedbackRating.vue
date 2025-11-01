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
const newRating = ref(0)
const newComment = ref('')
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

const submitFeedback = async () => {
  if (!newRating.value || !newComment.value) {
    alert('Please provide a rating and feedback')
    return
  }

  try {
    const res = await axios.post<Feedback>(
      `${backend}/users/feedback`,
      { rating: newRating.value, comment: newComment.value },
      { withCredentials: true }
    )
    feedbacks.value.unshift(res.data)
    newRating.value = 0
    newComment.value = ''
  } catch (err) {
    console.error(err)
    alert('Failed to submit feedback')
  }
}

onMounted(() => fetchFeedbacks())
</script>

<template>
  <div class="min-h-screen p-4 sm:p-8 text-gray-800 max-w-6xl mx-auto space-y-8">
    <!-- Submit Feedback -->
    <div class="bg-white/80 backdrop-blur-xl p-6 rounded-3xl shadow-2xl border border-sky-100 flex flex-col gap-4">
      <h2 class="text-3xl font-bold text-sky-800 mb-2">Submit Your Feedback</h2>

      <div class="flex items-center gap-2">
        <span
          v-for="n in 5"
          :key="n"
          @click="newRating = n"
          class="cursor-pointer text-2xl"
          :class="newRating >= n ? 'text-yellow-400' : 'text-gray-400'"
        >★</span>
        <span class="ml-2 text-gray-600">{{ newRating }}/5</span>
      </div>

      <textarea
        v-model="newComment"
        placeholder="Write your feedback..."
        rows="3"
        class="w-full p-4 rounded-2xl border border-sky-100 bg-sky-50/50 text-gray-700 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-sky-200 resize-none"
      ></textarea>

      <button
        @click="submitFeedback"
        class="self-start bg-gradient-to-r from-sky-500 to-blue-600 hover:from-sky-600 hover:to-blue-700 text-white font-semibold px-6 py-2.5 rounded-full shadow-md hover:shadow-lg flex items-center gap-2 transition-all"
      >
        <i class="fa-solid fa-paper-plane"></i> Submit Feedback
      </button>
    </div>

    <!-- Average Rating -->
    <div class="bg-white/80 backdrop-blur-xl p-4 rounded-3xl shadow-2xl border border-sky-100 flex items-center gap-4">
      <span class="text-xl font-bold text-sky-800">Average Rating:</span>
      <span class="text-yellow-400 text-2xl">★ {{ averageRating }}</span>
      <span class="text-gray-600">({{ feedbacks.length }} reviews)</span>
    </div>

    <!-- Feedback List -->
    <div class="space-y-6">
      <h3 class="text-3xl font-bold text-gray-200 mb-5 flex items-center gap-2">
        <i class="fa-solid fa-comments text-sky-400"></i> Feedback
      </h3>

      <div v-if="feedbacks.length === 0" class="text-gray-500 flex items-center gap-2">
        <i class="fa-solid fa-circle-exclamation text-yellow-500"></i> No feedback yet.
      </div>

      <div v-for="fb in feedbacks" :key="fb.id"
        class="relative bg-white/80 backdrop-blur-xl p-6 rounded-3xl shadow-sm border border-sky-100 flex flex-col md:flex-row gap-6 hover:shadow-md transition-all">
        
        <!-- Left: profile + email + date -->
        <div class="flex flex-col items-center w-28 flex-shrink-0 gap-2 text-center">
          <img
            :src="fb.profile_image || 'https://via.placeholder.com/150'"
            alt="Profile"
            class="w-16 h-16 md:w-20 md:h-20 rounded-full border-4 border-sky-200 object-cover shadow-sm"
          />
          <span class="text-gray-700 text-xs truncate w-full">{{ fb.user_email }}</span>
          <span class="text-gray-500 text-xs w-full">{{ new Date(fb.created_at).toLocaleDateString() }}</span>
        </div>

        <!-- Middle: comment -->
        <div class="flex-1 text-gray-700 text-sm md:text-base break-words">
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
