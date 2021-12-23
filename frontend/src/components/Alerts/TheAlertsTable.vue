/* eslint-disable vue/attribute-hyphenation */
<!-- TheAlertsTable.vue -->
<!-- The table where all currently filtered alerts are displayed, selected to take action, or link to an individual alert page -->

<template>
  <DataTable
    ref="dt"
    v-model:expandedRows="expandedRows"
    v-model:filters="alertTableFilter"
    v-model:selection="selectedRows"
    :value="alertTableStore.visibleQueriedAlertSummaries"
    :global-filter-fields="selectedColumns.field"
    :resizable-columns="true"
    :sort-order="-1"
    :loading="isLoading"
    column-resize-mode="expand"
    data-key="uuid"
    removable-sort
    responsive-layout="scroll"
    :sort-field="sortField"
    @sort="sort"
    @rowSelect="selectedAlertStore.select($event.data.uuid)"
    @rowUnselect="selectedAlertStore.unselect($event.data.uuid)"
    @rowSelect-all="
      selectedAlertStore.selectAll(alertTableStore.visibleQueriedAlertsUuids)
    "
    @rowUnselect-all="selectedAlertStore.unselectAll()"
  >
    <!--        ALERT TABLE TOOLBAR-->
    <template #header>
      <Toolbar style="border: none">
        <template #left>
          <MultiSelect
            :model-value="selectedColumns"
            :options="columns"
            option-label="header"
            placeholder="Select Columns"
            @update:modelValue="onColumnToggle"
          />
        </template>
        <template #right>
          <span class="p-input-icon-left p-m-1">
            <i class="pi pi-search" />
            <InputText
              v-model="alertTableFilter['global'].value"
              placeholder="Search in table"
            />
          </span>
          <!--            CLEAR TABLE FILTERS -->
          <Button
            icon="pi pi-refresh"
            class="p-button-rounded p-m-1"
            @click="reset()"
          />
          <!--            EXPORT TABLE -->
          <Button
            class="p-button-rounded p-m-1"
            icon="pi pi-download"
            @click="exportCSV($event)"
          />
        </template>
      </Toolbar>
    </template>

    <!-- DROPDOWN COLUMN-->
    <Column id="alert-expand" :expander="true" header-style="width: 3rem" />

    <!-- CHECKBOX COLUMN -->
    <!-- It's annoying, but the PrimeVue DataTable selectionMode attribute works when camelCase -->
    <Column
      id="alert-select"
      header-style="width: 3em"
      selectionMode="multiple"
    />

    <!-- DATA COLUMN -->
    <Column
      v-for="(col, index) of selectedColumns"
      :key="col.field + '_' + index"
      :field="col.field"
      :header="col.header"
      :sortable="true"
    >
      <!-- DATA COLUMN BODY-->
      <template #body="{ data }">
        <!-- NAME COLUMN - INCL. TAGS AND TODO: ALERT ICONS-->
        <div v-if="col.field === 'name'">
          <span class="p-m-1">
            <router-link :to="getAlertLink(data.uuid)">{{
              data.name
            }}</router-link></span
          >
          <br />
          <span>
            <Tag
              v-for="tag in data.tags"
              :key="tag.uuid"
              class="p-mr-2"
              rounded
              >{{ tag.value }}</Tag
            >
          </span>
          <span v-if="data.comments">
            <pre
              v-for="comment in data.comments"
              :key="comment.uuid"
              class="p-mr-2 comment"
            >
({{ comment.user.displayName }}) {{ comment.value }}</pre
            >
          </span>
        </div>
        <span v-else-if="col.field.includes('Time')">
          {{ formatDateTime(data[col.field]) }}</span
        >
        <span v-else> {{ data[col.field] }}</span>
      </template>
    </Column>

    <!--      ALERT ROW DROPDOWN -->
    <template #expansion="slotProps">
      <h5>Observables:</h5>
      <ul>
        <li v-for="obs of slotProps.data.observables" :key="obs.value">
          {{ obs }}
        </li>
      </ul>
    </template>
  </DataTable>
  <Paginator
    :rows="numRows"
    :rows-per-page-options="[5, 10, 50, 100]"
    :total-records="alertTableStore.totalAlerts"
    template="CurrentPageReport FirstPageLink PrevPageLink PageLinks NextPageLink LastPageLink RowsPerPageDropdown"
    current-page-report-template="Showing {first} to {last} of {totalRecords}"
    @page="
      onPage($event);
      selectedAlertStore.unselectAll();
    "
  ></Paginator>
