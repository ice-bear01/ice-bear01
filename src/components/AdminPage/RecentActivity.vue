<script setup>
import { ref } from "vue";

const userActivities = ref([
  {
    id: 1,
    user_email: "ruzhell@example.com",
    action: "placed an order",
    details: "Order #1024 — Steel Door",
    time: "5 minutes ago",
  },
  {
    id: 2,
    user_email: "mikaela@example.com",
    action: "signed up",
    details: "New account created",
    time: "10 minutes ago",
  },
  {
    id: 3,
    user_email: "ruzhell@example.com",
    action: "updated profile",
    details: "Changed profile picture",
    time: "30 minutes ago",
  },
  {
    id: 4,
    user_email: "carlo@example.com",
    action: "added new address",
    details: "Cebu City, Philippines",
    time: "1 hour ago",
  },
  {
    id: 5,
    user_email: "ruzhell@example.com",
    action: "canceled an order",
    details: "Order #1025 — Glass Window",
    time: "2 hours ago",
  },
    {
    id: 5,
    user_email: "ruzhell@example.com",
    action: "canceled an order",
    details: "Order #1025 — Glass Window",
    time: "2 hours ago",
  },
    {
    id: 5,
    user_email: "ruzhell@example.com",
    action: "canceled an order",
    details: "Order #1025 — Glass Window",
    time: "2 hours ago",
  },
]);

const getActivityIcon = (action) => {
  if (action.includes("order")) return "fa-cart-shopping";
  if (action.includes("signed up")) return "fa-user-plus";
  if (action.includes("updated profile")) return "fa-user-pen";
  if (action.includes("added new address")) return "fa-location-dot";
  if (action.includes("canceled")) return "fa-cart-shopping";
  return "fa-circle-check";
};

const getActivityColor = (action) => {
  if (action.includes("order")) return "text-green-400";
  if (action.includes("signed up")) return "text-blue-400";
  if (action.includes("updated profile")) return "text-yellow-400";
  if (action.includes("added new address")) return "text-purple-400";
  if (action.includes("canceled")) return "text-red-500";
  return "text-gray-300";
};
</script>

<template>
  <div
    class="bg-[#1f2937] text-white p-6 rounded-xl shadow-md h-screen overflow-y-auto relative"
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
