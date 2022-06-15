<!-- AlertUrlDomainSummary.vue -->
<!-- A simple table and chart of all URL domains in an alert and their frequency -->

<template>
  <Message v-if="error" severity="error" data-cy="error-banner">{{
    error
  }}</Message>
  <Panel
    v-if="domains.length"
    data-cy="alert-url-domain-summary"
    header="URL Domain Summary"
    :toggleable="true"
    :collapsed="true"
  >
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
          <Column field="domain" header="Domain" :sortable="true"></Column>
          <Column field="count" header="Count" :sortable="true"></Column>
        </DataTable>
      </div>
    </div>
  </Panel>
</template>

<script setup lang="ts">
  import Panel from "primevue/panel";
  import Chart from "primevue/chart";
  import DataTable from "primevue/datatable";
  import Column from "primevue/column";
  import Message from "primevue/message";

  import { defineProps, ref, onMounted } from "vue";
  import { Alert } from "@/services/api/alert";
  import { urlDomainSummaryIndividual } from "@/models/summaries";

  const props = defineProps({
    alertUuid: { type: String, required: true },
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
      urlDomainSummary = await Alert.readUrlDomainSummary(props.alertUuid);
    } catch (e: unknown) {
      if (typeof e === "string") {
        error.value = `URL Domain Summary: ${e}`;
      } else if (e instanceof Error) {
        error.value = `URL Domain Summary: ${e.message}`;
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
