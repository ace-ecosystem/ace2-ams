<!-- AlertActionToolbar.vue -->
<!-- Toolbar containing all alert-related actions, such as Disposition, Assign, Comment, etc. -->

<template>
  <TheNodeActionToolbarVue :reload-object="props.reloadObject">
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
  import { defineProps } from "vue";

  import Button from "primevue/button";

  import TheNodeActionToolbarVue from "../Node/TheNodeActionToolbar.vue";
  import RemediationModal from "@/components/Modals/RemediateModal";
  import DispositionModal from "@/components/Modals/DispositionModal";

  import { useAlertStore } from "@/stores/alert";
  import { useAlertTableStore } from "@/stores/alertTable";
  import { useModalStore } from "@/stores/modal";

  const alertStore = useAlertStore();
  const alertTableStore = useAlertTableStore();
  const modalStore = useModalStore();

  const props = defineProps({
    reloadObject: { type: String, required: true },
  });
  const open = (name) => {
    modalStore.open(name);
  };

  function requestReload() {
    if (props.reloadObject == "table") {
      alertTableStore.requestReload = true;
    } else if (props.reloadObject == "node") {
      alertStore.requestReload = true;
    }
  }
</script>
