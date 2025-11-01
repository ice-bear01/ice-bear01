<script setup lang="ts">
import { ref, computed, onMounted } from "vue";
import { useRouter } from "vue-router";
import axios from "axios";
import { useLoadingStore } from "@/store/loading";

const loading = useLoadingStore();
const backend = import.meta.env.VITE_BACKEND_URL;

interface Product {
  id: number;
  product_image: string;
  category: string;
  product_type: string;
  product_name: string;
  product_price: number;
  product_stock: number;
  is_archived?: boolean;
  actionLoading?: boolean;
}

const router = useRouter();
const products = ref<Product[]>([]);
const archivedProducts = ref<Product[]>([]);
const search = ref("");
const showArchived = ref(false);

// --- Modal States ---
const showConfirmModal = ref(false);
const showMessageModal = ref(false);
const modalMessage = ref("");
const confirmAction = ref<null | (() => Promise<void>)>(null);
const modalTitle = ref("");
const isConfirming = ref(false);

// Function to open confirmation modal
const openConfirmModal = (title: string, message: string, action: () => Promise<void>) => {
  modalTitle.value = title;
  modalMessage.value = message;
  confirmAction.value = action;
  showConfirmModal.value = true;
};

// Function to open info/success modal
const openMessageModal = (message: string) => {
  modalMessage.value = message;
  showMessageModal.value = true;
};

// Fetch all active products
const fetchProducts = async () => {
  try {
    const res = await axios.get<Product[]>(`${backend}/product/all`);
    products.value = res.data.map((p) => ({ ...p, actionLoading: false }));
  } catch (err) {
    console.error("Failed to fetch products:", err);
  }
};

// Fetch archived products
const fetchArchivedProducts = async () => {
  try {
    const res = await axios.get<Product[]>(`${backend}/product/archived`);
    archivedProducts.value = res.data.map((p) => ({ ...p, actionLoading: false }));
  } catch (err) {
    console.error("Failed to fetch archived products:", err);
  }
};

onMounted(() => {
  fetchProducts();
  fetchArchivedProducts();
});

// Filtered products
const filteredProducts = computed(() => {
  const list = showArchived.value ? archivedProducts.value : products.value;
  if (!search.value.trim()) return list;
  return list.filter((p) =>
    p.product_name.toLowerCase().includes(search.value.toLowerCase())
  );
});

// Navigation
const goToAddPage = () => router.push("/products/add");
const goToEditPage = (id: number) => router.push(`/products/update/${id}`);

// Delete product
const deleteProduct = async (id: number) => {
  openConfirmModal("Delete Product", "Are you sure you want to delete this product?", async () => {
    try {
      loading.show();
      await axios.delete(`${backend}/product/delete/${id}`);
      products.value = products.value.filter((p) => p.id !== id);
      archivedProducts.value = archivedProducts.value.filter((p) => p.id !== id);
      openMessageModal("Product deleted successfully.");
    } catch (err) {
      console.error("Failed to delete product:", err);
      openMessageModal("Failed to delete product.");
    } finally {
      loading.hide();
    }
  });
};

// Archive product
const archiveProduct = async (product: Product) => {
  openConfirmModal("Archive Product", "Are you sure you want to archive this product?", async () => {
    try {
      product.actionLoading = true;
      await axios.put(`${backend}/product/archive/${product.id}`);
      products.value = products.value.filter((p) => p.id !== product.id);
      archivedProducts.value.push({ ...product, is_archived: true });
      openMessageModal("Product archived successfully.");
    } catch (err) {
      console.error("Failed to archive product:", err);
      openMessageModal("Failed to archive product.");
    } finally {
      product.actionLoading = false;
    }
  });
};

// Unarchive product
const unarchiveProduct = async (product: Product) => {
  openConfirmModal("Restore Product", "Restore this product from archive?", async () => {
    try {
      product.actionLoading = true;
      await axios.put(`${backend}/product/unarchive/${product.id}`);
      archivedProducts.value = archivedProducts.value.filter((p) => p.id !== product.id);
      products.value.push({ ...product, is_archived: false });
      openMessageModal("Product restored successfully.");
    } catch (err) {
      console.error("Failed to unarchive product:", err);
      openMessageModal("Failed to restore product.");
    } finally {
      product.actionLoading = false;
    }
  });
};

// Handle confirm action
const handleConfirm = async () => {
  if (!confirmAction.value) return;
  isConfirming.value = true;
  await confirmAction.value();
  isConfirming.value = false;
  showConfirmModal.value = false;
};
</script>

