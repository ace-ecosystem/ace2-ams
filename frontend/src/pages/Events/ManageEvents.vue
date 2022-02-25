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
  import { onMounted, provide, inject, watch } from "vue";

  import TheNodeActionToolbarVue from "@/components/Node/TheNodeActionToolbar.vue";
  import TheFilterToolbar from "@/components/Filters/TheFilterToolbar.vue";
  import TheEventsTable from "@/components/Events/TheEventsTable.vue";
  import { useRoute, useRouter } from "vue-router";

  import { useFilterStore } from "@/stores/filter";
  import { parseFilters, populateCommonStores } from "@/etc/helpers";

  const route = useRoute();
  const router = useRouter();

  const config = inject("config");

  provide("availableFilters", config.events.eventFilters);
  provide("availableEditFields", config.events.eventEditableProperties);
  provide("rangeFilters", config.events.eventRangeFilters);
  provide("nodeType", "events");

  const filterStore = useFilterStore();

  onMounted(async () => {
    if (Object.keys(route.query).length) {
      // Will need to load common stores in order to find filter values
      await populateCommonStores();
      loadRouteQuery();
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
      filters: parseFilters(route.query, config.events.eventFilters),
    });
    // Reload page to clear URL params
    router.push("/manage_events");
  }
</script>
