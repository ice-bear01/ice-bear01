<template>
  <div class="flex flex-col items-center gap-5 py-10">
    <p class="text-3xl font-bold text-white">Select Your Category</p>
    <p class="text-white text-center max-w-2xl">
      Choose from a wide range of glass and aluminum products. Each category offers premium quality materials with professional installation services.
    </p>

    <div class="flex flex-col sm:flex-row justify-around flex-wrap gap-6">
      <!-- CARD: Doors -->
      <div
        class="relative bg-white/10 backdrop-blur-md border border-white/20 flex flex-col justify-between h-[380px] w-[360px] rounded-2xl items-center p-5 text-white shadow-md transition-all duration-700 hover:shadow-[0_0_40px_rgba(255,255,255,0.5)] hover:scale-105 group overflow-hidden animate-slide-down"
      >
        <!-- Shine Effect -->
        <div
          class="absolute inset-0 bg-gradient-to-r from-transparent via-white/30 to-transparent translate-x-[-100%] group-hover:translate-x-[100%] transition-transform duration-1000 ease-in-out"
        ></div>

        <!-- Content -->
        <div class="flex flex-col items-center text-center gap-3">
          <i class="fa-solid fa-door-open text-6xl"></i>
          <p class="font-bold text-2xl">Doors</p>
          <p class="text-gray-100">
            Premium glass and aluminum doors including sliding doors, swing doors, and custom entrance solutions for residential and commercial use.
          </p>
        </div>

        <!-- Button -->
        <button
          @click="$router.push('/dashboard/doors')"
          class="mt-4 border border-white/40 rounded-lg px-4 py-2 text-white hover:bg-[#006989] hover:shadow-lg transition-all duration-300"
        >
          SELECT DOORS
        </button>
      </div>

      <!-- CARD: Windows -->
      <div
        class="relative bg-white/10 backdrop-blur-md border border-white/20 flex flex-col justify-between h-[380px] w-[360px] rounded-2xl items-center p-5 text-white shadow-md transition-all duration-700 hover:shadow-[0_0_40px_rgba(255,255,255,0.5)] hover:scale-105 group overflow-hidden animate-slide-down delay-200"
      >
        <div
          class="absolute inset-0 bg-gradient-to-r from-transparent via-white/30 to-transparent translate-x-[-100%] group-hover:translate-x-[100%] transition-transform duration-1000 ease-in-out"
        ></div>

        <div class="flex flex-col items-center text-center gap-3">
          <i class="fa-regular fa-window-restore text-6xl"></i>
          <p class="font-bold text-2xl">Windows</p>
          <p class="text-gray-100">
            High-quality windows featuring double-pane glass, aluminum frames, and energy-efficient designs for optimal performance and aesthetics.
          </p>
        </div>

        <button
          @click="$router.push('/dashboard/windows')"
          class="mt-4 border border-white/40 rounded-lg px-4 py-2 text-white hover:bg-[#006989] hover:shadow-lg transition-all duration-300"
        >
          SELECT WINDOWS
        </button>
      </div>

      <!-- CARD: Others -->
      <div
        class="relative bg-white/10 backdrop-blur-md border border-white/20 flex flex-col justify-between h-[380px] w-[360px] rounded-2xl items-center p-5 text-white shadow-md transition-all duration-700 hover:shadow-[0_0_40px_rgba(255,255,255,0.5)] hover:scale-105 group overflow-hidden animate-slide-down delay-500"
      >
        <div
          class="absolute inset-0 bg-gradient-to-r from-transparent via-white/30 to-transparent translate-x-[-100%] group-hover:translate-x-[100%] transition-transform duration-1000 ease-in-out"
        ></div>

        <div class="flex flex-col items-center text-center gap-3">
          <i class="fa-solid fa-border-all text-6xl"></i>
          <p class="font-bold text-2xl">Others</p>
          <p class="text-gray-100">
            Specialized products including casement windows, glass tables, cabinets, partitions, and custom glass and aluminum solutions.
          </p>
        </div>

        <button
          @click="$router.push('/dashboard/others')"
          class="mt-4 border border-white/40 rounded-lg px-4 py-2 text-white hover:bg-[#006989] hover:shadow-lg transition-all duration-300"
        >
          SELECT OTHERS
        </button>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* Slide-down animation when page reloads */
@keyframes slideDown {
  0% {
    transform: translateY(-50px);
    opacity: 0;
  }
  100% {
    transform: translateY(0);
    opacity: 1;
  }
}

.animate-slide-down {
  animation: slideDown 0.8s ease-out both;
}

.delay-200 {
  animation-delay: 0.2s;
}
.delay-500 {
  animation-delay: 0.5s;
}
</style>
