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
          <span v-if="isObservable(i)">{{ treeItemName(i) }}</span>

          <span
            v-else
            style="cursor: pointer"
            @click="router.push(viewAnalysisRoute(i))"
            >{{ treeItemName(i) }}</span
          >

          <span v-if="hasTags(i)">
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
          <AlertTree :items="i.children" />
        </div>
      </li>
    </ul>
  </div>
</template>

<script setup>
  import NodeTagVue from "../Node/NodeTag.vue";
  import { onBeforeMount, defineProps, ref } from "vue";
  import { useAlertStore } from "@/stores/alert";
  const alertStore = useAlertStore();
  const openAlertId = ref(alertStore.openAlert.uuid);

  const props = defineProps({
    items: { type: Array, required: true },
  });

  const itemsExpandedStatus = ref({});

  onBeforeMount(() => {
    itemsExpandedStatus.value = generateExpandedStatus(props.items);
  });

  function generateExpandedStatus(items) {
    const expandedStatus = [];
    items.forEach((item, index) => {
      expandedStatus[index] = item.firstAppearance;
    });
    return expandedStatus;
  }
  function nodeExpanded(index) {
    return itemsExpandedStatus.value[index];
  }
  function toggleNodeExpanded(index) {
    itemsExpandedStatus.value[index] = !itemsExpandedStatus.value[index];
  }
  function toggleIcon(index) {
    return [
      "p-tree-toggler-icon pi pi-fw",
      {
        "pi-chevron-down": nodeExpanded(index),
        "pi-chevron-right": !nodeExpanded(index),
      },
    ];
  }

  import { useRouter } from "vue-router";
  const router = useRouter();
  function viewAnalysisRoute(item) {
    return {
      name: "View Analysis",
      params: { alertId: openAlertId.value, analysisID: item.uuid },
    };
  }

  function treeItemName(item) {
    if (isAnalysis(item)) {
      return item.analysisModuleType.value;
    } else {
      let type = null;
      let value = null;

      try {
        if (item.nodeMetadata.display) {
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
        }
      } catch (error) {
        type = item.type.value;
        value = item.value;
      }

      return type + ": " + value;
    }
  }
  function isAnalysis(item) {
    return item.nodeType === "analysis";
  }
  function isObservable(item) {
    return item.nodeType === "observable";
  }

  function containerClass(item) {
    return ["p-treenode", { "p-treenode-leaf": !item.children.length }];
  }

  function hasTags(item) {
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
</style>
