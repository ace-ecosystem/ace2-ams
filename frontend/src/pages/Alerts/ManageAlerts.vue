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
  import { onMounted, provide, inject, watch } from "vue";

  import TheAlertActionToolbar from "@/components/Alerts/TheAlertActionToolbar.vue";
  import TheFilterToolbar from "@/components/Filters/TheFilterToolbar.vue";
  import TheAlertsTable from "@/components/Alerts/TheAlertsTable.vue";
  import { useRoute, useRouter } from "vue-router";

  import { useFilterStore } from "@/stores/filter";
  import { useAlertTableStore } from "@/stores/alertTable";
  import { parseFilters } from "@/etc/helpers";
  import { populateCommonStores } from "@/stores/helpers";
  import { validAlertFilters } from "@/etc/constants/alerts";

  const route = useRoute();
  const router = useRouter();
  const config = inject("config");

  provide("availableFilters", config.alerts.alertFilters);
  provide("availableEditFields", {});
  provide("nodeType", "alerts");
  provide("rangeFilters", config.alerts.alertRangeFilters);

  const filterStore = useFilterStore();
  const alertTableStore = useAlertTableStore();

  onMounted(async () => {
    if (Object.keys(route.query).length) {
      // Will need to load common stores in order to find filter values
      await populateCommonStores();
      loadRouteQuery();
    }
    alertTableStore.routeFiltersLoaded = true;
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
      filters: parseFilters(route.query, validAlertFilters),
    });
    // Reload page to clear URL params
    router.push("/manage_alerts");
  }
</script>
