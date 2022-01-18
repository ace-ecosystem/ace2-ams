/* eslint-disable vue/attribute-hyphenation */
<!-- TheEventsTable.vue -->
<!-- The table where all currently filtered events are displayed, selected to take action, or link to an individual event page -->

<template>
  <DataTable
    ref="dt"
    v-model:expandedRows="expandedRows"
    v-model:filters="eventTableFilter"
    v-model:selection="selectedRows"
    :value="eventTableStore.visibleQueriedEventSummaries"
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
    @row-expand="rowExpand($event.data.uuid)"
    @row-collapse="rowCollapse($event.data.uuid)"
    @rowSelect="selectedEventStore.select($event.data.uuid)"
    @rowUnselect="selectedEventStore.unselect($event.data.uuid)"
    @rowSelect-all="
      selectedEventStore.selectAll(eventTableStore.visibleQueriedEventsUuids)
    "
    @rowUnselect-all="selectedEventStore.unselectAll()"
  >
    <!--        EVENT TABLE TOOLBAR-->
    <template #header>
      <Toolbar style="border: none">
        <template #start>
          <MultiSelect
            :model-value="selectedColumns"
            :options="columns"
            option-label="header"
            placeholder="Select Columns"
            @update:modelValue="onColumnToggle"
          />
        </template>
        <template #end>
          <span class="p-input-icon-left p-m-1">
            <i class="pi pi-search" />
            <InputText
              v-model="eventTableFilter['global'].value"
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
    <Column id="event-expand" :expander="true" header-style="width: 3rem" />

    <!-- CHECKBOX COLUMN -->
    <!-- It's annoying, but the PrimeVue DataTable selectionMode attribute works when camelCase -->
    <Column
      id="event-select"
      header-style="width: 3em"
      selection-mode="multiple"
    />

    <!-- DATA COLUMN -->
    <Column
      v-for="(col, index) of selectedColumns"
      :key="col.field + '_' + index"
      :field="col.field"
      :header="col.header"
      :sortable="col.sortable"
    >
      <!-- DATA COLUMN BODY-->
      <template #body="{ data }">
        <!-- NAME COLUMN - INCL. TAGS AND TODO: EVENT ICONS-->
        <div v-if="col.field === 'name'">
          <span class="p-m-1" data-cy="eventName">
            <router-link :to="getEventLink(data.uuid)">{{
              data.name
            }}</router-link></span
          >
          <br />
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
        <span v-else-if="Array.isArray(data[col.field])">
          {{ joinStringArray(data[col.field]) }}
        </span>
        <span v-else> {{ data[col.field] }}</span>
      </template>
    </Column>

    <!--      EVENT ROW DROPDOWN -->
    <template #expansion="slotProps">
      <ul>
        <li
          v-for="obs of expandedRowsData[slotProps.data.uuid]"
          :key="obs.value"
        >
          <span class="link-text" @click="1"
            >{{ obs.type.value }} : {{ obs.value }}</span
          >
        </li>
      </ul>
    </template>
  </DataTable>
  <Paginator
    :rows="numRows"
    :rows-per-page-options="[5, 10, 50, 100]"
    :total-records="eventTableStore.totalEvents"
    template="CurrentPageReport FirstPageLink PrevPageLink PageLinks NextPageLink LastPageLink RowsPerPageDropdown"
    current-page-report-template="Showing {first} to {last} of {totalRecords}"
    @page="
      onPage($event);
      selectedEventStore.unselectAll();
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
  import Toolbar from "primevue/toolbar";
  import Paginator from "primevue/paginator";

  import { camelToSnakeCase } from "@/etc/helpers";

  import { useFilterStore } from "@/stores/filter";
  import { useEventTableStore } from "@/stores/eventTable";
  import { useSelectedEventStore } from "@/stores/selectedEvent";

  const eventTableStore = useEventTableStore();
  const filterStore = useFilterStore();
  const selectedEventStore = useSelectedEventStore();

  const defaultColumns = [
    "createdTime",
    "name",
    "type",
    "vectors",
    "owner",
    "disposition",
  ];

  const eventTableFilter = ref({
    global: { value: null, matchMode: FilterMatchMode.CONTAINS },
  });

  const columns = ref([
    { field: "createdTime", header: "Created", sortable: true },
    { field: "name", header: "Name", sortable: true },
    { field: "owner", header: "Owner", sortable: true },
    { field: "status", header: "Status", sortable: true },
    { field: "type", header: "Type", sortable: true },
    { field: "vectors", header: "Vectors", sortable: false },
    { field: "threatActors", header: "Threat Actors", sortable: false },
    { field: "threats", header: "Threats", sortable: false },
    { field: "preventionTools", header: "Prevention Tools", sortable: false },
    { field: "riskLevel", header: "Risk Level", sortable: true },
  ]);
  const dt = ref(null);
  const error = ref(null);
  const expandedRows = ref([]);
  const expandedRowsData = ref({});
  const isLoading = ref(false);
  const selectedColumns = ref([]);
  const sortField = ref("createdTime");
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
      await loadEvents();
    },
    { deep: true },
  );

  eventTableStore.$subscribe(async (_, state) => {
    if (state.requestReload) {
      await reloadTable();
    }
  });

  const selectedRows = computed(() => {
    return eventTableStore.visibleQueriedEvents.filter((event) =>
      selectedEventStore.selected.includes(event.uuid),
    );
  });

  const reloadTable = async () => {
    selectedEventStore.unselectAll();
    eventTableStore.requestReload = false;
    await loadEvents();
  };

  const rowExpand = async (uuid) => {
    // const observables = await NodeTree.readNodesOfNodeTree(
    //   [uuid],
    //   "observable",
    // );
    // expandedRowsData.value[uuid] = observables.sort((a, b) => {
    //   if (a.type.value === b.type.value) {
    //     return a.value < b.value ? -1 : 1;
    //   } else {
    //     return a.type.value < b.type.value ? -1 : 1;
    //   }
    // });
  };

  const rowCollapse = (uuid) => {
    delete expandedRowsData.value[uuid];
  };

  onMounted(async () => {
    initEventTable();
    await loadEvents();
  });

  const exportCSV = () => {
    // Exports currently filtered events to CSV
    dt.value.exportCSV();
  };

  const formatDateTime = (dateTime) => {
    if (dateTime) {
      const d = new Date(dateTime);
      return d.toLocaleString("en-US");
    }

    return "None";
  };

  const getEventLink = (uuid) => {
    return "/event/" + uuid;
  };

  const initEventTable = () => {
    // Initializes event filter (the keyword search)
    eventTableFilter.value = {
      global: { value: null, matchMode: FilterMatchMode.CONTAINS },
    };
    selectedColumns.value = columns.value.filter((col) => {
      return defaultColumns.includes(col.field);
    });
    error.value = null;
  };

  const loadEvents = async () => {
    isLoading.value = true;
    try {
      await eventTableStore.readPage({
        sort: sortFilter.value,
        ...pageOptions.value,
        ...filterStore.events,
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
    selectedEventStore.unselectAll();
    numRows.value = event.rows;
    page.value = event.page;
    await loadEvents();
  };

  const reset = async () => {
    initEventTable();
    await sort({ sortField: "date", sortOrder: "-1" });
  };

  const sort = async (event) => {
    if (event.sortField) {
      sortField.value = event.sortField;
      sortOrder.value = event.sortOrder > 0 ? "asc" : "desc";
      await loadEvents();
    } else {
      sortField.value = null;
      sortOrder.value = null;
    }
  };

  const joinStringArray = (arr) => {
    return arr.join(", ");
  };
</script>

<style>
  .link-text:hover {
    cursor: pointer;
    text-decoration: underline;
    font-weight: bold;
  }
</style>
