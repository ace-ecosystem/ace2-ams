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
        // Turn the flat array into a nested tree structure
        const tree = arrayToTree(this.openAlert.tree, {
          id: "treeUuid",
          parentId: "parentTreeUuid",
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
