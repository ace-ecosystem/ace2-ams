<template>
  <div class="formgrid grid">
    <div v-if="!fixedPropertyType" class="field col-fixed">
      <Dropdown
        v-model="propertyType"
        data-cy="property-input-type"
        :options="propertyTypeOptions"
        option-label="label"
        type="text"
        class="w-13rem"
        tabindex="1"
        @change="
          clearPropertyValue();
          updateValue('propertyType', $event.value);
        "
      />
    </div>
    <div class="col w-16rem">
      <div v-if="isInputText" class="field">
        <InputText
          v-model="propertyValue"
          data-cy="property-input-value"
          class="inputfield w-16rem"
          type="text"
          @input="updateValue('propertyValue', $event.target.value)"
        ></InputText>
      </div>
      <div v-else-if="isDropdown" class="field">
        <Dropdown
          v-model="propertyValue"
          data-cy="property-input-value"
          class="inputfield w-16rem"
          :options="propertyValueOptions"
          :option-label="propertyValueOptionProperty"
          type="text"
          @change="updateValue('propertyValue', $event.value)"
        ></Dropdown>
      </div>
      <div v-else-if="isMultiSelect" class="field">
        <Multiselect
          v-model="propertyValue"
          data-cy="property-input-value"
          class="inputfield w-16rem"
          :options="propertyValueOptions"
          :option-label="propertyValueOptionProperty"
          type="text"
          @change="updateValue('propertyValue', $event.value)"
        ></Multiselect>
      </div>
      <div v-else-if="isChips" class="field p-fluid">
        <Chips
          v-model="propertyValue"
          data-cy="property-input-value"
          class="w-full"
          @update:model-value="updateValue('propertyValue', $event)"
        ></Chips>
      </div>
      <div v-else-if="isDate" class="field">
        <DatePicker
          v-model="propertyValue"
          mode="dateTime"
          class="inputfield w-16rem"
          is24hr
          @update:model-value="updateValue('propertyValue', $event)"
        >
          <template #default="{ inputValue, inputEvents }">
            <div class="p-inputgroup">
              <InputText
                data-cy="property-input-value"
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
            data-cy="property-input-value-category"
            :options="propertyValueOptions"
            :option-label="propertyValueOptionProperty"
            class="w-16rem"
            type="text"
            @change="updateValue('propertyValue', categorizedValueObject)"
          ></Dropdown>
        </div>
        <div class="field">
          <InputText
            v-model="categorizedValueValue"
            data-cy="property-input-value-value"
            class="w-16rem"
            type="text"
            @input="updateValue('propertyValue', categorizedValueObject)"
          ></InputText>
        </div>
      </div>
    </div>
    <div v-if="allowDelete" class="field col-fixed">
      <Button
        data-cy="property-input-delete"
        name="delete-property"
        icon="pi pi-times"
        class="w-3rem"
        @click="$emit('deleteFormField')"
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
  const availableEditFields = inject("availableEditFields");

  const emit = defineEmits(["update:modelValue", "deleteFormField"]);
  const props = defineProps({
    queue: { type: String, required: true },
    modelValue: { type: Object, required: true },
    fixedPropertyType: { type: Boolean, required: false },
    allowDelete: { type: Boolean, required: false },
    formType: { type: String, required: true },
  });

  const propertyTypeOptions =
    props.formType == "filter"
      ? availableFilters
      : props.formType == "edit"
      ? availableEditFields[props.queue]
      : null;

  const getPropertyTypeObject = (propertyType) => {
    if (!propertyType) {
      return propertyTypeOptions ? propertyTypeOptions[0] : null;
    }
    let property = propertyTypeOptions.find((option) => {
      return option.name === propertyType;
    });
    property = property ? property : null;
    return property;
  };

  const propertyType = ref(
    getPropertyTypeObject(props.modelValue.propertyType),
  );
  const propertyValue = ref(props.modelValue.propertyValue);

  // The categorizedValue property is a bit tricky
  // We need to copy the values and use those as the model
  // Otherwise, they will directly modify the filterStore state :/
  const categorizedValueCategory = ref(null);
  const categorizedValueValue = ref(null);

  const propertyValueOptions = computed(() => {
    if (propertyType.value && propertyType.value.store) {
      const store = propertyType.value.store();
      if (propertyType.value.queueDependent) {
        return store.getItemsByQueue(props.queue);
      } else {
        return store.allItems;
      }
    }
    return null;
  });

  onMounted(() => {
    // This will update the property to the default if one wasn't provided
    updateValue("propertyType", propertyType.value);

    // This will udpate the property value to the default (if available) if one wasn't provided
    if (!propertyValue.value) {
      clearPropertyValue();
      updateValue("propertyValue", propertyValue.value);
    }

    // we need to fill in the placeholder refs (see note above) for categorized value
    else if (isCategorizedValue.value) {
      categorizedValueCategory.value = propertyValue.value.category;
      categorizedValueValue.value = propertyValue.value.value;
    }
  });

  const propertyValueOptionProperty = computed(() => {
    if (propertyType.value) {
      return propertyType.value.optionProperty
        ? propertyType.value.optionProperty
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
    return propertyType.value ? propertyType.value.type : null;
  });

  watch(propertyType, async () => {
    if (propertyType.value.store) {
      const store = propertyType.value.store();
      await store.readAll();
    }
  });

  const clearPropertyValue = () => {
    if (isCategorizedValue.value) {
      propertyValue.value = {
        category: propertyValueOptions.value[0],
        value: null,
      };
      categorizedValueCategory.value = propertyValueOptions.value[0];
      categorizedValueValue.value = null;
    } else if (isDropdown.value) {
      propertyValue.value = propertyValueOptions.value[0];
    } else {
      propertyValue.value = null;
    }
  };

  const updateValue = (attribute, newValue) => {
    if (attribute === "propertyType") {
      emit("update:modelValue", {
        propertyType: newValue ? newValue.name : propertyType.value,
        propertyValue: propertyValue.value,
      });
    } else if (attribute === "propertyValue") {
      emit("update:modelValue", {
        propertyType: propertyType.value
          ? propertyType.value.name
          : propertyType.value,
        propertyValue: newValue,
      });
    }
  };
</script>
