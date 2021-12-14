<template>
  <router-link class="p-m-1" to="/manage_alerts"
    ><Chip @click="filterByTag"
      ><span class="p-chip-text">{{ tag.value }}</span></Chip
    ></router-link
  >
</template>

<script setup lang="ts">
  import Chip from "primevue/chip";

  import { defineProps, inject } from "vue";

  import { useFilterStore } from "@/stores/filter";
  const filterStore = useFilterStore();
  const filterType = inject("filterType");

  const props = defineProps({
    tag: { type: Object, required: true },
  });

  const filterByTag = () => {
    filterStore.setFilter({
      filterType: filterType,
      filterName: "tags",
      filterValue: props.tag,
    });
  };
</script>
