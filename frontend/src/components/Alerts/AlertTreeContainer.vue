<template>
  <Toolbar>
    <template #start>
      <div style="display: flex; align-items: center">
        <span>
          <Checkbox v-model="criticalOnly" :binary="true" />
        </span>
        <span style="padding-left: 3px"
          ><b>Critical Analysis </b
          ><i
            v-tooltip="'Hide irrelevant data points'"
            class="pi pi-question-circle"
          ></i
        ></span>
      </div>
    </template>
    <template #end>
      <Button
        label="Expand All"
        icon="pi pi-angle-double-down"
        class="mr-2"
        @click="expandAll"
      />
      <Button
        label="Collapse All"
        icon="pi pi-angle-double-up"
        class="mr-2"
        @click="collapseAll"
      />
    </template>
  </Toolbar>
  <Card style="overflow-x: scroll">
    <template #content>
      <div class="p-tree p-component p-tree-wrapper" style="border: none">
        <AlertTreeVue
          id="alert-tree"
          ref="tree"
          :items="alertStore.open.rootAnalysis.children"
          :alert-id="alertStore.open.uuid"
          :critical-only="criticalOnly"
        />
        <ScrollTop />
      </div>
    </template>
  </Card>
</template>
<script setup lang="ts">
  import { ref } from "vue";

  import Checkbox from "primevue/checkbox";

  import Button from "primevue/button";
  import Card from "primevue/card";
  import ScrollTop from "primevue/scrolltop";
  import Toolbar from "primevue/toolbar";

  import AlertTreeVue from "@/components/Alerts/AlertTree.vue";
  import { useAlertStore } from "@/stores/alert";

  const alertStore = useAlertStore();

  const criticalOnly = ref(true);

  const tree = ref<InstanceType<typeof AlertTreeVue>>();
  const collapseAll = () => {
    tree.value?.collapseAll();
  };
  const expandAll = () => {
    tree.value?.expandAll();
  };
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
