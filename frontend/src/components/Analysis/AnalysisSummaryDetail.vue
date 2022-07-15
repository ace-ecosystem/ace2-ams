<!-- AnalysisSummaryDetail.vue -->

<template>
  <div>
  <h1> {{summary}} </h1>
    <Card>
      <template #content>
      <div v-if="props.summary">
          <pre v-if="summary.format.value == 'pre'">{{summary.content}}</pre>
          <span v-else>{{summary.content}}</span>
        </div>
        </template>
    </Card>
  </div>
</template>

<script setup lang="ts">
    import { computed, defineProps, PropType } from "vue";
    import { analysisSummaryDetailRead } from "@/models/analysisSummaryDetail";
    import Card from "primevue/card";

    const props = defineProps({
    summary: {
      type: Object as PropType<analysisSummaryDetailRead>,
      required: true,
    },
  });

</script>