<script setup lang="ts">
import { ref, watch } from 'vue'
import { useOrderStore } from '@/store/order'

const backend = import.meta.env.VITE_BACKEND_URL

const orderStore = useOrderStore()
const quantity = ref(1)
const loading = ref(false)
const errorMessage = ref('')
const successMessage = ref('')

// Reset quantity and messages when product changes
watch(
  () => orderStore.selectedProduct,
  () => {
    quantity.value = 1
    errorMessage.value = ''
    successMessage.value = ''
  }
)

const confirmOrder = async () => {
  if (!orderStore.selectedProduct) return

  errorMessage.value = ''
  successMessage.value = ''
  loading.value = true

  const payload = {
    product_id: orderStore.selectedProduct.product_id,
    quantity: quantity.value,
  }

  try {
    const response = await fetch(`${backend}/orders/add-order`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(payload),
      credentials: 'include',
    })

    if (!response.ok) {
      const errorData = await response.json()
      errorMessage.value = errorData.detail || 'Failed to place order.'
      return
    }

    const orderData = await response.json()
    console.log('Order placed successfully:', orderData)
    successMessage.value = 'Order placed successfully!'

    setTimeout(() => {
      orderStore.closeModal()
      successMessage.value = ''
    }, 1000)
  } catch (err) {
    console.error('Network error:', err)
    errorMessage.value = 'Network error. Please try again.'
  } finally {
    loading.value = false
  }
}

const closeModal = () => {
  orderStore.closeModal()
  errorMessage.value = ''
  successMessage.value = ''
}
</script>

<template>
  <div
    v-if="orderStore.showModal"
    class="fixed inset-0 bg-black/60 flex items-center justify-center z-50 p-4"
  >
    <div
      class="bg-white/10 text-white rounded-3xl p-6 w-full max-w-[700px] backdrop-blur-md shadow-lg flex flex-col md:flex-row gap-6 items-center md:items-start overflow-y-auto max-h-[550px]"
    >
      <!-- Product Image -->
      <div class="w-full md:w-1/2 h-56 md:h-64 rounded-2xl overflow-hidden bg-white/5 flex-shrink-0">
        <img
          :src="orderStore.selectedProduct?.product_image"
          alt="Product"
          class="w-full h-full object-cover"
        />
      </div>

      <!-- Product Details -->
      <div class="flex-1 flex flex-col gap-3 text-center md:text-left">
        <h2 class="text-2xl font-bold">{{ orderStore.selectedProduct?.product_name }}</h2>
        <p class="text-white/70 text-sm">
          <i class="fas fa-layer-group mr-1"></i>
          {{ orderStore.selectedProduct?.category }} -
          {{ orderStore.selectedProduct?.product_type }}
        </p>
        <p class="text-white/70">
          <i class="fas fa-dollar-sign mr-1"></i>
          Price: ₱{{ orderStore.selectedProduct?.product_price }}
        </p>
        <p class="text-white/70">
          <i class="fas fa-boxes mr-1"></i>
          Stock: {{ orderStore.selectedProduct?.product_stock }}
        </p>
        <p class="text-white/50 text-sm mt-1">
          {{ orderStore.selectedProduct?.product_description }}
        </p>

        <!-- Quantity Input -->
        <div class="mt-2 flex flex-col sm:flex-row items-center gap-2 justify-center md:justify-start">
          <label for="quantity" class="text-white/70 flex items-center gap-1">
            <i class="fas fa-sort-numeric-up"></i> Quantity:
          </label>
          <input
            id="quantity"
            type="number"
            min="1"
            :max="orderStore.selectedProduct?.product_stock"
            v-model.number="quantity"
            class="w-24 text-black rounded-md px-2 py-1"
          />
        </div>

        <!-- Feedback -->
        <p v-if="errorMessage" class="text-red-400 text-sm mt-1">
          {{ errorMessage }}
        </p>
        <p v-if="successMessage" class="text-green-400 text-sm mt-1">
          {{ successMessage }}
        </p>

        <!-- Buttons -->
        <div class="flex flex-col sm:flex-row gap-3 mt-4">
          <button
            @click="confirmOrder"
            :disabled="loading"
            class="flex-1 px-4 py-2 bg-green-500/30 border border-white/30 rounded-3xl hover:bg-green-600 transition flex items-center justify-center gap-2"
          >
            <i class="fas fa-check"></i>
            {{ loading ? 'Processing...' : 'Confirm' }}
          </button>
          <button
            @click="closeModal"
            :disabled="loading"
            class="flex-1 px-4 py-2 bg-red-500/30 border border-white/30 rounded-3xl hover:bg-red-600 transition flex items-center justify-center gap-2"
          >
            <i class="fas fa-times"></i> Cancel
          </button>
        </div>
      </div>
    </div>
  </div>
</template>
