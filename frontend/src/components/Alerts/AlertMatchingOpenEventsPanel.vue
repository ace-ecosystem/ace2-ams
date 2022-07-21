<template>
  <Panel
    v-if="openEvents.length"
    data-cy="matching-open-events-panel"
    :header="panelHeader"
    :toggleable="true"
    :collapsed="true"
  >
    <DataTable
      data-cy="matching-open-events-table"
      :value="openEvents"
      responsive-layout="scroll"
    >
      <Column field="event.name" header="Event">
        <template #body="slotProps">
          <router-link :to="getEventLink(slotProps.data.event.uuid)">
            <span class="link-text">{{
              slotProps.data.event.name
            }}</span></router-link
          >
        </template>
      </Column>
      <Column field="percent" header="Match">
        <template #body="slotProps">
          {{ slotProps.data.percent }}% ({{ slotProps.data.count }})
        </template>
      </Column>
      <Column field="event.threats" header="Threat Names">
        <template #body="slotProps">
          <span v-if="!slotProps.data.event.threats.length">No threats</span>
          <span
            v-for="threat in slotProps.data.event.threats"
            :key="threat.uuid"
          >
            <Tag rounded>{{ threat.value }}</Tag>
          </span>
        </template>
      </Column>
      <Column field="event.allTags" header="Tags">
        <template #body="slotProps">
          <span v-if="!slotProps.data.event.allTags.length">No tags</span>
          <span v-for="tag in slotProps.data.event.allTags" :key="tag.uuid">
            <Tag rounded>{{ tag.value }}</Tag>
          </span>
        </template></Column
      >
    </DataTable>
  </Panel>
</template>

<script setup lang="ts">
  import { computed } from "vue";

  import Panel from "primevue/panel";
  import DataTable from "primevue/datatable";
  import Column from "primevue/column";
  import Tag from "primevue/tag";

  import { useAlertStore } from "@/stores/alert";

  const alertStore = useAlertStore();

  const openEvents = computed(() => {
    if (!alertStore.open) {
      return [];
    }

    const openEvents = alertStore.open.matchingEvents.find(
      (x) => x.status == "OPEN",
    );
    if (openEvents) {
      return openEvents.events;
    }
    return [];
  });

  const panelHeader = computed(() => {
    if (!openEvents.value.length) {
      return "";
    }

    return `Matching Open Events: ${openEvents.value.length} Event(s) | ${openEvents.value[0].count}/${alertStore.open.numberOfObservables} matching observables | ${openEvents.value[0].event.name}`;
  });

  const getEventLink = (uuid: string) => {
    return "/event/" + uuid;
  };
</script>

<style scoped>
  .link-text:hover {
    cursor: pointer;
    text-decoration: underline;
    font-weight: bold;
  }
</style>
