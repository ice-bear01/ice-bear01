<script setup lang="ts">
import { ref, computed, onUnmounted } from 'vue'
import axios from 'axios'
import router from '@/router'
import { useLoadingStore } from '@/store/loading'

const backend = import.meta.env.VITE_BACKEND_URL

const loading = useLoadingStore()
const errormessage = ref(false);
// --------------------
// Step tracking
// --------------------
const step = ref(1)
const nextStep = async () => {
  if (!canGoNext.value) return
  if (step.value === 1) {
    await sendCode()
    step.value = 2
  }
}
const prevStep = () => {
  if (step.value === 2) step.value = 1
}

// --------------------
// Form fields
// --------------------
const email = ref('')
const password = ref('')
const verificationCode = ref('')

// --------------------
// Validation
// --------------------
const canGoNext = computed(() => email.value.trim() !== '' && password.value.trim() !== '')

// --------------------
// Send/Resend code logic
// --------------------
const sendCodeCooldown = ref(0)
let interval: number | null = null
const sendingCode = ref(false)
const codeSentOnce = ref(false)

onUnmounted(() => {
  if (interval) clearInterval(interval)
})

const sendCode = async () => {
  if (sendCodeCooldown.value > 0 || sendingCode.value) return

  try {
    loading.show()
    sendingCode.value = true

    await axios.post(`${backend}/auth/send-code`, {
      email: email.value,
      purpose: 'register',
    })

    codeSentOnce.value = true
    sendCodeCooldown.value = 60
    interval = window.setInterval(() => {
      sendCodeCooldown.value--
      if (sendCodeCooldown.value <= 0 && interval) {
        clearInterval(interval)
        interval = null
      }
    }, 1000)
  } catch (error) {
    console.error('Error sending code:', error)
  } finally {
    sendingCode.value = false
    loading.hide()
  }
}

// --------------------
// Verify code logic
// --------------------
const verifyingCode = ref(false)

const verifyCode = async () => {
  if (verifyingCode.value) return

  try {
    loading.show()
    verifyingCode.value = true

    const verify = await axios.post(`${backend}/auth/verify-code`, {
      email: email.value,
      code: verificationCode.value,
    })
   

    if (verify) {
      await axios.post(
        `${backend}/users/auth/sign-up`,
        { email: email.value, password: password.value },
        { withCredentials: true }
      )
      router.push('/dashboard/home')
    }
  } catch (error: unknown) {
  if (axios.isAxiosError(error)) {
    if (error.response) {
      const status = error.response.status

      if (status === 400) {
        errormessage.value = true;
        console.error("Bad Request 400:", error.response.data)
        setTimeout(()=>{
          errormessage.value = false;
        },4000)
      }
    }
  } else {
    console.error("Unexpected error:", error)
  }
}
 finally {
    verifyingCode.value = false
    loading.hide()
  }
}
</script>

<template>
  <div class="bg-gradient-to-br min-h-screen flex items-center justify-center p-4">
    <div
      class="backdrop-blur-xl bg-white/20 border border-white/30 rounded-2xl shadow-2xl w-full max-w-md p-8 sm:p-10 text-white relative"
    >
      <!-- Heading -->
      <h2 class="text-3xl font-bold text-center mb-10 tracking-wide">
        Create Your Account
      </h2>

      <!-- Step Indicator -->
      <div class="flex items-center justify-center mb-8">
        <div class="relative flex items-center w-44">
          <div
            :class="[
              'w-10 h-10 flex items-center justify-center rounded-full font-bold transition-all duration-300',
              step === 1 ? 'bg-[#00c1d4] text-white' : 'bg-gray-300 text-gray-800'
            ]"
          >
            1
          </div>
          <div
            class="flex-1 h-[3px] mx-2 transition-all duration-300"
            :class="step > 1 ? 'bg-[#00c1d4]' : 'bg-gray-400'"
          ></div>
          <div
            :class="[
              'w-10 h-10 flex items-center justify-center rounded-full font-bold transition-all duration-300',
              step === 2 ? 'bg-[#00c1d4] text-white' : 'bg-gray-300 text-gray-800'
            ]"
          >
            2
          </div>
        </div>
      </div>

      <!-- Step 1 -->
      <transition name="fade" mode="out-in">
        <div v-if="step === 1" key="step1" class="flex flex-col gap-5">
          <div class="flex flex-col">
            <label class="mb-1 text-sm font-semibold text-gray-100">Email</label>
            <input
              v-model="email"
              type="email"
              placeholder="Enter your email"
              class="bg-white/10 border border-white/30 rounded-xl px-4 py-2 text-white placeholder-gray-300 focus:outline-none focus:ring-2 focus:ring-[#00c1d4]"
            />
          </div>

          <div class="flex flex-col">
            <label class="mb-1 text-sm font-semibold text-gray-100">Password</label>
            <input
              v-model="password"
              type="password"
              placeholder="Enter your password"
              class="bg-white/10 border border-white/30 rounded-xl px-4 py-2 text-white placeholder-gray-300 focus:outline-none focus:ring-2 focus:ring-[#00c1d4]"
            />
          </div>

          <button
            @click.prevent="nextStep"
            :disabled="!canGoNext"
            class="bg-[#00c1d4] hover:bg-[#00a4b5] disabled:bg-gray-400 disabled:cursor-not-allowed font-bold py-2 rounded-xl transition-all duration-200 shadow-md hover:shadow-lg"
          >
            Next
          </button>
        </div>

        <!-- Step 2 -->
        <div v-else key="step2" class="flex flex-col gap-5">
          <p class="text-sm text-gray-200 text-center">
            A verification code was sent to <br />
            <span class="font-semibold text-white">{{ email }}</span>
          </p>

          <div class="flex flex-col">
            <label class="mb-1 text-sm font-semibold text-gray-100">Verification Code</label>
            <input
              v-model="verificationCode"
              type="text"
              placeholder="Enter verification code"
              class="bg-white/10 border border-white/30 rounded-xl px-4 py-2 text-white placeholder-gray-300 focus:outline-none focus:ring-2 focus:ring-[#00c1d4]"
            />
          </div>

          <div class="flex justify-between items-center text-sm mt-1">
            <button
              @click.prevent="sendCode"
              :disabled="sendCodeCooldown > 0"
              class="text-[#b0efff] hover:underline disabled:text-gray-400 disabled:cursor-not-allowed"
            >
              {{ sendCodeCooldown > 0 ? `Resend in ${sendCodeCooldown}s` : codeSentOnce ? 'Resend Code' : 'Send Code' }}
            </button>
            <button
              @click.prevent="prevStep"
              class="text-gray-300 hover:underline"
            >
              Back
            </button>
          </div>
          <p v-if="errormessage" class="text-red-400">Email Already Exist</p>
          <button
            @click.prevent="verifyCode"
            class="bg-[#00c1d4] hover:bg-[#00a4b5] text-white font-bold py-2 rounded-xl transition-all duration-200 shadow-md hover:shadow-lg"
          >
            Verify & Complete
          </button>
        </div>
      </transition>

      <!-- Footer -->
      <p class="text-center text-gray-300 text-sm mt-6">
        Already have an account?
        <a @click="$router.replace('/login')" class="text-[#b0efff] font-semibold hover:underline cursor-pointer">
          Log in
        </a>
      </p>
    </div>
  </div>
</template>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: all 0.3s ease;
}
.fade-enter-from {
  opacity: 0;
  transform: translateY(10px);
}
.fade-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}
</style>
