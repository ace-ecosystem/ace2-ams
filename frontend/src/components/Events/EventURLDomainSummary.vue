<!-- EventURLDomainSummary.vue -->
<!-- A simple table and chart of all URL domains in an event and their frequency -->

<template>
  <Message v-if="error" severity="error" data-cy="error-banner">{{
    error
  }}</Message>
  <div class="flex justify-content-evenly">
    <div v-if="domains.length" style="width: 33%">
      <Chart type="pie" :data="chartData" data-cy="url-domain-pie-chart" />
    </div>
    <div style="width: 33%">
      <DataTable
        :value="domains"
        :loading="isLoading"
        responsive-layout="scroll"
        data-cy="url-domain-summary-table"
      >
        <template #empty> URL Domain Summary results empty. </template>
        <Column field="domain" header="Domain" :sortable="true"></Column>
        <Column field="count" header="Count" :sortable="true"></Column>
      </DataTable>
    </div>
  </div>
</template>

<script setup lang="ts">
  import Chart from "primevue/chart";
  import DataTable from "primevue/datatable";
  import Column from "primevue/column";
  import Message from "primevue/message";

  import { defineProps, ref, onMounted } from "vue";
  import { Event } from "@/services/api/event";
  import { urlDomainSummaryIndividual } from "@/models/summaries";

  const props = defineProps({
    eventUuid: { type: String, required: true },
  });

  const error = ref<string>();
  const isLoading = ref(false);
  const domains = ref<urlDomainSummaryIndividual[]>([]);
  const chartData = ref({
    labels: [] as string[],
    datasets: [
      {
        data: [],
        backgroundColor: ["#42A5F5", "#66BB6A", "#FFA726"],
        hoverBackgroundColor: ["#64B5F6", "#81C784", "#FFB74D"],
      },
    ] as any[],
  });

  onMounted(async () => {
    isLoading.value = true;

    let urlDomainSummary;

    try {
      urlDomainSummary = await Event.readUrlDomainSummary(props.eventUuid);
    } catch (e: unknown) {
      if (typeof e === "string") {
        error.value = e;
      } else if (e instanceof Error) {
        error.value = e.message;
      }
    }

    isLoading.value = false;

    if (!urlDomainSummary) {
      return;
    }

    domains.value = urlDomainSummary.domains;
    chartData.value.labels = urlDomainSummary.domains.map(
      (domainSummaryIndividual) => domainSummaryIndividual.domain,
    );
    chartData.value.datasets[0].data = urlDomainSummary.domains.map(
      (domainSummaryIndividual) => domainSummaryIndividual.count,
    );
  });
</script>
