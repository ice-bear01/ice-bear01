<script setup lang="ts">
import router from '@/router'
import axios from 'axios'
import { ref } from 'vue'
import { useLoadingStore } from '@/store/loading'

const loading = useLoadingStore()

const email = ref<string>('')
const password = ref<string>('')

const toAdminLogin = async () => {
  if (!email.value || !password.value) return
  try {
    loading.show()
    const login = await axios.post(
      'http://localhost:8000/users/auth/admin/login',
      { email: email.value, password: password.value },
      { withCredentials: true }
    )
    if (login) router.push('/admin/dashboard')
  } catch (err: any) {
    console.error(err)
    alert(err.response?.data?.detail || 'Login failed. Check your credentials.')
  } finally {
    email.value = ''
    password.value = ''
    loading.hide()
  }
}
</script>

<template>
  <div class="bg-gradient-to-br h-screen flex items-center justify-center p-4">
    <div
      class="backdrop-blur-lg bg-white/20 border border-white/30 rounded-2xl shadow-2xl p-8 sm:p-10 w-full max-w-md text-white"
    >
      <!-- Header -->
      <div class="text-center mb-8">
        <h1 class="text-3xl font-bold tracking-wide">Admin Login</h1>
        <p class="text-gray-200 text-sm mt-2">Log in to manage the dashboard</p>
      </div>

      <!-- Login Form -->
      <form class="flex flex-col gap-5" @submit.prevent="toAdminLogin">
        <div class="flex flex-col">
          <label for="email" class="mb-1 font-semibold text-gray-100">Email</label>
          <input
            v-model="email"
            type="email"
            id="email"
            placeholder="Enter your email"
            class="bg-white/10 border border-white/30 rounded-xl px-4 py-2 text-white placeholder-gray-300 focus:outline-none focus:ring-2 focus:ring-[#ff9900]"
            required
            autofocus
          />
        </div>

        <div class="flex flex-col">
          <label for="password" class="mb-1 font-semibold text-gray-100">Password</label>
          <input
            v-model="password"
            type="password"
            id="password"
            placeholder="Enter your password"
            class="bg-white/10 border border-white/30 rounded-xl px-4 py-2 text-white placeholder-gray-300 focus:outline-none focus:ring-2 focus:ring-[#ff9900]"
            required
          />
        </div>

        <button
          type="submit"
          :disabled="loading.isLoading"
          class="bg-[#00c1d4] hover:bg-[#00a4b5] text-white font-bold py-2 rounded-xl transition-all duration-200 shadow-md hover:shadow-lg disabled:opacity-50"
        >
          Log In
        </button>
      </form>
    </div>
  </div>
</template>

<style scoped>
input,
button {
  transition: all 0.2s ease;
}
</style>
