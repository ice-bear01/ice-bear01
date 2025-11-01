<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import axios from 'axios';
import { useRouter } from 'vue-router';
import { useOrderStore } from '@/store/order'; // Pinia store

const router = useRouter();
const orderStore = useOrderStore();
const backend = import.meta.env.VITE_BACKEND_URL;

interface Product {
  product_id: number;
  product_image?: string;
  category: string;
  product_type: string;
  product_name: string;
  product_price: number;
  product_stock: number;
  product_description?: string;
}

const products = ref<Product[]>([]);

const props = defineProps<{
  searchQuery: string;
  selectedType: string;
}>();

const filteredProducts = computed(() =>
  products.value.filter(
    (product) =>
      (props.selectedType === 'All' ||
        product.product_type.toLowerCase() === props.selectedType.toLowerCase()) &&
      product.product_name.toLowerCase().includes((props.searchQuery || '').toLowerCase())
  )
);

const viewDetail = (category: string, product_id: number) => {
  router.push(`/product/${category}/${product_id}`);
};

const orderProduct = (product: Product) => {
  orderStore.openModal(product);
};

// ✅ Fetch "Others" products from backend
onMounted(async () => {
  try {
    const { data } = await axios.get(`${backend}/product/category/Others`);
    products.value = data.map((p: any) => ({
      product_id: p.id,
      product_image: p.product_image,
      category: p.category,
      product_type: p.product_type,
      product_name: p.product_name,
      product_price: p.product_price,
      product_stock: p.product_stock,
      product_description: p.product_description,
    }));
  } catch (error) {
    console.error('Failed to fetch others products:', error);
  }
});
</script>

<template>
  <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 xl:grid-cols-4 gap-6 mt-5">
    <div v-for="product in filteredProducts" :key="product.product_id"
      class="w-full max-w-[280px] h-[480px] mx-auto p-5 bg-white/80 border border-sky-100 rounded-3xl text-gray-800 flex flex-col shadow-2xl transition-all duration-300 hover:scale-105 hover:shadow-xl">
      <!-- Image -->
      <div class="w-full h-[200px] mb-3 rounded-2xl overflow-hidden flex items-center justify-center bg-white/5">
        <img :src="product.product_image || ''" alt="Product Image" class="w-full h-full object-cover object-center" />
      </div>

      <!-- Category & Type -->
      <p class="font-medium text-gray-600 text-sm uppercase">
        {{ product.category }} — {{ product.product_type }}
      </p>

      <!-- Product Details -->
      <div class="my-2 flex-1">
        <p class="font-semibold text-lg uppercase truncate text-[#006989]">{{ product.product_name }}</p>
        <p class="text-sm">
          <i class="fas fa-peso-sign mr-1"></i>
          Price/Meter:
          <span class=" text-green-500">₱{{ product.product_price.toLocaleString() }}</span>
        </p>
        <p class="text-gray-600 text-sm">Stock: {{ product.product_stock }}</p>
        <p class="text-gray-500 text-xs mt-1 truncate-multiline">
          {{ product.product_description }}
        </p>
      </div>

      <!-- Buttons -->
      <div class="flex gap-3 mt-auto">
        <button @click="viewDetail(product.category, product.product_id)"
          class="flex-1 px-4 py-2 bg-gradient-to-r from-sky-500 to-blue-600 hover:from-sky-600 hover:to-blue-700 text-white font-semibold rounded-full shadow-md flex items-center justify-center gap-2 transition-all duration-200">
          <i class="fa-solid fa-eye"></i> View
        </button>
        <button @click="orderProduct(product)"
          class="flex-1 px-4 py-2 bg-green-500/80 border border-white/30 text-white rounded-full shadow-md hover:bg-green-600/60 transition-all duration-200">
          <i class="fa-solid fa-cart-plus"></i> Order
        </button>
      </div>
    </div>
  </div>
</template>
