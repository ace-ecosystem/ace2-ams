<!-- TheObjectTable.vue -->
<!-- The table where all currently filtered objects are displayed, selected to take action, or link to an individual object page -->

<template>
  <Toast data-cy="object-table-error" />
  <DataTable
    ref="datatable"
    v-model:expandedRows="expandedRows"
    v-model:filters="objectTableFilter"
    v-model:selection="selectedRows"
    data-key="uuid"
    :value="tableStore.visibleQueriedItemSummaries"
    :resizable-columns="true"
    :loading="isLoading"
    column-resize-mode="expand"
    responsive-layout="scroll"
    :sort-field="tableStore.sortField!"
    :sort-order="sortOrder"
    removable-sort
    @add-filter="addFilter"
    @sort="sort"
    @row-expand="$emit('rowExpand', $event)"
    @row-collapse="$emit('rowCollapse', $event)"
    @row-select="selectedStore.select($event.data.uuid)"
    @row-unselect="selectedStore.unselect($event.data.uuid)"
    @row-select-all="
      selectedStore.selectAll(tableStore.visibleQueriedItemsUuids)
    "
    @row-unselect-all="selectedStore.unselectAll()"
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
            @update:model-value="onColumnToggle($event as any)"
          />
        </template>
        <template #end>
          <!-- KEYWORD SEARCH -->
          <span v-if="keywordSearch" class="p-input-icon-left p-m-1">
            <i class="pi pi-search" />
            <InputText
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
            @click="exportCSV"
          />
          <slot name="tableHeaderEnd" />
        </template>
      </Toolbar>
    </template>

    <template #empty> No {{ objectType }} found. </template>

    <!-- EXPANSION ARROW COLUMN-->
    <Column
      v-if="rowExpansion"
      id="object-expand"
      :expander="true"
      header-style="width: 3rem"
    />

    <!-- CHECKBOX COLUMN -->
    <Column
      id="object-select"
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
        <div :class="cellClass(field)" @click="addFilter(data, field)">
          <slot name="rowCell" :data="data" :col="col" :field="field">{{
            data[field]
          }}</slot>
        </div>
      </template>
    </Column>

    <!-- ROW EXPANSION -->
    <template #expansion="{ data }">
      <slot name="rowExpansion" :data="data">No content provided.</slot>
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

