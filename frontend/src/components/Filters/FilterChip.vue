<!-- FilterTag.vue -->
<!-- A tag that shows a currently applied filter (by type, ex. 'queue' or 'owner' -->
<!-- Contains actions to remove/edit/add a filter through click actions or a dropdown menu-->
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
  import { alertFilters } from "@/etc/constants";
  import { isObject } from "@/etc/helpers";
  import Chip from "primevue/chip";

  import { inject, computed, defineProps } from "vue";

  import { useFilterStore } from "@/stores/filter";
  const filterStore = useFilterStore();
  const filterType = inject("filterType");

  const props = defineProps({
    filterName: { type: String, required: true },
    filterValue: { type: Object, required: true },
  });

  const filterNameObject = computed(() => {
    let filterNameObject = alertFilters.find((filter) => {
      return filter.name === props.filterName;
    });
    return filterNameObject ? filterNameObject : null;
  });

  const filterLabel = computed(() => {
    return filterNameObject.value.label;
  });

  function unsetFilter() {
    filterStore.unsetFilter({
      filterType: filterType,
      filterName: props.filterName,
    });
  }

  function formatValue(value) {
    console.log(filterNameObject.value.formatForAPI);
    if (filterNameObject.value.stringRepr) {
      return filterNameObject.value.stringRepr(value);
    } else if (filterNameObject.value.optionProperty && isObject(value)) {
      return value[filterNameObject.value.optionProperty];
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
