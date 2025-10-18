<script setup lang="ts">
import logo from "@/assets/img/logo.jpg";
</script>

<template>
  <div class="px-4 sm:px-10 md:px-16 flex flex-col gap-10">
    <!-- About Section -->
    <div class="bg-gray-200 w-full rounded-2xl p-6 sm:p-10">
      <div class="flex flex-col gap-5">
        <div class="flex flex-col sm:flex-row items-center sm:items-center gap-3">
          <img :src="logo" alt="logo" class="rounded-2xl h-[60px]" />
          <p class="text-2xl sm:text-3xl font-bold text-center sm:text-left">About</p>
        </div>

        <p class="text-justify text-sm sm:text-base leading-relaxed">
          Glass & Aluminum Supply has been at the forefront of the industry since 2009.
          We specialize in providing high-quality doors, windows, and custom solutions for
          residential, commercial, and industrial applications. Our commitment to excellence,
          innovation, and customer satisfaction has made us a trusted partner for architects,
          contractors, and homeowners throughout the region.
        </p>
      </div>

      <!-- About Cards -->
      <div class="flex flex-wrap justify-center sm:justify-around gap-6 mt-8">
        <div
          v-for="(card, index) in [
            { title: 'Premium Quality', text: 'We source the finest materials and adhere to rigorous quality control standards to ensure our products meet the highest expectations.' },
            { title: 'Expert Craftsmanship', text: 'Our team of skilled professionals has years of experience in crafting and installing glass and aluminum products with precision and attention to detail.' },
            { title: 'Custom Solutions', text: 'We offer tailored solutions to meet the unique needs of our clients, from custom designs to specialized installations.' },
            { title: 'Comprehensive Service', text: 'From consultation to installation, we provide a one-stop-shop experience, ensuring seamless communication and project management.' },
            { title: 'Innovation Focus', text: 'We\'re committed to staying at the forefront of industry trends and technologies, ensuring our products and services are always innovative and effective.' },
            { title: 'Customer Commitment', text: 'Our customers are at the heart of everything we do. We\'re dedicated to delivering exceptional service, support, and value to our clients.' },
          ]"
          :key="index"
          class="flex flex-col w-full sm:w-[300px] bg-white p-6 rounded-2xl gap-3 border-l-4 border-[#006989] shadow-sm hover:shadow-md transition-shadow"
        >
          <p class="text-xl font-bold text-[#006989]">{{ card.title }}</p>
          <p class="text-sm sm:text-base text-gray-700">{{ card.text }}</p>
        </div>
      </div>
    </div>

    <!-- Achievements Section -->
    <div class="bg-gray-200 rounded-2xl p-6 sm:p-10 flex flex-col gap-6">
      <div class="flex flex-col sm:flex-row items-center gap-3">
        <img :src="logo" alt="logo" class="rounded-2xl h-[60px]" />
        <p class="text-2xl sm:text-3xl font-bold text-center sm:text-left">Our Achievements</p>
      </div>

      <div class="flex flex-wrap justify-center sm:justify-around gap-6">
        <div
          v-for="(item, index) in [
            { value: '2,500+', label: 'Projects Completed' },
            { value: '98%', label: 'Customer Satisfaction' },
            { value: '15+', label: 'Years Experience' },
            { value: '50+', label: 'Team Members' },
          ]"
          :key="index"
          class="h-[140px] w-[200px] sm:w-[240px] md:w-[260px] bg-[#006989] rounded-2xl text-white flex flex-col items-center justify-center gap-2 shadow-lg"
        >
          <p class="text-2xl sm:text-3xl font-bold">{{ item.value }}</p>
          <p class="text-sm sm:text-base text-center">{{ item.label }}</p>
        </div>
      </div>
    </div>

    <!-- Timeline Section -->
    <div class="bg-gray-200 rounded-2xl p-6 sm:p-10 flex flex-col gap-8">
      <div class="flex flex-col sm:flex-row items-center gap-3">
        <img :src="logo" alt="logo" class="rounded-2xl h-[60px]" />
        <p class="text-2xl sm:text-3xl font-bold text-center sm:text-left">Company Timeline</p>
      </div>

      <div class="flex flex-col gap-8">
        <div
          v-for="(event, index) in [
            { year: '2009', title: 'Company Founded', desc: 'Glass & Aluminum Supply was established with a vision to provide premium glass and aluminum solutions to the local market.' },
            { year: '2014', title: 'Investing in People', desc: 'We prioritized staff development, providing training and opportunities for growth to ensure our team remained skilled and motivated.' },
            { year: '2016', title: 'Strategic Partnerships', desc: 'We forged partnerships with key suppliers, enabling us to offer more competitive pricing and enhanced services.' },
            { year: '2018', title: 'Innovation and Improvement', desc: 'We invested in R&D, exploring new technologies to improve our products and services.' },
            { year: '2020', title: 'Adapting to Change', desc: 'We navigated pandemic challenges, adapting operations to ensure continuity and customer satisfaction.' },
            { year: '2025', title: 'Digital Transformation', desc: 'We began a digital transformation journey, leveraging technology to enhance efficiency and customer experience.' },
          ]"
          :key="index"
          class="flex flex-col sm:flex-row items-start sm:items-center gap-4 sm:gap-8"
        >
          <p class="font-bold text-lg sm:text-xl bg-[#006989] text-white py-1 px-4 rounded-2xl min-w-[80px] text-center">
            {{ event.year }}
          </p>

          <div class="border-l-4 border-[#006989] rounded-xl pl-5 flex flex-col gap-2">
            <p class="font-bold text-lg sm:text-xl">{{ event.title }}</p>
            <p class="text-sm sm:text-base text-gray-700 leading-relaxed">{{ event.desc }}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
