<script setup lang="ts">
import { useRoute, useRouter } from "vue-router";
import logo from "@/assets/img/logo.jpg";
import axios from "axios";
import { ref, onMounted } from "vue";

const route = useRoute();
const router = useRouter();

const navItems = [
  { name: "Dashboard", path: "/admin/dashboard" },
  { name: "Product Management", path: "/admin/product-management" },
  { name: "Order Management Panel", path: "/admin/order-management" },
  { name: "Recent Activities", path: "/admin/recent-activities" },
];

const adminEmail = ref(""); // <-- admin email here

const goTo = (path: string) => {
  router.push(path);
};

// ---------------- Logout ----------------
const logout = async () => {
  try {
    await axios.post(
      "http://localhost:8000/users/auth/admin/logout",
      {},
      { withCredentials: true }
    );
    router.push("/admin/login");
  } catch (err) {
    console.error("Logout failed:", err);
    alert("Logout failed. Please try again.");
  }
};

// ---------------- Fetch Admin Email ----------------
const fetchAdminEmail = async () => {
  try {
    const res = await axios.get("http://localhost:8000/users/admin/profile", {
      withCredentials: true,
    });
    adminEmail.value = res.data.email;
  } catch (err) {
    console.error("Failed to fetch admin email:", err);
    adminEmail.value = "Unknown";
    router.push('/')
  }
};

// Fetch admin email on mount
onMounted(() => {
  fetchAdminEmail();
});
</script>

<template>
  <!-- Main container -->
  <div class="h-full w-full flex flex-col overflow-hidden">
    
    <!-- Navbar -->
    <nav
      class="h-[80px] w-full flex bg-[#eaebed] flex-row justify-between items-center px-4 shadow-2xl sticky top-0 z-50"
    >
      <div class="flex flex-row items-center gap-2">
        <img :src="logo" alt="logo" class="h-[50px] rounded-2xl" />
        <p class="font-bold text-2xl text-[#006989] underline">
          3J's Glass & Aluminum Supply
        </p>
      </div>
      <div class="flex items-center gap-5">
        <!-- Display admin email -->
        <p class="font-semibold text-gray-700">Logged in as: {{ adminEmail }}</p>

        <button
          @click="logout"
          class="font-bold hover:bg-[#006989] hover:text-white py-2 px-4 rounded-2xl transition"
        >
          Log-Out
        </button>
      </div>
    </nav>

    <!-- Main Content -->
    <div
      class="flex-1 overflow-y-auto px-5 sm:px-20 flex flex-col gap-10 pt-10"
    >
      <p class="text-white text-3xl sm:text-4xl text-center font-bold">
        3J's Admin Management
      </p>

      <!-- Button section -->
      <div
        class="w-full bg-gray-200 rounded p-5 flex flex-row items-center justify-around overflow-visible"
      >
        <!-- Render all buttons dynamically -->
        <div
          v-for="(item, index) in navItems"
          :key="index"
          class="relative group"
        >
          <button
            @click="goTo(item.path)"
            class="font-bold border transition-colors duration-200 py-2 px-4 rounded truncate max-w-[150px]"
            :class="[route.path === item.path
              ? 'border-[#006989] text-[#006989]'
              : 'border-transparent hover:border-[#006989]']"
          >
            {{ item.name }}
          </button>

          <!-- Tooltip -->
          <span
            class="absolute left-1/2 -translate-x-1/2 bottom-full mb-2 w-max px-3 py-1 text-sm text-white bg-gray-900 rounded opacity-0 group-hover:opacity-100 transition-opacity duration-200 z-50"
          >
            {{ item.name }}
          </span>
        </div>
      </div>

      <!-- Router View -->
      <div class="w-full h-full">
        <router-view />
      </div>
    </div>
  </div>
</template>
