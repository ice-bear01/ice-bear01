<script setup lang="ts">
import { ref, watch } from 'vue'
import { useOrderStore } from '@/store/order'

const backend = import.meta.env.VITE_BACKEND_URL
const orderStore = useOrderStore()
const orderNote = ref<string>('')

// numeric value for submission
const quantity = ref<number>(1)
// string bound to input so user can freely edit (can be empty while typing)
const quantityInput = ref<string>('1')

const loading = ref(false)
const errorMessage = ref('')
const successMessage = ref('')
const showInfo = ref(false)

watch(
  () => orderStore.selectedProduct,
  () => {
    quantity.value = 1
    quantityInput.value = '1'
    errorMessage.value = ''
    successMessage.value = ''
  }
)

const handleQuantityInput = (ev: Event) => {
  const input = ev.target as HTMLInputElement
  // allow empty
  let v = input.value
  // remove non-digits but keep empty
  v = v.replace(/[^\d]/g, '')
  // prevent multiple leading zeros
  if (v.length > 1 && v.startsWith('0')) {
    v = v.replace(/^0+/, '')
  }
  // update model (keep empty allowed)
  quantityInput.value = v
}

/**
 * When leaving the input, clamp to 1..99 and update numeric quantity.
 */
const handleQuantityBlur = () => {
  if (quantityInput.value === '' || quantityInput.value === null) {
    quantity.value = 1
    quantityInput.value = '1'
    return
  }

  let parsed = parseInt(quantityInput.value, 10)
  if (isNaN(parsed) || parsed < 1) parsed = 1
  if (parsed > 99) parsed = 99

  quantity.value = parsed
  quantityInput.value = String(parsed)
}

/**
 * Validate just before submit (ensures numeric quantity is set correctly).
 */
const validateQuantityBeforeSubmit = () => {
  if (quantityInput.value === '' || quantityInput.value === null) {
    quantity.value = 1
    quantityInput.value = '1'
    return
  }
  let parsed = parseInt(quantityInput.value.replace(/[^\d]/g, ''), 10)
  if (isNaN(parsed) || parsed < 1) parsed = 1
  if (parsed > 99) parsed = 99
  quantity.value = parsed
  quantityInput.value = String(parsed)
}

const confirmOrder = async () => {
  if (!orderStore.selectedProduct) return

  validateQuantityBeforeSubmit()

  errorMessage.value = ''
  successMessage.value = ''
  loading.value = true

  if (quantity.value < 1) {
    errorMessage.value = 'Quantity must be at least 1.'
    loading.value = false
    return
  }

  if (quantity.value > 99) {
    errorMessage.value = 'Quantity cannot exceed 99.'
    loading.value = false
    return
  }

  const payload = {
    product_id: orderStore.selectedProduct.product_id,
    quantity: quantity.value,
    order_note: orderNote.value,
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
  <div v-if="orderStore.showModal" class="fixed inset-0 bg-black/60 flex items-center justify-center z-60 p-4">
    <div
      class="relative bg-white/80 rounded-3xl p-6 w-full max-w-[700px] backdrop-blur-md shadow-lg flex flex-col md:flex-row gap-6 items-center md:items-start overflow-y-auto max-h-[550px] sm:max-h-[450px]">
      <!-- Info icon + tooltip (use mouseover/mouseout for reliability) -->


      <!-- Product Image -->
      <div class="w-full md:w-1/2 h-56 md:h-64 rounded-2xl overflow-hidden bg-white/5 flex-shrink-0">
        <img :src="orderStore.selectedProduct?.product_image" alt="Product" class="w-full h-full object-cover" />
      </div>

      <!-- Product Details -->
      <div class="flex-1 flex flex-col gap-3 text-center md:text-left">
        <h2 class="text-2xl font-bold text-[#006989]">
          {{ orderStore.selectedProduct?.product_name }}
        </h2>

        <p class="text-gray-900 text-sm">
          <i class="fas fa-layer-group mr-1"></i>
          {{ orderStore.selectedProduct?.category }} -
          {{ orderStore.selectedProduct?.product_type }}
        </p>

        <p class="text-gray-900 cursor-pointer">
          <i class="fas fa-peso-sign mr-1"></i>
          Price/Meter:
          <span class="text-green-500">₱{{ orderStore.selectedProduct?.product_price }}</span>
        </p>

        <!-- Red clickable note -->
        <p class="text-red-600 underline cursor-pointer text-sm" @click="showInfo = !showInfo">
          Note: Prices shown are estimated
        </p>

        <!-- Tooltip popup (reusing showInfo) -->
        <transition name="fade">
          <div v-if="showInfo"
            class="bg-white text-black text-sm p-3 rounded-lg shadow-lg border border-gray-300 mt-2 w-full">
            <p class="font-semibold text-[#006989] mb-1">Product Info</p>
            <p class="leading-snug">
              Prices shown are estimated and based on price per meter.
              Final cost will depend on the actual measurements taken by our staff during
              <strong>on-site</strong> assessment.
            </p>
          </div>
        </transition>

        <p class="text-gray-900 text-sm mt-1 truncate-multiline">
          {{ orderStore.selectedProduct?.product_description }}
        </p>
        <!-- Order Note Input -->
        <div class="mt-2 flex flex-col gap-1">
          <label for="order-note" class="text-gray-900 text-sm font-medium">Size/Measurement note:</label>
          <textarea id="order-note" v-model="orderNote" placeholder="Optional note..." rows="3"
            class="w-full text-black rounded-md px-2 py-1 border border-gray-900 resize-none focus:outline-none focus:ring-1 focus:ring-[#006989]"></textarea>
        </div>

        <!-- Quantity Input -->
        <div class="mt-2 flex flex-col sm:flex-row items-center gap-2 justify-center md:justify-start">
          <label for="quantity" class="text-gray-900 flex items-center gap-1">
            <i class="fas fa-sort-numeric-up"></i> Quantity:
          </label>

          <!-- v-model allows the user to delete the '1' and type freely -->
          <input
  id="quantity"
  type="text"
  inputmode="numeric"
  maxlength="3"
  v-model="quantityInput"
  @input="handleQuantityInput"
  @blur="handleQuantityBlur"
  class="w-24 text-black rounded-md px-2 py-1 
         border border-gray-400 bg-white 
         focus:border-blue-500 focus:ring-2 focus:ring-blue-300"
  placeholder="1"
  aria-label="Order quantity"
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
          <button @click="confirmOrder" :disabled="loading"
            class="flex-1 px-4 py-2 bg-green-500/30 border border-white/30 rounded-3xl hover:bg-green-600 transition flex items-center justify-center gap-2">
            <i class="fas fa-check"></i>
            {{ loading ? 'Processing...' : 'Confirm' }}
          </button>
          <button @click="closeModal" :disabled="loading"
            class="flex-1 px-4 py-2 bg-red-500/30 border border-white/30 rounded-3xl hover:bg-red-600 transition flex items-center justify-center gap-2">
            <i class="fas fa-times"></i> Cancel
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.18s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
