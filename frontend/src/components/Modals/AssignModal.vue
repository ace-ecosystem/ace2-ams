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
        :disabled="!selectedAlertStore.anySelected"
        @click="assignUser()"
      />
    </template>
  </BaseModal>
</template>

<script setup>
  import { defineProps, ref } from "vue";

  import Button from "primevue/button";
  import Dropdown from "primevue/dropdown";
  import Message from "primevue/message";
  import ProgressSpinner from "primevue/progressspinner";

  import BaseModal from "@/components/Modals/BaseModal";

  import { useAlertStore } from "@/stores/alert";
  import { useModalStore } from "@/stores/modal";
  import { useSelectedAlertStore } from "@/stores/selectedAlert";
  import { useUserStore } from "@/stores/user";

  const alertStore = useAlertStore();
  const modalStore = useModalStore();
  const selectedAlertStore = useSelectedAlertStore();
  const userStore = useUserStore();
  import { useAlertTableStore } from "@/stores/alertTable";
  const alertTableStore = useAlertTableStore();

  const error = ref(null);
  const isLoading = ref(false);
  const selectedUser = ref(null);

  const props = defineProps({
    name: { type: String, required: true },
  });

  const assignUser = async () => {
    isLoading.value = true;

    try {
      for (const uuid of selectedAlertStore.selected) {
        await alertStore.update(uuid, {
          owner: selectedUser.value.username,
        });
      }
    } catch (err) {
      error.value = err.message || "Something went wrong!";
    }
    isLoading.value = false;
    if (!error.value) {
      close();
      alertTableStore.requestReload = true;
    }
  };

  const handleError = () => {
    error.value = null;
    close();
  };

  const close = () => {
    selectedUser.value = null;
    modalStore.close(props.name);
  };
</script>
