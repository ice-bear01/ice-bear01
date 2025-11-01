<template>
  <div class="min-h-screen text-gray-800 p-4 sm:p-8">
    <div class="max-w-6xl mx-auto space-y-8">
      <!-- Page Header -->
      <div class="text-center text-white space-y-3">
        <p class="text-3xl font-bold">Select Your Category</p>
        <p class="max-w-2xl mx-auto">
          Choose from a wide range of glass and aluminum products. Each category offers premium quality materials with professional installation services.
        </p>
      </div>

      <!-- ✅ Carousel Section -->
      <div class="relative w-full overflow-hidden rounded-3xl shadow-xl max-h-[460px]">
        <div
          class="flex transition-transform duration-700 ease-in-out"
          :style="{ transform: `translateX(-${currentSlide * 100}%)` }"
        >
          <!-- Slides -->
          <div
            v-for="(slide, index) in slides"
            :key="index"
            class="relative min-w-full"
          >
            <img
              :src="slide.src"
              :alt="slide.title"
              class="w-full h-[380px] object-cover"
            />
            <div
              class="absolute bottom-6 left-6 bg-black/60 text-white p-4 rounded-lg"
            >
              <h2 class="text-xl font-semibold">{{ slide.title }}</h2>
              <p class="text-sm">{{ slide.desc }}</p>
            </div>
          </div>
        </div>

        <!-- Controls -->
        <button
          @click="prevSlide"
          class="absolute top-1/2 left-3 -translate-y-1/2 bg-white/60 hover:bg-white text-gray-800 rounded-full p-2 shadow-md"
        >
          <i class="fa-solid fa-chevron-left"></i>
        </button>
        <button
          @click="nextSlide"
          class="absolute top-1/2 right-3 -translate-y-1/2 bg-white/60 hover:bg-white text-gray-800 rounded-full p-2 shadow-md"
        >
          <i class="fa-solid fa-chevron-right"></i>
        </button>

        <!-- Indicators -->
        <div
          class="absolute bottom-4 left-1/2 -translate-x-1/2 flex gap-2"
        >
          <button
            v-for="(_, index) in slides.length"
            :key="index"
            @click="goToSlide(index)"
            class="w-3 h-3 rounded-full transition-all duration-300"
            :class="index === currentSlide ? 'bg-white' : 'bg-gray-400/70'"
          ></button>
        </div>
      </div>

      <!-- Category Cards -->
      <div
        class="flex flex-col sm:flex-row flex-wrap justify-center gap-6"
      >
        <!-- Doors -->
        <div
          class="relative bg-white/80 backdrop-blur-xl border border-sky-100 flex flex-col justify-between h-[380px] w-full max-w-[360px] rounded-3xl items-center p-6 text-gray-800 shadow-2xl transition-all duration-300 hover:scale-105 hover:shadow-xl"
        >
          <div class="flex flex-col items-center text-center gap-4">
            <i class="fa-solid fa-door-open text-6xl text-sky-700"></i>
            <p class="font-bold text-2xl">Doors</p>
            <p class="text-gray-700 text-sm md:text-base">
              Premium glass and aluminum doors including sliding doors, swing doors, and custom entrance solutions for residential and commercial use.
            </p>
          </div>
          <button
            @click="$router.push('/dashboard/doors')"
            class="mt-6 bg-gradient-to-r from-sky-500 to-blue-600 hover:from-sky-600 hover:to-blue-700 text-white font-semibold px-6 py-2.5 rounded-full shadow-md flex items-center justify-center gap-2 transition-all duration-200"
          >
            <i class="fa-solid fa-arrow-right"></i> SELECT DOORS
          </button>
        </div>

        <!-- Windows -->
        <div
          class="relative bg-white/80 backdrop-blur-xl border border-sky-100 flex flex-col justify-between h-[380px] w-full max-w-[360px] rounded-3xl items-center p-6 text-gray-800 shadow-2xl transition-all duration-300 hover:scale-105 hover:shadow-xl"
        >
          <div class="flex flex-col items-center text-center gap-4">
            <i class="fa-regular fa-window-restore text-6xl text-sky-700"></i>
            <p class="font-bold text-2xl">Windows</p>
            <p class="text-gray-700 text-sm md:text-base">
              High-quality windows featuring double-pane glass, aluminum frames, and energy-efficient designs for optimal performance and aesthetics.
            </p>
          </div>
          <button
            @click="$router.push('/dashboard/windows')"
            class="mt-6 bg-gradient-to-r from-sky-500 to-blue-600 hover:from-sky-600 hover:to-blue-700 text-white font-semibold px-6 py-2.5 rounded-full shadow-md flex items-center justify-center gap-2 transition-all duration-200"
          >
            <i class="fa-solid fa-arrow-right"></i> SELECT WINDOWS
          </button>
        </div>

        <!-- Others -->
        <div
          class="relative bg-white/80 backdrop-blur-xl border border-sky-100 flex flex-col justify-between h-[380px] w-full max-w-[360px] rounded-3xl items-center p-6 text-gray-800 shadow-2xl transition-all duration-300 hover:scale-105 hover:shadow-xl"
        >
          <div class="flex flex-col items-center text-center gap-4">
            <i class="fa-solid fa-border-all text-6xl text-sky-700"></i>
            <p class="font-bold text-2xl">Others</p>
            <p class="text-gray-700 text-sm md:text-base">
              Specialized products including casement windows, glass tables, cabinets, partitions, and custom glass and aluminum solutions.
            </p>
          </div>
          <button
            @click="$router.push('/dashboard/others')"
            class="mt-6 bg-gradient-to-r from-sky-500 to-blue-600 hover:from-sky-600 hover:to-blue-700 text-white font-semibold px-6 py-2.5 rounded-full shadow-md flex items-center justify-center gap-2 transition-all duration-200"
          >
            <i class="fa-solid fa-arrow-right"></i> SELECT OTHERS
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import doors from '@/assets/img/door.jpg'
import windows from '@/assets/img/window.jpg'
import others from '@/assets/img/other.jpg'


const slides = [
  {
    src: doors,
    title: 'Elegant Doors',
    desc: 'Stylish and durable glass and aluminum door designs.',
  },
  {
    src: windows,
    title: 'Modern Windows',
    desc: 'Energy-efficient, elegant window solutions.',
  },
  {
    src: others,
    title: 'Custom Creations',
    desc: 'Partitions, tables, and more — tailored to your needs.',
  },
]

const currentSlide = ref(0)

const nextSlide = () => {
  currentSlide.value = (currentSlide.value + 1) % slides.length
}

const prevSlide = () => {
  currentSlide.value =
    (currentSlide.value - 1 + slides.length) % slides.length
}

const goToSlide = (index) => {
  currentSlide.value = index
}

// Auto slide every 5 seconds
let interval
onMounted(() => {
  interval = setInterval(nextSlide, 5000)
})
onUnmounted(() => {
  clearInterval(interval)
})
</script>
