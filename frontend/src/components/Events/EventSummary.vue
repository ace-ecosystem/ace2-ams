<!-- EventSummary.vue -->
<!-- "Event Summary" section on Event Details page -->

<template>
  <h3>Event Summary</h3>
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
  import { ref, inject } from "vue";

  import Button from "primevue/button";
  import Column from "primevue/column";
  import DataTable from "primevue/datatable";
  import MultiSelect from "primevue/multiselect";
  import Toolbar from "primevue/toolbar";
  import EventTableCell from "./EventTableCell.vue";
  import { useEventStore } from "@/stores/event";

  import { parseEventSummary } from "@/stores/eventTable";

  const eventStore = useEventStore();

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
