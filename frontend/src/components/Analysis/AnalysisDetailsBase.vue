<!-- AnalysisDetailsBase.vue -->
<!-- Base/Details component for analysis details -->

<template>
  <div>
    <Card>
      <template #content>
        <div v-if="props.analysis">
          <pre>{{ prettyAnalysisDetails }}</pre>
        </div>
        <div v-else>Analysis is unavailable.</div>
      </template>
    </Card>
  </div>
</template>

<script setup lang="ts">
  import { computed, defineProps, PropType } from "vue";

  import { analysisRead } from "@/models/analysis";
  import Card from "primevue/card";

  const props = defineProps({
    analysis: {
      type: Object as PropType<analysisRead>,
      required: false,
      default: undefined,
    },
  });

  const prettyAnalysisDetails = computed(() => {
    if (props.analysis?.details) {
      return JSON.stringify(props.analysis.details, null, 4);
    }
    return "No analysis details available.";
  });
</script>
