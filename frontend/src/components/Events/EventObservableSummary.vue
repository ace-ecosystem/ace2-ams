<!-- EventURLSummary.vue -->
<!-- A simple list of all URLs contained in the given alert UUIDs -->

<template>
  <DataTable
    ref="dt"
    v-model:selection="modifiedEnabledForDetection"
    v-model:filters="filters"
    :value="visibleObservables"
    responsive-layout="scroll"
    data-key="uuid"
    :paginator="true"
    :rows="50"
    paginator-template="CurrentPageReport FirstPageLink PrevPageLink PageLinks NextPageLink LastPageLink RowsPerPageDropdown"
    :rows-per-page-options="[10, 20, 50]"
    current-page-report-template="Showing {first} to {last} of {totalRecords}"
    filter-display="row"
    :loading="isLoading"
  >
    <template #header>
      <div>
        <Button @click="updateDetectionStatuses">Save Detection Status</Button>
      </div>
    </template>
    <template #empty> No observables found. </template>
    <template #loading> Loading customers data. Please wait. </template>
    <Column
      selection-mode="multiple"
      header="For Detection"
      header-style="width: 3em"
      :show-filter-menu="false"
    >
      <template #filter>
        <Button @click="selectLowHitObservables">Select all low hits</Button>
        <Button @click="resetSelectedObservables">Reset Selection</Button>
      </template>
    </Column>
    <Column
      field="faqueueHits"
      header="FAQueue Hits"
      :sortable="true"
      :show-filter-menu="false"
    >
      <template #filter>
        <Button
          :label="toggleShowMaxHitsButtonText"
          @click="toggleShowMaxHits"
        ></Button>
      </template>
      <template #body="slotProps">
        <span>{{ slotProps.data.faqueueHits }}</span>
        <a :href="slotProps.data.faqueueLink" style="text-decoration: none"
          ><Button
            icon="pi pi-external-link"
            class="p-button-rounded p-button-text"
        /></a> </template
    ></Column>
    <Column
      field="type.value"
      header="Type"
      :sortable="true"
      :show-filter-menu="false"
    >
      <template #filter="{ filterModel, filterCallback }">
        <MultiSelect
          v-model="filterModel.value"
          :options="observableTypeStore.allItems"
          option-label="value"
          option-value="value"
          placeholder="Any"
          class="p-column-filter"
          @change="filterCallback()"
        >
        </MultiSelect>
      </template>
    </Column>
    <Column field="value" header="Value" :sortable="true">
      <template #filter="{ filterModel, filterCallback }">
        <InputText
          v-model="filterModel.value"
          type="text"
          class="p-column-filter"
          :placeholder="`Search by value`"
          @keyup="filterCallback()"
        /> </template
    ></Column>
  </DataTable>
</template>

<script setup>
  import { defineProps, computed, ref, onMounted, inject } from "vue";
  import Button from "primevue/button";
  import DataTable from "primevue/datatable";
  import InputText from "primevue/inputtext";
  import Column from "primevue/column";
  import MultiSelect from "primevue/multiselect";
  import { Event } from "@/services/api/event";
  import { FilterMatchMode } from "primevue/api";

  import { ObservableInstance } from "@/services/api/observable";

  import { useObservableTypeStore } from "@/stores/observableType";
  const observableTypeStore = useObservableTypeStore();

  const config = inject("config");
  const maxHits = ref(config.events.faqueue.mediumHits);
  const lowHits = ref(config.events.faqueue.lowHits);

  const props = defineProps({
    eventUuid: { type: String, required: true },
  });

  const isLoading = ref(false);
  const isShowingMaxHits = ref(true);
  const toggleShowMaxHitsButtonText = ref("Hide Max Hits");
  const observables = ref([]);
  const modifiedEnabledForDetection = ref([]);
  const currentlyEnabledForDetection = ref([]);

  onMounted(async () => {
    isLoading.value = true;
    await initData();
    isLoading.value = false;
  });

  const visibleObservables = computed(() => {
    if (isShowingMaxHits.value) {
      return observables.value;
    }
    return observables.value.filter((obs) => obs.faqueueHits < maxHits.value);
  });

  const initData = async () => {
    observables.value = await Event.readObservableSummary(props.eventUuid);
    currentlyEnabledForDetection.value = observables.value.filter(
      (obs) => obs.forDetection,
    );
    modifiedEnabledForDetection.value = currentlyEnabledForDetection.value;
  };

  const resetSelectedObservables = () => {
    modifiedEnabledForDetection.value = currentlyEnabledForDetection.value;
  };

  const selectLowHitObservables = () => {
    modifiedEnabledForDetection.value = [
      ...modifiedEnabledForDetection.value,
      ...observables.value.filter((obs) => obs.faqueueHits <= lowHits.value),
    ];
  };

  const toggleShowMaxHits = () => {
    if (isShowingMaxHits.value) {
      toggleShowMaxHitsButtonText.value = "Show Max Hits";
    } else {
      toggleShowMaxHitsButtonText.value = "Hide Max Hits";
    }
    isShowingMaxHits.value = !isShowingMaxHits.value;
  };

  const filters = ref({
    value: { value: null, matchMode: FilterMatchMode.STARTS_WITH },
    "type.value": { value: null, matchMode: FilterMatchMode.IN },
  });

  const updateDetectionStatuses = async () => {
    isLoading.value = true;
    const setFalse = currentlyEnabledForDetection.value.filter(
      (obs) => !modifiedEnabledForDetection.value.includes(obs),
    );
    for (const observable of setFalse) {
      await updateObservableDetectionStatus(observable.uuid, false);
    }
    const setTrue = modifiedEnabledForDetection.value.filter(
      (obs) => !currentlyEnabledForDetection.value.includes(obs),
    );
    for (const observable of setTrue) {
      await updateObservableDetectionStatus(observable.uuid, true);
    }
    await initData();
    isLoading.value = false;
  };

  const updateObservableDetectionStatus = async (uuid, forDetection) => {
    await ObservableInstance.update(uuid, { forDetection: forDetection });
  };
</script>

<style scoped>
  /deep/ .p-datatable-thead .p-checkbox .p-checkbox-box {
    display: none !important;
  }
</style>
