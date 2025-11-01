<script setup>
import { ref, onMounted } from "vue"
import axios from "axios"
import VueApexCharts from "vue3-apexcharts"
import jsPDF from "jspdf"
import { useLoadingStore } from "@/store/loading";

const loading = useLoadingStore();
const dateErrorMessage = ref("")
const showError = (msg) => {
  dateErrorMessage.value = msg
  setTimeout(() => {
    dateErrorMessage.value = ""
  }, 3000) // 3 seconds
}

// ---------------- State ----------------
const pendingOrders = ref(0)
const newCustomers = ref(0)
const salesThisWeekValue = ref(0)
const ordersThisWeekValue = ref(0)
const backend = import.meta.env.VITE_BACKEND_URL

// Date filter for report generation only
const startDate = ref("")
const endDate = ref("")

// ---------------- Donut Chart ----------------
const donutSeries = ref([])
const donutLabels = ref([])
const donutOptions = ref({
  chart: { type: "donut" },
  labels: [],
  legend: { position: "bottom", labels: { colors: "#fff" } },
  dataLabels: { enabled: true },
  colors: ["#3b82f6", "#10b981", "#f59e0b"],
})

// ---------------- Bar Chart ----------------
const barSeries = ref([{ name: "Orders", data: [] }])
const barCategories = ref([])
const barOptions = ref({
  chart: { type: "bar", height: 350, toolbar: { show: false } },
  plotOptions: { bar: { borderRadius: 6, columnWidth: "50%" } },
  dataLabels: { enabled: false },
  xaxis: { categories: [], labels: { style: { colors: "#fff" } } },
  yaxis: { labels: { style: { colors: "#fff" } } },
  grid: { borderColor: "#374151" },
  colors: ["#22c55e"],
  legend: { show: true, labels: { colors: "#fff" } },
})

// ---------------- Line Chart ----------------
const lineSeries = ref([{ name: "Sales", data: [] }])
const lineCategories = ref([])
const lineOptions = ref({
  chart: { type: "line", height: 350, toolbar: { show: false } },
  stroke: { curve: "smooth", width: 3 },
  xaxis: { categories: [], labels: { style: { colors: "#fff" } } },
  yaxis: { labels: { style: { colors: "#fff" } } },
  grid: { borderColor: "#374151" },
  colors: ["#f59e0b"],
  legend: { show: true, labels: { colors: "#fff" } },
})

// ---------------- Fetch Dashboard Data ----------------
const fetchDashboardData = async () => {
  try {
    const res = await axios.get(`${backend}/orders/dashboard-data`)
    const data = res.data

    const weekdays = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
    const dayMap = { Sun: 0, Mon: 0, Tue: 0, Wed: 0, Thu: 0, Fri: 0, Sat: 0 }
    const salesMap = {}
    const categoryMap = {}

    data.forEach((row) => {
      const day = new Date(row.order_date).toLocaleDateString("en-US", { weekday: "short" })
      dayMap[day] += Number(row.product_quantity)
      salesMap[day] = (salesMap[day] || 0) + Number(row.product_price) * Number(row.product_quantity)
      categoryMap[row.product_category] = (categoryMap[row.product_category] || 0) + Number(row.product_quantity)
    })

    // Donut
    donutLabels.value = Object.keys(categoryMap)
    donutSeries.value = Object.values(categoryMap)
    donutOptions.value = { ...donutOptions.value, labels: donutLabels.value }

    // Bar
    barCategories.value = weekdays
    barSeries.value[0].data = weekdays.map((d) => dayMap[d] || 0)

    // Line
    lineCategories.value = weekdays
    lineSeries.value[0].data = weekdays.map((d) => salesMap[d] || 0)

    // Summary
    ordersThisWeekValue.value = data.reduce((sum, row) => sum + Number(row.product_quantity), 0)
    const totalSales = data.reduce((sum, row) => sum + Number(row.product_price) * Number(row.product_quantity), 0)
    salesThisWeekValue.value = totalSales.toLocaleString("en-PH", { style: "currency", currency: "PHP" })
  } catch (err) {
    console.error("Failed to fetch dashboard data", err)
  }
}

