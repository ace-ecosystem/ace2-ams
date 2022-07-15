<!-- ViewAlert.vue -->

<template>
  <div v-if="error" class="p-col">
    <Message severity="error" data-cy="error-message" @close="handleError">{{
      error
    }}</Message>
  </div>
  <div style="position: sticky; top: 3.5em; z-index: 1">
    <TheAlertActionToolbar
      reload-object="object"
      :show-false-positive-shortcut="true"
      :show-ignore-shortcut="true"
      @false-positive-clicked="dispositionAlert('falsePositive')"
      @ignore-clicked="dispositionAlert('ignore')"
    />
  </div>
  <div v-if="alertStore.open">
    <TheAlertSummary />
    <br />
    <AlertMatchingOpenEventsPanel />
    <br />
    <!-- <Panel header="Summary Details" :toggleable="true" :collapsed="true">
      <div v-for="details in alertStore.open.rootAnalysis.Details">
        <AnalysisSummaryDetail />
      </div>
    </Panel> -->
    <br />
    <TheAlertDetails />
    <br />
    <AlertUrlDomainSummary :alert-uuid="alertID" />
    <br />
    <Card style="overflow-x: scroll">
      <template #content>
        <div class="p-tree p-component p-tree-wrapper" style="border: none">
          <AlertTree
            id="alert-tree"
            :items="alertStore.open.rootAnalysis.children"
            :alert-id="alertID"
          />
          <ScrollTop />
        </div>
      </template>
    </Card>
  </div>
</template>

<script setup lang="ts">
  import { onBeforeMount, onUnmounted, provide, inject, ref } from "vue";
  import { useRoute } from "vue-router";

  import Card from "primevue/card";
  import Message from "primevue/message";
  import ScrollTop from "primevue/scrolltop";

  import TheAlertActionToolbar from "@/components/Alerts/TheAlertActionToolbar.vue";
  import AlertUrlDomainSummary from "@/components/Alerts/AlertUrlDomainSummary.vue";
  import AlertMatchingOpenEventsPanel from "@/components/Alerts/AlertMatchingOpenEventsPanel.vue";
  import AlertTree from "@/components/Alerts/AlertTree.vue";
  import TheAlertSummary from "@/components/Alerts/TheAlertSummary.vue";
  import TheAlertDetails from "@/components/Alerts/TheAlertDetails.vue";
  import { useAlertStore } from "@/stores/alert";
  import { useAuthStore } from "@/stores/auth";
  import { useSelectedAlertStore } from "@/stores/selectedAlert";
  import AnalysisSummaryDetail from "@/components/Analysis/AnalysisSummaryDetail.vue";

  const authStore = useAuthStore();
  const route = useRoute();
  const alertStore = useAlertStore();
  const selectedAlertStore = useSelectedAlertStore();
  const alertID = route.params.alertID! as string;
  const config = inject("config") as Record<string, any>;
  const error = ref<string>();

  provide("objectType", "alerts");

  onBeforeMount(async () => {
    await initPage();
  });

  onUnmounted(() => {
    selectedAlertStore.unselectAll();
  });

  const dispositionAlert = async (disposition: "falsePositive" | "ignore") => {
    let dispositionString;

    if (disposition == "falsePositive") {
      dispositionString = config.alerts.FALSE_POSITIVE_DISPOSITION_STRING;
    } else {
      dispositionString = config.alerts.IGNORE_DISPOSITION_STRING;
    }
    if (dispositionString) {
      try {
        await alertStore.update([
          {
            uuid: alertID,
            disposition: dispositionString,
            historyUsername: authStore.user.username,
          },
        ]);
        await reloadPage();
      } catch (e: unknown) {
        if (typeof e === "string") {
          error.value = e;
        } else if (e instanceof Error) {
          error.value = e.message;
        }
      }
    } else {
      error.value = `Contact admin: disposition could not be set; string for '${disposition}' must be configured`;
    }
  };

  alertStore.$subscribe(async (_, state) => {
    if (state.requestReload) {
      await reloadPage();
    }
  });

  async function reloadPage() {
    alertStore.$reset();
    await alertStore.read(alertID);
  }

  async function initPage() {
    selectedAlertStore.unselectAll();
    selectedAlertStore.select(alertID);
    alertStore.$reset();
    await alertStore.read(alertID);
  }
  const handleError = () => {
    error.value = undefined;
    close();
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
