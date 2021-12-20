<!-- TagModal.vue -->
<!-- 'Tag' action modal, agnostic to what is being tagged -->

<template>
  <BaseModal :name="name" header="Add Tags">
    <span class="p-fluid">
      <Chips v-model="newTags" />
      <Dropdown
        :options="tags"
        option-label="label"
        :filter="true"
        placeholder="Select from existing tags"
        filter-placeholder="Search tags"
        @change="addExistingTag"
      />
    </span>
    <template #footer>
      <Button
        label="Nevermind"
        icon="pi pi-times"
        class="p-button-text"
        @click="close"
      />
      <Button label="Add" icon="pi pi-check" @click="close" />
    </template>
  </BaseModal>
</template>

<script>
  import Button from "primevue/button";
  import Chips from "primevue/chips";
  import Dropdown from "primevue/dropdown";

  import BaseModal from "@/components/Modals/BaseModal";

  export default {
    name: "TagModal",
    components: { BaseModal, Button, Chips, Dropdown },

    data() {
      return {
        newTags: [],

        tags: [
          { label: "oh_no", id: 1 },
          { label: "bad", id: 2 },
          { label: "malware", id: 3 },
        ],
      };
    },

    computed: {
      name() {
        return this.$options.name;
      },
    },

    methods: {
      addExistingTag(event) {
        // Add an existing tag to the list of tags to be added
        this.newTags.push(event.value.label);
      },

      close() {
        this.newTags = [];
        this.$store.dispatch("modals/close", this.name);
      },
    },
  };
</script>
