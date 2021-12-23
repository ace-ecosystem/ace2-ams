<!-- ManageAlerts.vue -->

<template>
  <br />
  <TheAlertActionToolbar />
  <br />
  <TheFilterToolbar id="FilterToolbar" />
  <br />
  <div id="AlertsTable" class="card">
    <TheAlertsTable />
  </div>
</template>

<script>
  import { alertFilters, alertRangeFilters } from "@/etc/constants";

  import TheAlertActionToolbar from "@/components/Alerts/TheAlertActionToolbar";
  import TheFilterToolbar from "@/components/Filters/TheFilterToolbar";
  import TheAlertsTable from "@/components/Alerts/TheAlertsTable";

  export default {
    components: { TheAlertsTable, TheFilterToolbar, TheAlertActionToolbar },
    provide() {
      return {
        availableFilters: alertFilters,
        filterType: "alerts",
        rangeFilters: alertRangeFilters,
      };
    },
  };
</script>
