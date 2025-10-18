<script setup lang="ts">
import { ref, computed, onMounted } from "vue";
import axios from "axios";
import { useLoadingStore } from "@/store/loading";

const loading = useLoadingStore();

// ----------------- Interfaces -----------------
interface DeliveryAddress {
  house_number?: string;
  street: string;
  barangay?: string;
  city: string;
  province?: string;
}

interface Order {
  order_id: number;
  product_id: number;
  user_email: string;
  product_price: number;
  quantity: number;
  status: string;
  delivery_address: DeliveryAddress;
  actionLoading?: boolean;
}

interface OrderLog {
  order_id: number;
  product_name: string;
  user_email: string;
  product_price: number;
  quantity: number;
  status: string;
  delivery_address: DeliveryAddress;
}

// ----------------- State -----------------
const orders = ref<Order[]>([]);
const orderLogs = ref<OrderLog[]>([]);
const search = ref("");
const showLogs = ref(false);

// ----------------- Fetch Orders -----------------
const fetchOrders = async () => {
  try {
    const res = await axios.get<Order[]>("http://localhost:8000/orders/order-admin");
    orders.value = res.data.map(order => ({ ...order, actionLoading: false }));
  } catch (err) {
    console.error(err);
  }
};

// ----------------- Fetch Order Logs -----------------
// ----------------- Fetch Order Logs -----------------
const fetchOrderLogs = async () => {
  try {
    const res = await axios.get<OrderLog[]>("http://localhost:8000/orders/order-log");
    // Map to ensure delivery_address always exists
    orderLogs.value = res.data.map(log => ({
      ...log,
      delivery_address: {
        house_number: log.delivery_address?.house_number ?? "",
        street: log.delivery_address?.street ?? "",
        barangay: log.delivery_address?.barangay ?? "",
        city: log.delivery_address?.city ?? "",
        province: log.delivery_address?.province ?? ""
      }
    }));
  } catch (err) {
    console.error(err);
  }
};

onMounted(() => {
  fetchOrders();
  fetchOrderLogs();
});

onMounted(() => {
  fetchOrders();
  fetchOrderLogs(); // fetch logs on mount
});

// ----------------- Computed -----------------
const filteredOrders = computed(() => {
  if (!search.value.trim()) return orders.value;
  return orders.value.filter(o =>
    o.user_email.toLowerCase().includes(search.value.toLowerCase())
  );
});

const filteredLogs = computed(() => {
  if (!search.value.trim()) return orderLogs.value;
  return orderLogs.value.filter(o =>
    o.user_email.toLowerCase().includes(search.value.toLowerCase())
  );
});

// ----------------- Actions -----------------
const approveOrFinishOrder = async (order: Order) => {
  if (["installed/shipped", "rejected"].includes(order.status.toLowerCase())) return;
  order.actionLoading = true;

  try {
    loading.show();
    const newStatus = order.status.toLowerCase() === "pending" ? "processing" : "installed/shipped";
    await axios.put(`http://localhost:8000/orders/update-status/${order.order_id}`, { status: newStatus });
    order.status = newStatus;
    fetchOrderLogs(); // refresh logs
  } catch (err) {
    console.error(err);
    alert("Failed to update order status");
  } finally {
    order.actionLoading = false;
    loading.hide();
  }
};

const rejectOrder = async (order: Order) => {
  if (order.status.toLowerCase() === "rejected") return;
  order.actionLoading = true;

  try {
    loading.show();
    await axios.put(`http://localhost:8000/orders/reject-order/${order.order_id}`);
    order.status = "rejected";
    fetchOrderLogs(); // refresh logs
  } catch (err) {
    console.error(err);
    alert("Failed to reject order");
  } finally {
    order.actionLoading = false;
    loading.hide();
  }
};

const deleteOrder = async (order: Order) => {
  if (!confirm(`Are you sure you want to delete order ${order.order_id}?`)) return;
  order.actionLoading = true;

  try {
    loading.show();
    await axios.delete(`http://localhost:8000/orders/${order.order_id}`);
    orders.value = orders.value.filter(o => o.order_id !== order.order_id);
    fetchOrderLogs(); // refresh logs
  } catch (err) {
    console.error(err);
    alert("Failed to delete order");
  } finally {
    order.actionLoading = false;
    loading.hide();
  }
};

// ----------------- Helper -----------------
const formatAddress = (address: DeliveryAddress) => {
  return [address.house_number, address.street, address.barangay, address.city, address.province]
    .filter(Boolean)
    .join(", ");
};

const toggleLogs = () => {
  showLogs.value = !showLogs.value;
};
</script>


