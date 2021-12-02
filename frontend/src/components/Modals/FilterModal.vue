<!-- FilterModal.vue -->
<!-- 'Filter' editing modal, agnostic to what data types are being filtered -->

<template>
  <BaseModal :name="name" header="Edit Filters">
    <div v-for="(filter, index) in formFilters" :key="filter.index">
      <FilterInput v-model="formFilters[index]"></FilterInput>
      <Button
        name="delete-filter"
        icon="pi pi-times"
        class="inputfield"
        @click="deleteFormFilter(index)"
      />
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
  import { mapActions } from "vuex";

  import Button from "primevue/button";

  import BaseModal from "@/components/Modals/BaseModal";
  import FilterInput from "../UserInterface/FilterInput.vue";

  export default {
    name: "EditFilterModal",
    components: { BaseModal, Button, FilterInput },

    inject: ["filterType"],

    data() {
      return {
        formFilters: [],
      };
    },

    computed: {
      currentlySetFilters() {
        return this.$store.getters[`filters/${this.filterType}`];
      },
      submitFilters() {
        let submitFilters = {};
        for (const index in this.formFilters) {
          const filter = this.formFilters[index];
          const filterName = filter.filterName ? filter.filterName : filter;
          submitFilters[filterName] = filter.filterValue;
        }
        return submitFilters;
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
