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

  import { NodeTree } from "@/services/api/nodeTree";
  import { alertSummary } from "@/models/alert";

  type alertSummaryKeys = keyof alertSummary;

  const columns = [
    {
      field: "dispositionTime",
      header: "Dispositioned Time",
      sortable: true,
      default: false,
    },
    {
      field: "insertTime",
      header: "Insert Time",
      sortable: true,
      default: false,
    },
    { field: "eventTime", header: "Event Time", sortable: true, default: true },
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
    alertObservables.value[alertUuid] = await getObservables(alertUuid);
  };

  const onRowCollapse = (event: { data: alertSummary }) => {
    const alertUuid = event.data.uuid;
    delete alertObservables.value[alertUuid];
  };

  const getObservables = async (uuid: string) => {
    const unsortedObservables = (await NodeTree.readNodesOfNodeTree(
      [uuid],
      "observable",
    )) as unknown as observableRead[];

    return unsortedObservables.sort((a: observableRead, b: observableRead) => {
      if (a.type.value === b.type.value) {
        return a.value < b.value ? -1 : 1;
      } else {
        return a.type.value < b.type.value ? -1 : 1;
      }
    });
  };
</script>

<style>
  .link-text:hover {
    cursor: pointer;
    text-decoration: underline;
    font-weight: bold;
  }
</style>
