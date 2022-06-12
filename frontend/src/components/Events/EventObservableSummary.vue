<!-- EventObservableSummary.vue -->
<!-- A table containing all observables in an event as well as FAQueue analysis info for each -->
<!-- Also includes controls for managing whether an observable should be enabled for detection  -->

<template>
  <Message v-if="error" severity="error" data-cy="error-banner">{{
    error
  }}</Message>
  <DataTable
    v-model:filters="filters"
    v-model:selection="modifiedEnabledForDetection"
    class="p-datatable-sm"
    :loading="isLoading"
    :paginator="true"
    :rows-per-page-options="[10, 20, 50]"
    :rows="50"
    :value="visibleObservables"
    current-page-report-template="Showing {first} to {last} of {totalRecords}"
    data-cy="observables-table"
    data-key="uuid"
    filter-display="row"
    :row-class="rowClass"
    paginator-template="CurrentPageReport FirstPageLink PrevPageLink PageLinks NextPageLink LastPageLink RowsPerPageDropdown"
    responsive-layout="scroll"
  >
    <template #empty> No observables found. </template>
    <template #loading> Loading observables... Just a sec. </template>
    <template #header>
      <div>
        <Button
          id="save-detection-status-button"
          label="Save Detection Status"
          icon="pi pi-save"
          :loading="isLoading"
          @click="updateDetectionStatuses"
        ></Button>
      </div>
    </template>
    <Column
      id="selection-column"
      selection-mode="multiple"
      header="For Detection"
      :show-filter-menu="false"
      style="width: 24em"
    >
      <template #filter>
        <div style="padding-left: 1em">
          <Button
            id="select-low-hits-button"
            class="p-button-sm"
            label="Select low hits"
            icon="pi pi-check-square"
            style="width: 12em; margin: 0.5em"
            @click="selectLowHitObservables"
          ></Button>

          <Button
            id="reset-selected-observables-button"
            class="p-button-sm"
            icon="pi pi-undo"
            label="Reset"
            style="width: 12em; margin: 0.5em"
            @click="resetSelectedObservables"
          ></Button>
        </div>
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
          id="toggle-max-hits-button"
          class="p-button-sm"
          :icon="toggleShowMaxHitsButtonIcon"
          :label="toggleShowMaxHitsButtonText"
          style="width: 10em"
          @click="toggleShowMaxHits"
        ></Button>
      </template>
      <template #body="slotProps">
        <div class="flex align-content-evenly">
          <span
            class="flex align-items-center justify-content-center"
            data-cy="faqueue-hits-count"
            style="width: 2em"
            >{{ slotProps.data.faqueueHits }}</span
          >
          <span class="flex align-items-center justify-content-center"
            ><a :href="slotProps.data.faqueueLink" style="text-decoration: none"
              ><Button
                icon="pi pi-external-link"
                class="p-button-rounded p-button-text"
                data-cy="faqueue-external-link"
            /></a>
          </span>
        </div>
      </template>
    </Column>
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
          data-cy="observable-type-filter-multiselect"
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
          data-cy="observable-value-filter-input"
          @keyup="filterCallback()"
        />
      </template>
    </Column>
    <Column field="relationships" header="Relationships">
      <template #body="slotProps">
        <NodeRelationshipVue
          v-for="relationship of slotProps.data.observableRelationships"
          :key="relationship.uuid"
          :type="relationship.type.value"
          :value="relationship.relatedNode.value"
        />
      </template>
    </Column>
    <Column field="tags" header="Tags">
      <template #body="slotProps">
        <MetadataTag
          v-for="tag of slotProps.data.tags"
          :key="tag.value"
          :tag="tag"
          override-node-type="alerts"
        />
      </template>
    </Column>
  </DataTable>
</template>

