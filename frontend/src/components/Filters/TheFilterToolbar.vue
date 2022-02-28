<!-- TheFilterToolbar.vue -->
<!-- A toolbar containing buttons/inputs to display/change applied filters for a given set of items (ex. alerts or events) -->

<template>
  <Toolbar>
    <template #start>
      <SplitButton
        data-cy="edit-filter-button"
        label="Quick Add"
        icon="pi pi-plus"
        :model="buttons"
        @click="toggleQuickAddPanel"
      ></SplitButton>
      <EditFilterModal name="EditFilterModal" />
      <FilterChipContainer></FilterChipContainer>
    </template>

    <template #end>
      <OverlayPanel
        ref="op"
        data-cy="quick-add-filter-panel"
        style="padding: 1rem"
        @keypress.enter="addFilter"
      >
        <NodePropertyInput
          v-model="filterModel"
          data-cy="filter-input"
          :allow-delete="false"
          form-type="filter"
          :queue="queue"
        >
        </NodePropertyInput>
        <Button
          data-cy="quick-add-filter-submit-button"
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
  import { inject, computed, ref } from "vue";

  import Button from "primevue/button";
  import FilterChipContainer from "@/components/Filters/FilterChipContainer.vue";
  import DateRangePicker from "@/components/UserInterface/DateRangePicker.vue";
  import EditFilterModal from "@/components/Modals/FilterModal.vue";
  import Toolbar from "primevue/toolbar";
  import OverlayPanel from "primevue/overlaypanel";
  import SplitButton from "primevue/splitbutton";
  import NodePropertyInput from "../Node/NodePropertyInput.vue";

  import { useFilterStore } from "@/stores/filter";
  import { useModalStore } from "@/stores/modal";
  import { useCurrentUserSettingsStore } from "@/stores/currentUserSettings";

  const filterStore = useFilterStore();
  const modalStore = useModalStore();
  const currentUserSettingsStore = useCurrentUserSettingsStore();

  import { copyToClipboard, formatNodeFiltersForAPI } from "@/etc/helpers";

  const config = inject("config");

  const nodeType = inject("nodeType");
  const filterOptions = {
    alerts: config.alerts.alertFilters,
    events: config.events.eventFilters,
  };

  const queue = computed(() => {
    return currentUserSettingsStore.$state["queues"][nodeType].value;
  });

  const clear = () => {
    filterStore.clearAll({ nodeType: nodeType });
  };

  const openFilterModal = () => {
    modalStore.open("EditFilterModal");
  };

  const reset = () => {
    filterStore.clearAll({ nodeType: nodeType });
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
    let link = `${window.location.origin}/manage_${nodeType}`;
    // If there are filters set, build the link for it
    if (Object.keys(filterStore[nodeType]).length) {
      let urlParams = new URLSearchParams(
        formatNodeFiltersForAPI(filterOptions[nodeType], filterStore[nodeType]),
      );
      link = `${
        window.location.origin
      }/manage_${nodeType}?${urlParams.toString()}`;
    }
    return link;
  }

  function copyLink() {
    const link = generateLink();
    copyToClipboard(link);
  }

  const filterModel = ref({
    propertyType: null,
    propertyValue: null,
  });

  const addFilter = () => {
    filterStore.setFilter({
      nodeType: nodeType,
      filterName: filterModel.value.propertyType,
      filterValue: filterModel.value.propertyValue,
    });
    filterModel.value = {
      propertyType: null,
      propertyValue: null,
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
