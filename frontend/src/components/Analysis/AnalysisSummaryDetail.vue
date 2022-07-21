<!-- AnalysisSummaryDetail.vue -->

<template>
  <Panel header="Summary Details" :toggleable="true" :collapsed="false">
    <div v-for="details of summaryDetails" :key="details.uuid">
      <div>
        <Card>
          <template #content>
            <div data-cy="summary-details-content">
              <div v-if="details">
                <Panel :header="details.header">
                  <pre v-if="details.format.value == 'pre'">{{
                    details.content
                  }}</pre>
                  <span v-else>{{ details.content }}</span>
                </Panel>
              </div>
            </div>
          </template>
        </Card>
      </div>
    </div>
  </Panel>
</template>

<script setup lang="ts">
  import { computed, defineProps, PropType } from "vue";
  import { analysisSummaryDetailRead } from "@/models/analysisSummaryDetail";
  import Card from "primevue/card";
  import Panel from "primevue/panel";

  const props = defineProps({
    summaryDetails: {
      type: Array as PropType<analysisSummaryDetailRead[]>,
      required: true,
    },
  });
</script>
