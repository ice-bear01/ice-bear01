<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount } from "vue";
import logo from "@/assets/img/logo.jpg";
import OrderConfirmationModal from "../modal/OrderConfirmationModal.vue";
import { useOrderStore } from "@/store/order";
import router from "@/router";
import axios from "axios";

const orderStore = useOrderStore();
const backend = import.meta.env.VITE_BACKEND_URL
// state to toggle dropdown visibility
const showMenu = ref(false);

// toggle menu
const toggleMenu = () => {
  showMenu.value = !showMenu.value;
};

// close menu when clicking outside
const closeMenu = (event: MouseEvent) => {
  const target = event.target as HTMLElement;
  if (!target.closest(".menu-container")) {
    showMenu.value = false;
  }
};

onMounted(() => {
  document.addEventListener("click", closeMenu);
});
onBeforeUnmount(() => {
  document.removeEventListener("click", closeMenu);
});

const goToProfile = () => {
  showMenu.value = false;
  router.push("/dashboard/user-profile");
};
const goToHome = () => {
  showMenu.value = false;
  router.push("/dashboard");
};
const goToFeedback = () => {
  showMenu.value = false;
  router.push("/dashboard/feedback");
};
const logout = async () => {
  showMenu.value = false;
  await axios.post(`${backend}/users/auth/logout`, { withCredentials: true });
  router.push("/login");
};
</script>

<template>
  <div class="flex flex-col min-h-screen">
    <!-- Order Modal -->
    <OrderConfirmationModal v-if="orderStore.showModal" />

    <!-- Navbar -->
    <nav
      class="h-20 w-full flex justify-between items-center px-6 bg-gradient-to-r from-sky-100 to-white shadow-lg sticky top-0 z-50 rounded-b-2xl border-b border-sky-200">
      <!-- Logo & Name -->
      <div class="flex items-center gap-3 cursor-pointer" @click="$router.push('/dashboard/home')">
        <img :src="logo" alt="Logo" class="h-14 w-14 rounded-xl shadow-sm object-cover" />
        <h1 class="font-bold sm:text-2xl text-sky-800 underline">3J's Glass & Aluminum Supply</h1>
      </div>

      <!-- Menu Buttons -->
      <div class="flex items-center gap-4 menu-container relative">
        <button @click="$router.push('/dashboard/track-order')"
          class="font-semibold text-sky-700 hover:text-white hover:bg-sky-600 px-4 py-2 rounded-lg transition-all duration-200 shadow-sm hover:shadow-md">
          Track Order
        </button>

        <!-- Dropdown Toggle -->
        <button @click.stop="toggleMenu"
          class="p-2 rounded-full hover:bg-gray-200 transition flex items-center justify-center">
          <i class="fa-solid fa-bars text-2xl text-gray-700"></i>
        </button>

        <!-- Dropdown Menu -->
        <transition name="fade">
          <div v-if="showMenu"
            class="absolute top-14 right-0 w-48 flex bg-white rounded-xl shadow-lg border border-gray-200 z-50 overflow-hidden">
            <ul class="flex flex-col w-full">
              <li>
                <button @click="goToProfile"
                  class="flex items-center px-4 py-2 hover:bg-sky-50 text-gray-800 font-medium w-full">
                  <i class="fa-solid fa-user w-6 flex-shrink-0"></i>
                  <span class="ml-2">Profile</span>
                </button>
              </li>
              <li>
                <button @click="goToHome" class="flex items-center px-4 py-2 hover:bg-sky-50 text-gray-800 font-medium w-full">
                  <i class="fa-solid fa-home w-6 flex-shrink-0"></i>
                  <span class="ml-2">Home</span>
                </button>
              </li>
                            <li>
                <button @click="goToFeedback" class="flex items-center px-4 py-2 hover:bg-sky-50 text-gray-800 font-medium w-full">
                  <i class="fa-solid fa-message w-6 flex-shrink-0"></i>
                  <span class="ml-2">Feedback</span>
                </button>
              </li>
              <li>
                <button @click="logout" class="flex items-center px-4 py-2 hover:bg-red-100 text-red-600 font-medium w-full">
                  <i class="fa-solid fa-right-from-bracket w-6 flex-shrink-0"></i>
                  <span class="ml-2">Logout</span>
                </button>
              </li>
            </ul>
          </div>
        </transition>

      </div>
    </nav>

    <!-- Router Content -->
    <div class="flex-1 p-4 sm:p-8">
      <router-view />
    </div>
  </div>
</template>

<style scoped>
/* Smooth fade for dropdown */
.fade-enter-active,
.fade-leave-active {
  transition: all 0.2s ease-in-out;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}
</style>
