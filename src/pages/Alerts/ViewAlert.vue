<!-- ViewAlert.vue -->

<template>
  <pre>{{ prettyAlert }}</pre>
</template>

<script>
  import { mapGetters } from "vuex";

  export default {
    computed: {
      ...mapGetters({
        openAlert: "alerts/openAlert",
      }),
      prettyAlert() {
        return JSON.stringify(this.openAlert, null, 2);
      },
    },
    async created() {
      this.$store.dispatch(
        "selectedAlerts/unselectAll",
        this.$route.params.alertID,
      );
      this.$store.dispatch("selectedAlerts/select", this.$route.params.alertID);
      await this.$store.dispatch(
        "alerts/openAlert",
        this.$route.params.alertID,
      );
    },
  };
</script>
