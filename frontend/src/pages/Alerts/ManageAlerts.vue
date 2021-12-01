<!-- ManageAlerts.vue -->

<template>
  <br />
  <TheAlertActionToolbar id="AlertActionToolbar" />
  <br />
  <TheFilterToolbar id="FilterToolbar" />
  <br />
  <div id="AlertsTable" class="card">
    <TheAlertsTable />
  </div>
</template>

<script>
  import {
    alertFilters,
    EVENT_TIME_AFTER_FILTER,
    EVENT_TIME_BEFORE_FILTER,
    INSERT_TIME_AFTER_FILTER,
    INSERT_TIME_BEFORE_FILTER,
    DISPOSITIONED_AFTER_FILTER,
    DISPOSITIONED_BEFORE_FILTER,
  } from "@/etc/constants";

  import TheAlertActionToolbar from "@/components/Alerts/TheAlertActionToolbar";
  import TheFilterToolbar from "@/components/Filters/TheFilterToolbar";
  import TheAlertsTable from "@/components/Alerts/TheAlertsTable";

  export default {
    components: { TheAlertsTable, TheFilterToolbar, TheAlertActionToolbar },
    provide() {
      return {
        availableFilters: alertFilters,
        filterType: "alerts",
        filterInputType: "Alerts/AlertFilterInput",
        rangeFilterOptions: ["Event Time", "Insert Time", "Dispositioned Time"],
        rangeFilters: {
          "Event Time": {
            start: EVENT_TIME_AFTER_FILTER,
            end: EVENT_TIME_BEFORE_FILTER,
          },
          "Insert Time": {
            start: INSERT_TIME_AFTER_FILTER,
            end: INSERT_TIME_BEFORE_FILTER,
          },
          "Dispositioned Time": {
            start: DISPOSITIONED_AFTER_FILTER,
            end: DISPOSITIONED_BEFORE_FILTER,
          },
        },
      };
    },
  };
</script>