<template>
  <div class="p-4 bg-[#111827] rounded-xl shadow-lg h-screen overflow-y-auto">
    <!-- Search & Toggle Logs Button -->
    <div class="flex flex-col sm:flex-row justify-between items-center mb-4 sticky top-0 z-50 bg-[#111827] py-2 px-2 shadow rounded-lg gap-2">
      <input
        v-model="search"
        type="text"
        placeholder="Search by user email..."
        class="w-full sm:w-1/2 px-3 py-1.5 rounded-md border border-gray-700 bg-[#1f2937] text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-indigo-500 transition"
      />
      <button
        @click="toggleLogs"
        class="px-4 py-1.5 bg-indigo-600 hover:bg-indigo-500 text-white font-semibold rounded-md shadow transition hover:scale-105"
      >
        {{ showLogs ? "Show Orders" : "Show Order Logs" }}
      </button>
    </div>

    <!-- Orders Table -->
    <div class="overflow-x-hidden" v-if="!showLogs">
      <table class="min-w-full text-gray-200 text-sm border-separate border-spacing-y-1">
        <thead class="bg-[#1f2937] text-gray-100 uppercase">
          <tr>
            <th class="py-2 px-2 text-center">Order Id</th>
            <th class="py-2 px-2 text-center">Product</th>
            <th class="py-2 px-2 text-center">Email</th>
            <th class="py-2 px-2 text-center">Address</th>
            <th class="py-2 px-2 text-center">Price</th>
            <th class="py-2 px-2 text-center">Qty</th>
            <th class="py-2 px-2 text-center">Status</th>
            <th class="py-2 px-2 text-center">Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="order in filteredOrders"
            :key="order.order_id"
            class="bg-[#1f2937] hover:bg-[#374151] rounded-lg transition"
          >
            <td class="py-1 px-2 text-center">{{ order.order_id }}</td>
            <td class="py-1 px-2 text-center">{{ order.product_id }}</td>
            <td class="py-1 px-2 text-center max-w-[120px] truncate" :title="order.user_email">{{ order.user_email }}</td>
            <td class="py-1 px-2 text-center max-w-[160px] truncate" :title="formatAddress(order.delivery_address)">{{ formatAddress(order.delivery_address) }}</td>
            <td class="py-1 px-2 text-center">${{ order.product_price }}</td>
            <td class="py-1 px-2 text-center">{{ order.quantity }}</td>
            <td class="py-1 px-2 text-center capitalize font-medium">
              <span
                :class="{
                  'text-blue-400': order.status.toLowerCase() === 'pending',
                  'text-yellow-400': order.status.toLowerCase() === 'processing',
                  'text-green-400': order.status.toLowerCase() === 'installed/shipped',
                  'text-red-400': order.status.toLowerCase() === 'rejected',
                }"
              >
                {{ order.status }}
              </span>
            </td>
            <td class="py-1 px-2 text-center flex flex-col sm:flex-row gap-1 justify-center items-center">
              <button
                @click="approveOrFinishOrder(order)"
                :disabled="order.actionLoading || ['installed/shipped','rejected'].includes(order.status.toLowerCase())"
                class="w-20 h-8 flex items-center justify-center rounded-md font-semibold text-white transition hover:scale-105"
                :class="order.status.toLowerCase() === 'pending' ? 'bg-blue-600 hover:bg-blue-500' :
                        order.status.toLowerCase() === 'processing' ? 'bg-yellow-600 hover:bg-yellow-500' :
                        'bg-gray-600 cursor-default'"
              >
                {{
                  order.status.toLowerCase() === 'pending' ? 'Approve' :
                  order.status.toLowerCase() === 'processing' ? 'Finish' :
                  order.status.toLowerCase() === 'installed/shipped' ? 'Completed' : 'Rejected'
                }}
              </button>

              <button
                v-if="order.status.toLowerCase() !== 'installed/shipped'"
                @click="rejectOrder(order)"
                :disabled="order.actionLoading || order.status.toLowerCase() === 'rejected'"
                class="w-20 h-8 flex items-center justify-center rounded-md bg-red-600 hover:bg-red-500 text-white font-semibold transition hover:scale-105"
              >
                Reject
              </button>

              <button
                @click="deleteOrder(order)"
                :disabled="order.actionLoading"
                class="w-10 h-8 flex items-center justify-center rounded-md bg-gray-700 hover:bg-gray-600 text-white transition hover:scale-105"
              >
                <i class="fa-solid fa-trash"></i>
              </button>
            </td>
          </tr>
        </tbody>
      </table>
      <div v-if="filteredOrders.length === 0" class="text-center py-4 text-gray-400">
        No orders found.
      </div>
    </div>

    <!-- Order Logs Table -->
    <div class="overflow-x-hidden" v-else>
      <table class="min-w-full text-gray-200 text-sm border-separate border-spacing-y-1">
        <thead class="bg-[#1f2937] text-gray-100 uppercase">
          <tr>
            <th class="py-2 px-2 text-center">Order ID</th>
            <th class="py-2 px-2 text-center">Product</th>
            <th class="py-2 px-2 text-center">Email</th>
            <th class="py-2 px-2 text-center">Address</th>
            <th class="py-2 px-2 text-center">Price</th>
            <th class="py-2 px-2 text-center">Quantity</th>
            <th class="py-2 px-2 text-center">Status</th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="log in filteredLogs"
            :key="log.order_id"
            class="bg-[#1f2937] hover:bg-[#374151] rounded-lg transition"
          >
            <td class="py-1 px-2 text-center">{{ log.order_id }}</td>
            <td class="py-1 px-2 text-center">{{ log.product_name }}</td>
            <td class="py-1 px-2 text-center max-w-[120px] truncate" :title="log.user_email">{{ log.user_email }}</td>
            <td class="py-1 px-2 text-center max-w-[160px] truncate" :title="formatAddress(log.delivery_address)">{{ formatAddress(log.delivery_address) }}</td>
            <td class="py-1 px-2 text-center">${{ log.product_price }}</td>
            <td class="py-1 px-2 text-center">{{ log.quantity }}</td>
            <td class="py-1 px-2 text-center capitalize font-medium">{{ log.status }}</td>
          </tr>
        </tbody>
      </table>
      <div v-if="filteredLogs.length === 0" class="text-center py-4 text-gray-400">
        No logs found.
      </div>
    </div>
  </div>
</template>