// ---------------- Report Generator ----------------
const generateReport = async () => {
  if (!startDate.value || !endDate.value) {
    showError("Please select both Start and End dates.")
    loading.hide()
    return
  }

  try {
    loading.show()
    const res = await axios.post(`${backend}/orders/dashboard-report`, {
      start_date: startDate.value,
      end_date: endDate.value,
    })

    const data = res.data

    if (!data.length) {
      loading.hide()
      return
    }

    // ---------------- PDF Setup ----------------
    const pdf = new jsPDF("p", "mm", "a4")
    const pageWidth = pdf.internal.pageSize.getWidth()

    // Header Banner
    pdf.setFillColor(31, 41, 55) // dark gray
    pdf.rect(0, 0, 210, 30, "F")
    pdf.setTextColor(255, 255, 255)
    pdf.setFont("helvetica", "bold")
    pdf.setFontSize(20)
    pdf.text("Glass & Aluminum Company", pageWidth / 2, 17, { align: "center" })
    pdf.setFont("helvetica", "normal")
    pdf.setFontSize(12)
    pdf.text(`Sales Report (${startDate.value} - ${endDate.value})`, pageWidth / 2, 25, { align: "center" })

    // Add generation date
    const now = new Date().toLocaleString("en-PH", { timeZone: "Asia/Manila" })
    pdf.setFontSize(10)
    pdf.setTextColor(100)
    pdf.text(`Generated on: ${now}`, 14, 38)

    // ---------------- Summary ----------------
    const totalOrders = data.reduce((sum, row) => sum + Number(row.product_quantity), 0)
    const totalSales = data.reduce((sum, row) => sum + Number(row.product_price) * Number(row.product_quantity), 0)

    pdf.setTextColor(0)
    pdf.setFont("helvetica", "bold")
    pdf.setFontSize(14)
    pdf.text("Sales Summary", 14, 50)

    pdf.setFont("helvetica", "normal")
    pdf.setFontSize(12)
    pdf.text(`Total Orders: ${totalOrders}`, 14, 58)
    pdf.text(
      `Total Sales: PHP ${totalSales.toLocaleString("en-PH", {
        minimumFractionDigits: 2,
      })}`,
      14,
      66
    )

    // ---------------- Table Header ----------------
    let y = 80
    pdf.setFont("helvetica", "bold")
    pdf.setFillColor(243, 244, 246) // light gray header
    pdf.rect(10, y - 6, 190, 10, "F")

    pdf.text("No.", 14, y)
    pdf.text("Product", 30, y)
    pdf.text("Category", 95, y)
    pdf.text("Qty", 135, y, { align: "right" })
    pdf.text("Price", 165, y, { align: "right" })
    pdf.text("Total", 200, y, { align: "right" })
    y += 6

    // ---------------- Table Rows ----------------
    pdf.setFont("helvetica", "normal")
    data.forEach((item, index) => {
      if (y > 270) {
        pdf.addPage()
        y = 20
        pdf.setFont("helvetica", "bold")
        pdf.text("No.", 14, y)
        pdf.text("Product", 30, y)
        pdf.text("Category", 95, y)
        pdf.text("Qty", 135, y, { align: "right" })
        pdf.text("Price", 165, y, { align: "right" })
        pdf.text("Total", 200, y, { align: "right" })
        y += 6
        pdf.setFont("helvetica", "normal")
      }

      const total = item.product_price * item.product_quantity

      pdf.text(String(index + 1), 14, y)
      pdf.text(item.product_name, 30, y)
      pdf.text(item.product_category, 95, y)
      pdf.text(String(item.product_quantity), 135, y, { align: "right" })
      pdf.text(
        `PHP ${Number(item.product_price).toFixed(2)}`,
        165,
        y,
        { align: "right" }
      )
      pdf.text(
        `PHP ${total.toLocaleString("en-PH", { minimumFractionDigits: 2 })}`,
        200,
        y,
        { align: "right" }
      )

      y += 8
    })


    // ---------------- Footer ----------------
    const totalPages = pdf.internal.getNumberOfPages()
    for (let i = 1; i <= totalPages; i++) {
      pdf.setPage(i)
      pdf.setFontSize(10)
      pdf.setTextColor(150)
      pdf.text(`Page ${i} of ${totalPages}`, pageWidth - 30, 290)
    }

    // ---------------- Save ----------------
    pdf.save(`Dashboard_Report_${startDate.value}_to_${endDate.value}.pdf`)
    loading.hide()
  } catch (error) {
    loading.hide()
  }
}

