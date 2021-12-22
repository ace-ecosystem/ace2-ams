<!-- DispositionModal.vue -->
<!-- 'Disposition' alert action modal, contains trigger to open SaveToEvent modal -->

<template>
  <BaseModal :name="name" header="Set Disposition">
    <div class="p-m-1 p-grid p-fluid p-formgrid p-grid">
      <div class="p-field p-col">
        <Listbox
          v-model="newDisposition"
          :options="alertDispositionStore.allItems"
          option-label="value"
          list-style="max-height:250px"
          style="width: 20rem"
        />
      </div>
      <div class="p-field p-col">
        <Textarea
          v-model="dispositionComment"
          :auto-resize="true"
          rows="5"
          cols="30"
          placeholder="Add a comment..."
        />
      </div>
    </div>

    <template #footer>
      <Button label="Save" class="p-button-outlined" @click="setDisposition" />
      <Button
        v-if="showAddToEventButton"
        label="Save to Event"
        class="p-button-raised"
        disabled
        @click="open('SaveToEventModal')"
      />
    </template>
    <!--  SAVE TO EVENT  -->
    <template #child>
      <SaveToEventModal @save-to-event="close" />
    </template>
  </BaseModal>
</template>

<script setup>
  import { computed, defineProps, ref } from "vue";

  import Button from "primevue/button";
  import Listbox from "primevue/listbox";
  import Textarea from "primevue/textarea";

  import BaseModal from "@/components/Modals/BaseModal";
  import SaveToEventModal from "@/components/Modals/SaveToEventModal";

  import { NodeComment } from "@/services/api/nodeComment";

  import { useAlertDispositionStore } from "@/stores/alertDisposition";
  import { useAlertStore } from "@/stores/alert";
  import { useAlertTableStore } from "@/stores/alertTable";
  import { useAuthStore } from "@/stores/auth";
  import { useModalStore } from "@/stores/modal";
  import { useSelectedAlertStore } from "@/stores/selectedAlert";

  const alertDispositionStore = useAlertDispositionStore();
  const alertStore = useAlertStore();
  const alertTableStore = useAlertTableStore();
  const authStore = useAuthStore();
  const modalStore = useModalStore();
  const selectedAlertStore = useSelectedAlertStore();

  const props = defineProps({
    name: { type: String, required: true },
  });

  const newDisposition = ref(null);
  const dispositionComment = ref(null);
  const isLoading = ref(false);
  const error = ref(null);

  const setDisposition = async () => {
    isLoading.value = true;

    try {
      for (const uuid of selectedAlertStore.selected) {
        await alertStore.update(uuid, {
          disposition: newDisposition.value.value,
        });
        if (dispositionComment.value) {
          await NodeComment.create({ ...commentData.value, nodeUuid: uuid });
        }
      }
    } catch (err) {
      error.value = err.message;
    }

    isLoading.value = false;

    if (!error.value) {
      close();
      alertTableStore.requestReload = true;
    }
  };

  const showAddToEventButton = computed(() => {
    // Only show add to event button if selected disposition is an 'elevated' disposition
    if (newDisposition.value) {
      return newDisposition.value.rank > 1;
    }
    return false;
  });

  const commentData = computed(() => {
    return {
      user: authStore.user ? authStore.user.username : null,
      value: dispositionComment.value,
    };
  });

  const handleError = () => {
    error.value = null;
    close();
  };

  const close = () => {
    newDisposition.value = null;
    dispositionComment.value = null;
    modalStore.close(props.name);
  };

  const open = (name) => {
    modalStore.open(name);
  };
</script>
