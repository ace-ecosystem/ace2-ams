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
        class="pi pi-pencil"
        style="cursor: pointer"
        @click="toggleOptionsMenu"
      />
      <i
        class="pi pi-times-circle"
        style="cursor: pointer"
        @click="unsetFilter"
      />
    </Chip>
    <OverlayPanel ref="op"  tabindex="1" @keypress.enter="updateFilter">
      <FilterInput
      tabindex="1" 
        v-model="filterModel"
        :fixed-filter-name="true"
        :allow-delete="false"
      >
      </FilterInput>
      <Button
        name="update-filter"
        icon="pi pi-check"
        tabindex="1" 
        @click="updateFilter"
      />
    </OverlayPanel>
  </span>
</template>

<script setup>
  import { alertFilters } from "@/etc/constants";
  import { isObject } from "@/etc/helpers";
  import Button from "primevue/button";
  import Chip from "primevue/chip";
  import OverlayPanel from "primevue/overlaypanel";
  import Dropdown from "primevue/dropdown";

  import { inject, computed, defineProps, ref } from "vue";

  import { useFilterStore } from "@/stores/filter";
  import FilterInput from "./FilterInput.vue";
import { reset } from "mockdate";
  const filterStore = useFilterStore();
  const filterType = inject("filterType");

  const op = ref(null);
  const toggleOptionsMenu = (event) => {
    op.value.toggle(event);
    resetFilterModel();
  };

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

  const filterModel = ref({
    filterName: props.filterName,
    filterValue: props.filterValue,
  });

  const filterLabel = computed(() => {
    return filterNameObject.value.label;
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
    toggleOptionsMenu();
  }

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
