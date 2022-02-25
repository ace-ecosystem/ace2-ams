<!-- TheNodesTable.vue -->
<!-- The table where all currently filtered nodes are displayed, selected to take action, or link to an individual node page -->

<template>
  <DataTable
    ref="datatable"
    v-model:expandedRows="expandedRows"
    v-model:filters="nodeTableFilter"
    v-model:selection="selectedRows"
    data-key="uuid"
    :value="tableStore.visibleQueriedItemSummaries"
    :global-filter-fields="selectedColumns.field"
    :resizable-columns="true"
    :loading="isLoading"
    column-resize-mode="expand"
    responsive-layout="scroll"
    :sort-field="tableStore.sortField"
    :sort-order="sortOrder"
    removable-sort
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
          <slot name="tableHeaderStart" />
          <!-- COLUMN SELECT -->
          <MultiSelect
            v-if="columnSelect"
            :model-value="selectedColumns"
            :options="columnOptions"
            data-cy="table-column-select"
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
              data-cy="table-keyword-search"
              placeholder="Search in table"
            />
          </span>
          <!-- CLEAR TABLE FILTERS -->
          <Button
            v-if="resetTable"
            data-cy="reset-table-button"
            icon="pi pi-refresh"
            class="p-button-rounded p-m-1"
            @click="reset()"
          />
          <!-- EXPORT TABLE TO CSV -->
          <Button
            v-if="exportCSV"
            data-cy="export-table-button"
            class="p-button-rounded p-m-1"
            icon="pi pi-download"
            @click="exportCSV($event)"
          />
          <slot name="tableHeaderEnd" />
        </template>
      </Toolbar>
    </template>

    <!-- EXPANSION ARROW COLUMN-->
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

    <!-- DATA COLUMNS -->
    <Column
      v-for="(col, index) of displayedColumns"
      :key="col.field + '_' + index"
      :field="col.field"
      :header="col.header"
      :sortable="col.sortable"
    >
      <!-- DATA COLUMN CELL BODIES-->
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
    data-cy="table-pagination-options"
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
    defineEmits,
    defineProps,
    inject,
    onMounted,
    ref,
  } from "vue";

  import { FilterMatchMode } from "primevue/api";
  import Button from "primevue/button";
  import Column from "primevue/column";
  import DataTable from "primevue/datatable";
  import InputText from "primevue/inputtext";
  import MultiSelect from "primevue/multiselect";
  import Paginator from "primevue/paginator";
  import Toolbar from "primevue/toolbar";

  import { useFilterStore } from "@/stores/filter";
  import { nodeSelectedStores, nodeTableStores } from "@/stores/index";

  const props = defineProps({
    columns: { type: Array, required: true },
    columnSelect: { type: Boolean, default: true },
    exportCSV: { type: Boolean, default: true },
    keywordSearch: { type: Boolean, default: true },
    resetTable: { type: Boolean, default: true },
    rowExpansion: { type: Boolean, default: true },
  });

  defineEmits(["rowExpand", "rowCollapse"]);

  const filterStore = useFilterStore();
  const nodeType = inject("nodeType");
  const tableStore = nodeTableStores[nodeType]();
  const selectedStore = nodeSelectedStores[nodeType]();

  const tableToolbarRequired =
    props.exportCSV ||
    props.keywordSearch ||
    props.columnSelect ||
    props.resetTable;

  const columnOptions = props.columns.filter((col) => !col.required);
  const requiredColumns = props.columns.filter((col) => col.required);
  const defaultColumns = props.columns.filter((col) => col.default);

  const datatable = ref(null);
  const error = ref(null);
  const expandedRows = ref([]);
  const isLoading = ref(false);
  const page = ref(0);
  const selectedColumns = ref([]);

  // Used for keyword search
  const nodeTableFilter = ref({
    global: { value: null, matchMode: FilterMatchMode.CONTAINS },
  });

  filterStore.$subscribe(
    async () => {
      await loadNodes();
    },
    { deep: true },
  );

  tableStore.$subscribe(async (_, state) => {
    if (state.requestReload) {
      await reloadTable();
    }
  });

  onMounted(async () => {
    initNodeTable();
    await loadNodes();
  });

  const displayedColumns = computed(() => {
    return [...requiredColumns, ...selectedColumns.value];
  });

  const selectedRows = computed(() => {
    return tableStore.visibleQueriedItems.filter((node) =>
      selectedStore.selected.includes(node.uuid),
    );
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

  const pageOptions = computed(() => {
    return {
      limit: tableStore.pageSize,
      offset: tableStore.pageSize * page.value,
    };
  });

  const exportCSV = () => {
    // Exports currently filtered nodes to CSV
    datatable.value.exportCSV();
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

  const onColumnToggle = (val) => {
    // Toggles selected columns to display
    // This method required/provided by Primevue 'ColToggle' docs
    selectedColumns.value = props.columns.filter((col) => val.includes(col));
  };

  const reloadTable = async () => {
    selectedStore.unselectAll();
    tableStore.requestReload = false;
    await loadNodes();
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
