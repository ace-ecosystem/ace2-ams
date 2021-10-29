<!-- SaveToEvent.vue -->
<!-- 'Save to Event' alert action modal, will close the Disposition Modal that opened it -->

<template>
  <BaseModal :name="name" header="Save to Event">
    <TabView class="p-m-1">
      <TabPanel
        v-for="eventType of existingEvents"
        :key="eventType.title"
        :header="eventType.title"
      >
        <div
          v-for="eventItem of eventType.events"
          :key="eventItem"
          class="p-field-radiobutton p-inputgroup"
        >
          <RadioButton
            :id="eventItem"
            v-model="selectedEvent"
            name="eventItem"
            :value="eventItem"
          />
          <label :for="eventItem">{{ eventItem }}</label>
        </div>
        <div class="p-field-radiobutton p-inputgroup">
          <RadioButton
            id="newEventItem"
            v-model="selectedEvent"
            name="newEventItem"
            value="New Event"
          />
          <label for="newEventItem">New Event</label>
        </div>
        <div v-if="newEventSelected" class="p-m-1 p-grid p-fluid p-formgrid">
          <div class="p-field p-col p-m-1">
            <InputText v-model="newEventName" name="newEventName" type="text" />
            <Textarea
              id="newEventComment"
              v-model="newEventComment"
              :auto-resize="true"
              rows="5"
              cols="30"
              placeholder="Add a comment..."
            />
            <Dropdown
              v-model="newEventComment"
              :options="suggestedComments"
              :show-clear="true"
              placeholder="Select from a past comment"
            />
          </div>
          <div class="p-col-1 p-m-1">
            <Button
              type="button"
              icon="pi pi-refresh"
              class="p-button-outlined p-m-1"
              @click="autoSetEventName"
            />
          </div>
        </div>
      </TabPanel>
    </TabView>
    <template #footer>
      <Button
        label="Back"
        icon="pi pi-arrow-left"
        class="p-button-text"
        @click="close"
      />
      <Button
        label="Save"
        icon="pi pi-check"
        :disabled="!anyEventSelected"
        @click="save"
      />
    </template>
  </BaseModal>
</template>

<script>
  import Button from "primevue/button";
  import Dropdown from "primevue/dropdown";
  import InputText from "primevue/inputtext";
  import RadioButton from "primevue/radiobutton";
  import TabPanel from "primevue/tabpanel";
  import TabView from "primevue/tabview";
  import Textarea from "primevue/textarea";

  import BaseModal from "@/components/Modals/BaseModal";

  export default {
    name: "SaveToEventModal",
    components: {
      BaseModal,
      Button,
      Dropdown,
      InputText,
      RadioButton,
      TabPanel,
      TabView,
      Textarea,
    },

    emits: ["save-to-event"],

    data() {
      return {
        selectedEvent: null,
        displaySaveToEventModal: false,

        existingEvents: [
          { title: "Open", events: ["event1", "event2"] },
          { title: "Closed", events: ["event3", "event4"] },
        ],

        newEventComment: null,
        newEventName: null,
        suggestedComments: ["this is an old comment", "and another"],
      };
    },

    computed: {
      anyEventSelected: function () {
        return Boolean(this.selectedEvent);
      },

      newEventSelected: function () {
        return this.selectedEvent === "New Event";
      },

      name() {
        return this.$options.name;
      },
    },

    created() {
      this.autoSetEventName();
    },

    methods: {
      autoSetEventName() {
        // Automagically set new event name using data from selected alerts
        this.newEventName = "this is a placeholder";
      },

      close() {
        this.selectedEvent = null;
        this.displaySaveToEventModal = false;
        this.existingEvents = [
          { title: "Open", events: ["event1", "event2"] },
          { title: "Closed", events: ["event3", "event4"] },
        ];
        this.newEventComment = null;
        this.newEventName = null;
        this.$store.dispatch("modals/close", this.name);
      },

      save() {
        this.close();
        this.$emit("save-to-event");
      },
    },
  };
</script>