<script setup lang="ts">
  import { defineProps, computed, ref, onMounted, inject } from "vue";
  import { FilterMatchMode } from "primevue/api";
  import Button from "primevue/button";
  import Column from "primevue/column";
  import DataTable, { DataTableFilterMeta } from "primevue/datatable";
  import InputText from "primevue/inputtext";
  import Message from "primevue/message";
  import MultiSelect from "primevue/multiselect";
  import NodeRelationshipVue from "@/components/Node/NodeRelationship.vue";
  import MetadataTag from "@/components/Metadata/MetadataTag.vue";

  import { Event } from "@/services/api/event";
  import { ObservableInstance } from "@/services/api/observable";

  import { useAuthStore } from "@/stores/auth";
  import { useObservableTypeStore } from "@/stores/observableType";
  import { observableSummary } from "@/models/eventSummaries";

  const config = inject("config") as Record<string, any>;
  const props = defineProps({
    eventUuid: { type: String, required: true },
  });

  const authStore = useAuthStore();
  const observableTypeStore = useObservableTypeStore();

  const currentlyEnabledForDetection = ref<observableSummary[]>([]);
  const error = ref<string>();
  const isLoading = ref(false);
  const isShowingMaxHits = ref(true);
  const lowHits = ref<number>(config.events.faqueue.lowHits);
  const maxHits = ref<number>(config.events.faqueue.mediumHits);
  const modifiedEnabledForDetection = ref<observableSummary[]>([]);
  const observables = ref<observableSummary[]>([]);
  const toggleShowMaxHitsButtonIcon = ref("pi pi-eye-slash");
  const toggleShowMaxHitsButtonText = ref("Hide Max Hits");

  onMounted(async () => {
    isLoading.value = true;
    try {
      await initData();
    } catch (e: unknown) {
      if (typeof e === "string") {
        error.value = `Could not fetch observable summary data: ${e}`;
      } else if (e instanceof Error) {
        error.value = `Could not fetch observable summary data: ${e.message}`;
      }
    }
    isLoading.value = false;
  });

  const initData = async () => {
    observables.value = await Event.readObservableSummary(props.eventUuid);
    currentlyEnabledForDetection.value = observables.value.filter(
      (obs) => obs.forDetection,
    );
    modifiedEnabledForDetection.value = currentlyEnabledForDetection.value;
  };
  const visibleObservables = computed(() => {
    if (isShowingMaxHits.value) {
      return observables.value;
    }
    return observables.value.filter(
      (obs: observableSummary) => obs.faqueueHits < maxHits.value,
    );
  });

  const resetSelectedObservables = () => {
    modifiedEnabledForDetection.value = currentlyEnabledForDetection.value;
  };

  const selectLowHitObservables = () => {
    modifiedEnabledForDetection.value = [
      ...modifiedEnabledForDetection.value,
      ...observables.value.filter(
        (obs: observableSummary) => obs.faqueueHits <= lowHits.value,
      ),
    ];
  };

  const toggleShowMaxHits = () => {
    if (isShowingMaxHits.value) {
      toggleShowMaxHitsButtonText.value = "Show Max Hits";
      toggleShowMaxHitsButtonIcon.value = "pi pi-eye";
    } else {
      toggleShowMaxHitsButtonText.value = "Hide Max Hits";
      toggleShowMaxHitsButtonIcon.value = "pi pi-eye-slash";
    }
    isShowingMaxHits.value = !isShowingMaxHits.value;
  };

  const updateDetectionStatuses = async () => {
    isLoading.value = true;
    const setFalse: observableSummary[] =
      currentlyEnabledForDetection.value.filter(
        (obs) => !modifiedEnabledForDetection.value.includes(obs),
      );
    for (const observable of setFalse) {
      await updateObservableDetectionStatus(observable.uuid, false);
    }
    const setTrue: observableSummary[] =
      modifiedEnabledForDetection.value.filter(
        (obs) => !currentlyEnabledForDetection.value.includes(obs),
      );
    for (const observable of setTrue) {
      await updateObservableDetectionStatus(observable.uuid, true);
    }
    await initData();
    isLoading.value = false;
  };

  const updateObservableDetectionStatus = async (
    uuid: string,
    forDetection: boolean,
  ) => {
    try {
      await ObservableInstance.update(uuid, {
        historyUsername: authStore.user.username,
        forDetection: forDetection,
      });
    } catch (e: unknown) {
      if (typeof e === "string") {
        error.value = `Could not update observables: ${e}`;
      } else if (e instanceof Error) {
        error.value = `Could not update observables: ${e.message}`;
      }
    }
  };

  const rowClass = (obs: observableSummary): string | undefined => {
    return obs.faqueueHits <= lowHits.value ? "low-hits" : undefined;
  };

  const filters = ref({
    value: { value: null, matchMode: FilterMatchMode.STARTS_WITH },
    "type.value": { value: null, matchMode: FilterMatchMode.IN },
  } as DataTableFilterMeta);
</script>

<style scoped>
  ::v-deep(.p-datatable-thead .p-checkbox .p-checkbox-box) {
    display: none !important;
  }
  ::v-deep(.low-hits) {
    background: #d4f0de !important;
  }
</style>
