<!-- FilterModal.vue -->
<!-- 'Filter' editing modal, agnostic to what data types are being filtered -->

<template>
  <BaseModal
    :name="name"
    header="Edit Filters"
    class="xl: w-5 lg:w-5 md:w-8"
    @dialogClose="loadFormFilters"
  >
    <div class="flex flex-wrap">
      <NodePropertyInput
        v-for="(filter, index) in formFilters"
        :key="filter.index"
        v-model="formFilters[index]"
        class="w-12"
        :allow-delete="true"
        @deleteFormFilter="deleteFormFilter(index)"
                input-type="filter"

      ></NodePropertyInput>
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
  import { computed, defineProps, inject, onMounted, ref } from "vue";

  import Button from "primevue/button";

  import BaseModal from "@/components/Modals/BaseModal";
  import NodePropertyInput from "../Node/NodePropertyInput.vue";

  import { useFilterStore } from "@/stores/filter";
  import { useModalStore } from "@/stores/modal";

  const filterStore = useFilterStore();
  const modalStore = useModalStore();

  onMounted(() => {
    loadFormFilters();
  });

  const props = defineProps({
    name: { type: String, required: true },
  });

  const nodeType = inject("nodeType");

  filterStore.$subscribe(
    () => {
      loadFormFilters();
    },
    { deep: true },
  );

  const formFilters = ref([]);

  const submitFilters = computed(() => {
    let submitFilters = {};
    for (const index in formFilters.value) {
      const filter = formFilters.value[index];
      const filterName = filter.propertyType ? filter.propertyType : filter;
      submitFilters[filterName] = filter.propertyValue;
    }
    return submitFilters;
  });

  const submit = () => {
    if (!Object.keys(submitFilters.value).length) {
      filterStore.clearAll({ nodeType: nodeType });
    }
    filterStore.bulkSetFilters({
      nodeType: nodeType,
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
    formFilters.value.push({ propertyType: null, propertyValue: null });
  };

  const loadFormFilters = () => {
    formFilters.value = [];
    for (const filter in filterStore.$state[nodeType]) {
      formFilters.value.push({
        propertyType: filter,
        propertyValue: filterStore.$state[nodeType][filter],
      });
    }
  };

  const close = () => {
    loadFormFilters();
    modalStore.close(props.name);
  };
</script>
