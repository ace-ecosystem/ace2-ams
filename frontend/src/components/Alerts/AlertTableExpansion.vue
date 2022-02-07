<!-- AlertTableExpansion.vue -->
<!-- Contains logic and functionality for displaying data in alert row dropdown, currently list of alert's observables -->

<template>
  <div v-if="isLoading" style="flex: 1">
    <ul>
      <li><Skeleton width="30%"></Skeleton></li>
      <li><Skeleton width="25%"></Skeleton></li>
      <li><Skeleton width="30%"></Skeleton></li>
      <li><Skeleton width="25%"></Skeleton></li>
    </ul>
  </div>
  <ul v-else>
    <!-- List each observable with link to filter -->
    <li v-for="obs of observables" :key="obs.value">
      <span class="link-text" @click="filterByObservable(obs)">{{
        formatObservable(obs)
      }}</span>
      <!-- Display each observable's tags -->
      <NodeTagVue v-for="tag of obs.tags" :key="tag.value" :tag="tag" />
    </li>
  </ul>
</template>

<script setup>
  import { computed, defineProps } from "vue";
  import Skeleton from "primevue/skeleton";

  import NodeTagVue from "../Node/NodeTag.vue";

  const props = defineProps({
    observables: { type: [Array, null], required: true },
  });

  const isLoading = computed(() => {
    return props.observables === null;
  });

  const formatObservable = (observable) => {
    return `${observable.type.value} : ${observable.value}`;
  };

  import { useFilterStore } from "@/stores/filter";
  const filterStore = useFilterStore();
  const filterByObservable = (observable) => {
    filterStore.bulkSetFilters({
      nodeType: "alerts",
      filters: {
        observable: {
          category: observable.type,
          value: observable.value,
        },
      },
    });
  };
</script>

<style>
  .link-text:hover {
    cursor: pointer;
    text-decoration: underline;
    font-weight: bold;
  }
</style>
