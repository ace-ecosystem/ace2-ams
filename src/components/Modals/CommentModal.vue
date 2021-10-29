<!-- CommentModal.vue -->
<!-- 'Comment' action modal, agnostic to what is being commented on -->

<template>
  <BaseModal :name="this.name" header="Add Comment">
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

<script>
  import Button from "primevue/button";
  import Dropdown from "primevue/dropdown";
  import Textarea from "primevue/textarea";

  import BaseModal from "@/components/Modals/BaseModal";

  export default {
    name: "CommentModal",
    components: { BaseModal, Button, Dropdown, Textarea },

    computed: {
      name() {
        return this.$options.name;
      },
    },

    data() {
      return {
        newComment: null,
        suggestedComments: ["this is an old comment", "and another"],
      };
    },

    methods: {
      close() {
        this.newComment = null;
        this.$store.dispatch("modals/close", this.name);
      },
    },
  };
</script>
