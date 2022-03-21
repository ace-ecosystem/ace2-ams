<!-- EmailAnalysis.vue -->

<template>
  <EmailAnalysisSummaryTable
    :event-uuid="eventUuid"
  ></EmailAnalysisSummaryTable>
  <br />
  <EmailAnalysisHeadersBody :event-uuid="eventUuid"></EmailAnalysisHeadersBody>
</template>

<script setup>
  import EmailAnalysisSummaryTable from "@/components/Analysis/EmailAnalysisSummaryTable.vue";
  import EmailAnalysisHeadersBody from "@/components/Analysis/EmailAnalysisHeadersBody.vue";

  import { defineProps } from "vue";

  defineProps({
    eventUuid: { type: String, required: true },
  });
</script>
