<!-- CommentModal.vue -->
<!-- 'Comment' action modal, agnostic to what is being commented on -->

<template>
  <BaseModal :name="name" header="Add Comment">
    <div>
      <div v-if="error" class="p-col">
        <Message severity="error" @close="handleError">{{ error }}</Message>
      </div>
    </div>
    <div class="p-m-1 p-grid p-fluid p-formgrid p-grid">
      <div class="p-field p-col">
        <Textarea
          v-model="newComment"
          :auto-resize="true"
          rows="5"
          cols="30"
          placeholder="Add a comment..."
        />
        <Dropdown
          v-model="newComment"
          :options="suggestedComments"
          :show-clear="true"
          placeholder="Select from a past comment"
        />
      </div>
    </div>
    <template #footer>
      <Button
        label="Nevermind"
        icon="pi pi-times"
        class="p-button-text"
        @click="close"
      />
      <Button label="Add" icon="pi pi-check" @click="addComment" />
    </template>
  </BaseModal>
</template>

<script setup>
  import { computed, defineProps, ref } from "vue";

  import Button from "primevue/button";
  import Dropdown from "primevue/dropdown";
  import Message from "primevue/message";

  import Textarea from "primevue/textarea";

  import BaseModal from "@/components/Modals/BaseModal";

  import { NodeComment } from "@/services/api/nodeComment";
  import { useModalStore } from "@/stores/modal";
  import { useSelectedAlertStore } from "@/stores/selectedAlert";

  const modalStore = useModalStore();
  const selectedAlertStore = useSelectedAlertStore();

  const error = ref(null);
  const isLoading = ref(false);
  const newComment = ref(null);
  const suggestedComments = ref(["this is an old comment", "and another"]);

  const props = defineProps({
    name: { type: String, required: true },
  });

  async function addComment() {
    isLoading.value = true;
    try {
      for (const uuid of selectedAlertStore.selected) {
        NodeComment.create({ ...commentData.value, nodeUuid: uuid });
      }
    } catch (err) {
      error.value = err.message || "Something went wrong!";
    }

    isLoading.value = false;
    if (!error.value) {
      close();
    }
  }

  const commentData = computed(() => {
    return {
      user: "analyst",
      value: newComment.value,
    };
  });

  const handleError = () => {
    error.value = null;
    close();
  };

  const close = () => {
    newComment.value = null;
    modalStore.close(props.name);
  };
</script>
