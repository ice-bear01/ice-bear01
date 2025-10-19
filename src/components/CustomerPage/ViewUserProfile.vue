<script setup lang="ts">
import { ref, onMounted } from "vue"
import axios from "axios"
import defaultProfileImage from "@/assets/img/logo.jpg"

const backend = import.meta.env.VITE_BACKEND_URL

interface UserAddress {
  id: number
  house_number: string
  street: string
  barangay: string
  city: string
  province: string
  is_active: boolean
}

const showForm = ref(false)
const addresses = ref<UserAddress[]>([])
const profileImage = ref(defaultProfileImage)
const email = ref("")
const fileInput = ref<HTMLInputElement | null>(null)

const newAddress = ref<Omit<UserAddress, "id" | "is_active">>({
  house_number: "",
  street: "",
  barangay: "",
  city: "",
  province: "",
})

const USE_MOCK = false

onMounted(async () => {
  if (USE_MOCK) {
    // --- Mock profile
    email.value = "mockuser@example.com"
    profileImage.value = defaultProfileImage

    // --- Mock addresses
    addresses.value = [
      {
        id: 1,
        house_number: "22B",
        street: "Sunrise St.",
        barangay: "Mabini",
        city: "Quezon City",
        province: "Metro Manila",
        is_active: true,
      },
      {
        id: 2,
        house_number: "45",
        street: "Luna Ave.",
        barangay: "San Miguel",
        city: "Pasig",
        province: "Metro Manila",
        is_active: false,
      },
    ]
    return
  }

  // ---------------- Fetch user profile ----------------
  try {
    const res = await axios.get(`${backend}/users/profile`, {
      withCredentials: true,
    })
    email.value = res.data.email
    if (res.data.profile_picture) profileImage.value = res.data.profile_picture
    await fetchAddresses()
  } catch (err) {
    console.error("Failed to fetch user profile:", err)
  }
})

// ---------------- Fetch addresses ----------------
const fetchAddresses = async () => {
  if (USE_MOCK) return
  try {
    const res = await axios.get<UserAddress[]>(
      `${backend}/users/addresses`,
      { withCredentials: true }
    )
    addresses.value = res.data
      .map(addr => ({ ...addr, is_active: addr.is_active ?? false }))
      .sort((a, b) => (b.is_active ? 1 : 0) - (a.is_active ? 1 : 0))
  } catch (err) {
    console.error("Failed to fetch addresses:", err)
  }
}

// ---------------- Upload new profile image ----------------
const handleImageUpload = (event: Event) => {
  const target = event.target as HTMLInputElement
  const file = target.files?.[0]
  if (!file) return

  const reader = new FileReader()
  reader.onload = async e => {
    const base64Image = e.target?.result as string
    profileImage.value = base64Image

    if (USE_MOCK) return
    try {
      const res = await axios.post(
        `${backend}/users/upload-profile-image`,
        { profile_image: base64Image },
        { withCredentials: true }
      )
      profileImage.value = res.data.image_url
    } catch (err) {
      console.error("Failed to upload profile image:", err)
    }
  }
  reader.readAsDataURL(file)
}

const triggerFilePicker = () => fileInput.value?.click()

// ---------------- Address CRUD ----------------
const addAddress = async () => {
  if (
    !newAddress.value.house_number ||
    !newAddress.value.street ||
    !newAddress.value.barangay ||
    !newAddress.value.city ||
    !newAddress.value.province
  ) {
    alert("Please fill in all fields")
    return
  }

  if (USE_MOCK) {
    addresses.value.push({
      id: Date.now(),
      ...newAddress.value,
      is_active: false,
    })
    showForm.value = false
    newAddress.value = { house_number: "", street: "", barangay: "", city: "", province: "" }
    return
  }

  try {
    await axios.post(
      `${backend}/users/address/add`,
      newAddress.value,
      { withCredentials: true }
    )
    await fetchAddresses()
    showForm.value = false
    newAddress.value = { house_number: "", street: "", barangay: "", city: "", province: "" }
  } catch (err) {
    console.error("Failed to add address:", err)
  }
}

const activateAddress = async (id: number) => {
  if (USE_MOCK) {
    addresses.value = addresses.value.map(addr => ({
      ...addr,
      is_active: addr.id === id,
    }))
    return
  }

  try {
    await axios.put(
      `${backend}/users/address/${id}/activate`,
      { is_active: true },
      { withCredentials: true }
    )
    await fetchAddresses()
  } catch (err) {
    console.error("Failed to activate address:", err)
  }
}

const deleteAddress = async (id: number) => {
  if (!confirm("Are you sure you want to delete this address?")) return

  if (USE_MOCK) {
    addresses.value = addresses.value.filter(addr => addr.id !== id)
    return
  }

  try {
    await axios.delete(`${backend}/users/address/${id}`, {
      withCredentials: true,
    })
    await fetchAddresses()
  } catch (err) {
    console.error("Failed to delete address:", err)
  }
}
</script>

