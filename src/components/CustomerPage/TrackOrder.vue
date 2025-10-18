<script setup lang="ts">
import axios from 'axios';
import { ref, onMounted } from 'vue';

interface DeliveryAddress {
  house_number?: string;
  street: string;
  barangay?: string;
  city: string;
  province?: string;
}

interface OrderResponse {
  order_id: number;
  status: string;
  created_at: string;
  product_image: string;
  product_category: string;
  product_type: string;
  product_name: string;
  product_price: number;
  quantity: number;
  total_price: number;
  delivery_address?: DeliveryAddress;
}

const orders = ref<OrderResponse[]>([]);
const loading = ref(false);
const error = ref('');

// const mockOrders: OrderResponse[] = [
//   {
//     order_id: 1,
//     status: 'Pending',
//     created_at: '2025-10-17T10:00:00Z',
//     product_image: 'https://images.unsplash.com/photo-1606813902917-42e11f21c7e2?auto=format&fit=crop&w=600&q=80',
//     product_category: 'Solar Energy',
//     product_type: 'Panel Type A',
//     product_name: 'SolarMax Pro 400W',
//     product_price: 249.99,
//     quantity: 2,
//     total_price: 499.98,
//     delivery_address: {
//       house_number: '123',
//       street: 'Sunshine St.',
//       barangay: 'Greenfields',
//       city: 'Manila',
//       province: 'Metro Manila',
//     },
//   },
//   {
//     order_id: 2,
//     status: 'Approved',
//     created_at: '2025-10-12T15:30:00Z',
//     product_image: 'https://images.unsplash.com/photo-1581093448795-5afadbfbbf2c?auto=format&fit=crop&w=600&q=80',
//     product_category: 'Wind Energy',
//     product_type: 'Turbine Model X',
//     product_name: 'WindBlaze 3000',
//     product_price: 1799.99,
//     quantity: 1,
//     total_price: 1799.99,
//     delivery_address: {
//       street: 'Ocean Breeze Ave.',
//       barangay: 'Bluewater',
//       city: 'Cebu City',
//       province: 'Cebu',
//     },
//   },
//   {
//     order_id: 3,
//     status: 'Rejected',
//     created_at: '2025-10-10T08:45:00Z',
//     product_image: 'https://images.unsplash.com/photo-1556906781-9a412961c28c?auto=format&fit=crop&w=600&q=80',
//     product_category: 'Hydro Energy',
//     product_type: 'Turbine Mini',
//     product_name: 'HydroSpin 1500',
//     product_price: 499.99,
//     quantity: 3,
//     total_price: 1499.97,
//     delivery_address: {
//       street: 'Riverbank Road',
//       city: 'Davao',
//       province: 'Davao del Sur',
//     },
//   },
// ];

const fetchOrders = async () => {
  loading.value = true;
  error.value = '';

  try {
    const response = await axios.get<OrderResponse[]>('http://localhost:8000/orders/', {
      withCredentials: true,
    });
    orders.value = response.data;

    // await new Promise((resolve) => setTimeout(resolve, 800)); // simulate loading
    // orders.value = mockOrders;
  } catch (err: any) {
    console.error(err);
    error.value = 'Failed to fetch orders.';
  } finally {
    loading.value = false;
  }
};

onMounted(() => {
  fetchOrders();
});

const statusColor = (status: string) => {
  const s = status.toLowerCase();
  if (s === 'pending') return 'text-orange-400 border-orange-400';
  if (s === 'rejected') return 'text-red-600 border-red-400';
  return 'text-green-400 border-green-400';
};
</script>

<template>
  <div class="p-6 text-base">
    <h1 class="text-3xl font-bold mb-6 flex items-center gap-2 text-white">
      <i class="fas fa-shipping-fast text-green-400"></i>
      Track Orders
    </h1>

    <div v-if="loading" class="text-white">Loading orders...</div>
    <div v-if="error" class="text-red-400">{{ error }}</div>
    <div v-if="orders.length === 0 && !loading" class="text-white/70">No orders found.</div>

    <div class="flex flex-col gap-6 sm:px-15">

      <div
        v-for="order in orders"
        :key="order.order_id"
        class="flex flex-col md:flex-row gap-4 bg-white/10 p-5 rounded-xl backdrop-blur-md shadow-lg group hover:shadow-2xl transition relative overflow-hidden"
      >
        <div
          class="absolute inset-0 bg-gradient-to-r from-white/0 via-white/20 to-white/0 opacity-0 group-hover:opacity-30 transition-all pointer-events-none"
          style="transform: skewX(-20deg);"
        ></div>

        <!-- Image -->
        <div class="w-full md:w-64 flex-shrink-0">
          <img
            :src="order.product_image"
            alt="Product"
            class="w-full h-56 md:h-full object-cover rounded-lg border border-white/20"
          />
        </div>

        <!-- Details -->
        <div class="flex-1 flex flex-col justify-between">
          <div class="space-y-2">
            <h2 class="text-xl font-semibold text-white">{{ order.product_name }}</h2>
            <p class="text-white/80 flex items-center gap-2">
              <i class="fas fa-layer-group"></i> {{ order.product_category }} - {{ order.product_type }}
            </p>

            <p class="text-white/80 flex items-center gap-2">
              <i class="fas fa-sort-numeric-up"></i> Quantity: {{ order.quantity }}
            </p>

            <p class="text-white/80 flex items-center gap-2">
              <i class="fas fa-dollar-sign"></i> Price: ${{ order.product_price }} | Total: ${{ order.total_price }}
            </p>

            <p class="text-white/80 flex items-center gap-2">
              <i class="fas fa-calendar-alt"></i> {{ new Date(order.created_at).toLocaleString() }}
            </p>

            <p class="flex items-center gap-2 mt-2 text-white">
              <i class="fas fa-truck" :class="statusColor(order.status)"></i>
              <span class="font-medium">Status:</span>
              <span :class="['px-3 py-1 rounded-full text-sm font-semibold border', statusColor(order.status)]">
                {{ order.status }}
              </span>
            </p>
          </div>

          <div class="mt-4 bg-white/10 p-4 rounded-lg border border-white/20 flex items-start gap-2">
            <i class="fas fa-map-marker-alt mt-1 text-white/70"></i>
            <div class="text-white/80">
              <p class="font-semibold mb-1 text-lg">Delivery Address</p>
              <p>
                {{ order.delivery_address?.house_number ?? '' }}
                {{ order.delivery_address?.street }},
                {{ order.delivery_address?.barangay ?? '' }},
                {{ order.delivery_address?.city }},
                {{ order.delivery_address?.province ?? '' }}
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.group:hover::before {
  content: '';
  position: absolute;
  top: 0;
  left: -50%;
  width: 50%;
  height: 100%;
  background: linear-gradient(120deg, rgba(255,255,255,0.1), rgba(255,255,255,0.3), rgba(255,255,255,0.1));
  transform: skewX(-20deg);
  animation: shine 1s forwards;
  pointer-events: none;
}

@keyframes shine {
  0% { left: -50%; }
  100% { left: 150%; }
}
</style>
