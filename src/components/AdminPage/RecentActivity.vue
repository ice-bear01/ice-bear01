<script setup>
import { ref, onMounted } from "vue";
import axios from "axios";

const userActivities = ref([]);

const backend = import.meta.env.VITE_BACKEND_URL;

const fetchRecentActivities = async () => {
  try {
    const response = await axios.get(`${backend}/admin/recent_activity`, {
      withCredentials: true, // include cookies if needed
    });
    // Format the data for display
    userActivities.value = response.data.map((item) => ({
      id: item.id,
      user_email: item.user_email,
      action: item.action,
      details: item.detail, // match your FastAPI field name
      time: new Date(item.created_at).toLocaleString("en-PH", {
        hour12: true,
        dateStyle: "medium",
        timeStyle: "short",
      }),
    }));
  } catch (error) {
    console.error("Error fetching recent activities:", error);
  }
};

onMounted(() => {
  fetchRecentActivities();
});

// 🎨 Icon and color functions
const getActivityIcon = (action) => {
  const act = action.toLowerCase();
  if (act.includes("order")) return "fa-cart-shopping";
  if (act.includes("sign")) return "fa-user-plus";
  if (act.includes("address")) return "fa-location-dot";
  if (act.includes("feedback")) return "fa-message";
  return "fa-circle-check";
};

const getActivityColor = (action) => {
  const act = action.toLowerCase();
  if (act.includes("order")) return "text-green-400";
  if (act.includes("sign")) return "text-blue-400";
  if (act.includes("feedback")) return "text-yellow-400";
  if (act.includes("address")) return "text-purple-400";
  return "text-gray-300";
};
</script>

<template>
  <div
    class="bg-gray-900 text-white p-6 rounded-xl shadow-md h-screen overflow-y-auto relative mb-5"
  >
    <h2 class="text-xl font-bold mb-4 flex items-center gap-2">
      <i class="fa-solid fa-clock-rotate-left"></i>
      User Recent Activity
    </h2>

    <ul class="space-y-4">
      <li
        v-for="activity in userActivities"
        :key="activity.id"
        class="flex items-start gap-3 border-b border-gray-700 pb-3"
      >
        <!-- Icon -->
        <div
          class="w-10 h-10 flex items-center justify-center rounded-full bg-[#374151]"
        >
          <i
            :class="[
              'fa-solid',
              getActivityIcon(activity.action),
              getActivityColor(activity.action),
              'text-lg',
            ]"
          ></i>
        </div>

        <!-- Activity Info -->
        <div class="flex-1">
          <p class="text-sm">
            <span class="font-semibold text-gray-200">{{ activity.user_email }}</span>
            <span class="text-gray-400"> {{ activity.action }} </span>
          </p>
          <p class="text-xs text-blue-400">{{ activity.details }}</p>
          <p class="text-xs text-gray-500 mt-1">🕒 {{ activity.time }}</p>
        </div>
      </li>
    </ul>

    <!-- Empty -->
    <div
      v-if="userActivities.length === 0"
      class="text-center text-gray-400 mt-6"
    >
      No recent user activity yet.
    </div>
  </div>
</template>
