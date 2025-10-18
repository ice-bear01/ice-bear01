<script setup lang="ts">
import router from '@/router'
import axios from 'axios'
import { ref } from 'vue'
import { useLoadingStore } from '@/store/loading'

const loading = useLoadingStore()

const email = ref<string>('')
const password = ref<string>('')

const showForgotModal = ref(false)
const forgotEmail = ref('')
const verificationCode = ref('')
const step = ref(1) // 1 = input email, 2 = input verification code
const sendingCode = ref(false)

const toLogin = async () => {
  try {
    loading.show()
    const login = await axios.post(
      'http://localhost:8000/users/auth/login',
      { email: email.value, password: password.value },
      { withCredentials: true }
    )
    if (login) router.push('/dashboard')
  } catch (err) {
    console.error(err)
  } finally {
    email.value = ''
    password.value = ''
    loading.hide()
  }
}

// Send verification code for password reset
const sendForgotCode = async () => {
  if (!forgotEmail.value.trim()) return
  try {
    loading.show()
    sendingCode.value = true
    const res = await axios.post('http://localhost:8000/auth/send-code', {
      email: forgotEmail.value,
    })
    if (res) {
      step.value = 2
    }
  } catch (err) {
    console.error('Error sending reset code:', err)
  } finally {
    sendingCode.value = false
    loading.hide()
  }
}

// Verify the code (optional: next step could be change password)
const verifyForgotCode = async () => {
  try {
    loading.show()
    const verify = await axios.post('http://localhost:8000/auth/verify-code', {
      email: forgotEmail.value,
      code: verificationCode.value,
    })
    if (verify) {
      alert('Email verified! You can now reset your password.')
      showForgotModal.value = false
      step.value = 1
      forgotEmail.value = ''
      verificationCode.value = ''
    }
  } catch (err) {
    console.error('Verification failed:', err)
  } finally {
    loading.hide()
  }
}
</script>

<template>
  <div class="bg-gradient-to-br h-screen flex items-center justify-center p-4">
    <div
      class="backdrop-blur-lg bg-white/20 border border-white/30 rounded-2xl shadow-2xl p-8 sm:p-10 w-full max-w-md text-white relative"
    >
      <div class="text-center mb-8">
        <h1 class="text-3xl font-bold tracking-wide">Welcome Back</h1>
        <p class="text-gray-200 text-sm mt-2">Log in to continue managing your account</p>
      </div>

      <!-- Login Form -->
      <form class="flex flex-col gap-5" @submit.prevent="toLogin">
        <div class="flex flex-col">
          <label for="email" class="mb-1 font-semibold text-gray-100">Email</label>
          <input
            v-model="email"
            type="email"
            id="email"
            placeholder="Enter your email"
            class="bg-white/10 border border-white/30 rounded-xl px-4 py-2 text-white placeholder-gray-300 focus:outline-none focus:ring-2 focus:ring-[#00c1d4]"
            required
          />
        </div>

        <div class="flex flex-col">
          <label for="password" class="mb-1 font-semibold text-gray-100">Password</label>
          <input
            v-model="password"
            type="password"
            id="password"
            placeholder="Enter your password"
            class="bg-white/10 border border-white/30 rounded-xl px-4 py-2 text-white placeholder-gray-300 focus:outline-none focus:ring-2 focus:ring-[#00c1d4]"
            required
          />
          <button
            type="button"
            @click="showForgotModal = true"
            class="text-sm text-[#b0efff] mt-1 hover:underline self-end transition-colors"
          >
            Forgot password?
          </button>
        </div>

        <button
          type="submit"
          class="bg-[#00c1d4] hover:bg-[#00a4b5] text-white font-bold py-2 rounded-xl transition-all duration-200 shadow-md hover:shadow-lg"
        >
          Log In
        </button>

        <p class="text-center text-gray-200 text-sm mt-4">
          Don’t have an account?
          <a @click="$router.replace('/signup')" class="text-[#b0efff] font-semibold hover:underline cursor-pointer">
            Sign up
          </a>
        </p>
      </form>
    </div>

    <!-- Forgot Password Modal -->
    <div
      v-if="showForgotModal"
      class="fixed inset-0 flex items-center justify-center bg-black/50 backdrop-blur-sm z-50"
    >
      <div class="bg-white rounded-2xl shadow-2xl p-8 w-[90%] sm:w-[400px] text-gray-800 relative">
        <p class="text-xl font-bold mb-2 text-center">Reset Password</p>

        <!-- Step 1: Enter Email -->
        <div v-if="step === 1">
          <p class="text-sm text-gray-600 mb-4 text-center">
            Enter your registered email to receive a verification code.
          </p>
          <input
            v-model="forgotEmail"
            type="email"
            placeholder="Enter your email"
            class="border border-gray-300 rounded-xl px-4 py-2 w-full mb-4 focus:outline-none focus:ring-2 focus:ring-[#00a4b5]"
          />
          <div class="flex justify-between gap-3">
            <button
              @click="showForgotModal = false"
              class="bg-gray-200 text-gray-700 px-4 py-2 rounded-xl w-1/2 hover:bg-gray-300 transition"
            >
              Cancel
            </button>
            <button
              @click="sendForgotCode"
              :disabled="sendingCode"
              class="bg-[#00a4b5] text-white px-4 py-2 rounded-xl w-1/2 hover:bg-[#008c9e] transition disabled:opacity-60"
            >
              {{ sendingCode ? 'Sending...' : 'Send Code' }}
            </button>
          </div>
        </div>

        <!-- Step 2: Enter Verification Code -->
        <div v-else-if="step === 2">
          <p class="text-sm text-gray-600 mb-4 text-center">
            We sent a verification code to <span class="font-semibold">{{ forgotEmail }}</span>.
          </p>
          <input
            v-model="verificationCode"
            type="text"
            placeholder="Enter verification code"
            class="border border-gray-300 rounded-xl px-4 py-2 w-full mb-4 focus:outline-none focus:ring-2 focus:ring-[#00a4b5]"
          />
          <div class="flex justify-between gap-3">
            <button
              @click="step = 1"
              class="bg-gray-200 text-gray-700 px-4 py-2 rounded-xl w-1/2 hover:bg-gray-300 transition"
            >
              Back
            </button>
            <button
              @click="verifyForgotCode"
              class="bg-[#00a4b5] text-white px-4 py-2 rounded-xl w-1/2 hover:bg-[#008c9e] transition"
            >
              Verify
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
input,
button {
  transition: all 0.2s ease;
}
</style>
