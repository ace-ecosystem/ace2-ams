<template>
  <div class="formgrid grid">
    <div class="field col-fixed">
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
          :option-label="filterOptionLabel"
          type="text"
          @change="updateValue('filterValue', $event.value)"
        ></Dropdown>
      </div>
      <div v-else-if="isMultiSelect" class="field">
        <Multiselect
          v-model="filterValue"
          class="inputfield w-16rem"
          :options="filterOptions"
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
    <div class="field col-fixed">
      <Button
        name="delete-filter"
        icon="pi pi-times"
        class="w-3rem"
        @click="$emit('deleteFormFilter')"
      />
    </div>
  </div>
</template>

<script>
  import InputText from "primevue/inputtext";

  import Button from "primevue/button";
  import Dropdown from "primevue/dropdown";

  import { DatePicker } from "v-calendar";

  import Chips from "primevue/chips";

  import Multiselect from "primevue/multiselect";

  export default {
    name: "FilterInput",
    components: {
      Button,
      Dropdown,
      InputText,
      Multiselect,
      Chips,
      DatePicker,
    },

    inject: ["availableFilters", "filterType"],

    props: ["modelValue"],
    emits: ["update:modelValue", "deleteFormFilter"],

    data() {
      return {
        filterName: this.getFilterNameObject(this.modelValue.filterName),
        filterValue: this.modelValue.filterValue,
      };
    },

    computed: {
      filterOptions() {
        if (this.filterName.options) {
          const options =
            this.$store.getters[`${this.filterName.options}/allItems`];
          if (options) {
            return options;
          }
        }
        return null;
      },
      filterOptionLabel() {
        return this.filterName.optionLabel
          ? this.filterName.optionLabel
          : "value";
      },
      filterOptionValue() {
        return this.filterName.optionValue ? this.filterName.optionValue : null;
      },
      isDate() {
        return this.inputType == "date";
      },
      isCategorizedValue() {
        return this.inputType == "categorizedValue";
      },
      isChips() {
        return this.inputType == "chips";
      },
      isInputText() {
        return this.inputType == "inputText";
      },
      isDropdown() {
        return this.inputType == "select";
      },
      isMultiSelect() {
        return this.inputType == "multiselect";
      },
      inputType() {
        return this.filterName ? this.filterName.type : null;
      },
    },

    mounted() {
      this.updateValue("filterName", null, this.filterName);
      this.filterValue = this.getFilterValueObject(this.filterValue);
    },

    methods: {
      updatedCategorizedValueObject(attr, event) {
        let category = null;
        let value = null;
        if (attr == "category") {
          category = event;
          value = this.filterValue.value;
        } else {
          category = this.filterValue.category;
          value = event;
        }
        return {
          category: category,
          value: value,
        };
      },
      clearFilterValue() {
        if (this.isCategorizedValue) {
          this.filterValue = { category: this.filterOptions[0], value: null };
        } else {
          this.filterValue = null;
        }
      },
      getFilterNameObject(filterName) {
        if (!filterName) {
          return this.availableFilters[0];
        }
        let filter = this.availableFilters.find((filter) => {
          return filter.name === filterName;
        });
        filter = filter ? filter : null;
        return filter;
      },
      getFilterValueObject(filterValue) {
        if (!filterValue || !this.filterOptions) {
          return filterValue;
        }
        let value = this.filterOptions.find((option) => {
          return option[this.filterOptionValue] === filterValue;
        });
        value = value ? value : null;
        return value;
      },
      updateValue(attribute, newValue) {
        if (attribute === "filterName") {
          this.$emit("update:modelValue", {
            filterName: newValue ? newValue.name : this.filterName.name,
            filterValue: this.filterValue,
          });
        } else if (attribute === "filterValue") {
          this.$emit("update:modelValue", {
            filterName: this.filterName.name,
            filterValue: this.filterOptionValue
              ? newValue[this.filterOptionValue]
              : newValue,
          });
        }
      },
    },
  };
</script>
