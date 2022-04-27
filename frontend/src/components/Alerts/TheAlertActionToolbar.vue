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
        @request-reload="requestReload"
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

<script setup lang="ts">
  import { ref, defineProps, PropType } from "vue";

  import Button from "primevue/button";

  import TheNodeActionToolbarVue from "@/components/Node/TheNodeActionToolbar.vue";
  import RemediationModal from "@/components/Modals/RemediateModal.vue";
  import DispositionModal from "@/components/Modals/DispositionModal.vue";

  import { useModalStore } from "@/stores/modal";

  const props = defineProps({
    reloadObject: {
      type: String as PropType<"table" | "node">,
      required: true,
    },
  });

  const modalStore = useModalStore();
  const open = (name: string) => {
    modalStore.open(name);
  };

  const toolbar = ref<InstanceType<typeof TheNodeActionToolbarVue>>();
  const requestReload = () => {
    toolbar.value?.requestReload();
  };
</script>
