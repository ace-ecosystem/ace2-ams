<!-- ViewAlert.vue -->

<template>
  <AlertTree v-if="alertStore.openAlert" :items="alertTree" />
</template>

<script setup>
  import { computed, onMounted, onUnmounted } from "vue";
  import { useRoute } from "vue-router";
  import { arrayToTree } from "performant-array-to-tree";

  import AlertTree from "@/components/Alerts/AlertTree";
  import { useAlertStore } from "@/stores/alert";
  import { useSelectedAlertStore } from "@/stores/selectedAlert";

  const alertStore = useAlertStore();
  const selectedAlertStore = useSelectedAlertStore();

  onMounted(async () => {
    selectedAlertStore.unselectAll();
    selectedAlertStore.select(useRoute().params.alertID);

    alertStore.$reset();
    await alertStore.read(useRoute().params.alertID);
  });

  onUnmounted(() => {
    selectedAlertStore.unselectAll();
  });

  const alertTree = computed(() =>
    arrayToTree(alertStore.openAlert.tree, {
      id: "treeUuid",
      parentId: "parentTreeUuid",
      dataField: null,
    }),
  );
</script>
