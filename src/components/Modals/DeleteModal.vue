<!-- DeleteModal.vue -->
<!-- 'Delete' action modal, agnostic to what type of data is being deleted -->

<template>
  <BaseModal :name="this.name" header="Delete">
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

<script>
  import Button from "primevue/button";

  import BaseModal from "@/components/Modals/BaseModal";

  export default {
    name: "DeleteModal",
    components: { BaseModal, Button },

    computed: {
      name() {
        return this.$options.name;
      },
    },

    methods: {
      close() {
        this.$store.dispatch("modals/close", this.name);
      },
    },
  };
</script>
