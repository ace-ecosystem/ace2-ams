<template>
  <div>
    <ul>
      <li v-for="i of items" :id="`ID-${i.treeUuid}`" :key="i.treeUuid">
        <span>
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

        <div>
          <AlertTree :items="i.children" />
        </div>
        <div v-if="showJumpToAnalysis(i)">
          <button @click="jumpToAnalysis(i)">Jump To Analysis</button>
        </div>
      </li>
    </ul>
  </div>
</template>

<script setup>
  import NodeTagVue from "../Node/NodeTag.vue";

  import { defineProps, inject } from "vue";

  const observableRefs = inject("observableRefs");

  const props = defineProps({
    items: { type: Array, required: true },
  });

  function getReferenceObservable(item) {
    if (!observableRefs.value) {
      return null;
    }
    if (observableRefs.value[item.uuid] == item.treeUuid) {
      return "self";
    }
    return observableRefs.value[item.uuid];
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

  function showJumpToAnalysis(item) {
    return isObservable(item) && getReferenceObservable(item) != "self";
  }

  function jumpToAnalysis(item) {
    const reference = getReferenceObservable(item);

    let element = document.querySelector(`#ID-${reference}`);
    element.scrollIntoView({ behavior: "smooth" });
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