<script setup lang="ts">
  import {
    computed,
    defineEmits,
    defineProps,
    inject,
    onMounted,
    ref,
    PropType,
  } from "vue";

  import { FilterMatchMode } from "primevue/api";
  import { useToast } from "primevue/usetoast";
  import Toast from "primevue/toast";
  import Button from "primevue/button";
  import Column from "primevue/column";
  import DataTable from "primevue/datatable";
  import InputText from "primevue/inputtext";
  import MultiSelect from "primevue/multiselect";
  import Paginator from "primevue/paginator";
  import Toolbar from "primevue/toolbar";

  import { objectSelectedStores, objectTableStores } from "@/stores/index";
  import { useFilterStore } from "@/stores/filter";
  import { loadFiltersFromStorage } from "@/stores/helpers";
  import { useCurrentUserSettingsStore } from "@/stores/currentUserSettings";

  import { inputTypes } from "@/etc/constants/base";
  import { propertyOption } from "@/models/base";
  import { alertRead } from "@/models/alert";
  import { eventRead } from "@/models/event";

  interface column {
    required?: boolean;
    default: boolean;
    field: string;
    header: string;
    sortable: boolean;
  }

  const props = defineProps({
    columns: { type: Array as PropType<column[]>, required: true },
    columnSelect: { type: Boolean, default: true },
    exportCSV: { type: Boolean, default: true },
    keywordSearch: { type: Boolean, default: true },
    resetTable: { type: Boolean, default: true },
    rowExpansion: { type: Boolean, default: true },
  });

  defineEmits(["rowExpand", "rowCollapse"]);

  const objectType = inject("objectType") as "alerts" | "events";
  const availableFilters = inject("availableFilters") as Record<
    string,
    propertyOption[]
  >;

  const tableStore = objectTableStores[objectType]();
  const selectedStore = objectSelectedStores[objectType]();
  const currentUserSettingsStore = useCurrentUserSettingsStore();
  const filterStore = useFilterStore();
  const toast = useToast();

  const tableToolbarRequired =
    props.exportCSV ||
    props.keywordSearch ||
    props.columnSelect ||
    props.resetTable;

  const columnOptions = props.columns.filter((col) => !col.required);
  const requiredColumns = props.columns.filter((col) => col.required);
  const defaultColumns = props.columns.filter((col) => col.default);

  const datatable = ref();
  const error = ref<string>();
  const expandedRows = ref([]);
  const isLoading = ref(false);
  const page = ref(0);
  const selectedColumns = ref<column[]>([]);

  // Used for keyword search
  const objectTableFilter = ref({
    global: { value: null, matchMode: FilterMatchMode.CONTAINS },
  });

  filterStore.$subscribe(
    async () => {
      if (tableStore.allFiltersLoaded) {
        await loadObjects();
      }
    },
    { deep: true },
  );

  tableStore.$subscribe(async (_, state) => {
    if (state.requestReload) {
      await reloadTable();
    }
  });

  onMounted(async () => {
    initObjectTable();
    if (!tableStore.allFiltersLoaded) {
      loadFiltersFromStorage();
    }
    await loadObjects();
  });

  const displayedColumns = computed(() => {
    return [...requiredColumns, ...selectedColumns.value];
  });

  const selectedRows = computed(() => {
    return tableStore.visibleQueriedSelectedItems;
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
    // Exports currently filtered objects to CSV
    datatable.value.exportCSV();
  };

  const initObjectTable = () => {
    // Initializes object filter (the keyword search)
    objectTableFilter.value = {
      global: { value: null, matchMode: FilterMatchMode.CONTAINS },
    };
    // Initializes selected columns to default
    selectedColumns.value = defaultColumns;
    //
    error.value = undefined;
  };

  const onColumnToggle = (val: column[]) => {
    // Toggles selected columns to display
    // This method required/provided by Primevue 'ColToggle' docs
    selectedColumns.value = props.columns.filter((col) => val.includes(col));
  };

  const reloadTable = async () => {
    selectedStore.unselectAll();
    tableStore.requestReload = false;
    await loadObjects();
  };

  const showError = (args: { detail: string }) => {
    toast.add({
      severity: "error",
      summary: `Failed to fetch ${objectType}`,
      detail: args.detail,
      life: 6000,
    });
  };

  const loadObjects = async () => {
    isLoading.value = true;
    try {
      await tableStore.readPage({
        sort: tableStore.sortFilter!,
        ...pageOptions.value,
        ...filterStore[objectType],
      });
    } catch (e: unknown) {
      if (typeof e === "string") {
        showError({ detail: e });
      } else if (e instanceof Error) {
        showError({ detail: e.message });
      }
    }
    isLoading.value = false;
  };

  const onPage = async (event: { rows: number; page: number }) => {
    selectedStore.unselectAll();
    tableStore.pageSize = event.rows;
    page.value = event.page;
    await loadObjects();
  };

  const reset = async () => {
    initObjectTable();
    tableStore.resetSort();
    await loadObjects();
  };

  const sort = async (event: { sortField: string; sortOrder: number }) => {
    if (event.sortField) {
      tableStore.sortField = event.sortField;
      tableStore.sortOrder = event.sortOrder > 0 ? "asc" : "desc";
      await loadObjects();
    } else {
      tableStore.sortField = null;
      tableStore.sortOrder = null;
    }
  };

  const currentQueue = ref(
    currentUserSettingsStore.queues[objectType]
      ? currentUserSettingsStore.queues[objectType]?.value
      : undefined,
  );

  const isFilterable = (field: string) => {
    if (!availableFilters || !currentQueue.value) {
      return false;
    }
    let filter = availableFilters[currentQueue.value].find((filter) => {
      return filter.name === field;
    });
    if (filter && filter.type === inputTypes.SELECT) {
      return true;
    }
    return false;
  };

  const cellClass = (field: string) => {
    return [{ filter: isFilterable(field) }];
  };

  const addFilter = (data: alertRead | eventRead, field: string) => {
    const object = tableStore.visibleQueriedItemById(data.uuid);
    if (isFilterable(field) && object && object[field]) {
      filterStore.setFilter({
        objectType: objectType,
        filterName: field,
        filterValue: object[field] as any,
      });
    }
  };
</script>

<style>
  .link-text:hover {
    cursor: pointer;
    text-decoration: underline;
    font-weight: bold;
  }

  .filter:hover {
    cursor: pointer;
  }
</style>
