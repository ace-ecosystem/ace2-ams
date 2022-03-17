<!-- EventURLDomainSummary.vue -->
<!-- A simple table and chart of all URL domains in an event and their frequency -->

<template>
  <div class="flex justify-content-evenly">
    <div style="width: 33%">
      <Chart type="pie" :data="chartData" data-cy="url-domain-pie-chart" />
    </div>
    <div style="width: 33%">
      <DataTable
        :value="domains"
        :loading="isLoading"
        responsive-layout="scroll"
        data-cy="url-domain-summary-table"
      >
        <Column field="domain" header="Domain" :sortable="true"></Column>
        <Column field="count" header="Count" :sortable="true"></Column>
      </DataTable>
    </div>
  </div>
</template>

<script setup>
  import Chart from "primevue/chart";
  import DataTable from "primevue/datatable";
  import Column from "primevue/column";
  import { defineProps, ref, onMounted } from "vue";
  import { Event } from "@/services/api/event";

  const props = defineProps({
    eventUuid: { type: String, required: true },
  });

  const isLoading = ref(false);
  const domains = ref([]);
  const chartData = ref({
    labels: [],
    datasets: [
      {
        data: [],
        backgroundColor: ["#42A5F5", "#66BB6A", "#FFA726"],
        hoverBackgroundColor: ["#64B5F6", "#81C784", "#FFB74D"],
      },
    ],
  });

  onMounted(async () => {
    isLoading.value = true;
    const urlDomainSummary = await Event.readUrlDomainSummary(props.eventUuid);
    domains.value = urlDomainSummary.domains;
    chartData.value.labels = urlDomainSummary.domains.map(
      (domainSummaryIndividual) => domainSummaryIndividual.domain,
    );
    chartData.value.datasets[0].data = urlDomainSummary.domains.map(
      (domainSummaryIndividual) => domainSummaryIndividual.count,
    );
    isLoading.value = false;
  });
</script>
