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
        data-cy="edit-filters"
        @click="open('EditFilterModal')"
      />
      <EditFilterModal name="EditFilterModal" />
      <Button
        type="button"
        icon="pi pi-refresh"
        label="Reset"
        class="p-button-outlined p-m-1"
        data-cy="reset-filters"
        @click="reset"
      />
      <Button
        type="button"
        icon="pi pi-filter-slash"
        label="Clear"
        class="p-button-outlined p-m-1"
        data-cy="clear-filters"
        @click="clear"
      />
    </template>
    <template #end>
      <DateRangePicker />
      <Button icon="pi pi-link" class="p-button-rounded" @click="copyLink" />
    </template>
  </Toolbar>
  <Toolbar class="transparent-toolbar">
    <template #start>
      <Button icon="pi pi-plus" class="p-m-1" @click="toggleOverlay" />
      <OverlayPanel ref="op" tabindex="1" @keypress.enter="updateFilter">
        <FilterInput v-model="filterModel" :allow-delete="false"> </FilterInput>
        <Button
          name="update-filter"
          icon="pi pi-check"
          tabindex="1"
          @click="addFilter"
        />
      </OverlayPanel>
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
  import { inject, ref, computed } from "vue";

  import Button from "primevue/button";
  import FilterChipContainer from "./FilterChipContainer.vue";
  import DateRangePicker from "@/components/UserInterface/DateRangePicker";
  import EditFilterModal from "@/components/Modals/FilterModal";
  import Toolbar from "primevue/toolbar";
  import OverlayPanel from "primevue/overlaypanel";
  import FilterInput from "./FilterInput.vue";

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

  const filterModel = ref({
    filterName: null,
    filterValue: null,
  });

  const addFilter = () => {
    filterStore.setFilter({
      filterType: filterType,
      filterName: filterModel.value.filterName,
      filterValue: filterModel.value.filterValue,
    });
    toggleOverlay();
    filterModel.value = {
      filterName: null,
      filterValue: null,
    };
  };

  const op = ref(null);
  const toggleOverlay = (event) => {
    op.value.toggle(event);
  };
</script>

<style>
  .transparent-toolbar {
    background: none;
    border: none;
    padding-bottom: 0;
  }
</style>
