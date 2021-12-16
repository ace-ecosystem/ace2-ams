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
  import { computed, onMounted, onUnmounted, provide } from "vue";
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
  });

  onUnmounted(() => {
    selectedAlertStore.unselectAll();
  });

  const alertTree = computed(() => {
    const tree = arrayToTree(alertStore.openAlert.tree, {
      id: "treeUuid",
      parentId: "parentTreeUuid",
      dataField: null,
    });
    traverseTree({ treeUuid: "root", children: tree });
    return tree;
  });

  // https://www.geeksforgeeks.org/preorder-traversal-of-n-ary-tree-without-recursion/
  function traverseTree(root) {
    let uniqueIds = [];
    let nodes = [];

    nodes.push(root);

    while (nodes.length != 0) {
      let current = nodes.pop();

      if (current != null) {
        if (uniqueIds.includes(current.uuid)) {
          current.firstAppearance = false;
        } else {
          current.firstAppearance = true;
          uniqueIds.push(current.uuid);
        }
        for (let i = current.children.length - 1; i >= 0; i--) {
          nodes.push(current.children[i]);
        }
      }
    }
  }
</script>

<style>
  .p-tree-container {
    margin: 0;
    padding: 0;
    list-style-type: none;
    overflow: auto;
  }
  .p-tree-wrapper {
    overflow: auto;
  }
</style>
