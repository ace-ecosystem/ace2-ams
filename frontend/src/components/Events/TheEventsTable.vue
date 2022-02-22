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
  import { ref, onMounted, computed } from "vue";

  import Dropdown from "primevue/dropdown";

  import EventAlertsTable from "./EventAlertsTable.vue";
  import TheNodeTable from "@/components/Node/TheNodeTable.vue";
  import EventTableCell from "@/components/Events/EventTableCell.vue";

  import { useEventQueueStore } from "@/stores/eventQueue";
  import { useCurrentUserSettingsStore } from "@/stores/currentUserSettings";
  import { useFilterStore } from "@/stores/filter";
  const eventQueueStore = useEventQueueStore();
  const currentUserSettingsStore = useCurrentUserSettingsStore();
  const filterStore = useFilterStore();

  import { eventQueueColumnMappings } from "@/etc/constants/events";

  const columns = ref([]);

  // This will cause the table to re-render,
  // which is necessary to dynamically re-set columns
  const key = ref(0);

  onMounted(() => {
    setColumns();
  });

  const setColumns = () => {
    if (currentUserSettingsStore.preferredEventQueue) {
      columns.value =
        eventQueueColumnMappings[
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
