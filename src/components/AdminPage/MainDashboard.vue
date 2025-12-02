<script setup>
import logo from "@/assets/img/logo.jpg"; // replace with your actual image file name
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

    const resCustomers = await axios.get(`${backend}/users/new-customer-count`)
    newCustomers.value = resCustomers.data.today_new_customers || 0

    const resPending = await axios.get(`${backend}/orders/pending-orders-count`);
    pendingOrders.value = resPending.data.pending_count || 0;


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

    // ---------------- PDF Setup ----------------(johnpaulgmail)
    const pdf = new jsPDF("p", "mm", "a4");
    const pageWidth = pdf.internal.pageSize.getWidth();

    // ---------------- Header with Logo ----------------
const imgWidth = 20;  // width of logo in mm
const imgHeight = 20; // height of logo in mm
const startX = 14;    // left margin for logo
const startY = 7;     // top margin for logo

// Add logo on the top-left
pdf.addImage(logo, "PNG", startX, startY, imgWidth, imgHeight);

// Add shop name beside logo
pdf.setTextColor(0, 0, 0);
pdf.setFont("helvetica", "bold");
pdf.setFontSize(20);
const shopNameX = startX + imgWidth + 5; // 5mm padding from logo
const shopNameY = startY + imgHeight / 3 + 5; // vertically center with logo
pdf.text("3J's Glass & Aluminum Shop", shopNameX, shopNameY);

// Add subtitle aligned with shop name
pdf.setFont("helvetica", "normal");
pdf.setFontSize(12);
const subtitleY = shopNameY + 8; // 8mm below shop name
pdf.text(`Sales Report (${startDate.value} - ${endDate.value})`, shopNameX, subtitleY);


    // Timestamp
    const now = new Date().toLocaleString("en-PH", { timeZone: "Asia/Manila" });
    pdf.setFontSize(10);
    pdf.setTextColor(100);
    pdf.text(`Generated on: ${now}`, 14, 38);

    // ---------------- Summary ----------------
    const totalOrders = data.reduce((sum, row) => sum + Number(row.product_quantity), 0);
    const totalSales = data.reduce(
      (sum, row) => sum + Number(row.product_price) * Number(row.product_quantity),
      0
    );

    pdf.setTextColor(0);
    pdf.setFont("helvetica", "bold");
    pdf.setFontSize(14);
    pdf.text("Sales Summary", 14, 50);

    pdf.setFont("helvetica", "normal");
    pdf.setFontSize(12);
    pdf.text(`Total Orders: ${totalOrders}`, 14, 58);
    pdf.text(
      `Total Sales: PHP ${totalSales.toLocaleString("en-PH", { minimumFractionDigits: 2 })}`,
      14,
      66
    );

    // ---------------- Table Setup ----------------
    let y = 80;

    const col = {
      no: 15,
      product: 60,
      category: 40,
      qty: 20,
      price: 30,
      total: 30,
    };

    const x = 10;

    // ---------------- Draw Table Header ----------------
    function drawTableHeader(startY) {
      pdf.setFont("helvetica", "bold");
      pdf.setTextColor(0);
      pdf.setLineWidth(0.2);

      pdf.rect(x, startY, 190, 10);

      pdf.line(x + col.no, startY, x + col.no, startY + 10);
      pdf.line(x + col.no + col.product, startY, x + col.no + col.product, startY + 10);
      pdf.line(x + col.no + col.product + col.category, startY, x + col.no + col.product + col.category, startY + 10);
      pdf.line(x + col.no + col.product + col.category + col.qty, startY, x + col.no + col.product + col.category + col.qty, startY + 10);
      pdf.line(x + col.no + col.product + col.category + col.qty + col.price, startY, x + col.no + col.product + col.category + col.qty + col.price, startY + 10);

      pdf.text("No.", x + 5, startY + 7);
      pdf.text("Product", x + col.no + 5, startY + 7);
      pdf.text("Category", x + col.no + col.product + 5, startY + 7);
      pdf.text("Qty", x + col.no + col.product + col.category + 5, startY + 7);
      pdf.text("Price", x + col.no + col.product + col.category + col.qty + 5, startY + 7);
      pdf.text("Total", x + col.no + col.product + col.category + col.qty + col.price + 5, startY + 7);

      return startY + 10;
    }

    y = drawTableHeader(y);

    // ---------------- Table Rows ----------------
    pdf.setFont("helvetica", "normal");

    data.forEach((item, index) => {
      if (y > 260) {
        pdf.addPage();
        y = 20;
        y = drawTableHeader(y);
      }

      const total = Number(item.product_price) * Number(item.product_quantity);

      // WRAPPED TEXTS
      const productText = pdf.splitTextToSize(item.product_name, col.product - 8);
      const categoryText = pdf.splitTextToSize(item.product_category, col.category - 8);
      const qtyText = String(item.product_quantity);
      const priceText = pdf.splitTextToSize(`PHP ${Number(item.product_price).toFixed(2)}`, col.price - 8);
      const totalText = pdf.splitTextToSize(
        `PHP ${total.toLocaleString("en-PH", { minimumFractionDigits: 2 })}`,
        col.total - 8
      );

      // Calculate row height based on wrapped lines
      const lineCount = Math.max(
        productText.length,
        categoryText.length,
        priceText.length,
        totalText.length
      );

      const rowHeight = Math.max(10, lineCount * 6);

      // Row outline
      pdf.rect(x, y, 190, rowHeight);

      // Vertical lines
      pdf.line(x + col.no, y, x + col.no, y + rowHeight);
      pdf.line(x + col.no + col.product, y, x + col.no + col.product, y + rowHeight);
      pdf.line(x + col.no + col.product + col.category, y, x + col.no + col.product + col.category, y + rowHeight);
      pdf.line(x + col.no + col.product + col.category + col.qty, y, x + col.no + col.product + col.category + col.qty, y + rowHeight);
      pdf.line(x + col.no + col.product + col.category + col.qty + col.price, y, x + col.no + col.product + col.category + col.qty + col.price, y + rowHeight);

      // Insert text
      pdf.text(String(index + 1), x + 5, y + 6);
      pdf.text(productText, x + col.no + 5, y + 6);
      pdf.text(categoryText, x + col.no + col.product + 5, y + 6);
      pdf.text(qtyText, x + col.no + col.product + col.category + 5, y + 6);
      pdf.text(priceText, x + col.no + col.product + col.category + col.qty + 5, y + 6);
      pdf.text(totalText, x + col.no + col.product + col.category + col.qty + col.price + 5, y + 6);

      y += rowHeight;
    });

    // ---------------- Footer ----------------
    const totalPages = pdf.internal.getNumberOfPages();
    for (let i = 1; i <= totalPages; i++) {
      pdf.setPage(i);
      pdf.setFontSize(10);
      pdf.setTextColor(150);
      pdf.text(`Page ${i} of ${totalPages}`, pageWidth - 30, 290);
    }
    //----------------------------johnpaulgmail til here-----------------


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
