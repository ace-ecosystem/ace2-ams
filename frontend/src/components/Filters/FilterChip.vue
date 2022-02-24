<!-- FilterTag.vue -->
<!-- A tag that shows a currently applied filter (by type, ex. 'queue' or 'owner' -->
<!-- Contains actions to remove (and eventually edit/add) a filter through click actions -->
<template>
  <span style="padding: 2px" data-cy="filter=chip">
    <Chip>
      <span class="p-chip-text filter-name-text chip-content"
        >{{ filterLabel }}:</span
      >
      <span
        data-cy="filter-chip-content"
        class="link-text p-chip-text chip-content"
        style="padding-left: 2px; padding-right: 2px; font-weight: bold"
        @click="unsetFilter"
      >
        {{ formatValue(filterValue) }}</span
      >
      <i
        data-cy="filter-chip-edit-button"
        class="pi pi-pencil icon-button chip-content"
        style="cursor: pointer"
        @click="
          toggleQuickEditMenu($event);
          resetFilterModel();
        "
      />
      <i
        data-cy="filter-chip-remove-button"
        class="pi pi-times-circle icon-button chip-content"
        style="cursor: pointer"
        @click="unsetFilter"
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
      >
      </NodePropertyInput>
      <Button
        data-cy="filter-chip-submit-button"
        name="update-filter"
        icon="pi pi-check"
        @click="
          updateFilter();
          toggleQuickEditMenu($event);
        "
      />
    </OverlayPanel>
  </span>
</template>

<script setup>
  import { inject, computed, defineProps, ref } from "vue";

  import { useFilterStore } from "@/stores/filter";

  import { isObject } from "@/etc/validators";
  import Button from "primevue/button";
  import Chip from "primevue/chip";
  import OverlayPanel from "primevue/overlaypanel";

  import NodePropertyInput from "../Node/NodePropertyInput.vue";
  const filterStore = useFilterStore();
  const nodeType = inject("nodeType");

  const config = inject("config");

  const op = ref(null);
  const toggleQuickEditMenu = (event) => {
    op.value.toggle(event);
  };

  const props = defineProps({
    filterName: { type: String, required: true },
    filterValue: { type: [String, Object, Array, Date], required: true },
  });

  const availableFilters = {
    alerts: config.alerts.alertFilters,
    events: config.events.eventFilters,
  };
  const filterOptions =
    nodeType in availableFilters ? availableFilters[nodeType] : [];
  const filterNameObject = filterOptions.find((filter) => {
    return filter.name === props.filterName;
  });

  const filterModel = ref({
    propertyType: props.filterName,
    propertyValue: props.filterValue,
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
      propertyValue: props.filterValue,
    };
  }

  function updateFilter() {
    filterStore.setFilter({
      nodeType: nodeType,
      filterName: props.filterName,
      filterValue: filterModel.value.propertyValue,
    });
  }

  function unsetFilter() {
    filterStore.unsetFilter({
      nodeType: nodeType,
      filterName: props.filterName,
    });
  }

  function formatValue(value) {
    if (filterNameObject) {
      if (filterNameObject.stringRepr) {
        return filterNameObject.stringRepr(value);
      } else if (filterNameObject.optionProperty && isObject(value)) {
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
