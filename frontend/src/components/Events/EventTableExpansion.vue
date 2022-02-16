<!-- EventTableExpansion.vue -->
<!-- Contains logic and functionality for displaying data in event row dropdown, currently table of alerts -->

<template>
  <div v-if="isLoading">Loading alerts, please hold...</div>
  <DataTable
    v-else
    :value="alerts"
    :paginator="true"
    :rows="10"
    :selection="selectedRows"
    paginator-template="CurrentPageReport FirstPageLink PrevPageLink PageLinks NextPageLink LastPageLink RowsPerPageDropdown"
    :rows-per-page-options="[5, 10, 50, 100]"
    :total-records="alerts.length"
    responsive-layout="scroll"
    current-page-report-template="Showing {first} to {last} of {totalRecords} alerts in the event"
    data-cy="expandedEvent"
    @rowSelect="selectedAlertStore.select($event.data.uuid)"
    @rowUnselect="selectedAlertStore.unselect($event.data.uuid)"
    @rowSelect-all=""
    @rowUnselect-all="selectedAlertStore.unselectAll()"
  >
    <!-- CHECKBOX COLUMN -->
    <Column
      id="alert-select"
      header-style="width: 3em"
      selection-mode="multiple"
    />

    <!-- DATA COLUMNS -->
    <Column
      v-for="col of columns"
      :key="col.field"
      :field="col.field"
      :header="col.header"
      :sortable="true"
      ><template #body="{ data, field }">
        <AlertTableCell :data="data" :field="field"></AlertTableCell> </template
    ></Column>
  </DataTable>
</template>

<script setup>
  import { computed, defineProps, onBeforeMount, onUnmounted, ref } from "vue";

  import Column from "primevue/column";
  import DataTable from "primevue/datatable";

  import AlertTableCell from "../Alerts/AlertTableCell.vue";
  import { useSelectedAlertStore } from "@/stores/selectedAlert";

  const selectedAlertStore = useSelectedAlertStore();

  const selectedRows = ref();

  onBeforeMount(() => {
    selectedAlertStore.unselectAll();
  });

  onUnmounted(() => {
    selectedAlertStore.unselectAll();
  });

  const columns = [
    { field: "eventTime", header: "Event Time" },
    { field: "name", header: "Name" },
    { field: "owner", header: "Owner" },
    { field: "disposition", header: "Disposition" },
  ];
  const props = defineProps({
    alerts: { type: [Array, null], required: true },
  });
  const isLoading = computed(() => {
    return props.alerts === null;
  });
</script>

<style>
  .link-text:hover {
    cursor: pointer;
    text-decoration: underline;
    font-weight: bold;
  }
</style>
