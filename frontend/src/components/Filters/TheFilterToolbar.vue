<!-- TheFilterToolbar.vue -->
<!-- A toolbar containing buttons/inputs to display/change applied filters for a given set of items (ex. alerts or events) -->

<template>
  <Toolbar style="overflow-x: auto">
    <template #start>
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
      <EditFilterModal name="EditFilterModal" />
    </template>
    <!--    TODO: SHOW APPLIED FILTERS -->
    <template #end>
      <!--      CLEAR FILTERS-->
      <Button
        type="button"
        icon="pi pi-filter-slash"
        label="Clear"
        class="p-button-outlined p-m-1"
        @click="clear"
      />
      <!--      RESET FILTERS-->
      <Button
        type="button"
        icon="pi pi-refresh"
        label="Reset"
        class="p-button-outlined p-m-1"
        @click="reset"
      />
      <Button icon="pi pi-link" class="p-button-rounded" @click="viewLink"/>
    </template>
  </Toolbar>
</template>

<script>
  export default {
    name: "TheFilterToolbar",
  };
</script>

<script setup>
  import { inject } from "vue";

  import Button from "primevue/button";
  import DateRangePicker from "@/components/UserInterface/DateRangePicker";
  import EditFilterModal from "@/components/Modals/FilterModal";
  import Toolbar from "primevue/toolbar";

  import { useFilterStore } from "@/stores/filter";
  import { useModalStore } from "@/stores/modal";

  const filterType = inject("filterType");

  const filterStore = useFilterStore();
  const modalStore = useModalStore();

  const clear = () => {
    filterStore.clearAll({ filterType: filterType });
  };

  const open = (name) => {
    modalStore.open(name);
  };

  const reset = () => {
    filterStore.clearAll({ filterType: filterType });
  };
</script>
