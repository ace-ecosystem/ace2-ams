<!-- EmailAnalysisSummaryTable.vue -->

<template>
  <h5>Email Summary</h5>
  <DataTable
    :value="emails"
    :loading="isLoading"
    responsive-layout="scroll"
    data-cy="email-analysis-table"
  >
    <Column field="alertUuid" header="URL"
      ><template #body="slotProps">
        <span class="flex align-items-center justify-content-center"
          ><router-link :to="`/alert/${slotProps.data.alertUuid}`" exact
            >Alert</router-link
          >
        </span>
      </template></Column
    >
    <Column field="time" header="Time" :sortable="true"
      ><template #body="slotProps">
        <span class="flex align-items-center justify-content-center">
          {{ formatDateTime(slotProps.data.time) }}
        </span>
      </template></Column
    >
    <Column field="fromAddress" header="From" :sortable="true"></Column>
    <Column field="toAddress" header="To" :sortable="true"></Column>
    <Column field="subject" header="Subject"> :sortable="true"</Column>
    <Column field="attachments" header="Attachments" :sortable="true"
      ><template #body="slotProps">
        <span class="flex align-items-center justify-content-center">
          {{ formatList(slotProps.data.attachments) }}
        </span>
      </template></Column
    >
    <Column field="ccAddresses" header="CC" :sortable="true"
      ><template #body="slotProps">
        <span class="flex align-items-center justify-content-center">
          {{ formatList(slotProps.data.ccAddresses) }}
        </span>
      </template></Column
    >
    <Column field="replyToAddress" header="Reply-To" :sortable="true"
      ><template #body="slotProps">
        <span
          v-if="slotProps.data.replyToAddress"
          class="flex align-items-center justify-content-center"
        >
          {{ slotProps.data.replyToAddress }}
        </span>
        <span>None</span>
      </template></Column
    >
    <Column field="messageId" header="Message-ID" :sortable="true"></Column>
    <template #empty> Could not find any emails. {{ error }} </template>
  </DataTable>
</template>

<script setup lang="ts">
  import DataTable from "primevue/datatable";
  import Column from "primevue/column";

  import { onMounted, ref, defineProps } from "vue";
  import { Event } from "@/services/api/event";
  import { emailSummary } from "@/models/eventSummaries";

  const props = defineProps({
    eventUuid: { type: String, required: true },
  });
  const isLoading = ref(false);
  const emails = ref<emailSummary[]>([]);
  const error = ref<string>();

  onMounted(async () => {
    isLoading.value = true;
    try {
      emails.value = await Event.readEmailSummary(props.eventUuid);
    } catch (e: unknown) {
      if (typeof e === "string") {
        error.value = e;
      } else if (e instanceof Error) {
        error.value = e.message;
      }
    }
    isLoading.value = false;
  });

  const formatDateTime = (dateTime: string) => {
    if (dateTime) {
      const d = new Date(dateTime);
      return d.toLocaleString("en-US", { timeZone: "UTC" });
    }

    return "None";
  };

  const formatList = (list: []) => {
    if (list.length) {
      return list.join(", ");
    }

    return "None";
  };
</script>
