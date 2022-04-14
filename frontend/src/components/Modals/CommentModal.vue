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
      </div>
    </div>
    <template #footer>
      <Button
        label="Nevermind"
        icon="pi pi-times"
        class="p-button-text"
        @click="close"
      />
      <Button
        label="Add"
        icon="pi pi-check"
        :disabled="!allowSubmit"
        @click="addComment"
      />
    </template>
  </BaseModal>
</template>

<script setup>
  import { computed, defineEmits, defineProps, ref, inject } from "vue";

  import Button from "primevue/button";
  import Message from "primevue/message";
  import Textarea from "primevue/textarea";

  import BaseModal from "@/components/Modals/BaseModal.vue";

  import { NodeComment } from "@/services/api/nodeComment";

  import { useAuthStore } from "@/stores/auth";
  import { nodeSelectedStores } from "@/stores/index";
  import { useModalStore } from "@/stores/modal";

  const emit = defineEmits(["requestReload"]);

  const props = defineProps({
    name: { type: String, required: true },
  });

  const nodeType = inject("nodeType");
  const authStore = useAuthStore();
  const selectedStore = nodeSelectedStores[nodeType]();
  const modalStore = useModalStore();

  const error = ref(null);
  const isLoading = ref(false);
  const newComment = ref("");

  async function addComment() {
    isLoading.value = true;
    try {
      await NodeComment.create(
        selectedStore.selected.map((uuid) => ({
          username: authStore.user.username,
          nodeUuid: uuid,
          ...commentData.value,
        })),
      );
    } catch (err) {
      error.value = err.message;
    }

    isLoading.value = false;
    if (!error.value) {
      close();
      emit("requestReload");
    }
  }

  const commentData = computed(() => {
    return {
      value: newComment.value,
    };
  });

  const allowSubmit = computed(() => {
    return selectedStore.anySelected && newComment.value.length;
  });

  const handleError = () => {
    error.value = null;
    close();
  };

  const close = () => {
    newComment.value = "";
    modalStore.close(props.name);
  };
</script>
