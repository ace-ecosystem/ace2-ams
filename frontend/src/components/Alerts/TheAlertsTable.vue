<!-- TheAlertsTable.vue -->
<!-- The table where all currently filtered alerts are displayed, selected to take action, or link to an individual alert page -->

<template>
  <TheNodeTable
    :columns="columns"
    @row-expand="onRowExpand"
    @row-collapse="onRowCollapse"
  >
    <template #rowCell="{ data, field }">
      <AlertTableCell
        :data="data"
        :field="(field as unknown as alertSummaryKeys)"
      ></AlertTableCell>
    </template>

    <!-- Row Expansion -->
    <template #rowExpansion="{ data }">
      <div data-cy="row-expansion">
        <AlertTableExpansion
          :observables="alertObservables[data.uuid]"
        ></AlertTableExpansion>
      </div>
    </template>
  </TheNodeTable>
</template>

<script setup lang="ts">
  import { ref } from "vue";

  import AlertTableCell from "@/components/Alerts/AlertTableCell.vue";
  import AlertTableExpansion from "@/components/Alerts/AlertTableExpansion.vue";
  import TheNodeTable from "@/components/Node/TheNodeTable.vue";

  import { observableRead } from "@/models/observable";

  import { Alert } from "@/services/api/alert";
  import { alertSummary } from "@/models/alert";

  type alertSummaryKeys = keyof alertSummary;

  interface column {
    required?: boolean;
    default: boolean;
    field: string;
    header: string;
    sortable: boolean;
  }

  const columns: column[] = [
    {
      field: "dispositionTime",
      header: "Dispositioned Time (UTC)",
      sortable: true,
      default: false,
    },
    {
      field: "insertTime",
      header: "Insert Time (UTC)",
      sortable: true,
      default: false,
    },
    {
      field: "eventTime",
      header: "Event Time (UTC)",
      sortable: true,
      default: true,
    },
    { field: "name", header: "Name", sortable: true, default: true },
    { field: "owner", header: "Owner", sortable: true, default: true },
    {
      field: "disposition",
      header: "Disposition",
      sortable: true,
      default: true,
    },
    {
      field: "dispositionUser",
      header: "Dispositioned By",
      sortable: true,
      default: false,
    },
    { field: "queue", header: "Queue", sortable: true, default: false },
    { field: "type", header: "Type", sortable: true, default: false },
  ];

  const alertObservables = ref<Record<string, null | observableRead[]>>({});

  const onRowExpand = async (event: { data: alertSummary }) => {
    const alertUuid = event.data.uuid;
    // Set to null first so AlertTableExpansion can show loading
    alertObservables.value[alertUuid] = null;
    alertObservables.value[alertUuid] = await Alert.readObservables([
      alertUuid,
    ]);
  };

  const onRowCollapse = (event: { data: alertSummary }) => {
    const alertUuid = event.data.uuid;
    delete alertObservables.value[alertUuid];
  };
</script>

<style>
  .link-text:hover {
    cursor: pointer;
    text-decoration: underline;
    font-weight: bold;
  }
</style>
