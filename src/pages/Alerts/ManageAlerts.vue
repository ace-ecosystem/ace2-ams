<!-- ManageAlerts.vue -->

<template>
  <br />
  <TheAlertActionToolbar />
  <br />
  <TheFilterToolbar />
  <br />
  <div class="card">
    <TheAlertsTable />
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
