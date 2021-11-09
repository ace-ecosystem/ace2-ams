/* eslint-disable vue/attribute-hyphenation */
<!-- TheAlertsTable.vue -->
<!-- The table where all currently filtered alerts are displayed, selected to take action, or link to an individual alert page -->

<template>
  <DataTable
    ref="dt"
    v-model:expandedRows="expandedRows"
    v-model:filters="alertTableFilter"
    v-model:selection="selectedRows"
    :value="alerts"
    :global-filter-fields="selectedColumns.field"
    :paginator="true"
    :resizable-columns="true"
    :totalRecords="totalAlerts"
    :rows="10"
    :rows-per-page-options="[5, 10, 50, 100]"
    :sort-order="-1"
    :lazy="true"
    :loading="isLoading"
    column-resize-mode="expand"
    current-page-report-template="Showing {first} to {last} of {totalRecords}"
    data-key="uuid"
    paginator-template="CurrentPageReport FirstPageLink PrevPageLink PageLinks NextPageLink LastPageLink RowsPerPageDropdown"
    removable-sort
    responsive-layout="scroll"
    sort-field="eventTime"
    name="AlertsTable"
    @page="onPage($event)"
    @rowSelect="alertSelect($event.data)"
    @rowUnselect="alertUnselect($event.data)"
    @rowSelect-all="alertSelectAll"
    @rowUnselect-all="alertUnselectAll"
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
      selectionMode="multiple"
      header-style="width: 3em"
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
          <span class="p-m-1"> {{ data.name }}</span>
          <br />
          <span>
            <Tag v-for="tag in data.tags" :key="tag" class="p-mr-2" rounded>{{
              tag
            }}</Tag>
          </span>
        </div>
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
</template>

<script>
  import { mapActions, mapGetters } from "vuex";

  import Button from "primevue/button";
  import Column from "primevue/column";
  import DataTable from "primevue/datatable";
  import { FilterMatchMode } from "primevue/api";
  import InputText from "primevue/inputtext";
  import MultiSelect from "primevue/multiselect";
  import Tag from "primevue/tag";
  import Toolbar from "primevue/toolbar";

  export default {
    name: "TheAlertsTable",
    components: {
      Button,
      Column,
      DataTable,
      InputText,
      MultiSelect,
      Tag,
      Toolbar,
    },

    data() {
      return {
        alertTableFilter: null,

        columns: [
          { field: "dispositionTime", header: "Dispositioned Time" },
          { field: "insertTime", header: "Insert Date" },
          { field: "eventTime", header: "Event Date" },
          { field: "name", header: "Name" },
          { field: "owner", header: "Owner" },
          { field: "disposition", header: "Disposition" },
          { field: "dispositionUser", header: "Dispositioned By" },
          { field: "queue", header: "Queue" },
          { field: "type", header: "Type" },
        ],

        defaultColumns: ["eventTime", "name", "owner", "disposition"],

        expandedRows: [],
        error: null,
        isLoading: false,
        selectedColumns: null,
        selectedRows: null,
      };
    },

    computed: {
      ...mapGetters({
        alerts: "alerts/visibleQueriedAlerts",
        totalAlerts: "alerts/totalAlerts",
        selectedAlerts: "selectedAlerts/selected",
      }),
    },

    async created() {
      this.reset();
      await this.loadAlerts({ limit: 10, offset: 0 });
    },

    methods: {
      ...mapActions({
        alertSelect: "selectedAlerts/select",
        alertUnselect: "selectedAlerts/selectAll",
        alertUnselectAll: "selectedAlerts/unselectAll",
        selectAll: "selectedAlerts/selectAll",
        getAllAlerts: "alerts/getAll",
      }),

      alertSelectAll() {
        let allAlertUuids = [];
        for (let i = 0; i < this.alerts.length; i++) {
          allAlertUuids.push(this.alerts[i].uuid);
        }
        this.selectAll(allAlertUuids);
      },

      reset() {
        // Sets the alert table selected columns and keyword search back to default
        this.initAlertTable();
        this.selectedColumns = [];
        this.selectedColumns = this.columns.filter((column) => {
          return this.defaultColumns.includes(column.field);
        });
        this.error = null;
      },

      initAlertTable() {
        // Initializes alert filter (the keyword search)
        this.alertTableFilter = {
          global: { value: null, matchMode: FilterMatchMode.CONTAINS },
        };
      },

      onColumnToggle(value) {
        // Toggles selected columns to display
        // This method required/provided by Primevue 'ColToggle' docs
        this.selectedColumns = this.columns.filter((col) =>
          value.includes(col),
        );
      },

      exportCSV() {
        // Exports currently filtered alerts to CSV
        this.$refs.dt.exportCSV();
      },

      onPage(event) {
        this.loadAlerts({ limit: event.rows, offset: event.rows * event.page });
      },

      async loadAlerts(options) {
        this.isLoading = true;
        try {
          await this.getAllAlerts(options);
        } catch (error) {
          this.error = error.message || "Something went wrong!";
        }
        this.isLoading = false;
      },
    },
  };
</script>
