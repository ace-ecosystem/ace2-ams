/* eslint-disable vue/attribute-hyphenation */
<!-- TheNodesTable.vue -->
<!-- The table where all currently filtered nodes are displayed, selected to take action, or link to an individual node page -->

<!-- ASSUMPTIONS FOR NODE CLASSES USING THIS COMPONENT -->

<template>
  <DataTable
    ref="dt"
    v-model:expandedRows="expandedRows"
    v-model:filters="nodeTableFilter"
    v-model:selection="selectedRows"
    :value="tableStore.visibleQueriedItemSummaries"
    :global-filter-fields="selectedColumns.field"
    :resizable-columns="true"
    :loading="isLoading"
    column-resize-mode="expand"
    data-key="uuid"
    removable-sort
    responsive-layout="scroll"
    :sort-field="tableStore.sortField"
    :sort-order="sortOrder"
    @sort="sort"
    @row-expand="$emit('rowExpand', $event)"
    @row-collapse="$emit('rowCollapse', $event)"
    @rowSelect="selectedStore.select($event.data.uuid)"
    @rowUnselect="selectedStore.unselect($event.data.uuid)"
    @rowSelect-all="
      selectedStore.selectAll(tableStore.visibleQueriedItemsUuids)
    "
    @rowUnselect-all="selectedStore.unselectAll()"
  >
    <!-- TABLE TOOLBAR-->
    <template v-if="tableToolbarRequired" #header>
      <Toolbar style="border: none">
        <template #start>
          <!-- COLUMN SELECT -->
          <MultiSelect
            v-if="columnSelect"
            :model-value="selectedColumns"
            :options="columns"
            option-label="header"
            placeholder="Select Columns"
            @update:modelValue="onColumnToggle"
          />
        </template>
        <template #end>
          <!-- KEYWORD SEARCH -->

          <span v-if="keywordSearch" class="p-input-icon-left p-m-1">
            <i class="pi pi-search" />
            <InputText
              v-model="nodeTableFilter['global'].value"
              placeholder="Search in table"
            />
          </span>
          <!-- CLEAR TABLE FILTERS -->
          <Button
            v-if="resetTable"
            icon="pi pi-refresh"
            class="p-button-rounded p-m-1"
            @click="reset()"
          />
          <!-- EXPORT TABLE -->
          <Button
            v-if="exportCSV"
            class="p-button-rounded p-m-1"
            icon="pi pi-download"
            @click="exportCSV($event)"
          />
        </template>
      </Toolbar>
    </template>

    <!-- DROPDOWN COLUMN-->
    <Column
      v-if="rowExpansion"
      id="node-expand"
      :expander="true"
      header-style="width: 3rem"
    />

    <!-- CHECKBOX COLUMN -->
    <Column
      id="node-select"
      header-style="width: 3em"
      selection-mode="multiple"
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
      <template #body="{ data, field }">
        <slot name="rowCell" :data="data" :col="col" :field="field"></slot>
      </template>
    </Column>

    <!-- ROW EXPANSION -->
    <template #expansion="{ data }">
      <slot name="rowExpansion" :data="data"></slot>
    </template>
  </DataTable>

  <Paginator
    :rows="tableStore.pageSize"
    :rows-per-page-options="[5, 10, 50, 100]"
    :total-records="tableStore.totalItems"
    template="CurrentPageReport FirstPageLink PrevPageLink PageLinks NextPageLink LastPageLink RowsPerPageDropdown"
    current-page-report-template="Showing {first} to {last} of {totalRecords}"
    @page="
      onPage($event);
      selectedStore.unselectAll();
    "
  ></Paginator>
</template>