<template>
  <div class="p-4 bg-gray-900 rounded-xl shadow-lg h-screen overflow-y-auto mb-5">
    <!-- Search / Toggle / Add -->
    <div
      class="flex flex-col sm:flex-row justify-between items-center mb-4 sticky top-0 z-50 bg-[#111827] py-2 px-2 shadow rounded-lg">
      
      <div class="flex items-center gap-2 w-full sm:w-auto">
        <!-- Toggle Archived -->
        <button
          @click="showArchived = !showArchived"
          class="px-3 py-1.5 rounded-md font-semibold transition text-white shadow-md"
          :class="showArchived ? 'bg-yellow-600 hover:bg-yellow-500' : 'bg-gray-700 hover:bg-gray-600'">
          <i class="fa-solid fa-box-archive mr-1"></i>
          {{ showArchived ? 'Show Active' : 'Show Archived' }}
        </button>

        <!-- Search -->
        <input
          v-model="search"
          type="text"
          placeholder="Search product..."
          class="w-full sm:w-60 px-3 py-1.5 rounded-md border border-gray-700 bg-gray-800 text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-indigo-500 transition" />
      </div>

      <button
        @click="goToAddPage"
        class="mt-2 sm:mt-0 px-4 py-1.5 bg-[#006989] hover:bg-[#025974] text-white font-semibold rounded-md shadow flex items-center gap-2 transition hover:scale-105">
        <i class="fa-solid fa-plus"></i> Add Product
      </button>
    </div>

    <!-- Products Table -->
    <div class="overflow-x-hidden">
      <table class="min-w-full text-gray-200 text-sm border-separate border-spacing-y-1">
        <thead class="bg-[#1f2937] text-gray-100 uppercase">
          <tr>
            <th class="py-2 px-2 text-center">ID</th>
            <th class="py-2 px-2 text-center">Image</th>
            <th class="py-2 px-2 text-center">Category</th>
            <th class="py-2 px-2 text-center">Type</th>
            <th class="py-2 px-2 text-center">Name</th>
            <th class="py-2 px-2 text-center">Price</th>
            <th class="py-2 px-2 text-center">Actions</th>
          </tr>
        </thead>

        <tbody>
          <tr
            v-for="product in filteredProducts"
            :key="product.id"
            class="bg-[#1f2937] hover:bg-[#374151] rounded-lg transition">
            <td class="py-1 px-2 text-center">{{ product.id }}</td>
            <td class="py-1 px-2 text-center">
              <img :src="product.product_image" alt="Product" class="w-12 h-12 rounded-md object-cover mx-auto" />
            </td>
            <td class="py-1 px-2 text-center max-w-[100px] truncate" :title="product.category">
              {{ product.category }}
            </td>
            <td class="py-1 px-2 text-center max-w-[100px] truncate" :title="product.product_type">
              {{ product.product_type }}
            </td>
            <td class="py-1 px-2 text-center max-w-[140px] truncate" :title="product.product_name">
              {{ product.product_name }}
            </td>
            <td class="py-1 px-2 text-center">₱{{ product.product_price }}</td>

            <td class="py-2 px-2 text-center">
              <div class="flex justify-center items-center gap-2">
                <!-- Edit -->
                <button
                  v-if="!showArchived"
                  @click="goToEditPage(product.id)"
                  class="w-9 h-9 flex items-center justify-center rounded-md bg-blue-600 hover:bg-blue-500 text-white text-base transition hover:scale-105 shadow-md">
                  <i class="fa-solid fa-pen-to-square"></i>
                </button>

                <!-- Archive / Unarchive -->
                <button
                  @click="showArchived ? unarchiveProduct(product) : archiveProduct(product)"
                  class="w-9 h-9 flex items-center justify-center rounded-md text-white text-base transition hover:scale-105 shadow-md"
                  :class="showArchived ? 'bg-green-600 hover:bg-green-500' : 'bg-yellow-600 hover:bg-yellow-500'">
                  <i :class="showArchived ? 'fa-solid fa-rotate-left' : 'fa-solid fa-box-archive'"></i>
                </button>

                <!-- Delete -->
                <button
                  @click="deleteProduct(product.id)"
                  class="w-9 h-9 flex items-center justify-center rounded-md bg-red-600 hover:bg-red-500 text-white text-base transition hover:scale-105 shadow-md">
                  <i class="fa-solid fa-trash"></i>
                </button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>

      <div v-if="filteredProducts.length === 0" class="text-center py-4 text-gray-400">
        No products found.
      </div>
    </div>

    <!-- Confirmation Modal -->
    <div
      v-if="showConfirmModal"
      class="fixed inset-0 flex items-center justify-center bg-black/60 z-50">
      <div class="bg-gray-800 text-white p-6 rounded-xl w-80 shadow-lg text-center">
        <h2 class="text-lg font-bold mb-2">{{ modalTitle }}</h2>
        <p class="text-sm text-gray-300 mb-4">{{ modalMessage }}</p>
        <div class="flex justify-center gap-3">
          <button
            @click="showConfirmModal = false"
            class="px-4 py-2 bg-gray-600 hover:bg-gray-500 rounded-md">
            Cancel
          </button>
          <button
            @click="handleConfirm"
            class="px-4 py-2 bg-red-600 hover:bg-red-500 rounded-md font-semibold"
            :disabled="isConfirming">
            {{ isConfirming ? 'Processing...' : 'Confirm' }}
          </button>
        </div>
      </div>
    </div>

    <!-- Message Modal -->
    <div
      v-if="showMessageModal"
      class="fixed inset-0 flex items-center justify-center bg-black bg-opacity-60 z-50">
      <div class="bg-gray-800 text-white p-6 rounded-xl w-80 shadow-lg text-center">
        <p class="text-sm mb-4">{{ modalMessage }}</p>
        <button
          @click="showMessageModal = false"
          class="px-4 py-2 bg-blue-600 hover:bg-blue-500 rounded-md font-semibold">
          OK
        </button>
      </div>
    </div>
  </div>
</template>
