<script setup lang="ts">
import Home from './WelcomePageComponent/Home.vue';
import About from './WelcomePageComponent/About.vue';
import Contact from './WelcomePageComponent/Contact.vue';
import logo from '@/assets/img/logo.jpg';

import { ref, onMounted, onBeforeUnmount } from 'vue';

const HomeRef = ref<HTMLElement | null>(null);
const AboutRef = ref<HTMLElement | null>(null);
const ContactRef = ref<HTMLElement | null>(null);

const activeSection = ref('home');
const isMenuOpen = ref(false);

const scrollTo = (section: HTMLElement | null) => {
  if (section) {
    section.scrollIntoView({ behavior: 'smooth', block: 'start' });
    isMenuOpen.value = false;
  }
};

let observer: IntersectionObserver | null = null;

onMounted(() => {
  const options = { root: null, threshold: 0.5 };

  observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        switch (entry.target) {
          case HomeRef.value:
            activeSection.value = 'home';
            break;
          case AboutRef.value:
            activeSection.value = 'about';
            break;
          case ContactRef.value:
            activeSection.value = 'contact';
            break;
        }
      }
    });
  }, options);

  if (HomeRef.value) observer.observe(HomeRef.value);
  if (AboutRef.value) observer.observe(AboutRef.value);
  if (ContactRef.value) observer.observe(ContactRef.value);
});

onBeforeUnmount(() => {
  if (observer) observer.disconnect();
});
</script>

<template>
  <div class="min-h-screen w-full flex flex-col">
    <!-- Navbar -->
    <nav class="h-20 w-full flex justify-between items-center px-6 bg-gradient-to-r from-sky-100 to-white shadow-lg sticky top-0 z-50 rounded-b-2xl border-b border-sky-200">
      <!-- Logo -->
      <div class="flex flex-row h-full items-center gap-2 cursor-pointer" @click="scrollTo(HomeRef)">
        <img :src="logo" alt="logo" class="h-[50px] rounded-2xl">
        <p class="font-bold text-xl sm:text-2xl text-[#006989] pr-5">3J's Glass & Aluminum Supply</p>
      </div>

      <!-- Desktop Navigation -->
      <div class="hidden md:flex h-full items-center justify-center gap-5">
        
        <button @click="scrollTo(HomeRef)"
          class="cursor-pointer font-bold transition-colors duration-300"
          :class="[activeSection === 'home' ? 'text-[#006989]' : 'text-black']">
          Home
        </button>

        <button @click="scrollTo(AboutRef)"
          class="cursor-pointer font-bold transition-colors duration-300"
          :class="[activeSection === 'about' ? 'text-[#006989]' : 'text-black']">
          About
        </button>

        <button @click="scrollTo(ContactRef)"
          class="cursor-pointer font-bold transition-colors duration-300"
          :class="[activeSection === 'contact' ? 'text-[#006989]' : 'text-black']">
          Contact Us
        </button>

        <div class="flex gap-2">
          <button class="cursor-pointer bg-gray-900 rounded px-4 py-1.5 text-white" @click="$router.push('/login')">Log-in</button>
          <button class="cursor-pointer font-bold border-1 rounded px-4 py-1.5" @click="$router.push('/signup')">Sign-up</button>
        </div>
      </div>

      <!-- Mobile Menu Icon -->
      <button @click="isMenuOpen = true" class="cursor-pointer md:hidden text-3xl text-[#006989]">
        <i class="fa-solid fa-bars"></i>
      </button>
    </nav>

    <!-- Modal Menu (Mobile) -->
    <div v-if="isMenuOpen" class="fixed inset-0 bg-black/50 flex items-center justify-center z-[60]">
      <div class="bg-white w-80 rounded-2xl p-6 relative flex flex-col gap-4 shadow-xl">
        
        <button @click="isMenuOpen = false"
          class="cursor-pointer absolute top-3 right-3 text-2xl text-gray-600 hover:text-[#006989]">
          <i class="fa-solid fa-xmark"></i>
        </button>

        <p class="text-center font-bold text-xl text-[#006989] mb-2">Menu</p>

        <button @click="scrollTo(HomeRef)" class="cursor-pointer py-2 text-lg font-semibold text-gray-800 hover:text-[#006989]">
          Home
        </button>
        <button @click="scrollTo(AboutRef)" class="cursor-pointer py-2 text-lg font-semibold text-gray-800 hover:text-[#006989]">
          About
        </button>
        <button @click="scrollTo(ContactRef)" class="cursor-pointer py-2 text-lg font-semibold text-gray-800 hover:text-[#006989]">
          Contact Us
        </button>

        <hr>

        <button @click="$router.push('/login')" class="cursor-pointer bg-gray-900 text-white py-2 rounded-lg">Log-in</button>
        <button @click="$router.push('/signup')" class="cursor-pointer border border-[#006989] text-[#006989] py-2 rounded-lg font-bold">
          Sign-up
        </button>

      </div>
    </div>

    <!-- Content Sections -->
    <div class="flex-1">
      <section ref="HomeRef" class="min-h-screen scroll-mt-[80px]">
        <Home />
      </section>
      <section ref="AboutRef" class="min-h-screen scroll-mt-[80px]">
        <About />
      </section>
      <section ref="ContactRef" class="min-h-screen scroll-mt-[80px]">
        <Contact />
      </section>
    </div>

    <!-- Footer -->
    <footer class="bg-gray-900 text-white py-10 border-t-4 border-[#006989] shadow-[inset_0_6px_0_#006989]">
      <div class="max-w-7xl mx-auto px-6 flex flex-col md:flex-row justify-between items-start md:items-center gap-8">
        
        <div class="flex flex-col items-start">
          <h2 class="text-2xl font-bold text-[#006989] mb-2">Glass</h2>
          <p class="text-gray-300 max-w-sm">
            High-quality glass and aluminum designs made for modern architecture. Durable, elegant, and built with passion.
          </p>
        </div>

        <div class="flex flex-col sm:flex-row gap-8">
          <div>
            <h3 class="font-semibold text-[#006989] mb-3">Contact Info</h3>
            <ul class="space-y-2 text-gray-300">
              <li><i class="fa-solid fa-envelope text-[#006989] mr-2"></i> support@glassdesigns.com</li>
              <li><i class="fa-solid fa-phone text-[#006989] mr-2"></i> +63 912 345 6789</li>
              <li><i class="fa-solid fa-location-dot text-[#006989] mr-2"></i>Zone-5, Bulan, Sorsogon, PH</li>
            </ul>
          </div>
        </div>

        <div class="flex flex-col items-start">
          <h3 class="font-semibold text-[#006989] mb-3">Follow Us</h3>
          <div class="flex gap-4">
            <a href="#" class="cursor-pointer hover:text-[#006989] transition-colors text-xl"><i class="fa-brands fa-facebook"></i></a>
            <a href="#" class="cursor-pointer hover:text-[#006989] transition-colors text-xl"><i class="fa-brands fa-instagram"></i></a>
            <a href="#" class="cursor-pointer hover:text-[#006989] transition-colors text-xl"><i class="fa-brands fa-twitter"></i></a>
            <a href="#" class="cursor-pointer hover:text-[#006989] transition-colors text-xl"><i class="fa-brands fa-linkedin"></i></a>
          </div>
        </div>

      </div>

      <div class="text-center mt-10 text-gray-400 text-sm border-t border-[#006989]/40 pt-6">
        © {{ new Date().getFullYear() }} Glass. All rights reserved.
      </div>
    </footer>
  </div>
</template>
