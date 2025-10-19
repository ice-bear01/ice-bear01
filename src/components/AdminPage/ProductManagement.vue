<script setup lang="ts">
import { ref, computed, onMounted } from "vue";
import { useRouter } from "vue-router";
import axios from "axios";
import { useLoadingStore } from "@/store/loading";

const loading = useLoadingStore();
const backend = import.meta.env.VITE_BACKEND_URL
interface Product {
  id: number;
  product_image: string;
  category: string;
  product_type: string;
  product_name: string;
  product_price: number;
  product_stock: number;
  actionLoading?: boolean;
}

const router = useRouter();
const products = ref<Product[]>([]);
const search = ref("");

// Fetch products
const fetchProducts = async () => {
  try {
    const res = await axios.get<Product[]>(`${backend}/product/all`);
    products.value = res.data.map((p) => ({ ...p, actionLoading: false }));
  } catch (err) {
    console.error("Failed to fetch products:", err);
  }
};

onMounted(fetchProducts);

// Filtered products
const filteredProducts = computed(() => {
  if (!search.value.trim()) return products.value;
  return products.value.filter((p) =>
    p.product_name.toLowerCase().includes(search.value.toLowerCase())
  );
});

// Navigation
const goToAddPage = () => router.push("/products/add");
const goToEditPage = (id: number) => router.push(`/products/update/${id}`);

// Delete product
const deleteProduct = async (id: number) => {
  if (!confirm("Are you sure you want to delete this product?")) return;
  try {
    loading.show();
    await axios.delete(`${backend}/product/delete/${id}`);
    products.value = products.value.filter((p) => p.id !== id);
    alert("Product deleted successfully.");
    loading.hide();
  } catch (err) {
    console.error("Failed to delete product:", err);
    alert("Failed to delete product.");
    loading.hide();
  }
};
</script>

<template>
  <div class="p-4 bg-[#111827] rounded-xl shadow-lg h-screen overflow-y-auto">
    <!-- Search and Add -->
    <div
      class="flex flex-col sm:flex-row justify-between items-center mb-4 sticky top-0 z-50 bg-[#111827] py-2 px-2 shadow rounded-lg">
      <input v-model="search" type="text" placeholder="Search product..."
        class="w-full sm:w-1/2 px-3 py-1.5 rounded-md border border-gray-700 bg-[#1f2937] text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-indigo-500 transition" />

      <button @click="goToAddPage"
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
            <th class="py-2 px-2 text-center">Stock</th>
            <th class="py-2 px-2 text-center">Actions</th>
          </tr>
        </thead>

        <tbody>
          <tr v-for="product in filteredProducts" :key="product.id"
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
            <td class="py-1 px-2 text-center">${{ product.product_price }}</td>
            <td class="py-1 px-2 text-center">{{ product.product_stock }}</td>

            <td class="py-2 px-2 text-center">
              <div class="flex justify-center items-center gap-2">
                <!-- Edit Button -->
                <button @click="goToEditPage(product.id)"
                  class="w-9 h-9 flex items-center justify-center rounded-md bg-blue-600 hover:bg-blue-500 text-white text-base transition hover:scale-105 shadow-md">
                  <i class="fa-solid fa-pen-to-square"></i>
                </button>

                <!-- Delete Button -->
                <button @click="deleteProduct(product.id)"
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
  </div>
</template>
