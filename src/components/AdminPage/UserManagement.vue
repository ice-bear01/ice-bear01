<template>
  <!-- CONFIRMATION MODAL -->
  <div v-if="showModal"
    class="fixed inset-0 bg-black/60 backdrop-blur-sm flex items-center justify-center z-[9999] p-4">
    <div class="bg-gray-800 p-6 rounded-xl shadow-xl w-full max-w-md border border-gray-700">
      <h2 class="text-xl font-bold mb-3 text-white">{{ modalTitle }}</h2>
      <p class="text-gray-300 mb-6">{{ modalMessage }}</p>

      <div class="flex justify-end gap-3">
        <button @click="closeModal"
          class="px-4 py-2 bg-gray-600 hover:bg-gray-700 rounded-lg">
          Cancel
        </button>

        <button v-if="modalConfirm"
          @click="modalConfirm(); closeModal()"
          class="px-4 py-2 bg-blue-600 hover:bg-blue-700 rounded-lg">
          Confirm
        </button>
      </div>
    </div>
  </div>

  <!-- MAIN CONTENT -->
  <div class="p-8 bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900 text-white rounded-2xl shadow-xl">
    <h2 class="text-3xl font-bold mb-6 text-center tracking-wide">User Management</h2>

    <div class="overflow-x-auto">
      <table class="min-w-full divide-y divide-gray-700">
        <thead class="bg-gray-800/70">
          <tr>
            <th class="px-6 py-3 text-left text-sm font-semibold text-gray-300 uppercase tracking-wider">ID</th>
            <th class="px-6 py-3 text-left text-sm font-semibold text-gray-300 uppercase tracking-wider">Email</th>
            <th class="px-6 py-3 text-left text-sm font-semibold text-gray-300 uppercase tracking-wider">Created At</th>
            <th class="px-6 py-3 text-left text-sm font-semibold text-gray-300 uppercase tracking-wider">Status</th>
            <th class="px-6 py-3 text-left text-sm font-semibold text-gray-300 uppercase tracking-wider">Actions</th>
          </tr>
          <tr class="bg-gray-700/50">
            <th class="px-6 py-2">
              <input v-model="searchQuery" type="text" placeholder="Search ID"
                class="w-full px-3 py-1 rounded-lg bg-gray-800 border border-gray-600 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm" />
            </th>
            <th class="px-6 py-2">
              <input v-model="searchQuery" type="text" placeholder="Search Email"
                class="w-full px-3 py-1 rounded-lg bg-gray-800 border border-gray-600 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm" />
            </th>
            <th class="px-6 py-2"></th>
            <th class="px-6 py-2"></th>
            <th class="px-6 py-2"></th>
          </tr>
        </thead>

        <tbody class="divide-y divide-gray-700">
          <tr v-for="user in filteredUsers" :key="user.id" class="hover:bg-gray-700/40 transition">
            <td class="px-6 py-4 text-sm">{{ user.id }}</td>
            <td class="px-6 py-4 text-sm">{{ user.email }}</td>
            <td class="px-6 py-4 text-sm">{{ formatDate(user.created_at) }}</td>
            <td class="px-6 py-4 text-sm">
              <span
                :class="user.status === 'active'
                  ? 'bg-green-600 text-white rounded-xl font-semibold shadow-md flex items-center justify-center'
                  : 'bg-red-600 text-white rounded-xl font-semibold shadow-md flex items-center justify-center'"
                class="w-24 h-8 text-center">
                {{ user.status }}
              </span>
            </td>
            <td class="px-6 py-4 text-sm flex gap-3">
              <button
                @click="confirmToggleUser(user)"
                :class="user.status === 'active'
                  ? 'bg-red-600 hover:bg-red-700'
                  : 'bg-green-600 hover:bg-green-700'"
                class="w-24 h-8 rounded-xl font-semibold shadow-md transition transform hover:scale-105">
                {{ user.status === 'active' ? 'Ban' : 'Unban' }}
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from "vue";
import axios from "axios";

const backend = import.meta.env.VITE_BACKEND_URL;
const users = ref([]);
const searchQuery = ref("");

// MODAL
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

// Fetch all users
const fetchUsers = async () => {
  try {
    const { data } = await axios.get(`${backend}/admin/users/`);
    users.value = data.map(u => ({
      id: u.user_id,
      email: u.email,
      created_at: u.created_at,
      status: u.is_active ? "active" : "banned"
    }));
  } catch (err) {
    console.error("Error fetching users:", err);
  }
};

// Confirm before toggle
const confirmToggleUser = (user) => {
  const action = user.status === "active" ? "ban" : "unban";
  openModal(
    "Confirm Action",
    `Are you sure you want to ${action} user ${user.email}?`,
    () => toggleUserStatus(user)
  );
};

// Toggle user status
const toggleUserStatus = async (user) => {
  try {
    const newStatus = user.status === "active" ? false : true;
    await axios.put(`${backend}/admin/users/${user.id}/status`, null, {
      params: { is_active: newStatus }
    });
    user.status = newStatus ? "active" : "banned";
  } catch (err) {
    console.error("Error updating user status:", err);
  }
};

// Format date
const formatDate = (dateStr) => {
  const date = new Date(dateStr);
  return date.toLocaleDateString() + " " + date.toLocaleTimeString();
};

// Filtered users
const filteredUsers = computed(() => {
  if (!searchQuery.value) return users.value;
  return users.value.filter(user =>
    user.id.toString().includes(searchQuery.value) ||
    user.email.toLowerCase().includes(searchQuery.value.toLowerCase())
  );
});

onMounted(fetchUsers);
</script>
