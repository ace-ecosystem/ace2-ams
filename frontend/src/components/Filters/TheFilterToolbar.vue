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

<script lang="ts">
  export default {
    name: "TheFilterToolbar",
  };
</script>

<script setup lang="ts">
  import { inject, computed, ref } from "vue";

  import Button from "primevue/button";
  import FilterChipContainer from "@/components/Filters/FilterChipContainer.vue";
  import DateRangePicker from "@/components/UserInterface/DateRangePicker.vue";
  import EditFilterModal from "@/components/Modals/FilterModal.vue";
  import Toolbar from "primevue/toolbar";
  import OverlayPanel from "primevue/overlaypanel";
  import SplitButton from "primevue/splitbutton";
  import NodePropertyInput from "@/components/Node/NodePropertyInput.vue";

  import { useAuthStore } from "@/stores/auth";
  import { useEventStatusStore } from "@/stores/eventStatus";
  import { useFilterStore } from "@/stores/filter";
  import { useModalStore } from "@/stores/modal";
  import { useCurrentUserSettingsStore } from "@/stores/currentUserSettings";
  import { validAlertFilters } from "@/etc/constants/alerts";
  import { validEventFilters } from "@/etc/constants/events";

  import { copyToClipboard, formatNodeFiltersForAPI } from "@/etc/helpers";
  import { queueRead } from "@/models/queue";
  import { eventStatusRead } from "@/models/eventStatus";

  const filterStore = useFilterStore();
  const modalStore = useModalStore();
  const authStore = useAuthStore();
  const currentUserSettingsStore = useCurrentUserSettingsStore();
  const eventStatusStore = useEventStatusStore();

  const nodeType = inject("nodeType") as "alerts" | "events";
  const validFilterOptions = {
    alerts: validAlertFilters,
    events: validEventFilters,
  };

  const queue = computed(() => {
    return currentUserSettingsStore.queues[nodeType] != null
      ? currentUserSettingsStore.queues[nodeType]!.value
      : "unknown";
  });

  const clear = () => {
    filterStore.clearAll({ nodeType: nodeType });
  };

  const openFilterModal = () => {
    modalStore.open("EditFilterModal");
  };

  const reset = () => {
    // reset all to start
    filterStore.clearAll({ nodeType: nodeType });
    if (nodeType === "alerts") {
      const filters: { queue?: queueRead[] } = {};
      // look for owner == current user OR none
      // currently explicit "no owner" filter is unavailable so, skip this one for now
      // filters.owner = authStore.user;

      // look for alerts with open disposition
      // currently explicit "no disposition" filter is unavailable so, skip this one for now
      // filters.disposition = null;

      // look for alerts in current user's preferred queue
      filters.queue = [
        currentUserSettingsStore.queues.alerts
          ? currentUserSettingsStore.queues.alerts
          : authStore.user.defaultAlertQueue,
      ];

      filterStore.bulkSetFilters({ nodeType: nodeType, filters: filters });
    } else if (nodeType === "events") {
      const filters: { queue?: queueRead[]; status?: eventStatusRead[] } = {};
      // look for events with 'OPEN' or "INTERNAL COLLECTION" (?) status
      // can't do OR filters right now, look only for 'OPEN' events
      const openStatus = eventStatusStore.items.find((status) => {
        return status.value === "OPEN";
      });
      if (openStatus) {
        filters.status = [openStatus];
      }

      // look for events in current user's preferred queue
      filters.queue = [
        currentUserSettingsStore.queues.events
          ? currentUserSettingsStore.queues.events
          : authStore.user.defaultEventQueue,
      ];

      filterStore.bulkSetFilters({ nodeType: nodeType, filters: filters });
    }
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
        formatNodeFiltersForAPI(
          validFilterOptions[nodeType],
          filterStore[nodeType],
        ) as unknown as URLSearchParams,
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
    if (filterModel.value.propertyType && filterModel.value.propertyValue) {
      filterStore.setFilter({
        nodeType: nodeType,
        filterName: filterModel.value.propertyType,
        filterValue: filterModel.value.propertyValue,
      });
    }
    filterModel.value = {
      propertyType: null,
      propertyValue: null,
    };
  };

  const op = ref();
  const toggleQuickAddPanel = (event: unknown) => {
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
