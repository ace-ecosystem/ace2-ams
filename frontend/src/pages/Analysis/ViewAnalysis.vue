<!-- ViewAnalysis.vue -->

<template>
  <Card id="view-analysis">
    <template #header>
      <Breadcrumb :home="home" :model="items"></Breadcrumb>
    </template>
    <template #content>
      <component
        :is="currentComponent"
        :analysis-uuid="route.params.analysisID"
        :analysis="analysis"
      ></component>
    </template>
  </Card>
</template>

<script setup>
  import AnalysisDetailsBase from "@/components/Analysis/AnalysisDetailsBase.vue";

  import { computed, onMounted, ref, inject, watch, shallowRef } from "vue";
  import { useRoute } from "vue-router";
  import Breadcrumb from "primevue/breadcrumb";

  import Card from "primevue/card";
  import { useAlertStore } from "@/stores/alert";
  import { Analysis } from "@/services/api/analysis";

  let alertStore = useAlertStore();

  let analysis = ref();

  const config = inject("config");
  const componentMapping = {
    ...config.analysis.analysisModuleComponents,
  };

  const currentComponent = shallowRef(AnalysisDetailsBase);

  const route = useRoute();

  onMounted(async () => {
    await initPage(route.params.analysisID, route.params.alertID);
  });

  async function initPage(analysisID, alertID) {
    try {
      analysis.value = await Analysis.read(analysisID);
    } catch {
      console.warn("Could not fetch analysis");
    }
    if (!alertStore.open) {
      try {
        await alertStore.read(alertID);
      } catch {
        console.warn("Could not fetch alert");
      }
    }
  }

  watch(analysis, () => {
    if (analysis.value?.analysisModuleType?.value in componentMapping) {
      currentComponent.value =
        componentMapping[analysis.value.analysisModuleType.value];
    } else {
      currentComponent.value = AnalysisDetailsBase;
    }
  });

  const alertName = computed(() => {
    if (alertStore.open) {
      return alertStore.open.name;
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
</script>
