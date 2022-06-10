<!-- ViewEvent.vue -->

<template>
  <br />
  <div v-if="eventStore.open">
    <EventDetailsMenuBar
      :event-uuid="route.params.eventID"
      @section-clicked="updateSection"
    ></EventDetailsMenuBar>
    <br />
    <Card data-cy="event-details-card">
      <template #title>
        <div data-cy="event-details-header">
          <span data-cy="event-title">{{ eventStore.open.name }}</span>

          <Button
            data-cy="event-details-link"
            icon="pi pi-link"
            class="p-button-secondary p-button-outlined p-button-sm"
            @click="copyLink"
          />
          <NodeTagVue
            v-for="tag in eventStore.open.tags"
            :key="tag.uuid"
            :tag="tag"
          ></NodeTagVue>
        </div>
      </template>
      <template #content>
        <div data-cy="event-details-content">
          <h3 id="event-section-title">{{ currentSection }}</h3>
          <component
            :is="currentComponent"
            :event-uuid="route.params.eventID"
            :event-alert-uuids="eventStore.open.alertUuids"
          ></component>
        </div>
      </template>
    </Card>
  </div>
</template>

<script setup>
  import {
    inject,
    onBeforeMount,
    onUnmounted,
    provide,
    ref,
    shallowRef,
  } from "vue";
  import { useRoute } from "vue-router";

  import Button from "primevue/button";
  import Card from "primevue/card";

  import AnalysisDetailsBase from "@/components/Analysis/AnalysisDetailsBase.vue";
  import EventDetailsMenuBar from "@/components/Events/TheEventDetailsMenuBar.vue";
  import EventSummary from "@/components/Events/EventSummary.vue";
  import NodeTagVue from "@/components/Node/NodeTag.vue";

  import { useEventStore } from "@/stores/event";
  import { useSelectedEventStore } from "@/stores/selectedEvent";

  import { copyToClipboard } from "@/etc/helpers";

  const route = useRoute();
  const eventStore = useEventStore();
  const selectedEventStore = useSelectedEventStore();

  const config = inject("config");
  const componentMapping = {
    ...config.analysis.analysisModuleComponents,
    ...config.events.defaultEventDetailsSections,
  };

  const currentSection = ref("Event Summary");
  const currentComponent = shallowRef(EventSummary);

  provide("nodeType", "events");
  provide("analysisModuleComponents", config.analysis.analysisModuleComponents);
  provide("availableFilters", config.events.eventFilters);
  provide("availableEditFields", config.events.eventEditableProperties);
  provide("closedEventStatus", config.events.closedEventStatus);

  onBeforeMount(async () => {
    await initPage(route.params.eventID);
  });

  onUnmounted(() => {
    selectedEventStore.unselectAll();
  });

  eventStore.$subscribe(async (_, state) => {
    if (state.requestReload) {
      await reloadPage(route.params.eventID);
    }
  });

  function copyLink() {
    copyToClipboard(window.location);
  }

  function updateSection(section) {
    currentSection.value = section;
    if (section in componentMapping) {
      currentComponent.value = componentMapping[section];
    } else {
      currentComponent.value = AnalysisDetailsBase;
    }
  }

  async function reloadPage() {
    eventStore.$reset();
    await eventStore.read(route.params.eventID);
  }

  async function initPage(eventID) {
    selectedEventStore.unselectAll();
    selectedEventStore.select(eventID);
    eventStore.$reset();
    await eventStore.read(eventID);
  }
</script>

<style>
  .p-tree-container {
    margin: 0;
    padding: 0;
    list-style-type: none;
    overflow: auto;
  }
  .p-tree-wrapper {
    overflow: auto;
  }
</style>
