<!-- DispositionModal.vue -->
<!-- 'Disposition' alert action modal, contains trigger to open SaveToEvent modal -->

<template>
  <BaseModal :name="name" header="Set Disposition">
    <div class="p-m-1 p-grid p-fluid p-formgrid p-grid">
      <div class="p-field p-col">
        <div
          v-for="disposition of dispositions"
          :key="disposition"
          class="p-field-radiobutton p-inputgroup"
        >
          <RadioButton
            :id="disposition"
            v-model="newDisposition"
            name="disposition"
            :value="disposition"
          />
          <label :for="disposition">{{ disposition }}</label>
        </div>
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
      <Button label="Save" class="p-button-outlined" @click="close" />
      <Button
        v-if="showAddToEventButton"
        label="Save to Event"
        class="p-button-raised"
        @click="open('SaveToEventModal')"
      />
    </template>
    <!--  SAVE TO EVENT  -->
    <template #child>
      <SaveToEventModal @save-to-event="close" />
    </template>
  </BaseModal>
</template>

<script>
  import Button from "primevue/button";
  import Dropdown from "primevue/dropdown";
  import RadioButton from "primevue/radiobutton";
  import Textarea from "primevue/textarea";

  import BaseModal from "@/components/Modals/BaseModal";
  import SaveToEventModal from "@/components/Modals/SaveToEventModal";

  export default {
    name: "DispositionModal",
    components: {
      BaseModal,
      Button,
      Dropdown,
      RadioButton,
      SaveToEventModal,
      Textarea,
    },

    data() {
      return {
        newDisposition: null,
        dispositions: [
          "FALSE_POSITIVE",
          "WEAPONIZATION",
          "COMMAND_AND_CONTROL",
        ],
        dispositionComment: null,
        elevated_dispositions: ["COMMAND_AND_CONTROL"],
        suggestedComments: ["this is an old comment", "and another"],
      };
    },

    computed: {
      name() {
        return this.$options.name;
      },

      showAddToEventButton: function () {
        // Only show add to event button if selected disposition is an 'elevated' disposition
        return this.elevated_dispositions.includes(this.newDisposition);
      },
    },

    methods: {
      close() {
        this.newDisposition = null;
        this.dispositionComment = null;
        this.$store.dispatch("modals/close", this.name);
      },

      open(name) {
        this.$store.dispatch("modals/open", name);
      },
    },
  };
</script>
