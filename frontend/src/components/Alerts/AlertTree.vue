<template>
  <div>
    <ul class="p-tree-container">
      <li
        v-for="(i, index) of items"
        :id="`ID-${i.treeUuid}`"
        :key="i.treeUuid"
        :class="containerClass(i)"
        :data-cy="treeItemName(i)"
      >
        <span class="p-treenode-content">
          <span v-if="!i.children.length">
            <i class="pi pi-fw pi-minus"></i>
          </span>
          <span v-else>
            <button
              type="button"
              class="p-link"
              tabindex="-1"
              @click="toggleNodeExpanded(index)"
            >
              <span :class="toggleIcon(index)"></span>
            </button>
          </span>
          <span
            v-if="isObservable(i)"
            class="treenode-text"
            @click="filterByObservable(i)"
            >{{ treeItemName(i) }}</span
          >

          <router-link v-else-if="isAnalysis(i)" :to="viewAnalysisRoute(i)"
            ><span class="treenode-text">{{
              treeItemName(i)
            }}</span></router-link
          >

          <span v-if="hasTags(i) && isObservable(i)">
            <NodeTagVue
              v-for="tag in i.tags"
              :key="tag.uuid"
              :tag="tag"
            ></NodeTagVue>
          </span>
        </span>

        <div
          v-if="nodeExpanded(index) && i.children.length"
          class="p-treenode-children"
        >
          <AlertTree :items="i.children" :alert-id="alertId" />
        </div>
      </li>
    </ul>
  </div>
</template>

<script setup lang="ts">
  import { useRouter } from "vue-router";
  import NodeTagVue from "@/components/Node/NodeTag.vue";
  import { onBeforeMount, defineProps, ref, PropType } from "vue";
  import { analysisTreeRead } from "@/models/analysis";
  import { observableTreeRead } from "@/models/observable";
  import { useFilterStore } from "@/stores/filter";

  const props = defineProps({
    items: {
      type: Array as PropType<(analysisTreeRead | observableTreeRead)[]>,
      required: true,
    },
    alertId: {
      type: String,
      required: true,
    },
  });

  const itemsExpandedStatus = ref<Record<number, boolean>>({});

  onBeforeMount(() => {
    itemsExpandedStatus.value = generateExpandedStatus(props.items);
  });

  function generateExpandedStatus(
    items: (analysisTreeRead | observableTreeRead)[],
  ) {
    const expandedStatus: Record<number, boolean> = {};
    items.forEach((item, index) => {
      expandedStatus[index] = item.firstAppearance
        ? item.firstAppearance
        : false;
    });
    return expandedStatus;
  }
  function nodeExpanded(index: number) {
    return itemsExpandedStatus.value[index];
  }
  function toggleNodeExpanded(index: number) {
    itemsExpandedStatus.value[index] = !itemsExpandedStatus.value[index];
  }
  function toggleIcon(index: number) {
    return [
      "p-tree-toggler-icon pi pi-fw",
      {
        "pi-chevron-down": nodeExpanded(index),
        "pi-chevron-right": !nodeExpanded(index),
      },
    ];
  }

  const router = useRouter();
  function viewAnalysisRoute(item: analysisTreeRead) {
    return {
      name: "View Analysis",
      params: { alertID: props.alertId, analysisID: item.uuid },
    };
  }

  const filterStore = useFilterStore();
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

  function treeItemName(item: analysisTreeRead | observableTreeRead) {
    if (isAnalysis(item)) {
      return item.analysisModuleType.value;
    } else {
      let type = null;
      let value = null;

      try {
        if (item.nodeMetadata && item.nodeMetadata.display) {
          if (item.nodeMetadata.display.type) {
            type =
              item.nodeMetadata.display.type + " (" + item.type.value + ")";
          } else {
            type = item.type.value;
          }

          if (item.nodeMetadata.display.value) {
            value = item.nodeMetadata.display.value;
          } else {
            value = item.value;
          }
        } else {
          throw new Error("No observable display metadata given");
        }
      } catch (error) {
        type = item.type.value;
        value = item.value;
      }

      return type + ": " + value;
    }
  }
  function isAnalysis(
    item: analysisTreeRead | observableTreeRead,
  ): item is analysisTreeRead {
    return item.nodeType === "analysis";
  }
  function isObservable(
    item: analysisTreeRead | observableTreeRead,
  ): item is observableTreeRead {
    return item.nodeType === "observable";
  }

  function containerClass(item: analysisTreeRead | observableTreeRead) {
    return ["p-treenode", { "p-treenode-leaf": !item.children.length }];
  }

  function hasTags(item: analysisTreeRead | observableTreeRead) {
    if ("tags" in item) {
      return item.tags.length;
    }
    return false;
  }
</script>

<style>
  .p-treenode-children {
    margin: 0;
    padding: 0;
    list-style-type: none;
  }
  .p-tree-toggler {
    cursor: pointer;
    user-select: none;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;
    position: relative;
  }
  .p-treenode-leaf > .p-treenode-content .p-tree-toggler {
    visibility: hidden;
  }
  .p-treenode-content {
    display: flex;
    align-items: center;
  }
  .treenode-text:hover {
    cursor: pointer;
    text-decoration: underline;
    font-weight: bold;
  }
</style>