<template>
  <div class="min-h-screen text-gray-800 p-4 sm:p-8">
    <div class="max-w-6xl mx-auto space-y-8">
      <!-- Profile Section -->
      <div
        class="relative bg-white/80 backdrop-blur-xl p-8 rounded-3xl shadow-2xl flex flex-col md:flex-row items-center md:items-start gap-8 border border-sky-100">
        <!-- Profile Picture -->
        <div class="relative group">
          <img :src="profileImage" alt="Profile"
            class="w-32 h-32 md:w-36 md:h-36 rounded-full border-4 border-sky-400 object-cover shadow-lg cursor-pointer hover:opacity-90 transition"
            @click="triggerFilePicker" />
          <div @click="triggerFilePicker"
            class="absolute inset-0 bg-black/40 rounded-full flex items-center justify-center opacity-0 group-hover:opacity-100 transition">
            <i class="fa-solid fa-camera text-white text-2xl"></i>
          </div>
          <input type="file" accept="image/*" class="hidden" ref="fileInput" @change="handleImageUpload" />
        </div>

        <!-- Info -->
        <div class="flex-1 text-center md:text-left">
          <h2 class="text-3xl font-bold text-sky-800 mb-2">User Profile</h2>
          <p class="text-gray-600 text-lg">
            <i class="fa-solid fa-envelope text-sky-400 mr-2"></i>{{ email }}
          </p>

          <button
            class="mt-6 bg-gradient-to-r from-sky-500 to-blue-600 hover:from-sky-600 hover:to-blue-700 text-white font-semibold px-6 py-2.5 rounded-full transition-all duration-200 shadow-md hover:shadow-lg flex items-center justify-center gap-2 mx-auto md:mx-0"
            @click="showForm = !showForm">
            <i :class="showForm ? 'fa-solid fa-xmark' : 'fa-solid fa-plus'"></i>
            {{ showForm ? "Cancel" : "Add Address" }}
          </button>

          <!-- Address Form -->
          <transition name="fade">
            <form v-if="showForm" @submit.prevent="addAddress"
              class="mt-6 bg-sky-50 p-5 rounded-2xl flex flex-col gap-3 shadow-inner border border-sky-100">
              <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
                <input v-model="newAddress.house_number" placeholder="House Number" class="input-style" />
                <input v-model="newAddress.street" placeholder="Street" class="input-style" />
                <input v-model="newAddress.barangay" placeholder="Barangay" class="input-style" />
                <input v-model="newAddress.city" placeholder="City" class="input-style" />
                <input v-model="newAddress.province" placeholder="Province" class="input-style md:col-span-2" />
              </div>
              <button type="submit" class="btn-primary mt-3">
                <i class="fa-solid fa-floppy-disk"></i> Save Address
              </button>
            </form>
          </transition>
        </div>
      </div>

      <!-- Addresses Section -->
      <div class="bg-white/80 backdrop-blur-xl p-8 rounded-3xl shadow-2xl border border-sky-100">
        <h2 class="text-3xl font-bold text-sky-800 mb-6 flex items-center gap-2">
          <i class="fa-solid fa-location-dot text-sky-500"></i> Delivery Addresses
        </h2>

        <div v-if="addresses.length === 0" class="text-gray-500 flex items-center gap-2">
          <i class="fa-solid fa-circle-exclamation text-yellow-500"></i>
          No addresses added yet.
        </div>

        <div class="flex flex-col gap-6">
          <div v-for="address in addresses" :key="address.id"
            class="relative bg-gradient-to-br from-white to-sky-50 border border-sky-100 rounded-2xl p-6 shadow-sm hover:shadow-md transition-all duration-200 hover:-translate-y-1">
            <div v-if="address.is_active"
              class="absolute top-3 right-3 bg-green-500 text-white text-xs px-3 py-1 rounded-full shadow">
              Active
            </div>

            <div class="space-y-2 text-gray-700 text-sm md:text-base">
              <div class="flex items-start gap-3">
                <span class="w-6 flex justify-center mt-1">
                  <i class="fa-solid fa-house text-sky-400"></i>
                </span>
                <p><b>House No:</b> {{ address.house_number }}</p>
              </div>

              <div class="flex items-start gap-3">
                <span class="w-6 flex justify-center mt-1">
                  <i class="fa-solid fa-road text-sky-400"></i>
                </span>
                <p><b>Street:</b> {{ address.street }}</p>
              </div>

              <div class="flex items-start gap-3">
                <span class="w-6 flex justify-center mt-1">
                  <i class="fa-solid fa-city text-sky-400"></i>
                </span>
                <p><b>Barangay:</b> {{ address.barangay }}</p>
              </div>

              <div class="flex items-start gap-3">
                <span class="w-6 flex justify-center mt-1">
                  <i class="fa-solid fa-building text-sky-400"></i>
                </span>
                <p><b>City:</b> {{ address.city }}</p>
              </div>

              <div class="flex items-start gap-3">
                <span class="w-6 flex justify-center mt-1">
                  <i class="fa-solid fa-map-location-dot text-sky-400"></i>
                </span>
                <p><b>Province:</b> {{ address.province }}</p>
              </div>
            </div>

            <div class="flex justify-end gap-2 mt-4">
              <button @click.stop="activateAddress(address.id)" :disabled="address.is_active"
                :class="address.is_active ? 'bg-gray-300 text-gray-600' : 'btn-primary'"
                class="px-4 py-1.5 rounded-full text-sm font-medium transition-transform hover:scale-105 flex items-center gap-1">
                <i class="fa-solid fa-toggle-on"></i>
                {{ address.is_active ? "Activated" : "Activate" }}
              </button>

              <button @click.stop="deleteAddress(address.id)"
                class="bg-red-500 hover:bg-red-600 text-white px-4 py-1.5 rounded-full text-sm font-medium transition-transform hover:scale-105 flex items-center gap-1">
                <i class="fa-solid fa-trash"></i> Delete
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
