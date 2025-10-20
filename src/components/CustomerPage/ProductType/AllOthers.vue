<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import axios from 'axios';
import { useRouter } from 'vue-router';
import { useOrderStore } from '@/store/order'; // Pinia store

const router = useRouter();
const orderStore = useOrderStore();
const backend = import.meta.env.VITE_BACKEND_URL
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
    product =>
      (props.selectedType === 'All' || product.product_type.toLowerCase() === props.selectedType.toLowerCase()) &&
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
    const { data } = await axios.get(`${backend}/product/category/others`);
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
  <div class="grid grid-cols-2 md:grid-cols-3 gap-4 mt-5">
    <div
      v-for="product in filteredProducts"
      :key="product.product_id"
      class="p-4 bg-white/10 rounded-3xl text-white flex flex-col justify-between"
    >
      <!-- Image Container -->
      <div class="w-full h-[300px] mb-2 rounded-2xl overflow-hidden bg-white/5 flex items-center justify-center">
        <img 
          :src="product.product_image || ''"
          alt="img"
          class="w-full h-full object-cover"
        />
      </div>

      <p class="font-medium text-white/70">{{ product.category }} - {{ product.product_type }}</p>

      <div class="mb-4">
        <p class="font-semibold text-lg">{{ product.product_name }}</p>
        <p class="text-white/70">Price: ${{ product.product_price }}</p>
        <p class="text-white/70">Stock: {{ product.product_stock }}</p>
        <p class="text-white/50 text-sm mt-1 truncate">{{ product.product_description }}</p>
      </div>

      <div class="flex gap-3 mt-auto">
        <button
          @click="viewDetail(product.category, product.product_id)"
          class="flex-1 px-4 py-2 bg-white/20 border border-white/30 rounded-3xl hover:bg-white/30 transition"
        >
          View Detail
        </button>
        <button
          @click="orderProduct(product)"
          class="flex-1 px-4 py-2 bg-green-500/30 border border-white/30 text-white rounded-3xl hover:bg-green-600 transition"
        >
          Order
        </button>
      </div>
    </div>
  </div>
</template>
