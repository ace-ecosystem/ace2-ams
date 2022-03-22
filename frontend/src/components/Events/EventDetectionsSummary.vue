<!-- EventDetectionSummary.vue -->
<!-- A simple table of all the detections in an event, their frequency, and a given alert to which they belong -->

<template>
  <div>
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
              class="flex align-items-center justify-content-center"
              data-cy="detection-value"
              style="width: 4em"
              >{{ slotProps.data.value }}</span
            >
            <span class="flex align-items-center justify-content-center"
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

<script setup>
  import Button from "primevue/button";
  import DataTable from "primevue/datatable";
  import Column from "primevue/column";
  import { defineProps, ref, onMounted } from "vue";
  import { Event } from "@/services/api/event";

  const props = defineProps({
    eventUuid: { type: String, required: true },
  });

  const isLoading = ref(false);
  const detections = ref([]);

  onMounted(async () => {
    isLoading.value = true;
    detections.value = await Event.readDetectionSummary(props.eventUuid);
    isLoading.value = false;
  });
</script>
