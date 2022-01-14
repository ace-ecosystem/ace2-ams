<template>
  <div class="formgrid grid">
    <div v-if="!fixedFilterName" class="field col-fixed">
      <Dropdown
        v-model="filterName"
        :options="availableFilters"
        option-label="label"
        type="text"
        class="w-13rem"
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
          class="inputfield w-16rem"
          type="text"
          @input="updateValue('filterValue', $event.target.value)"
        ></InputText>
      </div>
      <div v-else-if="isDropdown" class="field">
        <Dropdown
          v-model="filterValue"
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
            v-model="filterValue.category"
            :options="filterOptions"
            :option-label="filterOptionProperty"
            class="w-16rem"
            type="text"
            @change="
              updateValue(
                'filterValue',
                updatedCategorizedValueObject('category', $event.value),
              )
            "
          ></Dropdown>
        </div>
        <div class="field">
          <InputText
            v-model="filterValue.value"
            class="w-16rem"
            type="text"
            @input="
              updateValue(
                'filterValue',
                updatedCategorizedValueObject('value', $event.target.value),
              )
            "
          ></InputText>
        </div>
      </div>
    </div>
    <div v-if="allowDelete" class="field col-fixed">
      <Button
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

  onMounted(() => {
    if (isDropdown.value) {
      filterValue.value = filterOptions.value[0];
    }
    updateValue("filterName", filterName.value);
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

  const filterOptions = computed(() => {
    if (filterName.value.store) {
      const store = filterName.value.store();
      return store.allItems;
    }
    return null;
  });

  const filterOptionProperty = computed(() => {
    return filterName.value.optionProperty
      ? filterName.value.optionProperty
      : "value";
  });

  const isDate = computed(() => {
    return inputType.value == "date";
  });
  const isCategorizedValue = computed(() => {
    return inputType.value == "categorizedValue";
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

  const updatedCategorizedValueObject = (attr, event) => {
    let category = null;
    let value = null;
    if (attr == "category") {
      category = event;
      value = filterValue.value.value;
    } else {
      category = filterValue.value.category;
      value = event;
    }
    return {
      category: category,
      value: value,
    };
  };

  const clearFilterValue = () => {
    if (isCategorizedValue.value) {
      filterValue.value = { category: filterOptions.value[0], value: null };
    } else if (isDropdown.value) {
      filterValue.value = filterOptions.value[0];
    } else {
      filterValue.value = null;
    }
  };

  const updateValue = (attribute, newValue) => {
    if (attribute === "filterName") {
      emit("update:modelValue", {
        filterName: newValue ? newValue.name : filterName.value.name,
        filterValue: filterValue.value,
      });
    } else if (attribute === "filterValue") {
      emit("update:modelValue", {
        filterName: filterName.value.name,
        filterValue: newValue,
      });
    }
  };
</script>
