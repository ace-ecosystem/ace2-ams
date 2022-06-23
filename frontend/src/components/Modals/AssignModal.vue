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

<script setup lang="ts">
  import { computed, defineProps, ref, defineEmits, inject } from "vue";

  import Button from "primevue/button";
  import Dropdown from "primevue/dropdown";
  import Message from "primevue/message";
  import ProgressSpinner from "primevue/progressspinner";

  import BaseModal from "@/components/Modals/BaseModal.vue";

  import { useAuthStore } from "@/stores/auth";
  import { nodeSelectedStores, nodeStores } from "@/stores/index";
  import { useModalStore } from "@/stores/modal";
  import { useUserStore } from "@/stores/user";

  const props = defineProps({
    name: { type: String, required: true },
  });

  const emit = defineEmits(["requestReload"]);

  const objectType = inject("objectType") as "events" | "alerts";

  const authStore = useAuthStore();
  const selectedStore = nodeSelectedStores[objectType]();
  const nodeStore = nodeStores[objectType]();
  const modalStore = useModalStore();
  const userStore = useUserStore();

  const error = ref<string>();
  const isLoading = ref(false);
  const selectedUser = ref();

  const assignUser = async () => {
    isLoading.value = true;

    try {
      const updateData = selectedStore.selected.map((uuid) => ({
        uuid: uuid,
        owner: selectedUser.value.username,
        historyUsername: authStore.user.username,
      }));

      await nodeStore.update(updateData);
    } catch (e: unknown) {
      if (typeof e === "string") {
        error.value = e;
      } else if (e instanceof Error) {
        error.value = e.message;
      }
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
    error.value = undefined;
    close();
  };

  const close = () => {
    selectedUser.value = null;
    modalStore.close(props.name);
  };
</script>
