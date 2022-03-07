<!-- TheAlertDetails.vue -->

<template>
  <Card>
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
              </tbody>
            </table>
          </div>
        </AccordionTab>
      </Accordion>
    </template>
  </Card>
</template>

<script setup>
  import Accordion from "primevue/accordion";
  import AccordionTab from "primevue/accordiontab";
  import Button from "primevue/button";
  import Card from "primevue/card";
  import NodeTagVue from "../../components/Node/NodeTag.vue";

  import { copyToClipboard } from "@/etc/helpers";
  import { useAlertStore } from "@/stores/alert";
  import { getAllAlertTags } from "@/etc/helpers";
  import AlertTableCell from "./AlertTableCell.vue";

  const alertStore = useAlertStore();

  // Key 'values' must be properties of model alertSummary
  const alertDetailKeys = [
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

  function copyLink() {
    copyToClipboard(window.location);
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
