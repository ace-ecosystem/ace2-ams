<!-- ViewAnalysis.vue -->

<template>
  <Card>
    <template #header> {{ alertName }}: {{ analysisName }} </template>
    <template #content>
      {{ analysisDetails }}
    </template>
  </Card>
</template>

<script setup>
  import {
    computed,
    onMounted,
    onBeforeMount,
    onUnmounted,
    provide,
    ref,
  } from "vue";
  import { useRoute } from "vue-router";
  import Card from "primevue/card";
  import { useAlertStore } from "@/stores/alert";
  const alertStore = useAlertStore();

  import { Analysis } from "@/services/api/analysis";

  let analysis = ref();

  onMounted(async () => {
    analysis.value = await Analysis.read(useRoute().params.analysisID);
  });

  const alertName = computed(() => {
    if (alertStore.openAlert) {
      return alertStore.openAlert.alert.name;
    }
    return "Unknown Alert";
  });
  const analysisName = computed(() => {
    if (analysis.value) {
      return analysis.value.analysisModuleType.value;
    }
    return "Unknown Analysis";
  });
  const analysisDetails = computed(() => {
    if (analysis.value) {
      return analysis.value.details;
    }
    return "No details";
  });
</script>
