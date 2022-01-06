<!-- ManageAlerts.vue -->

<template>
  <br />
  <TheAlertActionToolbar page="Manage Alerts" />
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

  import { useFilterStore } from "@/stores/filter";

  export default {
    components: { TheAlertsTable, TheFilterToolbar, TheAlertActionToolbar },
    provide() {
      return {
        availableFilters: alertFilters,
        filterType: "alerts",
        rangeFilters: alertRangeFilters,
      };
    },
    created() {
      const filterStore = useFilterStore();

      const params = {};
      console.log(this.$router.currentRoute.value);
      console.log(this.$router.currentRoute.value.query);
    },
  };
</script>
