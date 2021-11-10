<!-- ManageAlerts.vue -->

<template>
  <br />
  <TheAlertActionToolbar id="AlertActionToolbar" />
  <br />
  <TheFilterToolbar id="FilterToolbar" />
  <br />
  <div id="AlertsTable" class="card">
    <TheAlertsTable id="AlertsTable" />
  </div>
</template>

<script>
  import TheAlertActionToolbar from "@/components/Alerts/TheAlertActionToolbar";
  import TheFilterToolbar from "@/components/Filters/TheFilterToolbar";
  import TheAlertsTable from "@/components/Alerts/TheAlertsTable";

  export default {
    components: { TheAlertsTable, TheFilterToolbar, TheAlertActionToolbar },
  };
</script>
