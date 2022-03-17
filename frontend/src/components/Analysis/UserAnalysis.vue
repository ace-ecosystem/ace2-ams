<!-- UserAnalysis.vue -->

<template>
  <DataTable :value="users" responsive-layout="scroll">
    <Column field="userId" header="User ID" :sortable="true"></Column>
    <Column field="email" header="Email" :sortable="true"></Column>
    <Column field="company" header="Company" :sortable="true"></Column>
    <Column field="division" header="Division" :sortable="true"></Column>
    <Column field="department" header="Department"> :sortable="true"</Column>
    <Column field="title" header="Title" :sortable="true"></Column>
    <Column
      field="managerEmail"
      header="Manager Email"
      :sortable="true"
    ></Column>
  </DataTable>
</template>

<script setup>
  import DataTable from "primevue/datatable";
  import Column from "primevue/column";

  import { onMounted, ref, defineProps } from "vue";
  import { Event } from "@/services/api/event";

  const props = defineProps({
    eventUuid: { type: String, required: true },
  });
  const isLoading = ref(false);
  const users = ref([]);

  onMounted(async () => {
    isLoading.value = true;
    users.value = await Event.readUserSummary(props.eventUuid);
    isLoading.value = false;
  });
</script>
