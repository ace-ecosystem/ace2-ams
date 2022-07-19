<template>
  <!-- <Toolbar>
    <template #start>
      <div style="display: flex; align-items: center">
        <span style="padding-right: 5px">Critical</span>
        <span>
          <InputSwitch v-model="allAnalysis" />
        </span>
        <span style="padding-left: 3px">All Analysis</span>
      </div>
    </template>
    <template #end>
      <Button
        label="Expand All"
        icon="pi pi-plus"
        class="mr-2"
        @click="expandAll"
      />
      <Button
        label="Collapse All"
        icon="pi pi-minus"
        class="mr-2"
        @click="collapseAll"
      />
      <Button
        label="Default"
        icon="pi pi-undo"
        class="mr-2"
        @click="resetExpansion"
      />
    </template>
  </Toolbar> -->
  <!-- <Toolbar>
    <template #start>
      <div style="display: flex; align-items: center">
        <span style="padding-right: 5px">Critical</span>
        <span>
          <InputSwitch v-model="allAnalysis" />
        </span>
        <span style="padding-left: 3px">All Analysis</span>
      </div>
    </template>
  </Toolbar> -->
  <Toolbar>
    <template #start>
      <ToggleButton
        v-model="allAnalysis"
        on-label="Critical Analysis"
        off-label="All Analysis"
      />
    </template>
  </Toolbar>
  <Card style="overflow-x: scroll">
    <template #content>
      <!-- <TabView>
        <TabPanel v-for="tab in tabs" :key="tab.title" :header="tab.title">
          <div class="p-tree p-component p-tree-wrapper" style="border: none">
            <AlertTree
              ref="alertTree"
              id="alert-tree"
              :items="alertStore.open.rootAnalysis.children"
              :alert-id="alertStore.open.uuid"
              :all-analysis="tab.allAnalysis"
            />
            <ScrollTop />
          </div>
        </TabPanel>
      </TabView> -->
      <div class="p-tree p-component p-tree-wrapper" style="border: none">
        <AlertTree
          ref="alertTree"
          id="alert-tree"
          :items="alertStore.open.rootAnalysis.children"
          :alert-id="alertStore.open.uuid"
          :all-analysis="allAnalysis"
        />
        <ScrollTop />
      </div>
    </template>
  </Card>
</template>
<script setup lang="ts">
  import { ref } from "vue";

  import InputSwitch from "primevue/inputswitch";

  import Button from "primevue/button";
  import Card from "primevue/card";
  import ScrollTop from "primevue/scrolltop";
  import Toolbar from "primevue/toolbar";

  import TabView from "primevue/tabview";
  import TabPanel from "primevue/tabpanel";
  import ToggleButton from "primevue/togglebutton";

  import AlertTree from "@/components/Alerts/AlertTree.vue";
  import { useAlertStore } from "@/stores/alert";

  const alertStore = useAlertStore();

  const tabs = ref([
    { title: "Critical Analysis", allAnalysis: false },
    { title: "All Analysis", allAnalysis: true },
  ]);

  // allAnalysis: true;
  // criticalAnalysis: false;
  const allAnalysis = ref(false);

  const alertTree = ref<InstanceType<typeof AlertTree>>();
  function collapseAll() {
    alertTree.value?.collapseAll();
  }
  function expandAll() {
    alertTree.value?.expandAll();
  }
  function resetExpansion() {
    alertTree.value?.resetExpansion();
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
