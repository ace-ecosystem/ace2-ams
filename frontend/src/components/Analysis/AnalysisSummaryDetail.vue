<!-- AnalysisSummaryDetail.vue -->

<template>
  <div>
    <Card>
      <div v-if="props.summary">
          <pre v-if="summary.format == 'pre'">{{summary.content}}</pre>
          <span v-else>{{summary.content}}</span>
        </div>
        <div v-else>Summary Detail is unavailable.</div>
    </Card>
  </div>
</template>

<script setup lang="ts">
    import { computed, defineProps, PropType } from "vue";
    import import { analysisRead } from "@/models/analysisSummaryDetail";
    import Card from "primevue/card";

    const props = defineProps({
    summary: {
      type: Object as PropType<analysisSummaryDetailRead>,
      required: true,
    },
  });

  
  
</script>