<template>
  <div>
    <ul class="p-tree-container">
      <li
        v-for="(i, index) of items"
        :id="`${i.leafId}`"
        :key="`${i.leafId}`"
        :class="containerClass(i)"
        :data-cy="treeItemName(i)"
      >
        <!-- <span v-if="leafVisible(index)" class="p-treenode-content"> -->
        <span class="p-treenode-content">
          <span v-if="!i.children.length">
            <i class="pi pi-fw pi-minus"></i>
          </span>
          <span v-else>
            <button
              type="button"
              class="p-link"
              tabindex="-1"
              @click="toggleLeafExpanded(index)"
            >
              <span :class="toggleIcon(index)"></span>
            </button>
          </span>
          <ObservableLeafVue
            v-if="isObservable(i)"
            :observable="i"
          ></ObservableLeafVue>

          <router-link v-else-if="isAnalysis(i)" :to="viewAnalysisRoute(i)"
            ><span class="treenode-text">{{
              treeItemName(i)
            }}</span></router-link
          >
        </span>

        <div
          v-if="leafVisible(index) && i.children.length"
          v-show="leafVisible(index) && leafExpanded(index)"
          class="p-treenode-children"
        >
          <AlertTree
            ref="childTree"
            :items="i.children"
            :alert-id="alertId"
            :critical-only="criticalOnly"
          />
        </div>
      </li>
    </ul>
  </div>
</template>

<script setup lang="ts">
  import ObservableLeafVue from "@/components/Observables/ObservableLeaf.vue";
  import {
    onBeforeMount,
    computed,
    defineProps,
    defineExpose,
    ref,
    PropType,
    watch,
  } from "vue";
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
    criticalOnly: {
      type: Boolean,
      required: true,
    },
  });

  const childExpandedStatus = ref<Record<number, boolean>>({});
  const childTree = ref<any>();

  onBeforeMount(() => {
    resetExpansion();
  });

  watch(
    () => props.criticalOnly,
    () => {
      resetExpansion();
    },
  );

  function generateExpandedStatus(
    items: (analysisTreeRead | observableTreeRead)[],
  ) {
    const expandedStatus: Record<number, boolean> = {};
    items.forEach((_, index) => {
      expandedStatus[index] = true;
    });
    return expandedStatus;
  }

  const childVisibleStatus = computed(() => {
    const visibleStatus: Record<number, boolean> = {};
    if (props.criticalOnly) {
      props.items.forEach((item, index) => {
        visibleStatus[index] = item.criticalPath ? item.criticalPath : false;
      });
    } else {
      props.items.forEach((item, index) => {
        visibleStatus[index] = true;
      });
    }
    console.log(visibleStatus);
    return visibleStatus;
  });

  function expandAll() {
    Object.keys(childExpandedStatus.value).forEach((key: any) => {
      childExpandedStatus.value[key] = true;
    });
    if (Array.isArray(childTree.value)) {
      childTree.value?.forEach((tree: any) => {
        tree.expandAll();
      });
    } else {
      childTree.value?.expandAll();
    }
  }
  function collapseAll() {
    Object.keys(childExpandedStatus.value).forEach((key: any) => {
      childExpandedStatus.value[key] = false;
    });
    if (Array.isArray(childTree.value)) {
      childTree.value?.forEach((tree: any) => {
        tree.collapseAll();
      });
    } else {
      childTree.value?.collapseAll();
    }
  }
  function resetExpansion() {
    childExpandedStatus.value = generateExpandedStatus(props.items);
    if (Array.isArray(childTree.value)) {
      childTree.value?.forEach((tree: any) => {
        tree.resetExpansion();
      });
    } else {
      childTree.value?.resetExpansion();
    }
  }
  function leafExpanded(index: number) {
    return childExpandedStatus.value[index];
  }
  function leafVisible(index: number) {
    return childVisibleStatus.value[index];
  }
  function toggleLeafExpanded(index: number) {
    childExpandedStatus.value[index] = !childExpandedStatus.value[index];
  }
  function toggleIcon(index: number) {
    if (!leafVisible(index)) {
      return ["p-tree-toggler-icon pi pi-fw", "pi pi-fw pi-minus"];
    }
    return [
      "p-tree-toggler-icon pi pi-fw",
      {
        "pi-chevron-down": leafExpanded(index),
        "pi-chevron-right": !leafExpanded(index),
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
    if (isAnalysis(item) && item.analysisModuleType) {
      return item.analysisModuleType.value;
    }
  }

  function isAnalysis(
    item: analysisTreeRead | observableTreeRead,
  ): item is analysisTreeRead {
    return item.objectType === "analysis";
  }
  function isObservable(
    item: analysisTreeRead | observableTreeRead,
  ): item is observableTreeRead {
    return item.objectType === "observable";
  }

  function containerClass(item: analysisTreeRead | observableTreeRead) {
    return ["p-treenode", { "p-treenode-leaf": !item.children.length }];
  }

  defineExpose({
    collapseAll,
    expandAll,
  });
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
