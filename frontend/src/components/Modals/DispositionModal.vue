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
        <Dropdown
          v-model="dispositionComment"
          :options="suggestedComments"
          :show-clear="true"
          placeholder="Select from a past comment"
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
  import Dropdown from "primevue/dropdown";
  import Listbox from "primevue/listbox";
  import Textarea from "primevue/textarea";

  import BaseModal from "@/components/Modals/BaseModal";
  import SaveToEventModal from "@/components/Modals/SaveToEventModal";

  import { NodeComment } from "@/services/api/nodeComment";

  import { useModalStore } from "@/stores/modal";
  import { useAlertDispositionStore } from "@/stores/alertDisposition";

  const alertDispositionStore = useAlertDispositionStore();
  const modalStore = useModalStore();
  import { useAuthStore } from "@/stores/auth";
  const authStore = useAuthStore();

  import { useAlertStore } from "@/stores/alert";
  import { useSelectedAlertStore } from "@/stores/selectedAlert";

  const alertStore = useAlertStore();
  const selectedAlertStore = useSelectedAlertStore();

  import { useAlertTableStore } from "@/stores/alertTable";
  const alertTableStore = useAlertTableStore();

  const props = defineProps({
    name: { type: String, required: true },
  });

  const error = ref(null);

  const isLoading = ref(false);
  const newDisposition = ref(null);
  const dispositionComment = ref(null);
  const suggestedComments = ref(["this is an old comment", "and another"]);

  const showAddToEventButton = computed(() => {
    // Only show add to event button if selected disposition is an 'elevated' disposition
    if (newDisposition.value) {
      return newDisposition.value.rank > 1;
    }
    return false;
  });

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
      error.value = err.message || "Something went wrong!";
    }

    isLoading.value = false;

    if (!error.value) {
      close();
      alertTableStore.requestReload = true;
    }
  };

  const commentData = computed(() => {
    return {
      user: authStore.user.username,
      value: dispositionComment.value,
    };
  });

  const close = () => {
    modalStore.close(props.name);
  };

  const open = (name) => {
    modalStore.open(name);
  };
</script>
