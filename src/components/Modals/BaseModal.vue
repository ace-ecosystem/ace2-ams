<!-- BaseModal.vue -->
<!-- Base Modal to use with 'modal' store module, handles opening and closing of a given modal -->
<!-- Credit to https://xon5.medium.com/a-vue-modal-manager-via-vuex-1ae530c8649 -->
<!-- Based off above 'Modal' component and changed to use PrimeVue's Dialog component -->

<template>
  <Dialog
    append-to="self"
    v-model:visible="isOpen"
    :header="header"
    :modal="true"
    @update:visible="close"
  >
    <template #header>
      <slot name="header"></slot>
    </template>
    <slot></slot>
    <template #footer>
      <slot name="footer"></slot>
    </template>
    <slot name="child"></slot>
  </Dialog>
</template>

<script>
  import Dialog from "primevue/dialog";

  export default {
    name: "BaseModal",
    components: { Dialog },

    props: {
      name: { type: String, required: true },
      header: { type: String, required: false },
    },

    computed: {
      isActive() {
        return this.$store.getters["modals/active"] === this.name;
      },

      isOpen() {
        return this.$store.getters["modals/allOpen"].includes(this.name);
      },
    },

    beforeUnmount() {
      if (this.isOpen) this.close();
    },

    methods: {
      close() {
        this.$store.dispatch("modals/close", this.name);
      },
    },
  };
</script>
