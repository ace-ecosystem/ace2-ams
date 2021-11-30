<!-- ViewAlert.vue -->

<template>
  <AlertTree :items="alertTree" />
</template>

<script>
  import { mapGetters } from "vuex";
  import { arrayToTree } from "performant-array-to-tree";

  import AlertTree from "@/components/Alerts/AlertTree";

  export default {
    components: { AlertTree },

    computed: {
      ...mapGetters({
        openAlert: "alerts/openAlert",
      }),

      alertTree() {
        // Join the analyses and observableInstances arrays into a single array
        const items = this.openAlert.analyses.concat(
          this.openAlert.observableInstances,
        );

        // Turn the flat array into a nested tree structure
        const tree = arrayToTree(items, {
          id: "uuid",
          parentId: "parentUuid",
          dataField: null,
        });

        return tree;
      },
    },

    async created() {
      this.$store.dispatch(
        "selectedAlerts/unselectAll",
        this.$route.params.alertID,
      );
      this.$store.dispatch("selectedAlerts/select", this.$route.params.alertID);
      await this.$store.dispatch(
        "alerts/getSingle",
        this.$route.params.alertID,
      );
    },
  };
</script>
