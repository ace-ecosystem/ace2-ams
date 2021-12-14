<template>
  <div>
    <ul class="p-tree-container">
      <li :class="containerClass(i)" v-for="(i, index) of items" :id="`ID-${i.treeUuid}`" :key="i.treeUuid">
        
        
        <span class="p-treenode-content">
          <span v-if="!i.children.length"> <i class="pi pi-fw pi-minus" ></i> 
          </span>
          <span v-else>
          <button :class="p-ripple" type="button" class=" p-link" @click="toggleNodeExpanded(index)" tabindex="-1" >
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

        <div class="p-treenode-children" v-if="nodeExpanded(index)">
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

  import { defineProps, inject, ref } from "vue";

  const observableRefs = inject("observableRefs");

  const props = defineProps({
    items: { type: Array, required: true },
  });

  let itemsExpandedStatus = ref({})
  
  props.items.forEach((el, index) => {
    itemsExpandedStatus.value[index] = true;
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

  function nodeExpanded(index) {
    return itemsExpandedStatus.value[index];
  }

  function toggleNodeExpanded(index) {
    itemsExpandedStatus.value[index] = !itemsExpandedStatus.value[index]
  }

  function containerClass(item) {
     return ['p-treenode', {'p-treenode-leaf': !item.children.length}];
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


  function toggleIcon(index) {
            return ['p-tree-toggler-icon pi pi-fw', {
                'pi-chevron-down': nodeExpanded(index),
                'pi-chevron-right': !nodeExpanded(index)
            }];
            
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

<style>
.p-tree-container {
    margin: 0;
    padding: 0;
    list-style-type: none;
    overflow: auto;
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
    margin-top: -.5rem;
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