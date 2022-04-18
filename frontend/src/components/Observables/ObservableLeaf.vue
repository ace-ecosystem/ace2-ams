<template>
  <span class="treenode-text" @click="filterByObservable(observable)">{{
    displayValue
  }}</span>

  <span v-if="hasTags(observable)">
    <NodeTagVue
      v-for="tag in observable.tags"
      :key="tag.uuid"
      :tag="tag"
    ></NodeTagVue
  ></span>
</template>

<script setup lang="ts">
  import NodeTagVue from "@/components/Node/NodeTag.vue";

  import { defineProps, computed, PropType } from "vue";

  import { useRouter } from "vue-router";

  import { observableTreeRead } from "@/models/observable";
  import { useFilterStore } from "@/stores/filter";

  const filterStore = useFilterStore();
  const router = useRouter();

  const props = defineProps({
    observable: {
      type: Object as PropType<observableTreeRead>,
      required: true,
    },
  });

  function hasTags(item: observableTreeRead) {
    if ("tags" in item) {
      return item.tags.length;
    }
    return false;
  }

  const displayValue = computed(() => {
    let type = null;
    let value = null;

    try {
      if (
        props.observable.nodeMetadata &&
        props.observable.nodeMetadata.display
      ) {
        if (props.observable.nodeMetadata.display.type) {
          type =
            props.observable.nodeMetadata.display.type +
            " (" +
            props.observable.type.value +
            ")";
        } else {
          type = props.observable.type.value;
        }

        if (props.observable.nodeMetadata.display.value) {
          value = props.observable.nodeMetadata.display.value;
        } else {
          value = props.observable.value;
        }
      } else {
        throw new Error("No observable display metadata given");
      }
    } catch (error) {
      type = props.observable.type.value;
      value = props.observable.value;
    }

    return type + ": " + value;
  });

  function filterByObservable(obs: observableTreeRead) {
    filterStore.bulkSetFilters({
      nodeType: "alerts",
      filters: {
        observable: {
          category: obs.type,
          value: obs.value,
        },
      },
    });
    router.replace({
      path: "/manage_alerts",
    });
  }
</script>
<style scoped>
  .treenode-text:hover {
    cursor: pointer;
    text-decoration: underline;
    font-weight: bold;
  }
</style>
