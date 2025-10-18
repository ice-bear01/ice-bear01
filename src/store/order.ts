import { defineStore } from 'pinia';

interface ProductDetails {
  product_id: number;
  product_name: string;
  product_image?: string;
  category: string;
  product_type: string;
  product_price: number;
  product_stock: number;
  product_description?: string;
}

export const useOrderStore = defineStore('order', {
  state: () => ({
    selectedProduct: null as ProductDetails | null,
    showModal: false,
  }),

  actions: {
    openModal(product: ProductDetails) {
      this.selectedProduct = product;
      this.showModal = true;
    },
    closeModal() {
      this.selectedProduct = null;
      this.showModal = false;
    },
  },
});
