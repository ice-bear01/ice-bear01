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

// Navigate to product detail page
const viewDetail = (category: string, product_id: number) => {
  router.push(`/product/${category}/${product_id}`);
};

// Open modal via Pinia (pass full product)
const orderProduct = (product: Product) => {
  orderStore.openModal(product);
};

// ✅ Fetch "Window" products from backend
onMounted(async () => {
  try {
    const { data } = await axios.get(`${backend}/product/category/window`);
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
    console.error('Failed to fetch window products:', error);
  }
});
</script>

<template>
  <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 xl:grid-cols-4 gap-6 mt-5">
    <div
      v-for="product in filteredProducts"
      :key="product.product_id"
      class="w-full max-w-[280px] h-[460px] mx-auto p-5 bg-white/10 rounded-3xl text-white flex flex-col hover:scale-[1.02] hover:bg-white/15 transition-transform"
    >
      <!-- Image container -->
      <div
        class="w-full h-[200px] mb-3 rounded-2xl overflow-hidden bg-white/5 flex items-center justify-center"
      >
        <img
          :src="product.product_image || ''"
          alt="Product Image"
          class="w-full h-full object-cover object-center"
        />
      </div>

      <!-- Category & Type -->
      <p class="font-medium text-white/60 text-sm">
        {{ product.category }} — {{ product.product_type }}
      </p>

      <!-- Product Details -->
      <div class="my-2 flex-1">
        <p class="font-semibold text-lg truncate">{{ product.product_name }}</p>
        <p class="text-white/70 text-sm">₱{{ product.product_price.toLocaleString() }}</p>
        <p class="text-white/70 text-sm">Stock: {{ product.product_stock }}</p>
        <p class="text-white/50 text-xs mt-1 line-clamp-2 truncate">
          {{ product.product_description }}
        </p>
      </div>

      <!-- Buttons -->
      <div class="flex gap-3 mt-auto">
        <button
          @click="viewDetail(product.category, product.product_id)"
          class="flex-1 px-4 py-2 bg-white/20 border border-white/30 rounded-3xl hover:bg-white/30 transition"
        >
          View
        </button>
        <button
          @click="orderProduct(product)"
          class="flex-1 px-4 py-2 bg-green-500/30 border border-white/30 text-white rounded-3xl hover:bg-green-600/60 transition"
        >
          Order
        </button>
      </div>
    </div>
  </div>
</template>
