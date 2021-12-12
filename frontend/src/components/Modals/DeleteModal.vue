<!-- DeleteModal.vue -->
<!-- 'Delete' action modal, agnostic to what type of data is being deleted -->

<template>
  <BaseModal :name="name" header="Delete">
    <div class="confirmation-content">
      <i class="pi pi-exclamation-triangle p-mr-3" style="font-size: 2rem" />
      <span>Are you sure you want to delete this?</span>
    </div>
    <template #footer>
      <Button
        label="Actually, no"
        icon="pi pi-times"
        @click="close"
        class="p-button-text"
      />
      <Button label="Do it!" icon="pi pi-check" @click="close" />
    </template>
  </BaseModal>
</template>

<script setup>
  import { defineProps } from "vue";

  import Button from "primevue/button";

  import BaseModal from "@/components/Modals/BaseModal";

  import { useModalStore } from "@/stores/modal";

  const modalStore = useModalStore();

  const props = defineProps({
    name: { type: String, required: true },
  });

  const close = () => {
    modalStore.close(props.name);
  };
</script>
