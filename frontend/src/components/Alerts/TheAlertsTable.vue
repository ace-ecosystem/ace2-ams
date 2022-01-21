<!-- TheAlertsTable.vue -->
<!-- The table where all currently filtered alerts are displayed, selected to take action, or link to an individual alert page -->

<template>
  <TheNodeTable
    :columns="columns"
    :column-select="true"
    :export-c-s-v="true"
    :keyword-search="true"
    :reset-table="true"
    :row-expansion="true"
  >
    <template #rowCell="{ data, field }">
      <AlertTableCell :data="data" :field="field"></AlertTableCell>
    </template>

    <!-- Row Expansion -->
    <template #rowExpansion="{ data }">
      <suspense>
        <template #fallback>
          <ul></ul>
        </template>
        <template #default>
          <AlertTableExpansion
            :uuid="data.uuid"
            :data="data"
          ></AlertTableExpansion>
        </template>
      </suspense>
    </template>
  </TheNodeTable>
</template>

<script setup>
  import { ref } from "vue";

  import TheNodeTable from "../Node/TheNodeTable";
  import AlertTableCell from "./AlertTableCell";
  import AlertTableExpansion from "./AlertTableExpansion";

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
</script>

<style>
  .link-text:hover {
    cursor: pointer;
    text-decoration: underline;
    font-weight: bold;
  }
</style>
