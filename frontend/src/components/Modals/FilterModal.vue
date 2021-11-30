<!-- FilterModal.vue -->
<!-- 'Filter' editing modal, agnostic to what data types are being filtered -->

<template>
  <BaseModal :name="name" header="Edit Filters">
    <div v-for="(filter, index) in formFilters" :key="filter.index">
      <component
        :is="filterInputComponent"
        v-model="formFilters[index]"
        @deleteFormFilter="deleteFormFilter(index)"
      ></component>
    </div>
    <template #footer>
      <Button
        label="Clear"
        icon="pi pi-times"
        class="p-button-text"
        @click="clear"
      />
      <Button
        label="Add"
        icon="pi pi-plus"
        class="p-button-text"
        @click="addNewFilter"
      />
      <Button label="Cancel" class="p-button-text" @click="close" />
      <Button
        label="Submit"
        icon="pi pi-check"
        @click="
          submit();
          close();
        "
      />
    </template>
  </BaseModal>
</template>

<script>
  import { defineAsyncComponent } from "vue";

  import { mapActions } from "vuex";

  import Button from "primevue/button";
  import Dropdown from "primevue/dropdown";

  import BaseModal from "@/components/Modals/BaseModal";
  import AlertFilterInput from "@/components/Alerts/AlertFilterInput";

  export default {
    name: "EditFilterModal",
    components: { BaseModal, Button, AlertFilterInput },

    inject: [
      "filterType",
      "rangeFilterOptions",
      "rangeFilters",
      "filterInputType",
    ],

    data() {
      return {
        formFilters: [],
      };
    },

    computed: {
      currentlySetFilters() {
        return this.$store.getters[`${this.filterType}/filters`];
      },
      submitFilters() {
        let submitFilters = {};
        for (const index in this.formFilters) {
          const filter = this.formFilters[index];
          submitFilters[filter.filterName.name] = filter.filterValue;
        }
        return submitFilters;
      },
      filterInputComponent() {
        return defineAsyncComponent(() =>
          import(`@/components/${this.filterInputType}`),
        );
      },
      filterInputPath() {
        return `@/components/${this.filterInputType}`;
      },
      name() {
        return this.$options.name;
      },
    },

    watch: {
      currentlySetFilters: {
        deep: true,
        handler: function () {
          this.resetFormFilters();
        },
      },
    },

    methods: {
      ...mapActions({
        bulkSetFilters: "filters/bulkSetFilters",
      }),
      updateForm(index, event) {
        console.log(index);
        console.log(event);
        this.formFilters[index][event.attr] = event.value;
      },
      submit() {
        this.bulkSetFilters({
          filterType: this.filterType,
          filters: this.submitFilters,
        });
      },
      deleteFormFilter(index) {
        this.formFilters.splice(index, 1);
      },
      clear() {
        this.formFilters = [];
      },
      addNewFilter() {
        this.formFilters.push({ filterName: null, filterValue: null });
      },
      resetFormFilters() {
        this.formFilters = [];
        for (const filter in this.currentlySetFilters) {
          this.formFilters.push({
            filterName: filter,
            filterValue: this.currentlySetFilters[filter],
          });
        }
      },
      close() {
        this.$store.dispatch("modals/close", this.name);
      },
    },
  };
</script>
