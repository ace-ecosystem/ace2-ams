<!-- EventSummary.vue -->
<!-- "Event Summary" section on Event Details page -->

<template>
  <h3>Event Summary</h3>
  <!-- Event Timeline -->
  <Timeline :value="timelineEvents" layout="horizontal" align="bottom">
    <template #marker="slotProps">
      <span class="custom-marker">
        <i :class="slotProps.item.icon"></i>
      </span>
    </template>
    <template #opposite="slotProps">
      <small class="p-text-secondary">{{
        formatDatetime(slotProps.item.datetime)
      }}</small>
    </template>
    <template #content="slotProps">
      {{ slotProps.item.label }}
    </template>
  </Timeline>
  <!-- Event Details Table -->
  <DataTable
    :value="[parseEventSummary(eventStore.open)]"
    :resizable-columns="true"
  >
    <!-- TABLE TOOLBAR-->
    <template #header>
      <Toolbar style="border: none">
        <template #start>
          <!-- COLUMN SELECT -->
          <MultiSelect
            :model-value="selectedColumns"
            :options="columnOptions"
            data-cy="table-column-select"
            option-label="header"
            placeholder="Select Columns"
            @update:model-value="onColumnToggle"
          />
        </template>
        <template #end>
          <Button
            data-cy="reset-table-button"
            icon="pi pi-refresh"
            class="p-button-rounded p-m-1"
            @click="reset()"
          />
        </template>
      </Toolbar>
    </template>

    <!-- DATA COLUMNS -->
    <Column
      v-for="(col, index) of selectedColumns"
      :key="col.field + '_' + index"
      :field="col.field"
      :header="col.header"
    >
      <!-- DATA COLUMN CELL BODIES-->
      <template #body="{ data, field }">
        <EventTableCell
          :data="data"
          :field="field"
          :show-tags="false"
        ></EventTableCell>
      </template>
    </Column>
  </DataTable>
</template>

<script setup>
  import { ref, inject, computed } from "vue";

  import { useEventStore } from "@/stores/event";
  import Button from "primevue/button";
  import Column from "primevue/column";
  import DataTable from "primevue/datatable";
  import EventTableCell from "./EventTableCell.vue";
  import MultiSelect from "primevue/multiselect";
  import Toolbar from "primevue/toolbar";
  import Timeline from "primevue/timeline";

  import { parseEventSummary } from "@/stores/eventTable";

  const eventStore = useEventStore();

  const eventTimes = [
    {
      label: "Event",
      datetime: eventStore.open.eventTime || eventStore.open.autoEventTime,
      icon: "pi pi-map-marker",
    },
    {
      label: "Alert",
      datetime: eventStore.open.alertTime || eventStore.open.autoAlertTime,
      icon: "pi pi-exclamation-triangle",
    },
    {
      label: "Ownership",
      datetime:
        eventStore.open.ownershipTime || eventStore.open.autoOwnershipTime,
      icon: "pi pi-user-plus",
    },
    {
      label: "Disposition",
      datetime:
        eventStore.open.dispositionTime ||
        eventStore.open.autoDispositionTime ||
        "TBD",
      icon: "pi pi-flag",
    },
    {
      label: "Contain",
      datetime: eventStore.open.containTime || "TBD",
      icon: "pi pi-shield",
    },
    {
      label: "Remediation",
      datetime: eventStore.open.remediationTime || "TBD",
      icon: "pi pi-check-circle",
    },
  ];

  const formatDatetime = (datetime) => {
    if (datetime != "TBD") {
      const d = new Date(datetime);
      return d.toLocaleString("en-US");
    }
    return datetime;
  };

  const timelineEvents = computed(() => {
    return [...eventTimes.filter((event) => event.datetime)];
  });

  const config = inject("config");
  const columns = ref(
    config.events.eventQueueColumnMappings[eventStore.open.queue.value],
  );
  const columnOptions = columns.value.filter((col) => !col.required);
  const selectedColumns = ref(columns.value.filter((col) => col.default));

  const onColumnToggle = (val) => {
    // Toggles selected columns to display
    // This method required/provided by Primevue 'ColToggle' docs
    selectedColumns.value = columns.value.filter((col) => val.includes(col));
  };

  const reset = () => {
    selectedColumns.value = columns.value.filter((col) => col.default);
  };
</script>
