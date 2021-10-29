<!-- RemediateModal.vue -->
<!-- 'Remediation' alert action modal -->

<template>
  <BaseModal :name="this.name" header="Remediate">
    <DataTable
      :value="remediationTargets"
      :rows="10"
      :sortOrder="1"
      columnResizeMode="fit"
      dataKey="id"
      removableSort
      responsiveLayout="scroll"
      sortField="type"
      stripedRows
      v-model:selection="selectedRemediations"
    >
      <Column
        id="remediation-select"
        selectionMode="multiple"
        headerStyle="width: 3em"
      />
      <Column field="type" header="Type" :sortable="true" />
      <Column field="target" header="Target" :sortable="true" />
      <Column field="status" header="Status" :sortable="true" />
    </DataTable>
    <template #footer>
      <Button label="Stop" class="p-button-text" />
      <Button label="Remove" icon="pi pi-times" />
      <Button label="Restore" icon="pi pi-check" />
    </template>
  </BaseModal>
</template>

<script>
  import Button from "primevue/button";
  import Column from "primevue/column";
  import DataTable from "primevue/datatable";

  import BaseModal from "@/components/Modals/BaseModal";

  export default {
    name: "RemediationModal",
    components: { BaseModal, Button, Column, DataTable },

    computed: {
      name() {
        return this.$options.name;
      },
    },

    data() {
      return {
        remediationTargets: [
          {
            type: "zerofox",
            target: "bad_url",
            status: "remediation failed",
            id: "123",
          },
          {
            type: "email",
            target: "msgID|email.com",
            status: "remediating",
            id: "124",
          },
          {
            type: "email",
            target: "msgID|email2.com",
            status: "removed",
            id: "125",
          },
          {
            type: "email",
            target: "msgID|email3.com",
            status: "restored",
            id: "126",
          },
        ],

        selectedRemediations: [],
      };
    },

    methods: {
      close() {
        this.selectedRemediations = [];
        this.$store.dispatch("modals/close", this.name);
      },
    },
  };
</script>
