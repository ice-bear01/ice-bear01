<script setup>
import { ref, onMounted, watch } from "vue";
import { useRoute, useRouter } from "vue-router";
import axios from "axios";
import { useLoadingStore } from "@/store/loading";

const loading = useLoadingStore();
const route = useRoute();
const router = useRouter();
const isEditing = ref(false);
const productId = ref(null);
const backend = import.meta.env.VITE_BACKEND_URL;

// -----------------------------
// Product structure
// -----------------------------
const product = ref({
  category: "",
  product_image: "",
  product_image_file: null,
  product_type: "",
  product_name: "",
  product_description: "",
  product_price: null,
  benefits: [],
  specification: [],
  installation_gallery: [],
});

// -----------------------------
// Modal
// -----------------------------
const showModal = ref(false);
const modalTitle = ref("");
const modalMessage = ref("");
const modalConfirm = ref(null);

const openModal = (title, message, onConfirm = null) => {
  modalTitle.value = title;
  modalMessage.value = message;
  modalConfirm.value = onConfirm;
  showModal.value = true;
};

const closeModal = () => {
  showModal.value = false;
};

// -----------------------------
// Dropdown options
// -----------------------------
const categories = ["Doors", "Windows", "Others"];
const typeMap = {
  Doors: ["Sliding", "Swing", "Folding", "Bifold"],
  Windows: ["Sliding", "Casement", "Awning", "Fixed", "Swing", "Side Opening"],
  Others: ["Glass Tabletops", "Mirrors", "Shelving", "Railing", "Panel", "Frame", "Display Cases", "Others"],
};
const typeOptions = ref([]);

watch(() => product.value.category, (newCategory, oldCategory) => {
  typeOptions.value = typeMap[newCategory] || [];
  if (oldCategory && oldCategory !== newCategory) {
    product.value.product_type = "";
  }
});

// -----------------------------
// Fetch product if editing
// -----------------------------
onMounted(async () => {
  if (route.params.id) {
    isEditing.value = true;
    productId.value = route.params.id;
    const { data } = await axios.get(`${backend}/product/${productId.value}`);
    product.value = {
      category: data.category,
      product_image: data.product_image,
      product_image_file: null,
      product_type: data.product_type,
      product_name: data.product_name,
      product_description: data.product_description,
      product_price: data.product_price,
      benefits: data.benefits.map(b => ({ ...b })),
      specification: data.specification.map(s => ({ ...s })),
      installation_gallery: data.installation_gallery.map(g => ({
        image: g.image,
        description: g.description,
        image_file: null,
      })),
    };
    typeOptions.value = typeMap[product.value.category] || [];
  }
});

// -----------------------------
// Dynamic list handling
// -----------------------------
const addKeyBenefit = () => product.value.benefits.push({ benefit_title: "", benefit_description: "" });
const removeKeyBenefit = (i) => product.value.benefits.splice(i, 1);

const addSpecification = () => product.value.specification.push({ specification_title: "", specification_description: "" });
const removeSpecification = (i) => product.value.specification.splice(i, 1);

const addGalleryItem = () => product.value.installation_gallery.push({ image_file: null, image: "", description: "" });
const removeGalleryItem = (i) => product.value.installation_gallery.splice(i, 1);

// -----------------------------
// Image File Validations
// -----------------------------
const isValidImage = (file) => {
  return file && file.type.startsWith("image/");
};

// Product Image
const handleProductImage = (event) => {
  const file = event.target.files[0];
  if (!file) return;

  if (!isValidImage(file)) {
    openModal("Invalid File", "Only image files (JPG, PNG, WEBP) are allowed.");
    return;
  }

  product.value.product_image_file = file;
  const reader = new FileReader();
  reader.onload = (e) => (product.value.product_image = e.target.result);
  reader.readAsDataURL(file);
};

// Gallery Image
const handleGalleryImage = (event, index) => {
  const file = event.target.files[0];
  if (!file) return;

  if (!isValidImage(file)) {
    openModal("Invalid File", "Only image files (JPG, PNG, WEBP) are allowed.");
    return;
  }

  product.value.installation_gallery[index].image_file = file;

  const reader = new FileReader();
  reader.onload = (e) => {
    product.value.installation_gallery[index].image = e.target.result;
  };
  reader.readAsDataURL(file);
};

