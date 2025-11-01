<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import axios from 'axios'
import { useOrderStore } from '@/store/order'

const backend = import.meta.env.VITE_BACKEND_URL
const orderStore = useOrderStore()
const route = useRoute()
const product_id = Number(route.params.product_id)

// Interfaces
interface KeyBenefit {
  benefit_title: string
  benefit_description: string
}

interface Specification {
  specification_title: string
  specification_description: string
}

interface Gallery {
  image: string
  description: string
}

interface ProductDetail {
  id: number
  category: string
  product_image: string
  product_type: string
  product_name: string
  product_description: string
  product_price: number
  product_stock: number
  benefits: KeyBenefit[]
  specification: Specification[]
  installation_gallery: Gallery[]
}

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

const product = ref<ProductDetail | null>(null)

onMounted(async () => {
  try {
    const { data } = await axios.get(`${backend}/product/${product_id}`)
    product.value = data
  } catch (error) {
    console.error('Failed to fetch product:', error)
  }
})

const orderProduct = () => {
  if (!product.value) return

  const simpleProduct: Product = {
    product_id: product.value.id,
    product_image: product.value.product_image,
    category: product.value.category,
    product_type: product.value.product_type,
    product_name: product.value.product_name,
    product_price: product.value.product_price,
    product_stock: product.value.product_stock,
    product_description: product.value.product_description,
  }

  orderStore.openModal(simpleProduct)
}
</script>

<template>
  <div class="w-full flex flex-col items-center">

    <!-- 🔹 Top Section -->
    <div
      class="w-full flex flex-col lg:flex-row gap-8 p-6 lg:p-10 max-w-7xl"
    >
      <!-- 🖼 Left: Product Image -->
      <div
        class="w-full lg:w-[500px] flex-shrink-0 flex items-center justify-center rounded-3xl overflow-hidden"
      >
        <img
          v-if="product"
          :src="product.product_image"
          alt="Product Image"
          class="w-full h-[300px] sm:h-[400px] lg:h-[500px] object-cover rounded-3xl"
        />
      </div>

      <!-- 📋 Right: Product Details -->
      <div
        class="flex-1 flex flex-col bg-white/80 rounded-2xl p-6 sm:p-8 gap-6"
      >
        <div class="flex-1 overflow-y-auto scrollbar-custom">
          <div v-if="product" class="flex flex-col gap-6">

            <!-- Product Title & Description -->
            <div>
              <p class="text-[#006989] font-semibold text-sm sm:text-base">
                {{ product.category }} - {{ product.product_type }}
              </p>
              <h1 class="text-2xl sm:text-3xl lg:text-4xl font-bold mt-2">
                {{ product.product_name }}
              </h1>
              <p class="text-gray-700 mt-2 text-sm sm:text-base">
                {{ product.product_description }}
              </p>
            </div>

            <!-- Specifications -->
            <div>
              <p class="text-lg sm:text-xl font-semibold mb-3 flex items-center gap-2">
                <i class="fas fa-cogs text-sky-500"></i> Material Specifications
              </p>
              <div class="grid sm:grid-cols-2 lg:grid-cols-3 gap-4">
                <div
                  v-for="spec in product.specification"
                  :key="spec.specification_title"
                  class="p-4 rounded-xl border-l-4 border-sky-500 bg-white flex flex-col gap-2"
                >
                  <p class="font-semibold text-base sm:text-lg">
                    {{ spec.specification_title }}
                  </p>
                  <p class="text-gray-700 text-sm sm:text-base">
                    {{ spec.specification_description }}
                  </p>
                </div>
              </div>
            </div>

            <!-- Key Benefits -->
            <div>
              <p class="text-lg sm:text-xl font-semibold mb-3 flex items-center gap-2">
                <i class="fas fa-star text-sky-500"></i> Key Benefits
              </p>
              <div class="grid sm:grid-cols-2 lg:grid-cols-3 gap-4">
                <div
                  v-for="benefit in product.benefits"
                  :key="benefit.benefit_title"
                  class="p-4 rounded-xl border-l-4 border-sky-500 bg-white flex flex-col gap-2"
                >
                  <p class="font-semibold text-base sm:text-lg">
                    {{ benefit.benefit_title }}
                  </p>
                  <p class="text-gray-700 text-sm sm:text-base">
                    {{ benefit.benefit_description }}
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 💵 Price & Order -->
        <div class="flex flex-col sm:flex-row justify-between items-center gap-4 border-t border-gray-300 pt-4">
          <div class="flex flex-col sm:flex-row items-center gap-4 text-gray-700 text-base sm:text-lg">
            <div class="flex items-center gap-2">
              <i class="fas fa-peso-sign text-green-500"></i>
              <span>{{ product?.product_price }}</span>
            </div>
            <div class="flex items-center gap-2">
              <i class="fas fa-box text-blue-500"></i>
              <span>{{ product?.product_stock }} in stock</span>
            </div>
          </div>

          <button
            @click="orderProduct"
            class="flex items-center gap-2 px-6 py-3 bg-green-500 hover:bg-green-600 rounded-2xl font-semibold text-white transition w-full sm:w-auto justify-center"
          >
            <i class="fas fa-cart-plus"></i>
            Order Now
          </button>
        </div>
      </div>
    </div>

    <!-- 🔹 Gallery Title -->
    <div class="w-full flex justify-center mt-10">
      <p class="text-2xl sm:text-3xl lg:text-4xl font-bold text-white text-center">
        Real Installation Gallery
      </p>
    </div>

    <!-- 🔹 Gallery Section -->
    <div class="w-full p-6 sm:p-10 grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
      <div
        v-if="product?.installation_gallery.length"
        v-for="img in product.installation_gallery"
        :key="img.image"
        class="rounded-3xl overflow-hidden relative cursor-pointer group bg-white/80 backdrop-blur-md border border-gray-500/70 hover:scale-[1.02] transition-transform p-2 max-w-[300px]"
      >
        <!-- Image -->
        <div class="h-56 sm:h-64 w-full relative rounded-t-3xl overflow-hidden">
          <img
            :src="img.image"
            alt="Gallery Image"
            class="w-full h-full object-cover transition-transform group-hover:scale-110"
          />
        </div>

        <!-- Description -->
        <div class="p-6 text-gray-900 text-center bg-white/5">
          <p class="text-sm sm:text-base">{{ img.description }}</p>
        </div>
      </div>
    </div>

  </div>
</template>
