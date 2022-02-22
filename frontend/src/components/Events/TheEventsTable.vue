/* eslint-disable vue/attribute-hyphenation */
<!-- TheEventsTable.vue -->
<!-- The table where all currently filtered events are displayed, selected to take action, or link to an individual event page -->

<template>
  <TheNodeTable :key="key" :columns="columns">
    <template #tableHeaderStart
      ><Dropdown
        v-model="currentUserSettingsStore.preferredEventQueue"
        :options="eventQueueStore.items"
        option-label="value"
        style="margin-right: 2%"
      ></Dropdown
    ></template>

    <template #rowCell="{ data, field }">
      <EventTableCell :data="data" :field="field"></EventTableCell>
    </template>

    <!-- Row Expansion -->
    <template #rowExpansion="{ data }">
      <EventAlertsTable :event-uuid="data.uuid"></EventAlertsTable>
    </template>
  </TheNodeTable>
</template>

<script setup>
  import { ref, onMounted } from "vue";

  import Dropdown from "primevue/dropdown";

  import TheNodeTable from "../Node/TheNodeTable";
  import EventTableCell from "./EventTableCell";
  import EventAlertsTable from "./EventAlertsTable.vue";

  import { useEventQueueStore } from "@/stores/eventQueue";
  import { useCurrentUserSettingsStore } from "@/stores/currentUserSettings";
  import { useFilterStore } from "@/stores/filter";
  const eventQueueStore = useEventQueueStore();
  const currentUserSettingsStore = useCurrentUserSettingsStore();
  const filterStore = useFilterStore();

  import { eventQueueColumnMappings } from "@/etc/constants/events";

  const columnMappings = ref(eventQueueColumnMappings);
  const columns = ref([]);
  const key = ref(0);

  onMounted(() => {
    setColumns();
  });

  const setColumns = () => {
    if (currentUserSettingsStore.preferredEventQueue) {
      columns.value =
        columnMappings.value[
          currentUserSettingsStore.preferredEventQueue.value
        ];

      filterStore.setFilter({
        nodeType: "events",
        filterName: "queue",
        filterValue: currentUserSettingsStore.preferredEventQueue,
      });

      key.value += 1;
    }
  };

  currentUserSettingsStore.$subscribe((mutation) => {
    if (mutation.events.key === "preferredEventQueue") {
      setColumns();
    }
  });
</script>
