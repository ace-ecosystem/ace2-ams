<!-- AlertActionToolbar.vue -->
<!-- Toolbar containing all alert-related actions, such as Disposition, Assign, Comment, etc. -->

<template>
  <TheNodeActionToolbarVue ref="toolbar" :reload-object="props.reloadObject">
    <template #start>
      <!--      DISPOSITION -->
      <Button
        class="p-m-1 p-button-normal p-button-success"
        icon="pi pi-thumbs-up"
        label="Disposition"
        @click="open('DispositionModal')"
      />
      <DispositionModal
        name="DispositionModal"
        @requestReload="requestReload"
      />
      <!--      REMEDIATE MODAL -->
      <Button
        class="p-m-1 p-button-sm"
        icon="pi pi-times-circle"
        label="Remediate"
        disabled
        @click="open('RemediationModal')"
      />
      <RemediationModal />
    </template>
  </TheNodeActionToolbarVue>
</template>

<script setup>
  import { ref, defineProps } from "vue";

  import Button from "primevue/button";

  import TheNodeActionToolbarVue from "../Node/TheNodeActionToolbar.vue";
  import RemediationModal from "@/components/Modals/RemediateModal";
  import DispositionModal from "@/components/Modals/DispositionModal";

  import { useModalStore } from "@/stores/modal";

  const props = defineProps({
    reloadObject: { type: String, required: true },
  });

  const modalStore = useModalStore();
  const open = (name) => {
    modalStore.open(name);
  };

  const toolbar = ref(null);
  const requestReload = () => {
    toolbar.value.requestReload();
  };
</script>
