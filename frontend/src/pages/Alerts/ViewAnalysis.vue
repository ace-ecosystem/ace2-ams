<!-- ViewAnalysis.vue -->

<template>
  <Card id="view-analysis">
    <template #header>
      <Breadcrumb :home="home" :model="items"></Breadcrumb>
    </template>
    <template #content>
      {{ analysisDetails }}
    </template>
  </Card>
</template>

<script setup>
  import { computed, onMounted, ref } from "vue";
  import { useRoute } from "vue-router";
  import Breadcrumb from "primevue/breadcrumb";

  import Card from "primevue/card";
  import { useAlertStore } from "@/stores/alert";
  let alertStore = useAlertStore();

  import { Analysis } from "@/services/api/analysis";

  let analysis = ref();

  onMounted(async () => {
    await initPage(useRoute().params.analysisID, useRoute().params.alertID);
  });

  async function initPage(analysisID, alertID) {
    analysis.value = await Analysis.read(analysisID);
    if (!alertStore.openAlert) {
      await alertStore.read(alertID);
    }
  }

  const alertName = computed(() => {
    if (alertStore.openAlert) {
      return alertStore.openAlert.name;
    }
    return "Unknown Alert";
  });
  const analysisName = computed(() => {
    if (analysis.value) {
      return analysis.value.analysisModuleType.value;
    }
    return "Unknown Analysis";
  });
  const home = { icon: "pi pi-home", to: "/" };
  const items = [
    { label: alertName, to: `/alert/${useRoute().params.alertID}` },
    { label: analysisName },
  ];
  const analysisDetails = computed(() => {
    if (analysis.value) {
      return analysis.value.details;
    }
    return "No details";
  });
</script>
