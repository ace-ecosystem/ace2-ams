/* eslint-disable vue/attribute-hyphenation */
<!-- TheEventsTable.vue -->
<!-- The table where all currently filtered events are displayed, selected to take action, or link to an individual event page -->

<template>
  <TheNodeTable :columns="columns" :row-expansion="false">
    <template #rowCell="{ data, field }">
      <EventTableCell :data="data" :field="field"></EventTableCell>
    </template>
  </TheNodeTable>
</template>

<script setup>
  import { ref } from "vue";

  import TheNodeTable from "../Node/TheNodeTable";
  import EventTableCell from "./EventTableCell";

  const columns = ref([
    { field: "createdTime", header: "Created", sortable: true, default: true },
    { field: "name", header: "Name", sortable: true, default: true },
    { field: "owner", header: "Owner", sortable: true, default: true },
    { field: "status", header: "Status", sortable: true, default: false },
    { field: "type", header: "Type", sortable: true, default: true },
    { field: "vectors", header: "Vectors", sortable: false, default: true },
    {
      field: "threatActors",
      header: "Threat Actors",
      sortable: false,
      default: false,
    },
    { field: "threats", header: "Threats", sortable: false, default: false },
    {
      field: "preventionTools",
      header: "Prevention Tools",
      sortable: false,
      default: false,
    },
    {
      field: "riskLevel",
      header: "Risk Level",
      sortable: true,
      default: false,
    },
  ]);
</script>
