<!-- TheAlertsTable.vue -->
<!-- The table where all currently filtered alerts are displayed, selected to take action, or link to an individual alert page -->

<template>
  <ul>
    <!-- List each observable with link to filter -->
    <li v-for="obs of observables" :key="obs.value">
      <span class="link-text" @click="filterByObservable(obs)">{{
        formatObservable(obs)
      }}</span>
      <!-- Display each observable's -->
      <NodeTagVue v-for="tag of obs.tags" :key="tag.value" :tag="tag" />
    </li>
  </ul>
</template>

<script setup>
  import { ref, defineProps, onMounted } from "vue";

  import NodeTagVue from "../Node/NodeTag.vue";

  import { NodeTree } from "@/services/api/nodeTree";

  const observables = ref(null);

  onMounted(async () => {
    await getObservables(props.uuid);
  });

  const props = defineProps({
    uuid: { type: String, required: true },
  });

  const getObservables = async (uuid) => {
    const unsortedObservables = await NodeTree.readNodesOfNodeTree(
      [uuid],
      "observable",
    );

    observables.value = unsortedObservables.sort((a, b) => {
      if (a.type.value === b.type.value) {
        return a.value < b.value ? -1 : 1;
      } else {
        return a.type.value < b.type.value ? -1 : 1;
      }
    });
  };

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
