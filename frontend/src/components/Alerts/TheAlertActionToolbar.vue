<!-- TheAlertActionToolbar.vue -->
<!-- Toolbar containing alert-specific actions, such as Disposition and Remediation -->

<template>
  <TheNodeActionToolbarVue ref="toolbar" :reload-object="props.reloadObject">
    <template #start>
      <!--      DISPOSITION -->
      <Button
        data-cy="disposition-button"
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
        data-cy="remediate-button"
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

  import TheNodeActionToolbarVue from "@/components/Node/TheNodeActionToolbar.vue";
  import RemediationModal from "@/components/Modals/RemediateModal.vue";
  import DispositionModal from "@/components/Modals/DispositionModal.vue";

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