</template>

<script setup>
  import { computed, onMounted, ref } from "vue";

  import Button from "primevue/button";
  import Column from "primevue/column";
  import DataTable from "primevue/datatable";
  import { FilterMatchMode } from "primevue/api";
  import InputText from "primevue/inputtext";
  import MultiSelect from "primevue/multiselect";
  import Tag from "primevue/tag";
  import Toolbar from "primevue/toolbar";
  import Paginator from "primevue/paginator";

  import { camelToSnakeCase } from "@/etc/helpers";
  import { useAlertTableStore } from "@/stores/alertTable";
  import { useFilterStore } from "@/stores/filter";
  import { useSelectedAlertStore } from "@/stores/selectedAlert";

  const alertTableStore = useAlertTableStore();
  const filterStore = useFilterStore();
  const selectedAlertStore = useSelectedAlertStore();

  const defaultColumns = ["eventTime", "name", "owner", "disposition"];

  const alertTableFilter = ref({
    global: { value: null, matchMode: FilterMatchMode.CONTAINS },
  });
  const columns = ref([
    { field: "dispositionTime", header: "Dispositioned Time" },
    { field: "insertTime", header: "Insert Time" },
    { field: "eventTime", header: "Event Time" },
    { field: "name", header: "Name" },
    { field: "owner", header: "Owner" },
    { field: "disposition", header: "Disposition" },
    { field: "dispositionUser", header: "Dispositioned By" },
    { field: "queue", header: "Queue" },
    { field: "type", header: "Type" },
  ]);
  const dt = ref(null);
  const error = ref(null);
  const expandedRows = ref([]);
  const isLoading = ref(false);
  const selectedColumns = ref([]);
  const selectedRows = ref([]);
  const sortField = ref("eventTime");
  const sortOrder = ref("desc");
  const numRows = ref(10);
  const page = ref(0);

  const sortFilter = computed(() => {
    return sortField.value
      ? `${camelToSnakeCase(sortField.value)}|${sortOrder.value}`
      : null;
  });

  const pageOptions = computed(() => {
    return {
      limit: numRows.value,
      offset: numRows.value * page.value,
    };
  });

  filterStore.$subscribe(
    async () => {
      await loadAlerts();
    },
    { deep: true },
  );

  alertTableStore.$subscribe(async (_, state) => {
    if (state.requestReload) {
      await reloadTable();
    }
  });

  const reloadTable = async () => {
    selectedRows.value = [];
    selectedAlertStore.unselectAll();
    alertTableStore.requestReload = false;
    await loadAlerts();
  };

  onMounted(async () => {
    initAlertTable();
    await loadAlerts();
  });

  const exportCSV = () => {
    // Exports currently filtered alerts to CSV
    dt.value.exportCSV();
  };

  const formatDateTime = (dateTime) => {
    if (dateTime) {
      const d = new Date(dateTime);
      return d.toLocaleString("en-US");
    }

    return "None";
  };

  const getAlertLink = (uuid) => {
    return "/alert/" + uuid;
  };

  const initAlertTable = () => {
    // Initializes alert filter (the keyword search)
    alertTableFilter.value = {
      global: { value: null, matchMode: FilterMatchMode.CONTAINS },
    };
    selectedColumns.value = columns.value.filter((col) => {
      return defaultColumns.includes(col.field);
    });
    error.value = null;
  };

  const loadAlerts = async () => {
    isLoading.value = true;
    try {
      await alertTableStore.readPage({
        sort: sortFilter.value,
        ...pageOptions.value,
        ...filterStore.alerts,
      });
    } catch (err) {
      error.value = err.message || "Something went wrong!";
    }
    isLoading.value = false;
  };

  const onColumnToggle = (val) => {
    // Toggles selected columns to display
    // This method required/provided by Primevue 'ColToggle' docs
    selectedColumns.value = columns.value.filter((col) => val.includes(col));
  };

  const onPage = async (event) => {
    selectedRows.value = [];
    numRows.value = event.rows;
    page.value = event.page;
    await loadAlerts();
  };

  const reset = async () => {
    initAlertTable();
    await sort({ sortField: "eventTime", sortOrder: "-1" });
  };

  const sort = async (event) => {
    if (event.sortField) {
      sortField.value = event.sortField;
      sortOrder.value = event.sortOrder > 0 ? "asc" : "desc";
      await loadAlerts();
    } else {
      sortField.value = null;
      sortOrder.value = null;
    }
  };
</script>
