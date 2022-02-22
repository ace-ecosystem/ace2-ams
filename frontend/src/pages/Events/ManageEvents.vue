<!-- ManageEvents.vue -->

<template>
  <br />
  <div id="EventActionToolbar">
    <TheNodeActionToolbarVue reload-object="table" />
  </div>
  <br />
  <div id="FilterToolbar"><TheFilterToolbar /></div>
  <br />
  <div id="EventsTable" class="card">
    <TheEventsTable />
  </div>
</template>

<script setup>
  import { onMounted, provide, watch } from "vue";

  import {
    eventEditableProperties,
    eventFilters,
    eventRangeFilters,
  } from "@/etc/constants/events";

  import TheNodeActionToolbarVue from "@/components/Node/TheNodeActionToolbar.vue";
  import TheFilterToolbar from "@/components/Filters/TheFilterToolbar";
  import TheEventsTable from "@/components/Events/TheEventsTable";
  import { useRoute, useRouter } from "vue-router";

  import { useFilterStore } from "@/stores/filter";
  import { useCurrentUserSettingsStore } from "@/stores/currentUserSettings";
  import { parseFilters, populateCommonStores } from "@/etc/helpers";
  import { useAuthStore } from "@/stores/auth";

  const route = useRoute();
  const router = useRouter();

  provide("availableFilters", eventFilters);
  provide("availableEditFields", eventEditableProperties);
  provide("nodeType", "events");
  provide("rangeFilters", eventRangeFilters);

  const authStore = useAuthStore();
  const filterStore = useFilterStore();
  const currentUserSettingsStore = useCurrentUserSettingsStore();

  onMounted(async () => {
    if (Object.keys(route.query).length) {
      // Will need to load common stores in order to find filter values
      await populateCommonStores();
      loadRouteQuery();
    }
    if (
      currentUserSettingsStore.preferredEventQueue !=
      authStore.user.defaultEventQueue
    ) {
      currentUserSettingsStore.preferredEventQueue =
        authStore.user.defaultEventQueue;
    }
  });

  watch(route, () => {
    if (Object.keys(route.query).length) {
      loadRouteQuery();
    }
  });

  function loadRouteQuery() {
    // load filters given in route
    filterStore.bulkSetFilters({
      nodeType: "events",
      filters: parseFilters(route.query, eventFilters),
    });
    // Reload page to clear URL params
    router.push("/manage_events");
  }
</script>
