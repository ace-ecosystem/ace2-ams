<!-- DispositionModal.vue -->
<!-- 'Disposition' alert action modal, contains trigger to open SaveToEvent modal -->

<template>
  <BaseModal :name="name" header="Set Disposition" :style="{ width: '75vw' }">
    <div>
      <div v-if="error" class="p-col">
        <Message severity="error" @close="handleError">{{ error }}</Message>
      </div>
    </div>
    <div class="p-m-1 p-grid p-fluid p-formgrid p-grid">
      <div class="p-field p-col">
        <Listbox
          v-model="newDisposition"
          :options="alertDispositionStore.allItems"
          option-label="value"
          list-style="max-height:250px"
          style="width: 70vw"
        >
          <template #option="slotProps">
            <AlertDispositionTag
              :disposition="slotProps.option.value"
            ></AlertDispositionTag>
          </template>
        </Listbox>
      </div>
      <div class="p-field p-col">
        <Textarea
          v-model="dispositionComment"
          :auto-resize="true"
          rows="5"
          cols="30"
          placeholder="Add a comment..."
        />
        <NodeCommentAutocomplete
          @comment-clicked="recentCommentClicked($event)"
        ></NodeCommentAutocomplete>
      </div>
    </div>

    <template #footer>
      <Button
        label="Save"
        class="p-button-outlined"
        :disabled="!allowSubmit"
        @click="setDisposition"
      />
      <Button
        v-if="showAddToEventButton"
        label="Save to Event"
        class="p-button-raised"
        :disabled="!allowSubmit"
        @click="open('SaveToEventModal')"
      />
    </template>
  </BaseModal>
  <!--  SAVE TO EVENT  -->
  <SaveToEventModal name="SaveToEventModal" @save-to-event="setDisposition" />
</template>

<script setup lang="ts">
  import { computed, defineEmits, defineProps, ref } from "vue";

  import Button from "primevue/button";
  import Message from "primevue/message";
  import Listbox from "primevue/listbox";
  import Textarea from "primevue/textarea";

  import BaseModal from "@/components/Modals/BaseModal.vue";
  import SaveToEventModal from "@/components/Modals/SaveToEventModal.vue";
  import AlertDispositionTag from "@/components/Alerts/AlertDispositionTag.vue";

  import { NodeComment } from "@/services/api/nodeComment";
  import NodeCommentAutocomplete from "@/components/Node/NodeCommentAutocomplete.vue";

  import { useAlertDispositionStore } from "@/stores/alertDisposition";
  import { useAlertStore } from "@/stores/alert";
  import { useAuthStore } from "@/stores/auth";
  import { useModalStore } from "@/stores/modal";
  import { useSelectedAlertStore } from "@/stores/selectedAlert";
  import { useRecentCommentsStore } from "@/stores/recentComments";

  import { alertDispositionRead } from "@/models/alertDisposition";
  import { nodeCommentCreate } from "@/models/nodeComment";

  const alertDispositionStore = useAlertDispositionStore();
  const alertStore = useAlertStore();
  const authStore = useAuthStore();
  const modalStore = useModalStore();
  const selectedAlertStore = useSelectedAlertStore();
  const recentCommentsStore = useRecentCommentsStore();

  const emit = defineEmits(["requestReload"]);

  const props = defineProps({
    name: { type: String, required: true },
  });

  const newDisposition = ref<alertDispositionRead>();
  const dispositionComment = ref<string>();
  const isLoading = ref(false);
  const error = ref<string>();

  const setDisposition = async () => {
    isLoading.value = true;

    try {
      const updateData = selectedAlertStore.selected.map((uuid) => ({
        uuid: uuid,
        disposition: newDisposition.value?.value,
        historyUsername: authStore.user.username,
      }));
      await alertStore.update(updateData);

      if (dispositionComment.value) {
        const commentCreateData: nodeCommentCreate[] =
          selectedAlertStore.selected.map((uuid) => ({
            username: authStore.user.username,
            nodeUuid: uuid,
            value: dispositionComment.value!,
          }));
        if (commentCreateData) {
          await NodeComment.create(commentCreateData);
        }
      }
    } catch (e: unknown) {
      if (typeof e === "string") {
        if (e.includes("409")) {
          console.warn("That comment already exists!");
        } else {
          error.value = e;
        }
      } else if (e instanceof Error) {
        if (e.message.includes("409")) {
          console.warn("That comment already exists!");
        } else {
          error.value = e.message;
        }
      }
    }

    isLoading.value = false;

    if (!error.value) {
      if (dispositionComment.value) {
        recentCommentsStore.addComment(dispositionComment.value);
      }
      close();
      emit("requestReload");
    }
  };

  const showAddToEventButton = computed(() => {
    // Only show add to event button if selected disposition is an 'elevated' disposition
    if (newDisposition.value) {
      return newDisposition.value.rank > 1;
    }
    return false;
  });

  const recentCommentClicked = (comment: string) => {
    dispositionComment.value = comment;
  };

  const handleError = () => {
    error.value = undefined;
    close();
  };

  const allowSubmit = computed(() => {
    return selectedAlertStore.anySelected && newDisposition.value;
  });

  const close = () => {
    newDisposition.value = undefined;
    dispositionComment.value = undefined;
    modalStore.close(props.name);
  };

  const open = (name: string) => {
    modalStore.open(name);
  };
</script>
