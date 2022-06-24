<!-- FilterModal.vue -->
<!-- 'Filter' editing modal, agnostic to what data types are being filtered -->

<template>
  <BaseModal
    :name="name"
    header="Edit Filters"
    class="xl: w-5 lg:w-5 md:w-8"
    @dialog-close="loadFormFilters"
  >
    <br />
    <NodeQueueSelector :node-queue="nodeType" /> <br />
    <div class="flex flex-wrap">
      <NodePropertyInput
        v-for="(filter, index) in formFilters"
        :key="index!"
        v-model="formFilters[index]"
        class="w-12"
        :allow-delete="true"
        :queue="queue"
        form-type="filter"
        data-cy="filter-input"
        @delete-form-field="deleteFormFilter(index)"
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

<script setup lang="ts">
  import { computed, defineProps, inject, onMounted, ref } from "vue";

  import Button from "primevue/button";

  import NodePropertyInput from "@/components/Node/NodePropertyInput.vue";
  import BaseModal from "@/components/Modals/BaseModal.vue";
  import NodeQueueSelector from "@/components/Node/NodeQueueSelector.vue";

  import { useFilterStore } from "@/stores/filter";
  import { useModalStore } from "@/stores/modal";
  import { useCurrentUserSettingsStore } from "@/stores/currentUserSettings";

  const filterStore = useFilterStore();
  const modalStore = useModalStore();
  const currentUserSettingsStore = useCurrentUserSettingsStore();

  onMounted(() => {
    loadFormFilters();
  });

  const props = defineProps({
    name: { type: String, required: true },
  });

  const nodeType = inject("nodeType") as "alerts" | "events";

  filterStore.$subscribe(
    () => {
      loadFormFilters();
    },
    { deep: true },
  );

  const formFilters = ref<
    { propertyType: string | null; propertyValue: unknown }[]
  >([]);

  const queue = computed(() => {
    return currentUserSettingsStore.queues[nodeType] != null
      ? currentUserSettingsStore.queues[nodeType]!.value
      : "unknown";
  });

  const submitFilters = computed(() => {
    let submitFilters: {
      [index: string]: { included: unknown[]; notIncluded: [] };
    } = {};
    for (const index in formFilters.value) {
      const filter = formFilters.value[index];
      if (filter.propertyType) {
        if (!submitFilters[filter.propertyType]) {
          submitFilters[filter.propertyType] = {
            included: [filter.propertyValue],
            notIncluded: [],
          };
        } else {
          submitFilters[filter.propertyType].included.push(
            filter.propertyValue,
          );
        }
      }
    }
    return submitFilters;
  });

  const submit = () => {
    if (!Object.keys(submitFilters.value).length) {
      filterStore.clearAll({ nodeType: nodeType });
    } else {
      filterStore.bulkSetFilters({
        nodeType: nodeType,
        filters: submitFilters.value,
      });
    }
  };

  const deleteFormFilter = (index: number) => {
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
    for (const filterType in filterStore.$state[nodeType]) {
      for (const filter of filterStore.$state[nodeType][filterType].included) {
        formFilters.value.push({
          propertyType: filterType,
          propertyValue: filter,
        });
      }
    }
  };

  const close = () => {
    loadFormFilters();
    modalStore.close(props.name);
  };
</script>
