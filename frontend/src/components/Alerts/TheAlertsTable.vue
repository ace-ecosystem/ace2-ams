<!-- TheAlertsTable.vue -->
<!-- The table where all currently filtered alerts are displayed, selected to take action, or link to an individual alert page -->

<template>
  <TheNodeTable
    :columns="columns"
    @rowExpand="onRowExpand"
    @rowCollapse="onRowCollapse"
  >
    <template #rowCell="{ data, field }">
      <AlertTableCell :data="data" :field="field"></AlertTableCell>
    </template>

    <!-- Row Expansion -->
    <template #rowExpansion="{ data }">
      <AlertTableExpansion
        :observables="alertObservables[data.uuid]"
      ></AlertTableExpansion>
    </template>
  </TheNodeTable>
</template>

<script setup>
  import { ref } from "vue";

  import { NodeTree } from "@/services/api/nodeTree";
  import TheNodeTable from "@/components/Node/TheNodeTable.vue";
  import AlertTableCell from "@/components/Alerts/AlertTableCell.vue";
  import AlertTableExpansion from "@/components/Alerts/AlertTableExpansion.vue";

  const columns = ref([
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
  ]);

  const alertObservables = ref({});

  const onRowExpand = async (event) => {
    const alertUuid = event.data.uuid;
    // Set to null first so AlertTableExpansion can show loading
    alertObservables.value[alertUuid] = null;
    alertObservables.value[alertUuid] = await getObservables(alertUuid);
  };
  const onRowCollapse = (event) => {
    const alertUuid = event.data.uuid;
    delete alertObservables.value[alertUuid];
  };

  const getObservables = async (uuid) => {
    const unsortedObservables = await NodeTree.readNodesOfNodeTree(
      [uuid],
      "observable",
    );

    return unsortedObservables.sort((a, b) => {
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
