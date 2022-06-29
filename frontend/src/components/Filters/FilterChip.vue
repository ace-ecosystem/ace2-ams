<!-- FilterChip.vue -->
<!-- A chip that shows a currently applied filter (by type, ex. 'queue' or 'owner' -->
<!-- Contains actions to remove (and eventually edit/add) a filter through click actions -->
<template>
  <span v-if="filterNameObject" style="padding: 2px" data-cy="filter-chip">
    <Chip>
      <span
        class="p-chip-text link-text filter-name-text chip-content"
        @click="unsetFilter"
        >{{ filterLabel }}:</span
      >
      <span
        v-for="(value, index) in filterValue.included"
        :key="(formatValue(value) as string)"
        data-cy="filter-chip-content"
        class="link-text p-chip-text chip-content"
      >
        <span
          style="padding-left: 2px; padding-right: 2px; font-weight: bold"
          @click="unsetFilterValue({ value: value, notIncluded: false })"
          >{{ formatValue(value as any) }}</span
        >
        <i
          data-cy="filter-chip-edit-button"
          class="pi pi-pencil icon-button chip-content"
          style="cursor: pointer"
          @click="openEditFilterValuePanel(value, $event)"
        />
        <span
          v-if="!(index == filterValue!.included.length - 1)||(filterValue!.notIncluded.length)"
          >|</span
        ></span
      >
      <span
        v-for="(value, index) in filterValue.notIncluded"
        :key="(formatValue(value) as string)"
        data-cy="filter-chip-content"
        class="link-text p-chip-text chip-content"
      >
        <span
          style="padding-left: 2px; padding-right: 2px; font-weight: bold"
          @click="unsetFilterValue({ value: value, notIncluded: true })"
          ><b>!</b> {{ formatValue(value as any) }}</span
        >
        <i
          data-cy="filter-chip-edit-button"
          class="pi pi-pencil icon-button chip-content"
          style="cursor: pointer"
          @click="openEditFilterValuePanel(value, $event)"
        />
        <span v-if="!(index == filterValue!.notIncluded.length - 1)"
          >|</span
        ></span
      >
      <i
        data-cy="filter-chip-add-button"
        class="pi pi-plus-circle icon-button chip-content"
        style="cursor: pointer"
        @click="openNewFilterValuePanel()"
      />
    </Chip>
    <OverlayPanel
      ref="op"
      data-cy="filter-chip-edit-panel"
      style="padding: 1rem"
    >
      <div class="flex justify-content-start pb-2">
        <b class="flex align-items-center justify-content-center pr-2">NOT</b>
        <InputSwitch
          v-model="filterModel.notIncluded"
          class="flex align-items-center justify-content-center"
          data-cy="filter-not-included-switch"
        ></InputSwitch>
      </div>
      <ObjectPropertyInput
        v-model="filterModel"
        :fixed-property-type="true"
        :allow-delete="false"
        form-type="filter"
        :queue="queue"
      >
      </ObjectPropertyInput>
      <Button
        data-cy="filter-chip-submit-button"
        name="update-filter"
        icon="pi pi-check"
        @click="submitFilterValue($event)"
      />
    </OverlayPanel>
  </span>
</template>

<script setup lang="ts">
  import { inject, computed, defineProps, ref, PropType } from "vue";

  import { useFilterStore } from "@/stores/filter";
  import { useCurrentUserSettingsStore } from "@/stores/currentUserSettings";
  import { validAlertFilters } from "@/etc/constants/alerts";
  import { validEventFilters } from "@/etc/constants/events";

  import { isObject } from "@/etc/validators";
  import Button from "primevue/button";
  import Chip from "primevue/chip";
  import OverlayPanel from "primevue/overlaypanel";
  import InputSwitch from "primevue/inputswitch";

  import ObjectPropertyInput from "@/components/Objects/ObjectPropertyInput.vue";
  import { alertFilterValues } from "@/models/alert";
  import { eventFilterValues } from "@/models/event";

  const currentUserSettingsStore = useCurrentUserSettingsStore();
  const filterStore = useFilterStore();
  const objectType = inject("objectType") as "alerts" | "events";

  const queue = computed(() => {
    return currentUserSettingsStore.queues[objectType] != null
      ? currentUserSettingsStore.queues[objectType]!.value
      : "unknown";
  });

  const op = ref();
  const toggleQuickEditMenu = (event: unknown) => {
    op.value.toggle(event);
  };

  const setFilterModelOldValue = (
    value?: alertFilterValues | eventFilterValues,
  ) => {
    if (value) {
      filterModelOldValue.value = {
        filterValue: value,
        notIncluded: filterModel.value.notIncluded,
      };
    } else {
      filterModelOldValue.value = undefined;
    }
  };

  interface filterValueProp {
    included: alertFilterValues[] | eventFilterValues[];
    notIncluded: alertFilterValues[] | eventFilterValues[];
  }

  const props = defineProps({
    filterName: { type: String, required: true },
    filterValue: {
      type: Object as PropType<filterValueProp>,
      required: true,
    },
  });

  const validFilters = {
    alerts: validAlertFilters,
    events: validEventFilters,
  };

  const filterNameObject = validFilters[objectType]
    ? validFilters[objectType].find((filter) => {
        return filter.name === props.filterName;
      })
    : null;

  const filterModelOldValue = ref<{
    filterValue: alertFilterValues | eventFilterValues;
    notIncluded: boolean;
  }>();

  const filterModel = ref({
    propertyType: props.filterName,
    propertyValue: undefined as alertFilterValues | eventFilterValues,
    notIncluded: false,
  });

  const filterLabel = computed(() => {
    if (filterNameObject) {
      return filterNameObject.label;
    }
    return "";
  });

  function submitFilterValue(event: unknown) {
    updateFilter();
    toggleQuickEditMenu(event);
    resetFilterModel({ notIncluded: false, value: undefined });
    setFilterModelOldValue();
  }

  function openEditFilterValuePanel(value: any, event: unknown) {
    toggleQuickEditMenu(event);
    resetFilterModel({ notIncluded: false, value: value });
    setFilterModelOldValue(value);
  }

  function openNewFilterValuePanel() {
    toggleQuickEditMenu(event);
    resetFilterModel({ notIncluded: false, value: undefined });
  }

  function resetFilterModel(args: {
    value: alertFilterValues | eventFilterValues | undefined;
    notIncluded: boolean;
  }) {
    filterModel.value = {
      propertyType: props.filterName,
      propertyValue: args.value,
      notIncluded: args.notIncluded,
    };
  }

  function updateFilter() {
    if (filterModelOldValue.value) {
      filterStore.unsetFilterValue({
        objectType: objectType,
        filterName: props.filterName,
        filterValue: filterModelOldValue.value.filterValue,
        isIncluded: !filterModelOldValue.value.notIncluded,
      });
    }
    filterStore.setFilter({
      objectType: objectType,
      filterName: props.filterName,
      filterValue: filterModel.value.propertyValue as
        | alertFilterValues
        | eventFilterValues,
      isIncluded: !filterModel.value.notIncluded,
    });
  }

  function unsetFilter() {
    filterStore.unsetFilter({
      objectType: objectType,
      filterName: props.filterName,
    });
  }

  function unsetFilterValue(args: {
    value: alertFilterValues | eventFilterValues;
    notIncluded: boolean;
  }) {
    filterStore.unsetFilterValue({
      objectType: objectType,
      filterName: props.filterName,
      filterValue: args.value,
      isIncluded: !args.notIncluded,
    });
  }

  function formatValue(value: alertFilterValues | eventFilterValues) {
    if (filterNameObject) {
      if (filterNameObject.displayRepr) {
        return filterNameObject.displayRepr(value);
      } else if (filterNameObject.stringRepr) {
        return filterNameObject.stringRepr(value);
      } else if (
        filterNameObject.optionProperty &&
        isObject(value) &&
        !("category" in value)
      ) {
        return value[filterNameObject.optionProperty];
      }
    }

    return value;
  }
</script>

<style>
  .filter-name-text {
    font-weight: bold;
  }
  .chip-content {
    margin-left: 2px;
    margin-right: 2px;
  }
  .chip-text {
    font-weight: bold;
    line-height: 1.5;
  }
  .icon-button:hover {
    font-weight: bold;
  }
</style>
