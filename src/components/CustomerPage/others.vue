<script setup lang="ts">
import { ref } from 'vue'
import AllOthers from './ProductType/AllOthers.vue'

const currentOthersComponent = ref<any>(AllOthers)
const searchOthers = ref('')
const selectedType = ref('All')
const productTypes = ["Glass Tabletops", "Mirrors", "Shelving","Railing","Panel","Frame","Display Cases", "Others"]

const dropdownOpen = ref(false)

function selectType(type: string) {
  selectedType.value = type
  dropdownOpen.value = false
}
</script>

<template>
  <div class="flex flex-col gap-10 p-6 sm:p-10">
    <!-- Header -->
    <div class="flex flex-col gap-3 text-center">
      <p class="font-bold text-3xl sm:text-4xl text-white">Others</p>
      <p class="max-w-xl mx-auto text-white/80 text-sm sm:text-base">
        Explore our extensive collection of premium glass and aluminum products.
      </p>
    </div>

    <!-- Filters -->
    <div
      class="w-full rounded-3xl bg-white/80 backdrop-blur-xl border border-sky-100 flex flex-col sm:flex-row items-center gap-4 sm:gap-6 py-4 px-6 sm:px-10 shadow-2xl"
    >
      <!-- Dropdown -->
      <div class="relative w-full sm:w-48">
        <button
          @click="dropdownOpen = !dropdownOpen"
          class="w-full px-4 py-3 bg-white/20 text-gray-800 rounded-3xl border border-white/30 flex justify-between items-center hover:bg-white/30 transition"
        >
          <span>{{ selectedType }}</span>
          <svg
            class="w-5 h-5 ml-2 transform transition-transform"
            :class="{ 'rotate-180': dropdownOpen }"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
          </svg>
        </button>

        <!-- Dropdown List -->
        <div
          v-if="dropdownOpen"
          class="absolute mt-2 w-full bg-white/80 backdrop-blur-xl border border-sky-100 rounded-2xl overflow-hidden z-50"
        >
          <div
            v-for="type in productTypes"
            :key="type"
            @click="selectType(type)"
            class="px-4 py-3 cursor-pointer hover:bg-white/30 transition text-gray-800 text-sm sm:text-base"
          >
            {{ type }}
          </div>
        </div>
      </div>

      <!-- Search -->
      <div class="w-full sm:w-auto flex-1 sm:flex-initial">
        <input
          type="text"
          v-model="searchOthers"
          placeholder="Search..."
          class="w-full sm:w-64 px-5 py-3 rounded-3xl bg-white/20 backdrop-blur-xl border border-sky-100 placeholder-gray-500 text-gray-800 focus:outline-none focus:ring-2 focus:ring-sky-200 transition"
        />
      </div>
    </div>

    <!-- Others Component -->
    <div class="w-full mt-4">
      <component
        :is="currentOthersComponent"
        :search-query="searchOthers"
        :selected-type="selectedType"
        :key="currentOthersComponent"
      />
    </div>
  </div>
</template>

<style scoped>
/* Handle dropdown on smaller devices */
@media (max-width: 640px) {
  .dropdown-menu {
    position: fixed !important;
    left: 10%;
    right: 10%;
    top: 50%;
    transform: translateY(-50%);
  }
}
</style>
