<!-- CommentModal.vue -->
<!-- 'Comment' action modal, agnostic to what is being commented on -->

<template>
  <BaseModal :name="name" header="Add Comment">
    <div class="p-m-1 p-grid p-fluid p-formgrid p-grid">
      <div class="p-field p-col">
        <Textarea
          v-model="newComment"
          :autoResize="true"
          rows="5"
          cols="30"
          placeholder="Add a comment..."
        />
        <Dropdown
          v-model="newComment"
          :options="suggestedComments"
          :showClear="true"
          placeholder="Select from a past comment"
        />
      </div>
    </div>
    <template #footer>
      <Button
        label="Nevermind"
        icon="pi pi-times"
        @click="close"
        class="p-button-text"
      />
      <Button label="Add" icon="pi pi-check" @click="close" />
    </template>
  </BaseModal>
</template>

<script setup>
  import { defineProps, ref } from "vue";

  import Button from "primevue/button";
  import Dropdown from "primevue/dropdown";
  import Textarea from "primevue/textarea";

  import BaseModal from "@/components/Modals/BaseModal";

  import { useModalStore } from "@/stores/modal";

  const modalStore = useModalStore();

  const newComment = ref(null);
  const suggestedComments = ref(["this is an old comment", "and another"]);

  const props = defineProps({
    name: { type: String, required: true },
  });

  const close = () => {
    newComment.value = null;
    modalStore.close(props.name);
  };
</script>
