<!-- EventDetectionSummary.vue -->
<!-- A simple table of all the detections in an event, their frequency, and a given alert to which they belong -->

<template>
  <div>
    <Message v-if="error" severity="error" data-cy="error-banner">{{
      error
    }}</Message>
    <DataTable
      :value="detections"
      :loading="isLoading"
      responsive-layout="scroll"
      data-cy="detection-summary-table"
    >
      <Column field="value" header="Detection">
        <template #body="slotProps">
          <div class="flex align-content-evenly">
            <span
              class="flex align-items-left justify-content-center"
              data-cy="detection-value"
              >{{ slotProps.data.value }}</span
            >
            <span
              class="flex align-items-left justify-content-center"
              style="width: 10%"
              ><a
                :href="`/alert/${slotProps.data.alertUuid}`"
                style="text-decoration: none"
                ><Button
                  icon="pi pi-external-link"
                  class="p-button-rounded p-button-text"
                  data-cy="detection-point-alert-link"
              /></a>
            </span>
          </div> </template
      ></Column>
      <Column
        field="count"
        header="Count"
        :sortable="true"
        style="width: 20%"
      ></Column>
      <template #empty>No detection points found.</template>
    </DataTable>
  </div>
</template>

<script setup lang="ts">
  import { defineProps, ref, onMounted } from "vue";

  import Button from "primevue/button";
  import Column from "primevue/column";
  import DataTable from "primevue/datatable";
  import Message from "primevue/message";

  import { Event } from "@/services/api/event";
  import { detectionPointSummary } from "@/models/eventSummaries";

  const props = defineProps({
    eventUuid: { type: String, required: true },
  });

  const isLoading = ref(false);
  const detections = ref<detectionPointSummary[]>([]);
  const error = ref<string>();

  onMounted(async () => {
    isLoading.value = true;
    try {
      detections.value = await Event.readDetectionSummary(props.eventUuid);
    } catch (e: unknown) {
      detections.value = [];
      if (typeof e === "string") {
        error.value = e;
      } else if (e instanceof Error) {
        error.value = e.message;
      }
    }
    isLoading.value = false;
  });
</script>
