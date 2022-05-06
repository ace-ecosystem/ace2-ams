<!-- EventAlertsTable.vue -->
<!-- Contains logic and functionality for displaying a table of alerts inside of an event -->

<template>
  <Message v-if="error" severity="error">{{ error }}</Message>
  <div v-if="isLoading" id="loading-message">
    Loading alerts, please hold...
  </div>
  <div v-else>
    <DataTable
      :value="visibleAlerts"
      :selection="selectedRows"
      responsive-layout="scroll"
      data-cy="event-alerts-table"
      @row-select="selectedAlertStore.select($event.data.uuid)"
      @row-unselect="selectedAlertStore.unselect($event.data.uuid)"
      @row-select-all="selectedAlertStore.selectAll(visibleAlertUuids)"
      @row-unselect-all="selectedAlertStore.unselectAll()"
    >
      <!-- TABLE TOOLBAR-->
      <template #header>
        <Toolbar style="border: none">
          <template #start>
            <!-- CLEAR TABLE FILTERS -->
            <Button
              data-cy="remove-alerts-button"
              icon="pi pi-times-circle"
              class="p-button-rounded p-m-1"
              label="Remove Alerts"
              @click="removeAlerts()"
            />
          </template>
        </Toolbar>
      </template>

      <!-- CHECKBOX COLUMN -->
      <Column
        id="alert-select"
        header-style="width: 3em"
        selection-mode="multiple"
      />

      <!-- DATA COLUMNS -->
      <Column
        v-for="col of columns"
        :key="col.field"
        :field="col.field"
        :header="col.header"
        :sortable="true"
        ><template #body="{ data, field }">
          <AlertTableCell
            :data="data"
            :field="(field as unknown as alertSummaryKeys)"
          ></AlertTableCell> </template
      ></Column>
      <template #empty>
        No alerts for this event were found. {{ error }}
      </template>
    </DataTable>

    <Paginator
      data-cy="event-alert-table-pagination-options"
      :rows="10"
      :rows-per-page-options="[5, 10, 50, 100]"
      :total-records="alerts.length"
      template="CurrentPageReport FirstPageLink PrevPageLink PageLinks NextPageLink LastPageLink RowsPerPageDropdown"
      current-page-report-template="Showing {first} to {last} of {totalRecords} alerts in the event"
      @page="
        onPage($event);
        selectedAlertStore.unselectAll();
      "
    ></Paginator>
  </div>
</template>

<script setup lang="ts">
  import { computed, defineProps, onBeforeMount, onUnmounted, ref } from "vue";

  import Message from "primevue/message";
  import Button from "primevue/button";
  import Column from "primevue/column";
  import DataTable from "primevue/datatable";
  import Paginator from "primevue/paginator";
  import Toolbar from "primevue/toolbar";

  import AlertTableCell from "@/components/Alerts/AlertTableCell.vue";

  import { Alert } from "@/services/api/alert";
  import { alertSummary } from "@/models/alert";
  import { useSelectedAlertStore } from "@/stores/selectedAlert";
  import { parseAlertSummary } from "@/etc/helpers";

  type alertSummaryKeys = keyof alertSummary;

  onBeforeMount(async () => {
    await initTable();
  });

  onUnmounted(() => {
    selectedAlertStore.unselectAll();
  });

  const props = defineProps({
    eventUuid: { type: String, required: true },
  });

  const selectedAlertStore = useSelectedAlertStore();

  const alerts = ref<alertSummary[]>([]);
  const error = ref<string>();
  const isLoading = ref(false);
  const page = ref(0);
  const pageSize = ref(10);

  const selectedRows = computed(() => {
    return alerts.value.filter((alert) =>
      selectedAlertStore.selected.includes(alert.uuid),
    );
  });

  const visibleAlerts = computed(() => {
    const start = page.value * pageSize.value;
    const end = start + pageSize.value;
    return alerts.value.slice(start, end);
  });

  const visibleAlertUuids = computed(() => {
    return visibleAlerts.value.map((x) => x.uuid);
  });

  const columns = [
    { field: "eventTime", header: "Event Time (UTC)" },
    { field: "name", header: "Name" },
    { field: "owner", header: "Owner" },
    { field: "disposition", header: "Disposition" },
  ];

  const getAlerts = async (uuid: string) => {
    let allAlerts;

    try {
      allAlerts = await Alert.readAllPages({
        eventUuid: uuid,
        sort: "event_time|asc",
      });
    } catch (e: unknown) {
      alerts.value = [];
      if (typeof e === "string") {
        error.value = e;
      } else if (e instanceof Error) {
        error.value = e.message;
      }
    }

    if (allAlerts) {
      return allAlerts.map((x) => parseAlertSummary(x));
    }
    return [];
  };

  const initTable = async () => {
    isLoading.value = true;
    selectedAlertStore.unselectAll();
    alerts.value = await getAlerts(props.eventUuid);
    isLoading.value = false;
  };

  const onPage = async (event: { page: number; rows: number }) => {
    selectedAlertStore.unselectAll();
    page.value = event.page;
    pageSize.value = event.rows;
  };

  const removeAlerts = async () => {
    // Remove the alerts from the event
    try {
      const updateData = selectedAlertStore.selected.map((uuid) => ({
        uuid: uuid,
        eventUuid: null,
      }));

      await Alert.update(updateData);

      // Reinitialize the table
      await initTable();
    } catch (e: unknown) {
      if (typeof e === "string") {
        error.value = `Could not remove alerts: ${e}`;
      } else if (e instanceof Error) {
        error.value = `Could not remove alerts: ${e.message}`;
      }
    }
  };
</script>

<style>
  .link-text:hover {
    cursor: pointer;
    text-decoration: underline;
    font-weight: bold;
  }
</style>
