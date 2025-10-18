<script setup lang="ts">
import HomeImg from "@/assets/img/web-page-img/HomeImg.png";
</script>

<template>
  <main class="py-16 md:py-24 px-4 md:px-10 bg-[#006989]">
    <div class="flex flex-col-reverse lg:flex-row items-center justify-between gap-10 lg:gap-20 max-w-7xl mx-auto">

      <!-- Left Content -->
      <div class="w-full lg:w-1/2 text-white text-center lg:text-left">
        <h1 class="text-3xl sm:text-4xl md:text-5xl font-light leading-tight">
          Welcome to <br />
          <strong class="font-semibold text-4xl sm:text-5xl md:text-6xl italic block mt-2">
            Glass & Aluminum Solutions
          </strong>
        </h1>

        <hr class="w-24 md:w-40 border-t-4 border-white my-6 mx-auto lg:mx-0">

        <p class="text-base sm:text-lg mt-4 max-w-md mx-auto lg:mx-0 leading-relaxed">
          Professional ordering and tracking system for all your glass and aluminum supply needs.
          Quality products, reliable service, seamless experience.
        </p>
      </div>

      <!-- Right Image -->
      <div class="w-full lg:w-1/2 flex justify-center">
        <img
          :src="HomeImg"
          alt="Glass and Aluminum"
          class="w-full max-w-[350px] sm:max-w-[450px] md:max-w-[550px] lg:max-w-[600px] object-contain drop-shadow-2xl"
        />
      </div>
    </div>
  </main>
</template>
