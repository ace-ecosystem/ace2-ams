<!-- FilterChip.vue -->
<!-- A chip that shows a currently applied filter (by type, ex. 'queue' or 'owner' -->
<!-- Contains actions to remove (and eventually edit/add) a filter through click actions -->
<template>
  <span v-if="filterNameObject" style="padding: 2px" data-cy="filter-chip">
    <Chip>
      <span
        class="p-chip-text link-text filter-name-text chip-content"
        @click="unsetFilter"
        >{{ filterLabel }}:</span
      >
      <span
        v-for="(value, index) in filterValue"
        :key="(formatValue(value) as string)"
        data-cy="filter-chip-content"
        class="link-text p-chip-text chip-content"
      >
        <span
          style="padding-left: 2px; padding-right: 2px; font-weight: bold"
          @click="unsetFilterValue(value)"
          >{{ formatValue(value as any) }}</span
        >
        <i
          data-cy="filter-chip-edit-button"
          class="pi pi-pencil icon-button chip-content"
          style="cursor: pointer"
          @click="
            toggleQuickEditMenu($event);
            setFilterModelOldValue(value);
            resetFilterModel();
          "
        />
        <span v-if="!(index == filterValue!.length - 1)">|</span></span
      >
      <i
        data-cy="filter-chip-add-button"
        class="pi pi-plus-circle icon-button chip-content"
        style="cursor: pointer"
        @click="
          toggleQuickEditMenu($event);
          resetFilterModel();
        "
      />
    </Chip>
    <OverlayPanel
      ref="op"
      data-cy="filter-chip-edit-panel"
      style="padding: 1rem"
      @keypress.enter="
        updateFilter();
        resetFilterModel();
      "
    >
      <NodePropertyInput
        v-model="filterModel"
        :fixed-property-type="true"
        :allow-delete="false"
        form-type="filter"
        :queue="queue"
      >
      </NodePropertyInput>
      <Button
        data-cy="filter-chip-submit-button"
        name="update-filter"
        icon="pi pi-check"
        @click="
          updateFilter();
          toggleQuickEditMenu($event);
          setFilterModelOldValue();
        "
      />
    </OverlayPanel>
  </span>
</template>

<script setup lang="ts">
  import { inject, computed, defineProps, ref, PropType } from "vue";

  import { useFilterStore } from "@/stores/filter";
  import { useCurrentUserSettingsStore } from "@/stores/currentUserSettings";
  import { validAlertFilters } from "@/etc/constants/alerts";
  import { validEventFilters } from "@/etc/constants/events";

  import { isObject } from "@/etc/validators";
  import Button from "primevue/button";
  import Chip from "primevue/chip";
  import OverlayPanel from "primevue/overlaypanel";

  import NodePropertyInput from "@/components/Node/NodePropertyInput.vue";
  import { alertFilterValues } from "@/models/alert";
  import { eventFilterValues } from "@/models/event";

  const currentUserSettingsStore = useCurrentUserSettingsStore();
  const filterStore = useFilterStore();
  const nodeType = inject("nodeType") as "alerts" | "events";

  const queue = computed(() => {
    return currentUserSettingsStore.queues[nodeType] != null
      ? currentUserSettingsStore.queues[nodeType]!.value
      : "unknown";
  });

  const op = ref();
  const toggleQuickEditMenu = (event: unknown) => {
    op.value.toggle(event);
  };

  const setFilterModelOldValue = (
    value?: alertFilterValues | eventFilterValues,
  ) => {
    if (value) {
      filterModelOldValue.value = value;
    } else {
      filterModelOldValue.value = undefined;
    }
  };

  const props = defineProps({
    filterName: { type: String, required: true },
    filterValue: {
      type: Array as PropType<alertFilterValues[] | eventFilterValues[]>,
      required: true,
    },
  });

  const validFilters = {
    alerts: validAlertFilters,
    events: validEventFilters,
  };

  const filterNameObject = validFilters[nodeType]
    ? validFilters[nodeType].find((filter) => {
        return filter.name === props.filterName;
      })
    : null;

  const filterModelOldValue = ref<alertFilterValues | eventFilterValues>();

  const filterModel = ref({
    propertyType: props.filterName,
    propertyValue: undefined as alertFilterValues | eventFilterValues,
  });

  const filterLabel = computed(() => {
    if (filterNameObject) {
      return filterNameObject.label;
    }
    return "";
  });

  function resetFilterModel() {
    filterModel.value = {
      propertyType: props.filterName,
      propertyValue: undefined as alertFilterValues | eventFilterValues,
    };
  }

  function updateFilter() {
    filterStore.unsetFilterValue({
      nodeType: nodeType,
      filterName: props.filterName,
      filterValue: filterModelOldValue.value,
    });
    filterStore.setFilter({
      nodeType: nodeType,
      filterName: props.filterName,
      filterValue: filterModel.value.propertyValue as
        | alertFilterValues
        | eventFilterValues,
    });
  }

  function unsetFilter() {
    filterStore.unsetFilter({
      nodeType: nodeType,
      filterName: props.filterName,
    });
  }

  function unsetFilterValue(value: alertFilterValues | eventFilterValues) {
    filterStore.unsetFilterValue({
      nodeType: nodeType,
      filterName: props.filterName,
      filterValue: value,
    });
  }

  function formatValue(value: alertFilterValues | eventFilterValues) {
    if (filterNameObject) {
      if (filterNameObject.displayRepr) {
        return filterNameObject.displayRepr(value);
      } else if (filterNameObject.stringRepr) {
        return filterNameObject.stringRepr(value);
      } else if (
        filterNameObject.optionProperty &&
        isObject(value) &&
        !("category" in value)
      ) {
        return value[filterNameObject.optionProperty];
      }
    }

    return value;
  }
</script>

<style>
  .filter-name-text {
    font-weight: bold;
  }
  .chip-content {
    margin-left: 2px;
    margin-right: 2px;
  }
  .chip-text {
    font-weight: bold;
    line-height: 1.5;
  }
  .icon-button:hover {
    font-weight: bold;
  }
</style>
