<!-- EventTableExpansion.vue -->
<!-- Contains logic and functionality for displaying data in event row dropdown, currently table of alerts -->

<template>
  <div v-if="isLoading">Loading alerts, please hold...</div>
  <div v-else>
    <DataTable
      :value="visibleAlerts"
      :selection="selectedRows"
      responsive-layout="scroll"
      data-cy="expandedEvent"
      @rowSelect="selectedAlertStore.select($event.data.uuid)"
      @rowUnselect="selectedAlertStore.unselect($event.data.uuid)"
      @rowSelect-all="selectedAlertStore.selectAll(visibleAlertUuids)"
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
          <AlertTableCell
            :data="data"
            :field="field"
          ></AlertTableCell> </template
      ></Column>
    </DataTable>

    <Paginator
      data-cy="alert-table-pagination-options"
      :rows="10"
      :rows-per-page-options="[5, 10, 50, 100]"
      :total-records="alerts.length"
      template="CurrentPageReport FirstPageLink PrevPageLink PageLinks NextPageLink LastPageLink RowsPerPageDropdown"
      current-page-report-template="Showing {first} to {last} of {totalRecords} alerts in the event"
      @page="
        onPage($event);
        selectedAlertStore.unselectAll();
      "
    ></Paginator>
  </div>
</template>

<script setup>
  import { computed, defineProps, onBeforeMount, onUnmounted, ref } from "vue";

  import Column from "primevue/column";
  import DataTable from "primevue/datatable";
  import Paginator from "primevue/paginator";

  import AlertTableCell from "../Alerts/AlertTableCell.vue";
  import { useSelectedAlertStore } from "@/stores/selectedAlert";

  const selectedAlertStore = useSelectedAlertStore();

  onBeforeMount(() => {
    selectedAlertStore.unselectAll();
  });

  onUnmounted(() => {
    selectedAlertStore.unselectAll();
  });

  const props = defineProps({
    alerts: { type: [Array, null], required: true },
  });

  const page = ref(0);
  const pageSize = ref(10);

  const isLoading = computed(() => {
    return props.alerts === null;
  });

  const selectedRows = computed(() => {
    return props.alerts.filter((alert) =>
      selectedAlertStore.selected.includes(alert.uuid),
    );
  });

  const visibleAlerts = computed(() => {
    const start = page.value * pageSize.value;
    const end = start + pageSize.value;
    return props.alerts.slice(start, end);
  });

  const visibleAlertUuids = computed(() => {
    return visibleAlerts.value.map((x) => x.uuid);
  });

  const columns = [
    { field: "eventTime", header: "Event Time" },
    { field: "name", header: "Name" },
    { field: "owner", header: "Owner" },
    { field: "disposition", header: "Disposition" },
  ];

  const onPage = async (event) => {
    selectedAlertStore.unselectAll();
    page.value = event.page;
    pageSize.value = event.rows;
  };
</script>

<style>
  .link-text:hover {
    cursor: pointer;
    text-decoration: underline;
    font-weight: bold;
  }
</style>
