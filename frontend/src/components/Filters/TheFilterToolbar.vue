<!-- TheFilterToolbar.vue -->
<!-- A toolbar containing buttons/inputs to display/change applied filters for a given set of items (ex. alerts or events) -->

<template>
  <!-- Filter Action Toolbar -->
  <Toolbar style="overflow-x: auto">
    <template #start>
      <Button
        type="button"
        icon="pi pi-filter"
        label="Edit"
        class="p-button-outlined p-m-1"
        @click="open('EditFilterModal')"
      />
      <EditFilterModal name="EditFilterModal" />
      <Button
        type="button"
        icon="pi pi-refresh"
        label="Reset"
        class="p-button-outlined p-m-1"
        @click="reset"
      />
      <Button
        type="button"
        icon="pi pi-filter-slash"
        label="Clear"
        class="p-button-outlined p-m-1"
        @click="clear"
      />
    </template>
    <template #end>
      <DateRangePicker />
      <Button icon="pi pi-link" class="p-button-rounded" @click="copyLink" />
    </template>
  </Toolbar>

  <!-- Filter Chips "Toolbar" -->
  <Toolbar v-if="!filtersAreEmpty" class="transparent-toolbar">
    <template #start>
      <FilterChipContainer></FilterChipContainer>
    </template>

    <template #end> </template>
  </Toolbar>
</template>

<script>
  export default {
    name: "TheFilterToolbar",
  };
</script>

<script setup>
  import { computed, inject } from "vue";

  import Button from "primevue/button";
  import FilterChipContainer from "./FilterChipContainer.vue";
  import DateRangePicker from "@/components/UserInterface/DateRangePicker";
  import EditFilterModal from "@/components/Modals/FilterModal";
  import Toolbar from "primevue/toolbar";

  import { useFilterStore } from "@/stores/filter";
  import { useModalStore } from "@/stores/modal";

  const filterStore = useFilterStore();
  const modalStore = useModalStore();

  import { formatForAPI } from "@/services/api/alert";
  import { copyToClipboard } from "@/etc/helpers";

  const filterType = inject("filterType");

  const filtersAreEmpty = computed(() => {
    return Object.keys(filterStore[filterType]).length === 0;
  });

  function generateLink() {
    let link = `${window.location.origin}/manage_alerts`;
    // If there are filters set, build the link for it
    if (Object.keys(filterStore[filterType]).length) {
      let urlParams = new URLSearchParams(
        formatForAPI(filterStore[filterType]),
      );
      link = `${window.location.origin}/manage_alerts?${urlParams.toString()}`;
    }
    return link;
  }

  function copyLink() {
    const link = generateLink();
    copyToClipboard(link);
  }

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

<style>
  .transparent-toolbar {
    background: none;
    border: none;
    padding-bottom: 0;
  }
</style>
