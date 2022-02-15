/* eslint-disable vue/attribute-hyphenation */
<!-- TheEventsTable.vue -->
<!-- The table where all currently filtered events are displayed, selected to take action, or link to an individual event page -->

<template>
  <TheNodeTable
    :columns="columns"
    @rowExpand="onRowExpand"
    @rowCollapse="onRowCollapse"
  >
    <template #rowCell="{ data, field }">
      <EventTableCell :data="data" :field="field"></EventTableCell>
    </template>

    <!-- Row Expansion -->
    <template #rowExpansion="{ data }">
      <EventTableExpansion
        :alerts="eventAlerts[data.uuid]"
      ></EventTableExpansion>
    </template>
  </TheNodeTable>
</template>

<script setup>
  import { ref } from "vue";

  import TheNodeTable from "@/components/Node/TheNodeTable.vue";
  import EventTableCell from "@/components/Events/EventTableCell.vue";
  import EventTableExpansion from "@/components/Events/EventTableExpansion.vue";

  import { Alert } from "@/services/api/alert";
  import { parseAlertSummary } from "@/etc/helpers";

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

  const eventAlerts = ref({});

  const onRowExpand = async (event) => {
    const eventUuid = event.data.uuid;
    eventAlerts.value[eventUuid] = null;
    eventAlerts.value[eventUuid] = await getAlerts(eventUuid);
  };
  const onRowCollapse = (event) => {
    const eventUuid = event.data.uuid;
    delete eventAlerts.value[eventUuid];
  };

  const getAlerts = async (uuid) => {
    const allAlerts = await Alert.readAllPages({
      eventUuid: uuid,
      sort: "event_time|asc",
    });

    return allAlerts.map((x) => parseAlertSummary(x));
  };
</script>
