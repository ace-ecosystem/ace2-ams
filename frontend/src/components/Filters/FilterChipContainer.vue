<!-- FilterTagList.vue -->
<!-- A container for tags for all currently applied filters, meant to be displayed in TheFilterToolbar -->
<template>
  <div style="overflow: hidden">
    <FilterChipVue
      v-for="filterName in setFilters"
      :key="filterName"
      :filter-name="filterName"
      :filter-value="filterValue(filterName)"
    >
    </FilterChipVue>
  </div>
</template>

<script setup>
  import FilterChipVue from "@/components/Filters/FilterChip.vue";
  import { inject, computed } from "vue";

  import { useFilterStore } from "@/stores/filter";
  const filterStore = useFilterStore();
  const nodeType = inject("nodeType");

  const setFilters = computed(() => {
    return Object.keys(filterStore[nodeType]);
  });

  function filterValue(filterName) {
    return filterStore[nodeType][filterName];
  }
</script>
