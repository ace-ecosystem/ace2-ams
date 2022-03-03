<!-- ViewAlert.vue -->

<template>
  <TheAlertActionToolbar reload-object="node" />
  <div v-if="alertStore.open">
    <TheAlertDetails />
    <br />
    <Card>
      <template #content>
        <div class="p-tree p-component p-tree-wrapper" style="border: none">
          <AlertTree id="alert-tree" :items="alertStore.open.children" />
        </div>
      </template>
    </Card>
  </div>
</template>

<script setup>
  import { onBeforeMount, onUnmounted, provide } from "vue";
  import Card from "primevue/card";
  import { useRoute } from "vue-router";

  import TheAlertActionToolbar from "@/components/Alerts/TheAlertActionToolbar.vue";
  import AlertTree from "@/components/Alerts/AlertTree.vue";
  import TheAlertDetails from "@/components/Alerts/TheAlertDetails.vue";
  import { useAlertStore } from "@/stores/alert";
  import { useSelectedAlertStore } from "@/stores/selectedAlert";

  const route = useRoute();
  const alertStore = useAlertStore();
  const selectedAlertStore = useSelectedAlertStore();

  provide("nodeType", "alerts");

  onBeforeMount(async () => {
    await initPage(route.params.alertID);
  });

  onUnmounted(() => {
    selectedAlertStore.unselectAll();
  });

  alertStore.$subscribe(async (_, state) => {
    if (state.requestReload) {
      await reloadPage(route.params.alertID);
    }
  });

  async function reloadPage() {
    alertStore.$reset();
    await alertStore.read(route.params.alertID);
  }

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
