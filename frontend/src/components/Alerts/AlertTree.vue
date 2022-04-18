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
          <span v-if="isObservable(i)">
            <ObservableLeafVue :observable="i"></ObservableLeafVue
          ></span>

          <router-link v-else-if="isAnalysis(i)" :to="viewAnalysisRoute(i)"
            ><span class="treenode-text">{{
              treeItemName(i)
            }}</span></router-link
          >
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
  import ObservableLeafVue from "@/components/Observables/ObservableLeaf.vue";
  import { onBeforeMount, defineProps, ref, PropType } from "vue";
  import { analysisTreeRead } from "@/models/analysis";
  import { observableTreeRead } from "@/models/observable";

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

  function viewAnalysisRoute(item: analysisTreeRead) {
    return {
      name: "View Analysis",
      params: { alertID: props.alertId, analysisID: item.uuid },
    };
  }

  function treeItemName(item: analysisTreeRead | observableTreeRead) {
    if (isAnalysis(item)) {
      return item.analysisModuleType.value;
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
