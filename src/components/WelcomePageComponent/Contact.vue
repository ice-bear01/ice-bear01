<template>
  <div
    class="min-h-screen flex flex-col items-center justify-center text-white p-8"
  >
    <h2 class="text-4xl font-bold mb-4">Contact Us</h2>
    <p class="text-center max-w-xl mb-10 text-gray-200">
      Have questions or need a quote? Reach out through any of the options below
      or send us a direct message.
    </p>

    <!-- Contact Info Cards -->
    <div
      class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 mb-12 w-full max-w-6xl animate-slide-up"
    >
      <!-- Email -->
      <div
        class="bg-white/10 backdrop-blur-md border border-white/20 rounded-2xl shadow-[ -10px_0_15px_#006989 ] p-6 flex flex-col items-center text-center transition-all duration-500 hover:scale-105 hover:shadow-[0_0_25px_#006989]"
      >
        <i class="fa-solid fa-envelope text-4xl text-[#006989] mb-3"></i>
        <h3 class="font-bold text-xl mb-1">Email</h3>
        <p class="text-gray-200">support@glassdesigns.com</p>
      </div>

      <!-- Phone -->
      <div
        class="bg-white/10 backdrop-blur-md border border-white/20 rounded-2xl shadow-[ -10px_0_15px_#006989 ] p-6 flex flex-col items-center text-center transition-all duration-500 hover:scale-105 hover:shadow-[0_0_25px_#006989]"
      >
        <i class="fa-solid fa-phone text-4xl text-[#006989] mb-3"></i>
        <h3 class="font-bold text-xl mb-1">Phone</h3>
        <p class="text-gray-200">+63 912 345 6789</p>
      </div>

      <!-- Location -->
      <div
        class="bg-white/10 backdrop-blur-md border border-white/20 rounded-2xl shadow-[ -10px_0_15px_#006989 ] p-6 flex flex-col items-center text-center transition-all duration-500 hover:scale-105 hover:shadow-[0_0_25px_#006989]"
      >
        <i class="fa-solid fa-location-dot text-4xl text-[#006989] mb-3"></i>
        <h3 class="font-bold text-xl mb-1">Location</h3>
        <p class="text-gray-200">123 Glass St., Makati City, PH</p>
      </div>

      <!-- Hours -->
      <div
        class="bg-white/10 backdrop-blur-md border border-white/20 rounded-2xl shadow-[ -10px_0_15px_#006989 ] p-6 flex flex-col items-center text-center transition-all duration-500 hover:scale-105 hover:shadow-[0_0_25px_#006989]"
      >
        <i class="fa-solid fa-clock text-4xl text-[#006989] mb-3"></i>
        <h3 class="font-bold text-xl mb-1">Working Hours</h3>
        <p class="text-gray-200">Mon–Sat: 8:00 AM – 6:00 PM</p>
      </div>
    </div>

    <!-- Contact Form -->
    <div
      class="bg-white/10 backdrop-blur-md border border-white/20 rounded-2xl shadow-[ -10px_0_15px_#006989 ] p-8 w-full max-w-lg animate-slide-up delay-300"
    >
      <form class="flex flex-col gap-5">
        <div class="flex flex-col">
          <label class="text-sm font-semibold mb-1">Full Name</label>
          <input
            type="text"
            placeholder="Enter your full name"
            class="p-3 rounded-lg bg-white/20 text-white placeholder-gray-300 focus:outline-none focus:ring-2 focus:ring-[#006989]"
          />
        </div>

        <div class="flex flex-col">
          <label class="text-sm font-semibold mb-1">Email</label>
          <input
            type="email"
            placeholder="Enter your email address"
            class="p-3 rounded-lg bg-white/20 text-white placeholder-gray-300 focus:outline-none focus:ring-2 focus:ring-[#006989]"
          />
        </div>

        <div class="flex flex-col">
          <label class="text-sm font-semibold mb-1">Message</label>
          <textarea
            rows="4"
            placeholder="Type your message here..."
            class="p-3 rounded-lg bg-white/20 text-white placeholder-gray-300 focus:outline-none focus:ring-2 focus:ring-[#006989]"
          ></textarea>
        </div>

        <button
          type="submit"
          class="mt-3 bg-[#006989] hover:bg-[#00526c] transition-all duration-300 text-white font-semibold py-3 rounded-lg shadow-lg hover:shadow-[0_0_25px_#006989]"
        >
          Send Message
        </button>
      </form>
    </div>
  </div>
</template>

<style scoped>
@keyframes slideUp {
  0% {
    transform: translateY(40px);
    opacity: 0;
  }
  100% {
    transform: translateY(0);
    opacity: 1;
  }
}

.animate-slide-up {
  animation: slideUp 0.8s ease-out both;
}

.delay-300 {
  animation-delay: 0.3s;
}
</style>
