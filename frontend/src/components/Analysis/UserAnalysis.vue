<!-- UserAnalysis.vue -->

<template>
  <DataTable
    :value="users"
    responsive-layout="scroll"
    :loading="isLoading"
    data-cy="user-analysis-table"
  >
    <Column field="userId" header="User ID" :sortable="true"></Column>
    <Column field="email" header="Email" :sortable="true"></Column>
    <Column field="company" header="Company" :sortable="true"></Column>
    <Column field="division" header="Division" :sortable="true"></Column>
    <Column field="department" header="Department" :sortable="true"> </Column>
    <Column field="title" header="Title" :sortable="true"></Column>
    <Column
      field="managerEmail"
      header="Manager Email"
      :sortable="true"
    ></Column>
    <template #empty> No users could be found. {{ error }} </template>
  </DataTable>
</template>

<script setup lang="ts">
  import DataTable from "primevue/datatable";
  import Column from "primevue/column";

  import { onMounted, ref, defineProps } from "vue";
  import { Event } from "@/services/api/event";
  import { userSummary } from "@/models/eventSummaries";

  const props = defineProps({
    eventUuid: { type: String, required: true },
  });
  const isLoading = ref(false);
  const users = ref<userSummary[]>([]);
  const error = ref<string>();

  onMounted(async () => {
    isLoading.value = true;
    try {
      users.value = await Event.readUserSummary(props.eventUuid);
    } catch (e: unknown) {
      if (typeof e === "string") {
        error.value = e;
      } else if (e instanceof Error) {
        error.value = e.message;
      }
    }
    isLoading.value = false;
  });
</script>
