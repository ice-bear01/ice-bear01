<script setup>
import { ref, onMounted } from "vue";
import { useRoute, useRouter } from "vue-router";
import axios from "axios";
import { useLoadingStore } from "@/store/loading";

const loading = useLoadingStore();
const route = useRoute();
const router = useRouter();
const isEditing = ref(false);
const productId = ref(null);
const backend = import.meta.env.VITE_BACKEND_URL
// Product structure aligned with backend
const product = ref({
  category: "",
  product_image: "",
  product_image_file: null, // file object
  product_type: "",
  product_name: "",
  product_description: "",
  product_price: null,
  product_stock: null,
  key_benefits: [],
  specification: [],
  gallery: [],
});

// -----------------------------
// Fetch product if editing
// -----------------------------
onMounted(async () => {
  if (route.params.id) {
    isEditing.value = true;
    productId.value = route.params.id;
    const { data } = await axios.get(`${backend}/product/${productId.value}`);

    // Map backend response to local model
    product.value = {
      category: data.category,
      product_image: data.product_image,
      product_image_file: null,
      product_type: data.product_type,
      product_name: data.product_name,
      product_description: data.product_description,
      product_price: data.product_price,
      product_stock: data.product_stock,
      key_benefits: data.key_benefits.map(b => ({
        benefit_title: b.benefit_title,
        benefit_description: b.benefit_description
      })),
      specification: data.specification.map(s => ({
        specification_title: s.specification_title,
        specification_description: s.specification_description
      })),
      gallery: data.gallery.map(g => ({
        image: g.image,
        description: g.description,
        image_file: null,
      }))
    };
  }
});

// -----------------------------
// Dynamic list handling
// -----------------------------
const addKeyBenefit = () => product.value.key_benefits.push({ benefit_title: "", benefit_description: "" });
const removeKeyBenefit = (i) => product.value.key_benefits.splice(i, 1);

const addSpecification = () => product.value.specification.push({ specification_title: "", specification_description: "" });
const removeSpecification = (i) => product.value.specification.splice(i, 1);

const addGalleryItem = () => product.value.gallery.push({ image_file: null, image: "", description: "" });
const removeGalleryItem = (i) => product.value.gallery.splice(i, 1);

// -----------------------------
// File handling
// -----------------------------
const handleProductImage = (event) => {
  const file = event.target.files[0];
  if (file) {
    product.value.product_image_file = file;
    const reader = new FileReader();
    reader.onload = (e) => (product.value.product_image = e.target.result);
    reader.readAsDataURL(file);
  }
};

const handleGalleryImage = (event, index) => {
  const file = event.target.files[0];
  if (file) {
    product.value.gallery[index].image_file = file;
    const reader = new FileReader();
    reader.onload = (e) => {
      product.value.gallery[index].image = e.target.result; // for preview & backend
    };
    reader.readAsDataURL(file);
  }
};

