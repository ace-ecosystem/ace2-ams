<!-- ViewAlert.vue -->

<template>
  <Card>
    <template #content>
      <div class="p-tree p-component p-tree-wrapper" style="border: none">
        <AlertTree v-if="alertStore.openAlert" :items="alertTree" />
      </div>
    </template>
  </Card>
</template>

<script setup>
  import {
    computed,
    onMounted,
    onUnmounted,
    provide,
    ref,
    readonly,
  } from "vue";
  import Card from "primevue/card";
  import { useRoute } from "vue-router";
  import { arrayToTree } from "performant-array-to-tree";

  import AlertTree from "@/components/Alerts/AlertTree";
  import { useAlertStore } from "@/stores/alert";
  import { useSelectedAlertStore } from "@/stores/selectedAlert";

  const alertStore = useAlertStore();
  const selectedAlertStore = useSelectedAlertStore();

  provide("filterType", "alerts");

  onMounted(async () => {
    selectedAlertStore.unselectAll();
    selectedAlertStore.select(useRoute().params.alertID);

    alertStore.$reset();
    await alertStore.read(useRoute().params.alertID);

    alertTree.value.forEach((node) => {
      traverseTree(node);
    });
  });

  onUnmounted(() => {
    selectedAlertStore.unselectAll();
  });

  const alertTree = computed(() =>
    arrayToTree(alertStore.openAlert.tree, {
      id: "treeUuid",
      parentId: "parentTreeUuid",
      dataField: null,
    }),
  );

  let observableRefs = ref({});

  function traverseTree(node) {
    if (!(node.uuid in observableRefs.value) && "forDetection" in node) {
      observableRefs.value[node.uuid] = node.treeUuid;
    }
    if (node.children.length) {
      node.children.forEach((child) => {
        traverseTree(child);
      });
    }
  }

  provide("observableRefs", readonly(observableRefs));
</script>

<style>
  .p-tree-container {
    margin: 0;
    padding: 0;
    list-style-type: none;
    overflow: auto;
  }
  .p-tree {
    border: none;
  }
  .p-treenode-children {
    margin: 0;
    padding: 0;
    list-style-type: none;
  }
  .p-tree-wrapper {
    overflow: auto;
  }
  .p-treenode-selectable {
    cursor: pointer;
    user-select: none;
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
  .p-tree-filter {
    width: 100%;
  }
  .p-tree-filter-container {
    position: relative;
    display: block;
    width: 100%;
  }
  .p-tree-filter-icon {
    position: absolute;
    top: 50%;
    margin-top: -0.5rem;
  }
  .p-tree-loading {
    position: relative;
    min-height: 4rem;
  }
  .p-tree .p-tree-loading-overlay {
    position: absolute;
    z-index: 1;
    display: flex;
    align-items: center;
    justify-content: center;
  }
  .p-tree-flex-scrollable {
    display: flex;
    flex: 1;
    height: 100%;
    flex-direction: column;
  }
  .p-tree-flex-scrollable .p-tree-wrapper {
    flex: 1;
  }
</style>
