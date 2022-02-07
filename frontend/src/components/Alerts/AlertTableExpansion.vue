<!-- AlertTableExpansion.vue -->
<!-- Contains logic and functionality for displaying data in alert row dropdown, currently list of alert's observables -->

<template>
  <ul>
    <!-- List each observable with link to filter -->
    <li v-for="obs of props.observables" :key="obs.value">
      <span class="link-text" @click="filterByObservable(obs)">{{
        formatObservable(obs)
      }}</span>
      <!-- Display each observable's tags -->
      <NodeTagVue v-for="tag of obs.tags" :key="tag.value" :tag="tag" />
    </li>
  </ul>
</template>

<script setup>
  import { defineProps } from "vue";
  import NodeTagVue from "../Node/NodeTag.vue";

  const props = defineProps({
    observables: { type: Array, required: true },
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
