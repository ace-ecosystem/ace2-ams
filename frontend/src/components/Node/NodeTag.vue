<template>
  <router-link class="p-m-1" to="/manage_alerts"
    ><Chip @click="filterByTag"
      ><span class="p-chip-text">{{ tag.value }}</span></Chip
    ></router-link
  >
</template>

<script setup>
  import Chip from "primevue/chip";

  import { inject, defineProps } from "vue";
  const props = defineProps({
    tag: { type: Object, required: true },
  });

  import { useFilterStore } from "@/stores/filter";
  const filterStore = useFilterStore();
  const filterType = inject("filterType");
  function filterByTag() {
    filterStore.setFilter({
      filterType: filterType,
      filterName: "tags",
      filterValue: props.tag,
    });
  }
</script>
