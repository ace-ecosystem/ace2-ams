<!-- AlertURLDomainSummary.vue -->
<!-- A simple table and chart of all URL domains in an alert and their frequency -->

<template>
  <Panel
    v-if="domainCounts.length"
    v-model:collapsed="isCollapsed"
    data-cy="url-domain-summary-panel"
  >
    <template #header>
      <span style="cursor: pointer" @click="isCollapsed = !isCollapsed"
        >URL Domain Summary <i :class="headerIcon"></i
      ></span>
    </template>
    <div class="flex">
      <div style="width: 33%">
        <DataTable
          :value="domainCounts"
          responsive-layout="scroll"
          data-cy="url-domain-summary-table"
        >
          <Column field="domain" header="Domain" :sortable="true"></Column>
          <Column field="count" header="Count" :sortable="true"></Column>
          <Column field="percent" header="Percent" :sortable="true"></Column>
        </DataTable>
      </div>
    </div>
  </Panel>
</template>

<script setup lang="ts">
  import DataTable from "primevue/datatable";
  import Column from "primevue/column";
  import Panel from "primevue/panel";

  import { ref, computed } from "vue";
  import { useAlertStore } from "@/stores/alert";

  const alertStore = useAlertStore();
  const isCollapsed = ref(true);

  const headerIcon = computed(() => {
    return isCollapsed.value ? "pi pi-chevron-down" : "pi pi-chevron-up";
  });

  const domainCounts = computed(() => {
    const total = alertStore.openObservables.length;
    const domains = {};
    const domainsCounts = [];

    alertStore.openObservables.forEach((obs) => {
      if (obs.type.value == "fqdn") {
        if (obs.value in domains) {
          domains[obs.value] += 1;
        } else {
          domains[obs.value] = 1;
        }
      }
    });

    for (const [key, value] of Object.entries(domains)) {
      const percent = (value / total) * 100;
      domainsCounts.push({
        domain: key,
        count: value,
        percent: `${percent.toFixed(2)}%`,
      });
    }
    return domainsCounts;
  });
</script>
