<!-- FilterModal.vue -->
<!-- 'Filter' editing modal, agnostic to what data types are being filtered -->

<template>
  <BaseModal
    :name="name"
    header="Edit Filters"
    style="max-width: 625px"
    @dialog-close="loadFormFilters"
  >
    <br />
    <QueueSelector :object-queue="objectType" /> <br />
    <b v-if="formFilters.length">NOT</b> <br />
    <div class="flex flex-wrap">
      <span
        v-for="(filter, index) in formFilters"
        :key="index!"
        style="width: 100%"
      >
        <div class="flex">
          <InputSwitch
            v-model="formFilters[index].notIncluded"
            class="flex align-items-center"
            data-cy="filter-not-included-switch"
          ></InputSwitch>
          <ObjectPropertyInput
            v-model="formFilters[index]"
            class="flex align-items-center"
            :allow-delete="true"
            :queue="queue"
            form-type="filter"
            data-cy="filter-input"
            @delete-form-field="deleteFormFilter(index)"
          ></ObjectPropertyInput>
        </div>
      </span>
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
  import InputSwitch from "primevue/inputswitch";

  import ObjectPropertyInput from "@/components/Objects/ObjectPropertyInput.vue";
  import BaseModal from "@/components/Modals/BaseModal.vue";
  import QueueSelector from "@/components/Queues/QueueSelector.vue";

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

  const objectType = inject("objectType") as "alerts" | "events";

  filterStore.$subscribe(
    () => {
      loadFormFilters();
    },
    { deep: true },
  );

  const formFilters = ref<
    {
      propertyType: string | null;
      propertyValue: unknown;
      notIncluded: boolean;
    }[]
  >([]);

  const queue = computed(() => {
    return currentUserSettingsStore.queues[objectType] != null
      ? currentUserSettingsStore.queues[objectType]!.value
      : "unknown";
  });

  function submitFilters() {
    let submitFilters: {
      [index: string]: { included: unknown[]; notIncluded: unknown[] };
    } = {};
    for (const index in formFilters.value) {
      const filter = formFilters.value[index];
      if (filter.propertyType) {
        //  If there is not an entry for this filter type yet
        if (!submitFilters[filter.propertyType]) {
          if (filter.notIncluded) {
            submitFilters[filter.propertyType] = {
              included: [],
              notIncluded: [filter.propertyValue],
            };
          } else {
            submitFilters[filter.propertyType] = {
              included: [filter.propertyValue],
              notIncluded: [],
            };
          }
        } else {
          // If there is an entry for this filter type
          if (filter.notIncluded) {
            submitFilters[filter.propertyType].notIncluded.push(
              filter.propertyValue,
            );
          } else {
            submitFilters[filter.propertyType].included.push(
              filter.propertyValue,
            );
          }
        }
      }
    }
    return submitFilters;
  }

  const submit = () => {
    const filters = submitFilters();
    if (!Object.keys(filters).length) {
      filterStore.clearAll({ objectType: objectType });
    } else {
      filterStore.bulkSetFilters({
        objectType: objectType,
        filters: filters,
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
    formFilters.value.push({
      propertyType: null,
      propertyValue: null,
      notIncluded: false,
    });
  };

  const loadFormFilters = () => {
    formFilters.value = [];
    for (const filterType in filterStore.$state[objectType]) {
      for (const filter of filterStore.$state[objectType][filterType]
        .included) {
        formFilters.value.push({
          propertyType: filterType,
          propertyValue: filter,
          notIncluded: false,
        });
      }
      for (const filter of filterStore.$state[objectType][filterType]
        .notIncluded) {
        formFilters.value.push({
          propertyType: filterType,
          propertyValue: filter,
          notIncluded: true,
        });
      }
    }
  };

  const close = () => {
    loadFormFilters();
    modalStore.close(props.name);
  };
</script>