// -----------------------------
// Submit with validation
// -----------------------------
const saveProduct = async () => {
  try {
    // ------------------------
    // Basic validation
    // ------------------------
    if (
      !product.value.category ||
      !product.value.product_type ||
      !product.value.product_name ||
      !product.value.product_description ||
      product.value.product_price === null ||
      product.value.product_stock === null
    ) {
      alert("Please fill in all required fields.");
      return;
    }

    const MAX_PRICE = 99999999.99; // matches DECIMAL(10,2)
    if (product.value.product_price > MAX_PRICE) {
      alert(`Price cannot exceed ${MAX_PRICE.toLocaleString()}`);
      return;
    }

    if (product.value.product_stock < 0) {
      alert("Stock cannot be negative");
      return;
    }

    for (const b of product.value.key_benefits) {
      if (!b.benefit_title || !b.benefit_description) {
        alert("Please fill in all key benefit fields.");
        return;
      }
    }

    for (const s of product.value.specification) {
      if (!s.specification_title || !s.specification_description) {
        alert("Please fill in all specification fields.");
        return;
      }
    }

    for (const g of product.value.gallery) {
      if (!g.image || !g.description) {
        alert("Please fill in all gallery items.");
        return;
      }
    }

    // ------------------------
    // Prepare payload
    // ------------------------
    const payload = {
      category: product.value.category,
      product_type: product.value.product_type,
      product_name: product.value.product_name,
      product_description: product.value.product_description,
      product_price: product.value.product_price,
      product_stock: product.value.product_stock,
      product_image: product.value.product_image,
      key_benefits: product.value.key_benefits,
      specification: product.value.specification,
      gallery: product.value.gallery.map(g => ({
        image: g.image,
        description: g.description
      }))
    };

    // ------------------------
    // Save to backend
    // ------------------------
    if (isEditing.value) {
      loading.show();
      await axios.put(`${backend}/product/update/${productId.value}`, payload);
    } else {
      loading.show();
      await axios.post(`${backend}/product/add-product`, payload);
    }
    loading.hide();
    alert("Product saved successfully!");
    router.go(-1);
  } catch (err) {
    console.error(err);
    alert("Error saving product.");
    loading.hide();
  }
};
</script>
<template>
  <div class="p-8 bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900 text-white rounded-2xl shadow-xl">
    <h2 class="text-3xl font-bold mb-6 text-center tracking-wide">
      {{ isEditing ? "Update Product" : "Add New Product" }}
    </h2>

    <form @submit.prevent="saveProduct" class="space-y-10">
      <!-- Product Details -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
        <!-- Left Column -->
        <div class="space-y-5">
          <div>
            <label class="block mb-1 text-gray-300 font-medium">Category</label>
            <input v-model="product.category" placeholder="Enter category"
              class="w-full p-3 rounded-lg bg-gray-700 border border-gray-600 focus:ring-2 focus:ring-blue-500 transition" required />
          </div>

          <div>
            <label class="block mb-1 text-gray-300 font-medium">Product Type</label>
            <input v-model="product.product_type" placeholder="Enter product type"
              class="w-full p-3 rounded-lg bg-gray-700 border border-gray-600 focus:ring-2 focus:ring-blue-500 transition" required />
          </div>

          <div>
            <label class="block mb-1 text-gray-300 font-medium">Product Name</label>
            <input v-model="product.product_name" placeholder="Enter product name"
              class="w-full p-3 rounded-lg bg-gray-700 border border-gray-600 focus:ring-2 focus:ring-blue-500 transition" required />
          </div>

          <div>
            <label class="block mb-1 text-gray-300 font-medium">Description</label>
            <textarea v-model="product.product_description" placeholder="Write a short description"
              rows="4" class="w-full p-3 rounded-lg bg-gray-700 border border-gray-600 focus:ring-2 focus:ring-blue-500 transition" required></textarea>
          </div>
        </div>

        <!-- Right Column -->
        <div class="space-y-5">
          <div>
            <label class="block mb-2 text-gray-300 font-medium">Product Image</label>
            <div
              class="border-2 border-dashed border-gray-600 p-5 rounded-xl flex flex-col items-center justify-center cursor-pointer hover:bg-gray-700 transition"
              @click="$refs.productImage.click()">
              <span v-if="!product.product_image" class="text-gray-400 text-sm">Click to upload image</span>
              <img v-if="product.product_image" :src="product.product_image"
                class="max-h-48 object-contain rounded-md shadow-md" />
            </div>
            <input ref="productImage" type="file" class="hidden" @change="handleProductImage" />
          </div>

          <div>
            <label class="block mb-1 text-gray-300 font-medium">Stock</label>
            <input type="number" v-model.number="product.product_stock" placeholder="Enter stock quantity"
              class="w-full p-3 rounded-lg bg-gray-700 border border-gray-600 focus:ring-2 focus:ring-blue-500 transition" required />
          </div>

          <div>
            <label class="block mb-1 text-gray-300 font-medium">Price</label>
            <input type="number" v-model.number="product.product_price" placeholder="Enter price"
              class="w-full p-3 rounded-lg bg-gray-700 border border-gray-600 focus:ring-2 focus:ring-blue-500 transition" required />
          </div>
        </div>
      </div>

      <!-- Key Benefits -->
      <div class="bg-gray-800/60 rounded-xl p-6 shadow-lg border border-gray-700">
        <div class="flex justify-between items-center mb-4">
          <h3 class="text-xl font-semibold text-white">Key Benefits</h3>
          <button type="button" @click="addKeyBenefit"
            class="px-3 py-1 rounded-lg bg-blue-600 hover:bg-blue-700 text-sm transition">+ Add Benefit</button>
        </div>

        <div v-for="(benefit, index) in product.key_benefits" :key="'benefit-' + index"
          class="bg-gray-700/70 p-4 rounded-lg mb-3 space-y-2">
          <input v-model="benefit.benefit_title" placeholder="Benefit Title"
            class="w-full p-2 rounded bg-gray-800 border border-gray-600 focus:ring-1 focus:ring-blue-400 transition" />
          <input v-model="benefit.benefit_description" placeholder="Benefit Description"
            class="w-full p-2 rounded bg-gray-800 border border-gray-600 focus:ring-1 focus:ring-blue-400 transition" />
          <button type="button" @click="removeKeyBenefit(index)"
            class="text-red-400 hover:text-red-500 text-sm">Remove</button>
        </div>
      </div>

      <!-- Specifications -->
      <div class="bg-gray-800/60 rounded-xl p-6 shadow-lg border border-gray-700">
        <div class="flex justify-between items-center mb-4">
          <h3 class="text-xl font-semibold text-white">Specifications</h3>
          <button type="button" @click="addSpecification"
            class="px-3 py-1 rounded-lg bg-blue-600 hover:bg-blue-700 text-sm transition">+ Add Spec</button>
        </div>

        <div v-for="(spec, index) in product.specification" :key="'spec-' + index"
          class="bg-gray-700/70 p-4 rounded-lg mb-3 space-y-2">
          <input v-model="spec.specification_title" placeholder="Specification Title"
            class="w-full p-2 rounded bg-gray-800 border border-gray-600 focus:ring-1 focus:ring-blue-400 transition" />
          <input v-model="spec.specification_description" placeholder="Specification Description"
            class="w-full p-2 rounded bg-gray-800 border border-gray-600 focus:ring-1 focus:ring-blue-400 transition" />
          <button type="button" @click="removeSpecification(index)"
            class="text-red-400 hover:text-red-500 text-sm">Remove</button>
        </div>
      </div>

      <!-- Gallery -->
      <div class="bg-gray-800/60 rounded-xl p-6 shadow-lg border border-gray-700">
        <div class="flex justify-between items-center mb-4">
          <h3 class="text-xl font-semibold text-white">Installation Gallery</h3>
          <button type="button" @click="addGalleryItem"
            class="px-3 py-1 rounded-lg bg-blue-600 hover:bg-blue-700 text-sm transition">+ Add Image</button>
        </div>

        <div class="flex gap-5 overflow-x-auto pb-3">
          <div v-for="(item, index) in product.gallery" :key="'gallery-' + index"
            class="min-w-[200px] border border-gray-700 bg-gray-700/70 p-3 rounded-xl flex flex-col items-center hover:scale-105 transition-transform duration-300 shadow-md">
            
            <div
              class="w-full h-48 flex items-center justify-center border border-gray-600 rounded-lg mb-2 cursor-pointer hover:bg-gray-800"
              @click="$refs['gallery' + index][0].click()">
              <span v-if="!item.image" class="text-sm text-gray-400">Upload</span>
              <img v-if="item.image" :src="item.image" class="object-cover h-48 w-full rounded-lg" />
            </div>

            <input type="file" class="hidden" :ref="'gallery' + index" @change="e => handleGalleryImage(e, index)" />
            <input v-model="item.description" placeholder="Caption"
              class="p-2 rounded bg-gray-800 border border-gray-600 w-full text-sm focus:ring-1 focus:ring-blue-400 transition" />
            <button type="button" @click="removeGalleryItem(index)"
              class="text-red-400 hover:text-red-500 text-sm mt-1">Remove</button>
          </div>
        </div>
      </div>

      <!-- Buttons -->
      <div class="flex justify-end gap-4 pt-4">
        <button type="button" @click="router.go(-1)"
          class="px-5 py-2 rounded-lg bg-gray-600 hover:bg-gray-700 transition font-medium">Cancel</button>
        <button type="submit"
          class="px-5 py-2 rounded-lg bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 transition font-semibold shadow-md">
          {{ isEditing ? "Update Product" : "Add Product" }}
        </button>
      </div>
    </form>
  </div>
</template>
