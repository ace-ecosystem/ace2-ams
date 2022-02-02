<template>
  <div class="formgrid grid">
    <div v-if="!fixedFilterName" class="field col-fixed">
      <Dropdown
        v-model="filterName"
        data-cy="filter-input-type"
        :options="availableFilters"
        option-label="label"
        type="text"
        class="w-13rem"
        tabindex="1"
        @change="
          clearFilterValue();
          updateValue('filterName', $event.value);
        "
      />
    </div>
    <div class="col w-16rem">
      <div v-if="isInputText" class="field">
        <InputText
          v-model="filterValue"
          data-cy="filter-input-value"
          class="inputfield w-16rem"
          type="text"
          @input="updateValue('filterValue', $event.target.value)"
        ></InputText>
      </div>
      <div v-else-if="isDropdown" class="field">
        <Dropdown
          v-model="filterValue"
          data-cy="filter-input-value"
          class="inputfield w-16rem"
          :options="filterOptions"
          :option-label="filterOptionProperty"
          type="text"
          @change="updateValue('filterValue', $event.value)"
        ></Dropdown>
      </div>
      <div v-else-if="isMultiSelect" class="field">
        <Multiselect
          v-model="filterValue"
          data-cy="filter-input-value"
          class="inputfield w-16rem"
          :options="filterOptions"
          :option-label="filterOptionProperty"
          type="text"
          @change="updateValue('filterValue', $event.value)"
        ></Multiselect>
      </div>
      <div v-else-if="isChips" class="field p-fluid">
        <Chips
          v-model="filterValue"
          data-cy="filter-input-value"
          class="w-full"
          @update:model-value="updateValue('filterValue', $event)"
        ></Chips>
      </div>
      <div v-else-if="isDate" class="field">
        <DatePicker
          v-model="filterValue"
          mode="dateTime"
          class="inputfield w-16rem"
          is24hr
          @update:model-value="updateValue('filterValue', $event)"
        >
          <template #default="{ inputValue, inputEvents }">
            <div class="p-inputgroup">
              <InputText
                data-cy="filter-input-value"
                class="inputfield w-16rem"
                type="text"
                :value="inputValue"
                placeholder="Enter a date!"
                v-on="inputEvents"
              />
            </div>
          </template>
        </DatePicker>
      </div>
      <div v-else-if="isCategorizedValue">
        <div class="field">
          <Dropdown
            v-model="categorizedValueCategory"
            data-cy="filter-input-value-category"
            :options="filterOptions"
            :option-label="filterOptionProperty"
            class="w-16rem"
            type="text"
            @change="updateValue('filterValue', categorizedValueObject)"
          ></Dropdown>
        </div>
        <div class="field">
          <InputText
            v-model="categorizedValueValue"
            data-cy="filter-input-value-value"
            class="w-16rem"
            type="text"
            @input="updateValue('filterValue', categorizedValueObject)"
          ></InputText>
        </div>
      </div>
    </div>
    <div v-if="allowDelete" class="field col-fixed">
      <Button
        data-cy="filter-input-delete"
        name="delete-filter"
        icon="pi pi-times"
        class="w-3rem"
        @click="$emit('deleteFormFilter')"
      />
    </div>
  </div>
</template>

<script setup>
  import {
    computed,
    defineEmits,
    defineProps,
    inject,
    onMounted,
    ref,
    watch,
  } from "vue";

  import Button from "primevue/button";
  import Chips from "primevue/chips";
  import Dropdown from "primevue/dropdown";
  import InputText from "primevue/inputtext";
  import Multiselect from "primevue/multiselect";

  import { DatePicker } from "v-calendar";

  const availableFilters = inject("availableFilters");
  const emit = defineEmits(["update:modelValue", "deleteFormFilter"]);
  const props = defineProps({
    modelValue: { type: Object, required: true },
    fixedFilterName: { type: Boolean, required: false },
    allowDelete: { type: Boolean, required: false },
  });

  const getFilterNameObject = (filterName) => {
    if (!filterName) {
      return availableFilters[0];
    }
    let filter = availableFilters.find((filter) => {
      return filter.name === filterName;
    });
    filter = filter ? filter : null;
    return filter;
  };

  const filterName = ref(getFilterNameObject(props.modelValue.filterName));
  const filterValue = ref(props.modelValue.filterValue);

  // The categorizedValue filter is a bit tricky
  // We need to copy the values and use those as the model
  // Otherwise, they will directly modify the filterStore state :/
  const categorizedValueCategory = ref(null);
  const categorizedValueValue = ref(null);

  const filterOptions = computed(() => {
    if (filterName.value && filterName.value.store) {
      const store = filterName.value.store();
      return store.allItems;
    }
    return null;
  });

  onMounted(() => {
    // This will update the filter to the default if one wasn't provided
    updateValue("filterName", filterName.value);
    // This will udpate the filter value to the default (if available) if one wasn't provided
    if (!filterValue.value) {
      clearFilterValue();
      updateValue("filterValue", filterValue.value);
    }
    // we need to fill in the placeholder refs (see note above) for categorized value
    else if (isCategorizedValue.value) {
      categorizedValueCategory.value = filterValue.value.category;
      categorizedValueValue.value = filterValue.value.value;
    }
  });

  const filterOptionProperty = computed(() => {
    if (filterName.value) {
      return filterName.value.optionProperty
        ? filterName.value.optionProperty
        : "value";
    }
    return null;
  });

  const isDate = computed(() => {
    return inputType.value == "date";
  });
  const isCategorizedValue = computed(() => {
    return inputType.value == "categorizedValue";
  });
  const categorizedValueObject = computed(() => {
    return {
      category: categorizedValueCategory.value,
      value: categorizedValueValue.value,
    };
  });
  const isChips = computed(() => {
    return inputType.value == "chips";
  });

  const isInputText = computed(() => {
    return inputType.value == "inputText";
  });

  const isDropdown = computed(() => {
    return inputType.value == "select";
  });

  const isMultiSelect = computed(() => {
    return inputType.value == "multiselect";
  });

  const inputType = computed(() => {
    return filterName.value ? filterName.value.type : null;
  });

  watch(filterName, async () => {
    if (filterName.value.store) {
      const store = filterName.value.store();
      await store.readAll();
    }
  });

  const clearFilterValue = () => {
    if (isCategorizedValue.value) {
      filterValue.value = { category: filterOptions.value[0], value: null };
      categorizedValueCategory.value = filterOptions.value[0];
      categorizedValueValue.value = null;
    } else if (isDropdown.value) {
      filterValue.value = filterOptions.value[0];
    } else {
      filterValue.value = null;
    }
  };

  const updateValue = (attribute, newValue) => {
    if (attribute === "filterName") {
      emit("update:modelValue", {
        filterName: newValue ? newValue.name : filterName.value,
        filterValue: filterValue.value,
      });
    } else if (attribute === "filterValue") {
      emit("update:modelValue", {
        filterName: filterName.value ? filterName.value.name : filterName.value,
        filterValue: newValue,
      });
    }
  };
</script>
