<!-- TheFilterToolbar.vue -->
<!-- A toolbar containing buttons/inputs to display/change applied filters for a given set of items (ex. alerts or events) -->

<template>
  <Toolbar style="overflow-x: auto">
    <template #left>
      <!--      DATE PICKER -->
      <i class="pi pi-calendar"></i>
      <Calendar
        id="startTimeFilter"
        v-model="startTimeFilterData"
        class="p-m-1"
        :manual-input="true"
        :show-time="true"
        selection-mode="single"
        style="width: 180px"
      />
      to
      <Calendar
        id="endTimeFilter"
        v-model="endTimeFilterData"
        class="p-m-1"
        :manual-input="true"
        :show-time="true"
        selection-mode="single"
        style="width: 180px"
      />
      <!--      EDIT FILTERS -->
      <Button
        type="button"
        icon="pi pi-filter"
        label="Edit"
        class="p-button-outlined p-m-1"
        style="float: right"
        @click="open('EditFilterModal')"
      />
      <EditFilterModal />
    </template>
    <!--    TODO: SHOW APPLIED FILTERS -->
    <template #right>
      <!--      CLEAR FILTERS-->
      <Button
        type="button"
        icon="pi pi-filter-slash"
        label="Clear"
        class="p-button-outlined p-m-1"
      />
      <!--      RESET FILTERS-->
      <Button
        type="button"
        icon="pi pi-refresh"
        label="Reset"
        class="p-button-outlined p-m-1"
      />
    </template>
  </Toolbar>
</template>

<script>
  import Button from "primevue/button";
  import Calendar from "primevue/calendar";
  import Toolbar from "primevue/toolbar";

  import EditFilterModal from "@/components/Modals/FilterModal";

  export default {
    name: "TheFilterToolbar",
    components: { Button, Calendar, EditFilterModal, Toolbar },

    data() {
      return {
        endTimeFilterData: null,
        startTimeFilterData: null,
      };
    },

    methods: {
      open(name) {
        this.$store.dispatch("modals/open", name);
      },
    },
  };
</script>
