<!-- FilterModal.vue -->
<!-- 'Filter' editing modal, agnostic to what data types are being filtered -->

<template>
  <BaseModal
    :name="name"
    header="Edit Filters"
    class="xl: w-5 lg:w-5 md:w-8"
    @dialogClose="clear"
  >
    <div class="flex flex-wrap">
      <FilterInput
        v-for="(filter, index) in formFilters"
        :key="filter.index"
        v-model="formFilters[index]"
        class="w-12"
        @deleteFormFilter="deleteFormFilter(index)"
      ></FilterInput>
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

<script setup>
  import { computed, defineProps, inject, ref } from "vue";

  import Button from "primevue/button";

  import BaseModal from "@/components/Modals/BaseModal";
  import FilterInput from "@/components/UserInterface/FilterInput.vue";

  import { useFilterStore } from "@/stores/filter";
  import { useModalStore } from "@/stores/modal";

  const filterStore = useFilterStore();
  const modalStore = useModalStore();

  const props = defineProps({
    name: { type: String, required: true },
  });

  const filterType = inject("filterType");

  filterStore.$subscribe(
    () => {
      resetFormFilters();
    },
    { deep: true },
  );

  const formFilters = ref([]);

  const submitFilters = computed(() => {
    let submitFilters = {};
    for (const index in formFilters.value) {
      const filter = formFilters.value[index];
      const filterName = filter.filterName ? filter.filterName : filter;
      submitFilters[filterName] = filter.filterValue;
    }
    return submitFilters;
  });

  const submit = () => {
    filterStore.bulkSetFilters({
      filterType: filterType,
      filters: submitFilters.value,
    });
  };

  const deleteFormFilter = (index) => {
    formFilters.value.splice(index, 1);
  };

  const clear = () => {
    formFilters.value = [];
  };

  const addNewFilter = () => {
    formFilters.value.push({ filterName: null, filterValue: null });
  };

  const resetFormFilters = () => {
    formFilters.value = [];
    for (const filter in filterStore.$state[filterType]) {
      formFilters.value.push({
        filterName: filter,
        filterValue: filterStore.$state[filterType][filter],
      });
    }
  };

  const close = () => {
    resetFormFilters();
    modalStore.close(props.name);
  };
</script>
