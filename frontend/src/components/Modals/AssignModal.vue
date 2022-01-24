<!-- AssignModal.vue -->
<!-- 'Assign' alert action modal -->

<template>
  <BaseModal :name="name" header="Assign Ownership">
    <div>
      <div v-if="error" class="p-col">
        <Message severity="error" @close="handleError">{{ error }}</Message>
      </div>
    </div>
    <div class="p-m-1 p-grid p-fluid p-formgrid p-grid">
      <div v-if="!isLoading" class="p-field p-col">
        <Dropdown
          v-model="selectedUser"
          :options="userStore.allItems"
          option-label="displayName"
          placeholder="Select a user"
        />
      </div>
      <div v-if="isLoading" class="p-col p-offset-3">
        <ProgressSpinner />
      </div>
    </div>
    <template #footer>
      <Button
        label="Nevermind"
        icon="pi pi-times"
        class="p-button-text"
        @click="close"
      />
      <Button
        label="Assign"
        icon="pi pi-check"
        :disabled="!allowSubmit"
        @click="assignUser()"
      />
    </template>
  </BaseModal>
</template>

<script setup>
  import { computed, defineProps, ref, defineEmits, inject } from "vue";

  import Button from "primevue/button";
  import Dropdown from "primevue/dropdown";
  import Message from "primevue/message";
  import ProgressSpinner from "primevue/progressspinner";

  import BaseModal from "@/components/Modals/BaseModal";

  import { nodeSelectedStores, nodeStores } from "@/stores/index";
  import { useModalStore } from "@/stores/modal";
  import { useUserStore } from "@/stores/user";

  const props = defineProps({
    name: { type: String, required: true },
  });

  const emit = defineEmits(["requestReload"]);

  const nodeType = inject("nodeType");

  const selectedStore = nodeSelectedStores[nodeType]();
  const nodeStore = nodeStores[nodeType]();
  const modalStore = useModalStore();
  const userStore = useUserStore();

  const error = ref(null);
  const isLoading = ref(false);
  const selectedUser = ref(null);

  const assignUser = async () => {
    isLoading.value = true;

    try {
      const updateData = selectedStore.selected.map((uuid) => ({
        uuid: uuid,
        owner: selectedUser.value.username,
      }));

      await nodeStore.update(updateData);
    } catch (err) {
      error.value = err.message;
    }
    isLoading.value = false;
    if (!error.value) {
      close();
      emit("requestReload");
    }
  };

  const allowSubmit = computed(() => {
    return selectedStore.anySelected && selectedUser.value;
  });

  const handleError = () => {
    error.value = null;
    close();
  };

  const close = () => {
    selectedUser.value = null;
    modalStore.close(props.name);
  };
</script>
