<!-- TheFilterToolbar.vue -->
<!-- A toolbar containing buttons/inputs to display/change applied filters for a given set of items (ex. alerts or events) -->

<template>
  <Toolbar style="overflow-x: auto">
    <template #left>
      <!--      DATE PICKERS  -->
      <DateRangePicker />
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
        @click="clearFilters"
      />
      <!--      RESET FILTERS-->
      <Button
        type="button"
        icon="pi pi-refresh"
        label="Reset"
        class="p-button-outlined p-m-1"
        @click="resetFilters"
      />
    </template>
  </Toolbar>
</template>

<script>
  import Button from "primevue/button";
  import DateRangePicker from "@/components/UserInterface/DateRangePicker";
  import EditFilterModal from "@/components/Modals/FilterModal";
  import Toolbar from "primevue/toolbar";

  export default {
    name: "TheFilterToolbar",
    components: {
      Button,
      DateRangePicker,
      EditFilterModal,
      Toolbar,
    },

    methods: {
      clearFilters() {
        this.clearDate(this.startFilter);
        this.clearDate(this.endfilter);
      },

      resetFilters() {
        this.clearDate(this.startFilter);
        this.clearDate(this.endfilter);
      },

      open(name) {
        this.$store.dispatch("modals/open", name);
      },
    },
  };
</script>
