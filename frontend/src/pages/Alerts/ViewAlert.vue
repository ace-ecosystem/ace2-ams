<!-- ViewAlert.vue -->

<template>
  <TheAlertActionToolbar id="AlertActionToolbar" />
  <Card>
    <template #content>
      <div class="p-tree p-component p-tree-wrapper" style="border: none">
        <AlertTree
          v-if="alertStore.openAlert"
          id="alert-tree"
          :items="alertStore.openAlert.tree"
        />
      </div>
    </template>
  </Card>
</template>

<script setup>
  import { onBeforeMount, onUnmounted, provide } from "vue";
  import Card from "primevue/card";
  import { useRoute } from "vue-router";

  import TheAlertActionToolbar from "@/components/Alerts/TheAlertActionToolbar";
  import AlertTree from "@/components/Alerts/AlertTree";
  import { useAlertStore } from "@/stores/alert";
  import { useSelectedAlertStore } from "@/stores/selectedAlert";

  const route = useRoute();
  const alertStore = useAlertStore();
  const selectedAlertStore = useSelectedAlertStore();

  provide("filterType", "alerts");

  onBeforeMount(async () => {
    await initPage(route.params.alertID);
  });

  onUnmounted(() => {
    selectedAlertStore.unselectAll();
  });

  alertStore.$subscribe(async (_, state) => {
    if (state.requestReload) {
      await alertStore.read(route.params.alertID);
    }
  });

  async function initPage(alertID) {
    selectedAlertStore.unselectAll();
    selectedAlertStore.select(alertID);
    alertStore.$reset();
    await alertStore.read(alertID);
  }
</script>

<style>
  .p-tree-container {
    margin: 0;
    padding: 0;
    list-style-type: none;
    overflow: auto;
  }
  .p-tree-wrapper {
    overflow: auto;
  }
</style>