<script setup>
  import {
    computed,
    defineProps,
    defineEmits,
    onMounted,
    ref,
    inject,
  } from "vue";

  import Button from "primevue/button";
  import Column from "primevue/column";
  import DataTable from "primevue/datatable";
  import { FilterMatchMode } from "primevue/api";
  import InputText from "primevue/inputtext";
  import MultiSelect from "primevue/multiselect";
  import Toolbar from "primevue/toolbar";
  import Paginator from "primevue/paginator";

  import { useAlertTableStore } from "@/stores/alertTable";
  import { useEventTableStore } from "@/stores/eventTable";
  import { useSelectedAlertStore } from "@/stores/selectedAlert";
  import { useSelectedEventStore } from "@/stores/selectedEvent";
  import { useFilterStore } from "@/stores/filter";

  const filterStore = useFilterStore();

  const props = defineProps({
    columns: { type: Array, required: true },
    exportCSV: { type: Boolean, required: true },
    keywordSearch: { type: Boolean, required: true },
    columnSelect: { type: Boolean, required: true },
    resetTable: { type: Boolean, required: true },
    rowExpansion: { type: Boolean, required: true },
  });
  defineEmits(["rowExpand", "rowCollapse"]);

  const nodeType = inject("nodeType");

  const columns = ref(props.columns);

  const dt = ref(null);
  const error = ref(null);
  const expandedRows = ref([]);
  const isLoading = ref(false);
  const selectedColumns = ref([]);
  const page = ref(0);

  const nodeTableStores = {
    alerts: useAlertTableStore,
    events: useEventTableStore,
  };
  const nodeSelectedStores = {
    alerts: useSelectedAlertStore,
    events: useSelectedEventStore,
  };

  const tableStore = nodeTableStores[nodeType]();
  const selectedStore = nodeSelectedStores[nodeType]();

  const defaultColumns = columns.value.filter((col) => {
    return col.default;
  });

  const tableToolbarRequired =
    props.exportCSV ||
    props.keywordSearch ||
    props.columnSelect ||
    props.resetTable;

  const nodeTableFilter = ref({
    global: { value: null, matchMode: FilterMatchMode.CONTAINS },
  });

  const pageOptions = computed(() => {
    return {
      limit: tableStore.pageSize,
      offset: tableStore.pageSize * page.value,
    };
  });

  onMounted(async () => {
    tableStore.$subscribe(async (_, state) => {
      if (state.requestReload) {
        await reloadTable();
      }
    });

    initNodeTable();
    await loadNodes();
  });

  const sortOrder = computed(() => {
    switch (tableStore.sortOrder) {
      case "asc": {
        return 1;
      }
      case "desc": {
        return -1;
      }
      default: {
        return 0;
      }
    }
  });

  const selectedRows = computed(() => {
    return tableStore.visibleQueriedItems.filter((node) =>
      selectedStore.selected.includes(node.uuid),
    );
  });

  const reloadTable = async () => {
    selectedStore.unselectAll();
    tableStore.requestReload = false;
    await loadNodes();
  };

  filterStore.$subscribe(
    async () => {
      await loadNodes();
    },
    { deep: true },
  );

  const exportCSV = () => {
    // Exports currently filtered nodes to CSV
    dt.value.exportCSV();
  };

  const initNodeTable = () => {
    // Initializes node filter (the keyword search)
    nodeTableFilter.value = {
      global: { value: null, matchMode: FilterMatchMode.CONTAINS },
    };
    // Initializes selected columns to default
    selectedColumns.value = defaultColumns;
    //
    error.value = null;
  };

  const loadNodes = async () => {
    isLoading.value = true;
    try {
      await tableStore.readPage({
        sort: tableStore.sortFilter,
        ...pageOptions.value,
        ...filterStore[nodeType],
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
    selectedStore.unselectAll();
    tableStore.pageSize = event.rows;
    page.value = event.page;
    await loadNodes();
  };

  const reset = async () => {
    initNodeTable();
    tableStore.resetSort();
    await loadNodes();
  };

  const sort = async (event) => {
    if (event.sortField) {
      tableStore.sortField = event.sortField;
      tableStore.sortOrder = event.sortOrder > 0 ? "asc" : "desc";
      await loadNodes();
    } else {
      tableStore.sortField = null;
      tableStore.sortOrder = null;
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
