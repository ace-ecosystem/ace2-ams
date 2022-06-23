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
      <NodeCommentAutocomplete
        @comment-clicked="recentCommentClicked($event)"
      ></NodeCommentAutocomplete>
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

<script setup lang="ts">
  import { computed, defineEmits, defineProps, ref, inject } from "vue";

  import Button from "primevue/button";
  import Message from "primevue/message";
  import Textarea from "primevue/textarea";

  import BaseModal from "@/components/Modals/BaseModal.vue";
  import NodeCommentAutocomplete from "@/components/Node/NodeCommentAutocomplete.vue";

  import { NodeComment } from "@/services/api/nodeComment";

  import { useAuthStore } from "@/stores/auth";
  import { nodeSelectedStores } from "@/stores/index";
  import { useModalStore } from "@/stores/modal";
  import { useRecentCommentsStore } from "@/stores/recentComments";

  const emit = defineEmits(["requestReload"]);

  const props = defineProps({
    name: { type: String, required: true },
  });

  const objectType = inject("objectType") as "alerts" | "events";
  const authStore = useAuthStore();
  const selectedStore = nodeSelectedStores[objectType]();
  const modalStore = useModalStore();
  const recentCommentsStore = useRecentCommentsStore();

  const error = ref<string>();
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
    } catch (e: unknown) {
      if (typeof e === "string") {
        error.value = e;
      } else if (e instanceof Error) {
        error.value = e.message;
      }
    }

    isLoading.value = false;
    if (!error.value) {
      recentCommentsStore.addComment(newComment.value);
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

  const recentCommentClicked = (comment: string) => {
    newComment.value = comment;
  };

  const handleError = () => {
    error.value = undefined;
    close();
  };

  const close = () => {
    newComment.value = "";
    modalStore.close(props.name);
  };
</script>
