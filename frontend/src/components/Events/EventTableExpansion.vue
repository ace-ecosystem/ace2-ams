<!-- EventTableExpansion.vue -->
<!-- Contains logic and functionality for displaying data in event row dropdown, currently table of alerts -->

<template>
  <DataTable
    :value="alerts"
    :paginator="true"
    :rows="10"
    paginator-template="CurrentPageReport FirstPageLink PrevPageLink PageLinks NextPageLink LastPageLink RowsPerPageDropdown"
    :rows-per-page-options="[5, 10, 50, 100]"
    :total-records="alerts.length"
    responsive-layout="scroll"
    current-page-report-template="Showing {first} to {last} of {totalRecords} alerts in the event"
    :loading="isLoading"
    data-cy="expandedEvent"
  >
    <template #loading>Loading alerts, please wait...</template>
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
  import { ref, defineProps, onMounted } from "vue";

  import Column from "primevue/column";
  import DataTable from "primevue/datatable";

  import AlertTableCell from "../Alerts/AlertTableCell.vue";

  import { Alert } from "@/services/api/alert";
  import { parseAlertSummary } from "@/etc/helpers";

  const alerts = ref([]);
  const isLoading = ref(false);

  const columns = [
    { field: "eventTime", header: "Event Time" },
    { field: "name", header: "Name" },
    { field: "owner", header: "Owner" },
    { field: "disposition", header: "Disposition" },
  ];

  onMounted(async () => {
    await getAlerts(props.uuid);
  });

  const props = defineProps({
    uuid: { type: String, required: true },
  });

  const getAlerts = async (uuid) => {
    isLoading.value = true;
    const allAlerts = await Alert.readAllPages({
      eventUuid: uuid,
      sort: "event_time|asc",
    });

    alerts.value = allAlerts.map((x) => parseAlertSummary(x));
    isLoading.value = false;
  };
</script>

<style>
  .link-text:hover {
    cursor: pointer;
    text-decoration: underline;
    font-weight: bold;
  }
</style>
