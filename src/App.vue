<script setup lang="ts">
import { useLoadingStore } from '@/store/loading';

const loading = useLoadingStore()
</script>

<template>
  <div 
    v-if="loading.isLoading" 
    class="absolute z-100 inset-0 flex items-center justify-center bg-black/50 text-white"
  >
    <i class="fa-solid fa-spinner fa-spin-pulse text-4xl"></i>
  </div>
  <div class="h-full w-full bg-[#006989]">
    <router-view />
  </div>
</template>