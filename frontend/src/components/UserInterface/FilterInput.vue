<template>
  <Dropdown
    v-model="filterName"
    :options="availableFilters"
    option-label="label"
    type="text"
    @change="
      clearFilterValue();
      updateValue('filterName', $event.value);
    "
  />
  <InputText
    v-if="isInputText"
    v-model="filterValue"
    type="text"
    @input="updateValue('filterValue', $event.target.value)"
  ></InputText>
  <Dropdown
    v-else-if="isDropdown"
    v-model="filterValue"
    :options="filterOptions"
    type="text"
    @change="updateValue('filterValue', $event.value)"
  ></Dropdown>
  <Multiselect
    v-else-if="isMultiSelect"
    v-model="filterValue"
    :options="filterOptions"
    type="text"
    @change="updateValue('filterValue', $event.value)"
  ></Multiselect>
  <Chips
    v-else-if="isChips"
    v-model="filterValue"
    @update:model-value="updateValue('filterValue', $event)"
  ></Chips>
  <DatePicker
    v-else-if="isDate"
    v-model="filterValue"
    mode="dateTime"
    is24hr
    @update:model-value="updateValue('filterValue', $event)"
  >
    <template #default="{ inputValue, inputEvents }">
      <div class="p-inputgroup">
        <InputText
          type="text"
          :value="inputValue"
          placeholder="Enter a date!"
          v-on="inputEvents"
        />
      </div>
    </template>
  </DatePicker>
  <div v-else-if="isCategorizedValue">
    <Dropdown
      v-model="filterValue.category"
      :options="filterOptions"
      type="text"
      @change="
        updateValue(
          'filterValue',
          updatedCategorizedValueObject('category', $event.value),
        )
      "
    ></Dropdown>
    <InputText
      v-model="filterValue.value"
      type="text"
      @input="
        updateValue(
          'filterValue',
          updatedCategorizedValueObject('value', $event.target.value),
        )
      "
    ></InputText>
  </div>
</template>

<script>
  import InputText from "primevue/inputtext";

  import Dropdown from "primevue/dropdown";

  import { DatePicker } from "v-calendar";

  import Chips from "primevue/chips";

  import Multiselect from "primevue/multiselect";

  export default {
    name: "FilterInput",
    components: {
      Dropdown,
      InputText,
      Multiselect,
      Chips,
      DatePicker,
    },

    inject: ["availableFilters", "filterType"],

    props: ["modelValue"],
    emits: ["update:modelValue"],

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
            return options.map((option) => option[this.filterOptionLabel]);
          }
        }
        return null;
      },
      filterOptionLabel() {
        return this.filterName.optionValue
          ? this.filterName.optionValue
          : "value";
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
          this.filterValue = { category: this.filterOptions[0], val: null };
        } else {
          this.filterValue = null;
        }
      },
      getFilterNameObject(filterName) {
        if (!filterName) {
          filterName = "disposition";
        }
        let filter = this.availableFilters.filter((filter) => {
          return filter.name === filterName;
        });
        console.log(filter);
        filter = filter ? filter[0] : null;
        return filter;
      },
      updateValue(attribute, newValue) {
        if (attribute === "filterName") {
          this.$emit("update:modelValue", {
            filterName: newValue,
            filterValue: this.filterValue,
          });
        } else if (attribute === "filterValue") {
          this.$emit("update:modelValue", {
            filterName: this.filterName,
            filterValue: newValue,
          });
        }
      },
    },
  };
</script>
