<!-- TheAlertDetails.vue -->

<template>
  <Message v-if="error" severity="error" data-cy="error-message">{{
    error
  }}</Message>

  <Card v-if="alertStore.openAlertSummary">
    <template #title>
      {{ alertStore.open.name }}
      <Button
        icon="pi pi-link"
        class="p-button-secondary p-button-outlined p-button-sm"
        @click="copyLink"
      />
      <NodeTagVue
        v-for="tag in getAllAlertTags(alertStore.open)"
        :key="tag.uuid"
        :tag="tag"
      ></NodeTagVue>
    </template>

    <template #content>
      <Accordion :active-index="0">
        <AccordionTab header="Details">
          <div class="p-datatable-wrapper">
            <table class="p-datatable p-datatable-sm full-size-table">
              <tbody class="p-datatable-tbody">
                <tr v-for="key in alertDetailKeys" :key="key.value">
                  <td class="header-cell">{{ key.label }}</td>
                  <td class="content-cell">
                    <AlertTableCell
                      :field="key.value"
                      :data="alertStore.openAlertSummary"
                    ></AlertTableCell>
                  </td>
                </tr>
                <tr v-if="!alertDetectionPoints.length && !isLoading">
                  <td class="header-cell">No detections found</td>
                  <td></td>
                </tr>
                <tr v-if="isLoading">
                  <td class="header-cell">Loading detections...</td>
                  <td></td>
                </tr>
                <tr
                  v-for="detection in alertDetectionPoints"
                  :key="detection.uuid"
                >
                  <td class="header-cell">Detection</td>
                  <td class="content-cell">
                    {{ detection.value }}
                  </td>
                </tr>
                <tr v-if="alertStore.open['instructions']">
                  <td class="header-cell">Instructions</td>
                  <td class="content-cell">
                    {{ alertStore.open["instructions"] }}
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </AccordionTab>
      </Accordion>
    </template>
  </Card>
</template>

<script setup lang="ts">
  import Accordion from "primevue/accordion";
  import AccordionTab from "primevue/accordiontab";
  import Button from "primevue/button";
  import Card from "primevue/card";
  import Message from "primevue/message";

  import NodeTagVue from "@/components/Node/NodeTag.vue";

  import { copyToClipboard } from "@/etc/helpers";
  import { useAlertStore } from "@/stores/alert";
  import { getAllAlertTags } from "@/etc/helpers";
  import AlertTableCell from "./AlertTableCell.vue";
  import { alertSummary } from "@/models/alert";
  import { observableRead } from "@/models/observable";
  import { NodeTree } from "@/services/api/nodeTree";
  import { onMounted, ref } from "@pinia/testing/node_modules/vue-demi";
  import { nodeDetectionPointRead } from "@/models/nodeDetectionPoint";

  const alertStore = useAlertStore();

  const alertDetailKeys: { value: keyof alertSummary; label: string }[] = [
    { value: "insertTime", label: "Insert Time" },
    { value: "eventTime", label: "Event Time" },
    { value: "tool", label: "Tool" },
    { value: "toolInstance", label: "Tool Instance" },
    { value: "type", label: "Type" },
    { value: "disposition", label: "Disposition" },
    { value: "eventUuid", label: "Event" },
    { value: "queue", label: "Queue" },
    { value: "owner", label: "Owner" },
    { value: "comments", label: "Comments" },
  ];

  const alertDetectionPoints = ref<nodeDetectionPointRead[]>([]);
  const isLoading = ref(false);
  const error = ref<string>();

  onMounted(async () => {
    if (alertStore.openAlertSummary) {
      isLoading.value = true;
      await getAllDetectionPoints(alertStore.openAlertSummary.uuid);
      isLoading.value = false;
    }
  });
//todo convert to computed
  const getAllDetectionPoints = async (uuid: string) => {
    try {
      const unsortedObservables = (await NodeTree.readNodesOfNodeTree(
        [uuid],
        "observable",
      )) as unknown as observableRead[];

      unsortedObservables.forEach((observable) => {
        alertDetectionPoints.value = [
          ...alertDetectionPoints.value,
          ...observable.detectionPoints,
        ];
      });
    } catch (e: unknown) {
      if (typeof e === "string") {
        error.value = e;
      } else if (e instanceof Error) {
        error.value = e.message;
      }
      return;
    }
  };

  function copyLink() {
    copyToClipboard(window.location.href);
  }
</script>

<style scoped>
  .full-size-table {
    width: 100%;
  }
  .header-cell {
    width: 15%;
    font-weight: bold;
  }
  .content-cell {
    width: 85%;
  }
</style>
