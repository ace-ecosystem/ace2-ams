<!-- EventTableExpansion.vue -->
<!-- Contains logic and functionality for displaying data in event row dropdown, currently table of alerts -->

<template>
  <DataTable :value="alerts">
    <Column
      v-for="(value, name) of columns"
      :key="name"
      :field="name"
      :header="value"
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

  const alerts = ref(null);
  const columns = {
    eventTime: "Event Time",
    name: "Name",
    owner: "Owner",
    disposition: "Disposition",
  };

  onMounted(async () => {
    await getAlerts(props.uuid);
  });

  const props = defineProps({
    uuid: { type: String, required: true },
  });

  const getAlerts = async (uuid) => {
    const allAlerts = await Alert.readAllPages({
      eventUuid: uuid,
      sort: "event_time|asc",
    });

    alerts.value = allAlerts.map((x) => parseAlertSummary(x));
  };
</script>

<style>
  .link-text:hover {
    cursor: pointer;
    text-decoration: underline;
    font-weight: bold;
  }
</style>