// ---------------- Lifecycle ----------------
onMounted(() => {
  fetchDashboardData()
})
</script>

<template>
  <div class="h-full w-full flex flex-col pb-5 gap-8 bg-gray-900 p-6 rounded-xl shadow-lg mb-5">
    <!-- Header -->
    <div class="flex justify-between items-center flex-wrap gap-4">
      <p class="text-3xl text-white font-bold tracking-wide">
        Admin Dashboard Overview
      </p>

      <div class="flex items-center gap-3">
        <div class="flex flex-col text-white">
          <label for="start" class="text-sm mb-1">Start Date</label>
          <input id="start" type="date" v-model="startDate"
            class="bg-gray-800 text-white rounded-md px-3 py-2 border border-gray-700 focus:ring-2 focus:ring-emerald-500" />
        </div>

        <div class="flex flex-col text-white">
          <label for="end" class="text-sm mb-1">End Date</label>
          <input id="end" type="date" v-model="endDate"
            class="bg-gray-800 text-white rounded-md px-3 py-2 border border-gray-700 focus:ring-2 focus:ring-emerald-500" />
        </div>

<div class="relative flex flex-col mt-6">
  <p v-if="dateErrorMessage" 
     class="absolute -top-6 left-0 text-red-500 font-semibold text-sm transition-opacity duration-300">
    {{ dateErrorMessage }}
  </p>

  <button @click="generateReport"
          class="bg-gradient-to-r from-green-500 to-emerald-600 hover:opacity-90 text-white font-semibold px-5 py-2 rounded-lg shadow-md transition-all duration-200">
    🧾 Generate PDF Report
  </button>
</div>


      </div>
    </div>

    <!-- Summary Cards -->
    <div class="grid grid-cols-2 gap-6">
      <div class="bg-gradient-to-br from-orange-400 to-amber-500 p-6 rounded-xl flex flex-col gap-2 shadow-lg">
        <p class="text-white font-bold text-lg">Pending Orders</p>
        <p class="text-white text-2xl font-semibold">{{ pendingOrders }}</p>
      </div>

      <div class="bg-gradient-to-br from-purple-600 to-indigo-600 p-6 rounded-xl flex flex-col gap-2 shadow-lg">
        <p class="text-white font-bold text-lg">New Customer Sign-ups</p>
        <p class="text-white text-2xl font-semibold">{{ newCustomers }}</p>
      </div>
    </div>

    <!-- Charts Section -->
    <div class="grid grid-cols-2 gap-6">
      <!-- Sales Line Chart -->
      <div class="bg-gray-800 p-5 rounded-xl shadow-lg">
        <p class="text-white text-xl font-semibold mb-4">Sales This Week</p>
        <div id="sales-chart" class="rounded-lg p-4 bg-gray-900">
          <VueApexCharts type="line" height="350" :options="lineOptions" :series="lineSeries" />
        </div>
      </div>

      <!-- Orders Bar Chart -->
      <div class="bg-gray-800 p-5 rounded-xl shadow-lg">
        <p class="text-white text-xl font-semibold mb-4">Orders This Week</p>
        <div id="orders-chart" class="rounded-lg p-4 bg-gray-900">
          <VueApexCharts type="bar" height="350" :options="barOptions" :series="barSeries" />
        </div>
      </div>
    </div>

    <!-- Donut Chart -->
    <div class="bg-gray-800 p-5 rounded-xl shadow-lg">
      <p class="text-white text-xl font-semibold mb-4">
        Most Ordered Product Categories
      </p>
      <div id="donut-chart" class="rounded-lg p-4 flex items-center justify-center bg-gray-900">
        <VueApexCharts type="donut" height="300" :options="donutOptions" :series="donutSeries" />
      </div>
    </div>
  </div>
</template>
