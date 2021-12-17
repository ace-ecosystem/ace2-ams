<!-- ViewAlert.vue -->

<template>
  <AlertTree v-if="alertStore.openAlert" :items="alertStore.openAlert.tree" />
</template>

<script setup>
  import { onMounted, onUnmounted } from "vue";
  import { useRoute } from "vue-router";

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
</script>
