<!-- AssignModal.vue -->
<!-- 'Assign' alert action modal -->

<template>
  <BaseModal :name="name" header="Assign Ownership">
    <div>
      <div v-if="error" class="p-col">
        <Message severity="error" @close="handleError">{{ error }}</Message>
      </div>
    </div>
    <div class="p-m-1 p-grid p-fluid p-formgrid p-grid">
      <div v-if="!isLoading" class="p-field p-col">
        <Dropdown
          v-model="selectedUser"
          :options="users"
          option-label="displayName"
          placeholder="Select a user"
        />
      </div>
      <div v-if="isLoading" class="p-col p-offset-3">
        <ProgressSpinner />
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
        label="Assign"
        icon="pi pi-check"
        :disabled="!anyAlertsSelected"
        @click="assignUserClicked()"
      />
    </template>
  </BaseModal>
</template>

<script>
  import { mapState, mapGetters, mapActions } from "vuex";

  import Button from "primevue/button";
  import Dropdown from "primevue/dropdown";
  import Message from "primevue/message";
  import ProgressSpinner from "primevue/progressspinner";

  import BaseModal from "@/components/Modals/BaseModal";

  export default {
    name: "AssignModal",
    components: { BaseModal, Button, Dropdown, Message, ProgressSpinner },

    computed: {
      name() {
        return this.$options.name;
      },
      isOpen() {
        return this.$store.getters["modals/allOpen"].includes(this.name);
      },
      ...mapState({
        selectedAlerts: (state) => state.selectedAlerts.selected,
      }),
      ...mapGetters({
        users: "users/allItems",
        anyAlertsSelected: "selectedAlerts/anySelected",
        multipleAlertsSelected: "selectedAlerts/multipleSelected",
      }),
    },

    data() {
      return {
        error: null,
        isLoading: false,
        selectedUser: null,
      };
    },

    watch: {
      isOpen: function (oldValue, newValue) {
        if (newValue === false) {
          this.loadUsers();
        }
      },
    },

    created() {
      this.loadUsers();
    },

    methods: {
      ...mapActions({
        updateAlert: "alerts/updateAlert",
        updateAlerts: "alerts/updateAlerts",
      }),
      async loadUsers() {
        this.isLoading = true;
        try {
          await this.$store.dispatch("users/getAll");
        } catch (error) {
          this.error = error.message || "Something went wrong!";
        }
        this.isLoading = false;
      },
      assignUserClicked() {
        this.isLoading = true;
        if (this.multipleAlertsSelected) {
          this.assignUserToMultiple();
        } else {
          this.assignUser();
        }
        this.isLoading = false;
      },
      async assignUser() {
        try {
          await this.updateAlert({
            oldAlertUUID: this.selectedAlerts[0],
            update: { owner: this.selectedUser },
          });
          this.close();
        } catch (error) {
          this.error = error.message || "Something went wrong!";
        }
      },
      async assignUserToMultiple() {
        try {
          await this.updateAlerts({
            oldAlertUUIDs: this.selectedAlerts,
            update: { owner: this.selectedUser },
          });
          this.close();
        } catch (error) {
          this.error = error.message || "Something went wrong!";
        }
      },
      handleError() {
        this.error = null;
      },
      close() {
        this.selectedUser = null;
        this.$store.dispatch("modals/close", this.name);
      },
    },
  };
</script>