// -----------------------------
// Save product
// -----------------------------
const saveProduct = async () => {
  try {
    // Required Fields
    if (!product.value.category || !product.value.product_type || !product.value.product_name ||
      !product.value.product_description || product.value.product_price === null) {
      openModal("Missing Required Fields", "Please fill in all required fields.");
      return;
    }

    // ADD MODE – Require Image
    if (!isEditing.value && !product.value.product_image_file) {
      openModal("Image Required", "Please upload a product image before submitting.");
      return;
    }

    // Price Validation
    const MAX_PRICE = 99999999.99;
    if (product.value.product_price > MAX_PRICE) {
      openModal("Invalid Price", `Price cannot exceed ${MAX_PRICE.toLocaleString()}.`);
      return;
    }

    // Benefits Validation
    for (const b of product.value.benefits) {
      if (!b.benefit_title || !b.benefit_description) {
        openModal("Missing Benefit Details", "Please complete all key benefit fields.");
        return;
      }
    }

    // Specification Validation
    for (const s of product.value.specification) {
      if (!s.specification_title || !s.specification_description) {
        openModal("Missing Specification", "Please complete all specification fields.");
        return;
      }
    }

    // Gallery Validation
    for (const g of product.value.installation_gallery) {
      if (!g.image || !g.description) {
        openModal("Incomplete Gallery", "Please add an image and caption to all gallery items.");
        return;
      }
    }

    // Payload
    const payload = {
      category: product.value.category,
      product_type: product.value.product_type,
      product_name: product.value.product_name,
      product_description: product.value.product_description,
      product_price: product.value.product_price,
      product_image: product.value.product_image,
      benefits: product.value.benefits,
      specification: product.value.specification,
      installation_gallery: product.value.installation_gallery.map(g => ({ image: g.image, description: g.description })),
    };

    loading.show();

    if (isEditing.value) {
      await axios.put(`${backend}/product/update/${productId.value}`, payload);
      loading.hide();
      openModal("Success", "Product updated successfully!", () => router.go(-1));
    } else {
      await axios.post(`${backend}/product/add-product`, payload);
      loading.hide();
      openModal("Success", "Product added successfully!", () => router.go(-1));
    }

  } catch (err) {
    console.error(err);
    loading.hide();
    openModal("Error", "An error occurred while saving the product.");
  }
};
</script>

<template>
  <!-- CUSTOM MODAL -->
  <div v-if="showModal"
    class="fixed inset-0 bg-black/60 backdrop-blur-sm flex items-center justify-center z-[9999] p-4">
    <div class="bg-gray-800 p-6 rounded-xl shadow-xl w-full max-w-md border border-gray-700">
      <h2 class="text-xl font-bold mb-3 text-white">{{ modalTitle }}</h2>
      <p class="text-gray-300 mb-6">{{ modalMessage }}</p>

      <div class="flex justify-end gap-3">
        <button @click="closeModal"
          class="px-4 py-2 bg-gray-600 hover:bg-gray-700 rounded-lg">
          Close
        </button>

        <button v-if="modalConfirm"
          @click="modalConfirm(); closeModal()"
          class="px-4 py-2 bg-blue-600 hover:bg-blue-700 rounded-lg">
          OK
        </button>
      </div>
    </div>
  </div>

  <!-- MAIN FORM -->
  <div class="p-8 bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900 text-white rounded-2xl shadow-xl">
    <h2 class="text-3xl font-bold mb-6 text-center tracking-wide">
      {{ isEditing ? "Update Product" : "Add New Product" }}
    </h2>

    <form @submit.prevent="saveProduct" class="space-y-10">
      <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
        <div class="space-y-5">
          <!-- Category Dropdown -->
          <div>
            <label class="block mb-1 text-gray-300 font-medium">Category</label>
            <select v-model="product.category"
              class="w-full p-3 rounded-lg bg-gray-700 border border-gray-600 focus:ring-2 focus:ring-blue-500 transition" required>
              <option value="" disabled>Select Category</option>
              <option v-for="cat in categories" :key="cat" :value="cat">{{ cat }}</option>
            </select>
          </div>

          <!-- Product Type Dropdown -->
          <div>
            <label class="block mb-1 text-gray-300 font-medium">Product Type</label>
            <select v-model="product.product_type"
              class="w-full p-3 rounded-lg bg-gray-700 border border-gray-600 focus:ring-2 focus:ring-blue-500 transition" required>
              <option value="" disabled>Select Type</option>
              <option v-for="type in typeOptions" :key="type" :value="type">{{ type }}</option>
            </select>
          </div>

          <!-- Product Name -->
          <div>
            <label class="block mb-1 text-gray-300 font-medium">Product Name</label>
            <input v-model="product.product_name" placeholder="Enter product name"
              class="w-full p-3 rounded-lg bg-gray-700 border border-gray-600 focus:ring-2 focus:ring-blue-500 transition" required />
          </div>

          <!-- Description -->
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
            <input ref="productImage" type="file" accept="image/*" class="hidden" @change="handleProductImage" />

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

        <div v-for="(benefit, index) in product.benefits" :key="'benefit-' + index"
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
          <div v-for="(item, index) in product.installation_gallery" :key="'gallery-' + index"
            class="min-w-[200px] border border-gray-700 bg-gray-700/70 p-3 rounded-xl flex flex-col items-center hover:scale-105 transition-transform duration-300 shadow-md">

            <div
              class="w-full h-48 flex items-center justify-center border border-gray-600 rounded-lg mb-2 cursor-pointer hover:bg-gray-800"
              @click="$refs['gallery' + index][0].click()">
              <span v-if="!item.image" class="text-sm text-gray-400">Upload</span>
              <img v-if="item.image" :src="item.image" class="object-cover h-48 w-full rounded-lg" />
            </div>

            <input type="file" accept="image/*" class="hidden" :ref="'gallery' + index" @change="e => handleGalleryImage(e, index)" />
            <input v-model="item.description" placeholder="Caption"
              class="p-2 rounded bg-gray-800 border border-gray-600 w-full text-sm focus:ring-1 focus:ring-blue-400 transition" />
            <button type="button" @click="removeGalleryItem(index)"
              class="text-red-400 hover:text-red-500 text-sm mt-1">Remove</button>
          </div>
        </div>
      </div>

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
