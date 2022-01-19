<!-- FilterTag.vue -->
<!-- A tag that shows a currently applied filter (by type, ex. 'queue' or 'owner' -->
<!-- Contains actions to remove (and eventually edit/add) a filter through click actions -->
<template>
  <span style="padding: 2px">
    <Chip>
      <span class="p-chip-text filter-name-text chip-content"
        >{{ filterLabel }}:</span
      >
      <span
        class="link-text p-chip-text chip-content"
        style="padding-left: 2px; padding-right: 2px; font-weight: bold"
        @click="unsetFilter"
      >
        {{ formatValue(filterValue) }}</span
      >
      <i
        class="pi pi-pencil icon-button chip-content"
        style="cursor: pointer"
        @click="
          toggleQuickEditMenu($event);
          resetFilterModel();
        "
      />
      <i
        class="pi pi-times-circle icon-button chip-content"
        style="cursor: pointer"
        @click="unsetFilter"
      />
    </Chip>
    <OverlayPanel
      ref="op"
      style="padding: 1rem"
      @keypress.enter="
        updateFilter();
        resetFilterModel();
      "
    >
      <FilterInput
        v-model="filterModel"
        :fixed-filter-name="true"
        :allow-delete="false"
      >
      </FilterInput>
      <Button name="update-filter" icon="pi pi-check" @click="updateFilter();toggleQuickEditMenu($event);" />
    </OverlayPanel>
  </span>
</template>

<script setup>
  import { inject, computed, defineProps, ref } from "vue";

  import { useFilterStore } from "@/stores/filter";

  import { alertFilters } from "@/etc/constants";
  import { isObject } from "@/etc/helpers";
  import Button from "primevue/button";
  import Chip from "primevue/chip";
  import OverlayPanel from "primevue/overlaypanel";

  import FilterInput from "./FilterInput.vue";
  const filterStore = useFilterStore();
  const filterType = inject("filterType");

  const op = ref(null);
  const toggleQuickEditMenu = (event) => {
    op.value.toggle(event);
  };

  const props = defineProps({
    filterName: { type: String, required: true },
    filterValue: { type: [String, Object, Array, Date], required: true },
  });

  const filterOptions = filterType === "alerts" ? alertFilters : [];
  const filterNameObject = filterOptions.find((filter) => {
    return filter.name === props.filterName;
  });

  const filterModel = ref({
    filterName: props.filterName,
    filterValue: props.filterValue,
  });

  const filterLabel = computed(() => {
    if (filterNameObject) {
      return filterNameObject.label;
    }
    return "";
  });

  function resetFilterModel() {
    filterModel.value = {
      filterName: props.filterName,
      filterValue: props.filterValue,
    };
  }

  function updateFilter() {
    filterStore.setFilter({
      filterType: filterType,
      filterName: props.filterName,
      filterValue: filterModel.value.filterValue,
    });
  }

  function unsetFilter() {
    filterStore.unsetFilter({
      filterType: filterType,
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
