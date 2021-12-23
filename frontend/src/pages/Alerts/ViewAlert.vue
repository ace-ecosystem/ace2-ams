<!-- ViewAlert.vue -->

<template>
  <Card>
    <template #content>
      <div class="p-tree p-component p-tree-wrapper" style="border: none">
        <AlertTree
          v-if="alertStore.openAlert"
          :items="alertStore.openAlert.children"
          id="alert-tree"
        />
      </div>
    </template>
  </Card>
</template>

<script setup>
  import { onBeforeMount, onUnmounted, provide } from "vue";
  import Card from "primevue/card";
  import { useRoute } from "vue-router";

  import AlertTree from "@/components/Alerts/AlertTree";
  import { useAlertStore } from "@/stores/alert";
  import { useSelectedAlertStore } from "@/stores/selectedAlert";

  const alertStore = useAlertStore();
  const selectedAlertStore = useSelectedAlertStore();

  provide("filterType", "alerts");

  onBeforeMount(async () => {
    await initPage(useRoute().params.alertID);
  });

  onUnmounted(() => {
    selectedAlertStore.unselectAll();
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
