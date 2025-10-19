<script setup>
import { ref, onMounted, watch } from "vue";
import VueApexCharts from "vue3-apexcharts";

// ---------------- Summary Cards ----------------
const pendingOrders = ref(0);
const newCustomers = ref(0);
const backend = import.meta.env.VITE_BACKEND_URL
// ---------------- Donut Chart ----------------
const donutSeries = ref([]);
const donutLabels = ref([]);
const donutOptions = ref({
  chart: { type: "donut" },
  labels: [],
  legend: { position: "bottom", labels: { colors: "#ffffff" } },
  dataLabels: { enabled: true },
  colors: ["#3b82f6", "#10b981", "#f59e0b"],
});

// ---------------- Bar Chart ----------------
const barSeries = ref([{ name: "Orders", data: [] }]);
const barCategories = ref([]);
const barOptions = ref({
  chart: { type: "bar", height: 350, toolbar: { show: false } },
  plotOptions: { bar: { borderRadius: 6, columnWidth: "50%" } },
  dataLabels: { enabled: false },
  xaxis: { categories: [], labels: { style: { colors: "#ffffff" } } },
  yaxis: { labels: { style: { colors: "#ffffff" } } },
  grid: { borderColor: "#374151" },
  colors: ["#22c55e"],
  legend: { show: true, labels: { colors: "#ffffff" } },
});

// ---------------- Line Chart ----------------
const lineSeries = ref([{ name: "Sales", data: [] }]);
const lineCategories = ref([]);
const lineOptions = ref({
  chart: { type: "line", height: 350, toolbar: { show: false } },
  stroke: { curve: "smooth", width: 3 },
  xaxis: { categories: [], labels: { style: { colors: "#ffffff" } } },
  yaxis: { labels: { style: { colors: "#ffffff" } } },
  grid: { borderColor: "#374151" },
  colors: ["#f59e0b"],
  legend: { show: true, labels: { colors: "#ffffff" } },
});

// ---------------- Fetch Functions ----------------
const fetchDashboardData = async () => {
  try {
    const res = await fetch(`${backend}/orders/dashboard-data`);
    const data = await res.json();

    // Donut: Most ordered product categories
    const categoryMap = {};
    data.forEach(row => {
      categoryMap[row.product_category] = (categoryMap[row.product_category] || 0) + Number(row.product_quantity);
    });
    donutLabels.value = Object.keys(categoryMap);
    donutSeries.value = Object.values(categoryMap);
    donutOptions.value = { ...donutOptions.value, labels: donutLabels.value };

    // Bar: Orders per weekday
    const weekdays = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];
    const dayMap = { Sun: 0, Mon: 0, Tue: 0, Wed: 0, Thu: 0, Fri: 0, Sat: 0 };

    data.forEach(row => {
      const day = new Date(row.order_date).toLocaleDateString("en-US", { weekday: "short" });
      dayMap[day] = (dayMap[day] || 0) + Number(row.product_quantity);
    });

    // Ensure series matches weekdays order
    barCategories.value = weekdays;
    barSeries.value[0].data = weekdays.map(d => dayMap[d] || 0);
    barOptions.value = { ...barOptions.value, xaxis: { ...barOptions.value.xaxis, categories: barCategories.value } };


    // Line: Sales per weekday
    const salesMap = {};
    data.forEach(row => {
      const day = new Date(row.order_date).toLocaleDateString("en-US", { weekday: "short" });
      salesMap[day] = (salesMap[day] || 0) + Number(row.product_price) * Number(row.product_quantity);
    });
    lineCategories.value = Object.keys(salesMap);
    lineSeries.value[0].data = Object.values(salesMap);
    lineOptions.value = { ...lineOptions.value, xaxis: { ...lineOptions.value.xaxis, categories: lineCategories.value } };

  } catch (err) {
    console.error("Failed to fetch dashboard data", err);
  }
};

const fetchPendingOrders = async () => {
  try {
    const res = await fetch(`${backend}/orders/pending-orders-count`);
    const data = await res.json();
    pendingOrders.value = data.pending_count;
  } catch (err) {
    console.error("Failed to fetch pending orders count", err);
  }
};

const fetchNewCustomerCount = async () => {
  try {
    const res = await fetch(`${backend}/users/new-customer-count`);
    const data = await res.json();
    newCustomers.value = data.today_new_customers;
  } catch (err) {
    console.error("Failed to fetch new customer count", err);
  }
};

onMounted(() => {
  fetchDashboardData();
  fetchPendingOrders();
  fetchNewCustomerCount();
});
</script>

<template>
  <div class="h-full w-full flex flex-col pb-5 gap-8">
    <p class="text-3xl text-white font-bold">Admin Dashboard Overview</p>

    <div class="flex flex-row gap-6">
      <!-- Summary Cards -->
      <div class="flex flex-col justify-between gap-6 w-1/3">
        <div class="bg-orange-400 p-6 rounded-xl flex flex-col gap-2 shadow h-full">
          <p class="text-white font-bold text-xl">Pending Orders</p>
          <p class="text-white">Pending: {{ pendingOrders }}</p>
        </div>
        <div class="bg-purple-600 p-6 rounded-xl flex flex-col gap-2 shadow h-full">
          <p class="text-white font-bold text-xl">New Customer Sign-up</p>
          <p class="text-white">Today: {{ newCustomers }}</p>
        </div>
      </div>

      <!-- Sales Line Chart -->
      <div class="flex-1 bg-[#1f2937] p-5 rounded-xl">
        <p class="text-white text-xl font-bold mb-4">Sales This Week</p>
        <div class="rounded-lg p-4">
          <VueApexCharts type="line" height="350" :options="lineOptions" :series="lineSeries" />
        </div>
      </div>
    </div>

    <!-- Donut + Bar Charts -->
    <div class="flex flex-row gap-6">
      <!-- Donut Chart -->
      <div class="flex-1 bg-[#1f2937] p-5 rounded-xl">
        <p class="text-white text-xl font-bold mb-4">Most Ordered Product Categories</p>
        <div class="rounded-lg p-4 flex items-center justify-center">
          <VueApexCharts type="donut" height="300" :options="donutOptions" :series="donutSeries" />
        </div>
      </div>

      <!-- Bar Chart -->
      <div class="flex-1 bg-[#1f2937] p-5 rounded-xl">
        <p class="text-white text-xl font-bold mb-4">Orders This Week</p>
        <div class="rounded-lg p-4">
          <VueApexCharts type="bar" height="300" :options="barOptions" :series="barSeries" />
        </div>
      </div>
    </div>
  </div>
</template>
