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
        v-if="alertObservables[data.uuid]"
        :observables="alertObservables[data.uuid]"
      ></AlertTableExpansion>
      <div v-else style="flex: 1">
        <ul>
          <li><Skeleton width="30%"></Skeleton></li>
          <li><Skeleton width="25%"></Skeleton></li>
          <li><Skeleton width="30%"></Skeleton></li>
          <li><Skeleton width="25%"></Skeleton></li>
        </ul>
      </div>
    </template>
  </TheNodeTable>
</template>

<script setup>
  import { ref } from "vue";

  import Skeleton from "primevue/skeleton";

  import TheNodeTable from "../Node/TheNodeTable";
  import AlertTableCell from "./AlertTableCell";
  import AlertTableExpansion from "./AlertTableExpansion";
  import { NodeTree } from "@/services/api/nodeTree";

  const columns = ref([
    { field: "dispositionTime", header: "Dispositioned Time", default: false },
    { field: "insertTime", header: "Insert Time", default: false },
    { field: "eventTime", header: "Event Time", default: true },
    { field: "name", header: "Name", default: true },
    { field: "owner", header: "Owner", default: true },
    { field: "disposition", header: "Disposition", default: true },
    { field: "dispositionUser", header: "Dispositioned By", default: false },
    { field: "queue", header: "Queue", default: false },
    { field: "type", header: "Type", default: false },
  ]);

  const alertObservables = ref({});

  const onRowExpand = async (event) => {
    const alertUuid = event.data.uuid;
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
