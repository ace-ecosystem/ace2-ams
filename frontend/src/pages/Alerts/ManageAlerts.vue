<!-- ManageAlerts.vue -->

<template>
  <br />
  <div id="AlertActionToolbar">
    <TheAlertActionToolbar reload-object="table" />
  </div>
  <br />
  <div id="FilterToolbar"><TheFilterToolbar /></div>
  <br />
  <div id="AlertsTable" class="card">
    <TheAlertsTable />
  </div>
</template>

<script setup>
  import { onMounted, provide, watch } from "vue";

  import { alertFilters, alertRangeFilters } from "@/etc/constants";

  import TheAlertActionToolbar from "@/components/Alerts/TheAlertActionToolbar";
  import TheFilterToolbar from "@/components/Filters/TheFilterToolbar";
  import TheAlertsTable from "@/components/Alerts/TheAlertsTable";
  import { useRoute, useRouter } from "vue-router";

  import { useFilterStore } from "@/stores/filter";
  import { parseFilters, populateCommonStores } from "@/etc/helpers";

  const route = useRoute();
  const router = useRouter();

  provide("availableFilters", alertFilters);
  provide("nodeType", "alerts");
  provide("rangeFilters", alertRangeFilters);

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
      nodeType: "alerts",
      filters: parseFilters(route.query, alertFilters),
    });
    // Reload page to clear URL params
    router.push("/manage_alerts");
  }
</script>
