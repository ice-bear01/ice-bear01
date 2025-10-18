<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'
import { useOrderStore } from '@/store/order'

const router = useRouter()
const orderStore = useOrderStore()

// Product interface
interface Product {
  product_id: number
  product_image?: string
  category: string
  product_type: string
  product_name: string
  product_price: number
  product_stock: number
  product_description?: string
}

// Products state
const products = ref<Product[]>([])

// Props for filtering
const props = defineProps<{
  searchQuery: string
  selectedType: string
}>()

// Computed filtered products
const filteredProducts = computed(() =>
  products.value.filter(
    (product) =>
      (props.selectedType === 'All' ||
        product.product_type.toLowerCase() === props.selectedType.toLowerCase()) &&
      product.product_name.toLowerCase().includes((props.searchQuery || '').toLowerCase())
  )
)

// Navigate to product detail page
const viewDetail = (category: string, product_id: number) => {
  router.push(`/product/${category}/${product_id}`)
}

// Open modal via Pinia (pass full product)
const orderProduct = (product: Product) => {
  orderStore.openModal(product)
}

// Fetch "Door" products from backend
onMounted(async () => {
  try {
    const { data } = await axios.get('http://localhost:8000/product/category/door')
    products.value = data.map((p: any) => ({
      product_id: p.id,
      product_image: p.product_image,
      category: p.category,
      product_type: p.product_type,
      product_name: p.product_name,
      product_price: p.product_price,
      product_stock: p.product_stock,
      product_description: p.product_description,
    }))
  } catch (error) {
    console.error('Failed to fetch products from backend:', error)

    // // 🧪 Temporary Mock Data for Responsive Testing (Fallback)
    // products.value = [
    //   {
    //     product_id: 1,
    //     product_image:
    //       'https://images.unsplash.com/photo-1582582424013-7a40a6b2d1f2?auto=format&fit=crop&w=600&q=80',
    //     category: 'Door',
    //     product_type: 'Sliding',
    //     product_name: 'Aluminum Sliding Door',
    //     product_price: 12000,
    //     product_stock: 15,
    //     product_description: 'Modern sliding door with tempered glass finish.',
    //   },
    //   {
    //     product_id: 2,
    //     product_image:
    //       'https://images.unsplash.com/photo-1572025442646-e417efc7b8c0?auto=format&fit=crop&w=600&q=80',
    //     category: 'Door',
    //     product_type: 'Swing',
    //     product_name: 'Classic Swing Door',
    //     product_price: 10500,
    //     product_stock: 10,
    //     product_description: 'Elegant swing door made from durable aluminum frame.',
    //   },
    //   {
    //     product_id: 3,
    //     product_image:
    //       'https://images.unsplash.com/photo-1505691938895-1758d7feb511?auto=format&fit=crop&w=600&q=80',
    //     category: 'Door',
    //     product_type: 'Folding',
    //     product_name: 'Folding Door Deluxe',
    //     product_price: 14000,
    //     product_stock: 8,
    //     product_description: 'Space-saving folding door with smooth glide mechanism',
    //   },
    //   {
    //     product_id: 4,
    //     product_image:
    //       'https://images.unsplash.com/photo-1598300052341-cd13d8b53b30?auto=format&fit=crop&w=600&q=80',
    //     category: 'Window',
    //     product_type: 'Casement',
    //     product_name: 'Casement Window Pro',
    //     product_price: 7000,
    //     product_stock: 20,
    //     product_description: 'Weather-sealed casement window for modern homes.',
    //   },
    //   {
    //     product_id: 5,
    //     product_image:
    //       'https://images.unsplash.com/photo-1593642634443-44adaa06623a?auto=format&fit=crop&w=600&q=80',
    //     category: 'Other',
    //     product_type: 'Glass tabletop',
    //     product_name: 'Tempered Glass Tabletop',
    //     product_price: 3500,
    //     product_stock: 25,
    //     product_description: 'Premium tempered glass tabletop for office or dining use.',
    //   },
    //   {
    //     product_id: 6,
    //     product_image:
    //       'https://images.unsplash.com/photo-1570129477492-45c003edd2be?auto=format&fit=crop&w=600&q=80',
    //     category: 'Other',
    //     product_type: 'Mirror',
    //     product_name: 'Beveled Wall Mirror',
    //     product_price: 2800,
    //     product_stock: 30,
    //     product_description: 'Stylish wall mirror with polished beveled edges.',
    //   },
    // ]
  }
})
</script>

<template>
  <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 xl:grid-cols-4 gap-6 mt-5">
    <div
      v-for="product in filteredProducts"
      :key="product.product_id"
      class="p-5 bg-white/10 rounded-3xl text-white flex flex-col justify-between hover:scale-[1.02] hover:bg-white/15 transition-transform"
    >
      <!-- Image -->
      <div class="w-full h-56 mb-3 rounded-2xl overflow-hidden bg-white/5 flex items-center justify-center">
        <img
          :src="product.product_image || ''"
          alt="Product Image"
          class="w-full h-full object-cover"
        />
      </div>

      <!-- Category & Type -->
      <p class="font-medium text-white/60 text-sm">
        {{ product.category }} — {{ product.product_type }}
      </p>

      <!-- Details -->
      <div class="my-2">
        <p class="font-semibold text-lg truncate">{{ product.product_name }}</p>
        <p class="text-white/70 text-sm">₱{{ product.product_price.toLocaleString() }}</p>
        <p class="text-white/70 text-sm">Stock: {{ product.product_stock }}</p>
        <p class="text-white/50 text-xs mt-1 line-clamp-2">
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
