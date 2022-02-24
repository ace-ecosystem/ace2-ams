/* eslint-disable vue/attribute-hyphenation */
<!-- TheEventsTable.vue -->
<!-- The table where all currently filtered events are displayed, selected to take action, or link to an individual event page -->

<template>
  <TheNodeTable :key="key" :columns="columns">
    <template #tableHeaderStart
      ><Dropdown
        v-model="currentUserSettingsStore.preferredEventQueue"
        :options="queueStore.items"
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
  import { ref, onMounted, inject } from "vue";

  import Dropdown from "primevue/dropdown";

  import EventAlertsTable from "./EventAlertsTable.vue";
  import TheNodeTable from "@/components/Node/TheNodeTable.vue";
  import EventTableCell from "@/components/Events/EventTableCell.vue";

  import { useCurrentUserSettingsStore } from "@/stores/currentUserSettings";
  import { useFilterStore } from "@/stores/filter";
  import { useQueueStore } from "@/stores/queue";
  const queueStore = useQueueStore();
  const currentUserSettingsStore = useCurrentUserSettingsStore();
  const filterStore = useFilterStore();

  const config = inject("config");

  const columns = ref([]);
  const preferredEventQueue = ref(currentUserSettingsStore.preferredEventQueue);

  // This will cause the table to re-render,
  // which is necessary to dynamically re-set columns
  const key = ref(0);

  onMounted(() => {
    setColumns();
  });

  const setColumns = () => {
    if (preferredEventQueue.value) {
      columns.value =
        config.events.eventQueueColumnMappings[preferredEventQueue.value.value];

      filterStore.setFilter({
        nodeType: "events",
        filterName: "queue",
        filterValue: preferredEventQueue.value,
      });

      key.value += 1;
    }
  };

  currentUserSettingsStore.$subscribe((_, state) => {
    if (state.preferredEventQueue != preferredEventQueue.value) {
      preferredEventQueue.value = state.preferredEventQueue;
      setColumns();
    }
  });
</script>
