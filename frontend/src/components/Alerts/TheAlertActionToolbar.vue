<!-- TheAlertActionToolbar.vue -->
<!-- Toolbar containing alert-specific actions, such as Disposition and Remediation -->

<template>
  <div>
    <TheNodeActionToolbarVue ref="toolbar" :reload-object="props.reloadObject">
      <template #start>
        <!-- FALSE POSITIVE -->
        <Button
          v-if="showFalsePositiveShortcut"
          data-cy="false-positive-button"
          class="p-m-1 p-button-normal p-button-success"
          icon="pi pi-thumbs-up"
          label="FP"
          @click="emit('falsePositiveClicked')"
        />
        <!-- IGNORE -->
        <Button
          v-if="showIgnoreShortcut"
          data-cy="ignore-button"
          class="p-m-1 p-button-sm"
          icon="pi pi-check"
          label="Ignore"
          @click="emit('ignoreClicked')"
        />
        <!-- DISPOSITION -->
        <Button
          data-cy="disposition-button"
          class="p-m-1 p-button-sm"
          icon="pi pi-thumbs-up"
          label="Disposition"
          @click="open('DispositionModal')"
        />
        <DispositionModal
          name="DispositionModal"
          @request-reload="requestReload"
        />
        <!-- REMEDIATE MODAL -->
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
  </div>
</template>

<script setup lang="ts">
  import { ref, defineEmits, defineProps, PropType } from "vue";

  import Button from "primevue/button";

  import TheNodeActionToolbarVue from "@/components/Node/TheNodeActionToolbar.vue";
  import RemediationModal from "@/components/Modals/RemediateModal.vue";
  import DispositionModal from "@/components/Modals/DispositionModal.vue";

  import { useModalStore } from "@/stores/modal";

  const emit = defineEmits(["falsePositiveClicked", "ignoreClicked"]);

  const props = defineProps({
    reloadObject: {
      type: String as PropType<"table" | "node">,
      required: true,
    },
    showFalsePositiveShortcut: {
      type: Boolean,
      required: false,
      default: false,
    },
    showIgnoreShortcut: { type: Boolean, required: false, default: false },
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
