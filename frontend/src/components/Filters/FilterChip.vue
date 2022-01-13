<!-- FilterTag.vue -->
<!-- A tag that shows a currently applied filter (by type, ex. 'queue' or 'owner' -->
<!-- Contains actions to remove (and eventually edit/add) a filter through click actions -->
<template>
  <span style="padding: 2px">
    <Chip>
      <span class="p-chip-text filter-name-text">{{ filterLabel }}:</span>
      <span
        class="link-text p-chip-text"
        style="padding-left: 2px; padding-right: 2px; font-weight: bold"
        @click="unsetFilter"
      >
        {{ formatValue(filterValue) }}</span
      >
      <i
        class="pi pi-times-circle"
        style="cursor: pointer"
        @click="unsetFilter"
      />
    </Chip>
  </span>
</template>

<script setup>
  import { inject, computed, defineProps } from "vue";

  import { useFilterStore } from "@/stores/filter";

  import { alertFilters } from "@/etc/constants";
  import { isObject } from "@/etc/helpers";
  import Chip from "primevue/chip";

  const props = defineProps({
    filterName: { type: String, required: true },
    filterValue: { type: [String, Object, Array, Date], required: true },
  });

  const filterStore = useFilterStore();
  const filterType = inject("filterType");
  const filterOptions = filterType === "alerts" ? alertFilters : [];
  const filterNameObject = filterOptions.find((filter) => {
    return filter.name === props.filterName;
  });

  const filterLabel = computed(() => {
    if (filterNameObject) {
      return filterNameObject.label;
    }
    return "";
  });

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
  .chip-text {
    font-weight: bold;
    line-height: 1.5;
  }
</style>
