<template>
  <div>
    <ul class="p-tree-container">
      <li
        v-for="(i, index) of items"
        :id="`ID-${i.treeUuid}`"
        :key="i.treeUuid"
        :class="containerClass(i)"
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
          <router-link v-else :to="getAnalysisLink(i)">{{
            treeItemName(i)
          }}</router-link>
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

  import { defineProps, ref } from "vue";

  const props = defineProps({
    items: { type: Array, required: true },
  });

  const itemsExpandedStatus = ref({});

  props.items.forEach((item, index) => {
    itemsExpandedStatus.value[index] = item.firstAppearance ? true : false;
  });

  function nodeExpanded(index) {
    return itemsExpandedStatus.value[index];
  }

  function toggleNodeExpanded(index) {
    itemsExpandedStatus.value[index] = !itemsExpandedStatus.value[index];
  }

  function containerClass(item) {
    return ["p-treenode", { "p-treenode-leaf": !item.children.length }];
  }

  function getAnalysisLink(item) {
    return "/analysis/" + item.uuid;
  }

  function isAnalysis(item) {
    return "analysisModuleType" in item;
  }
  function isObservable(item) {
    return "forDetection" in item;
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

  function treeItemName(item) {
    if (isAnalysis(item)) {
      return item.analysisModuleType.value;
    }

    if (isObservable(item)) {
      return item.type.value + ": " + item.value;
    }
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
