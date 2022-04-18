<!-- BaseModal.vue -->
<!-- Base Modal to use with 'modal' store module, handles opening and closing of a given modal -->
<!-- Credit to https://xon5.medium.com/a-vue-modal-manager-via-vuex-1ae530c8649 -->
<!-- Based off above 'Modal' component and changed to use PrimeVue's Dialog component -->

<template>
  <Dialog
    v-model:visible="isOpen"
    append-to="self"
    :header="header"
    :modal="true"
    :style="props.style"
    :draggable="false"
    @update:visible="close"
    :data-cy="name"
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
  export default {
    name: "BaseModal",
  };
</script>

<script setup>
  import { onBeforeUnmount, computed, defineEmits, defineProps } from "vue";
  import Dialog from "primevue/dialog";

  import { useModalStore } from "@/stores/modal";

  const store = useModalStore();

  const emit = defineEmits(["dialogClose"]);

  const props = defineProps({
    name: { type: String, required: true },
    header: { type: String, required: false },
    style: { type: Object, required: false },
  });

  const isOpen = computed(() => {
    return store.openModals.includes(props.name);
  });

  const close = () => {
    emit("dialogClose");
    store.close(props.name);
  };

  onBeforeUnmount(() => {
    if (isOpen.value) {
      close();
    }
  });
</script>
