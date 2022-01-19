<!-- TheFilterToolbar.vue -->
<!-- A toolbar containing buttons/inputs to display/change applied filters for a given set of items (ex. alerts or events) -->

<template>
  <Toolbar>
    <template #start>
      <SplitButton
        label="Quick Add"
        icon="pi pi-plus"
        :model="buttons"
        @click="toggleQuickAddPanel"
      ></SplitButton>
      <EditFilterModal name="EditFilterModal" />
      <FilterChipContainer></FilterChipContainer>
    </template>

    <template #end>
      <OverlayPanel ref="op" style="padding: 1rem" @keypress.enter="addFilter">
        <FilterInput v-model="filterModel" :allow-delete="false"> </FilterInput>
        <Button
          name="update-filter"
          icon="pi pi-check"
          @click="
            toggleQuickAddPanel($event);
            addFilter();
          "
        />
      </OverlayPanel>
      <DateRangePicker />
    </template>
  </Toolbar>
</template>

<script>
  export default {
    name: "TheFilterToolbar",
  };
</script>

<script setup>
  import { inject, ref } from "vue";

  import Button from "primevue/button";
  import FilterChipContainer from "./FilterChipContainer.vue";
  import DateRangePicker from "@/components/UserInterface/DateRangePicker";
  import EditFilterModal from "@/components/Modals/FilterModal";
  import Toolbar from "primevue/toolbar";
  import OverlayPanel from "primevue/overlaypanel";
  import SplitButton from "primevue/splitbutton";
  import FilterInput from "./FilterInput.vue";

  import { useFilterStore } from "@/stores/filter";
  import { useModalStore } from "@/stores/modal";

  const filterStore = useFilterStore();
  const modalStore = useModalStore();

  import { formatForAPI } from "@/services/api/alert";
  import { copyToClipboard } from "@/etc/helpers";

  const filterType = inject("filterType");

  const clear = () => {
    filterStore.clearAll({ filterType: filterType });
  };

  const openFilterModal = () => {
    modalStore.open("EditFilterModal");
  };

  const reset = () => {
    filterStore.clearAll({ filterType: filterType });
  };

  const buttons = [
    {
      label: "Edit",
      icon: "pi pi-filter",
      command: openFilterModal,
    },
    {
      label: "Reset",
      icon: "pi pi-refresh",
      command: reset,
    },
    {
      label: "Clear All",
      icon: "pi pi-filter-slash",
      command: clear,
    },
    {
      label: "Copy Link",
      icon: "pi pi-link",
      command: copyLink,
    },
  ];

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
    filterModel.value = {
      filterName: null,
      filterValue: null,
    };
  };

  const op = ref(null);
  const toggleQuickAddPanel = (event) => {
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
