/* eslint-disable vue/no-mutating-props */
<template>
  <Dropdown
    v-model="filterName"
    :options="alertFilters"
    option-label="label"
    type="text"
    @change="
      clearFilterValue();
      $emit('update:modelValue', {
        filterName: $event.value,
        filterValue: null,
      });
    "
  />
  <InputText
    v-if="isInputText"
    v-model="filterValue"
    type="text"
    @input="
      $emit('update:modelValue', {
        filterName: modelValue.filterName,
        filterValue: $event.target.value,
      })
    "
  ></InputText>
  <Dropdown
    v-else-if="isDropdown"
    v-model="filterValue"
    :options="alertFilters"
    option-label="label"
    type="text"
    @input="
      $emit('update:modelValue', {
        filterName: modelValue.filterName,
        filterValue: $event.target.value,
      })
    "
  ></Dropdown>
  <Multiselect
    v-else-if="isMultiSelect"
    v-model="filterValue"
    :options="alertFilters"
    option-label="label"
    type="text"
    @input="
      $emit('update:modelValue', {
        filterName: modelValue.filterName,
        filterValue: $event.target.value,
      })
    "
  ></Multiselect>
  <Chips
    v-else-if="isChips"
    v-model="filterValue"
    @input="
      $emit('update:modelValue', {
        filterName: modelValue.filterName,
        filterValue: $event.target.value,
      })
    "
  ></Chips>
  <DateRangePicker
    v-else-if="isDate"
    v-model="filterValue"
    @input="
      $emit('update:modelValue', {
        filterName: modelValue.filterName,
        filterValue: $event.target.value,
      })
    "
  ></DateRangePicker>
</template>

<script>
  import { alertFilters } from "@/etc/constants";
  import { mapActions } from "vuex";
  import InputText from "primevue/inputtext";

  import Chips from "primevue/chips";
  import DateRangePicker from "@/components/UserInterface/DateRangePicker";

  import Button from "primevue/button";
  import Dropdown from "primevue/dropdown";
  import Multiselect from "primevue/multiselect";

  import BaseModal from "@/components/Modals/BaseModal";

  export default {
    name: "AlertFilterInput",
    components: { Dropdown, InputText, Multiselect, Chips, DateRangePicker },

    inject: ["filterType", "rangeFilterOptions", "rangeFilters"],

    props: ["modelValue"],
    emits: ["update:modelValue"],

    data() {
      return {
        filterName: this.modelValue.filterName,
        filterValue: this.modelValue.filterValue,
      };
    },

    computed: {
      alertFilters() {
        return alertFilters;
      },
      isDate() {
        return this.inputType == "date";
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
        return this.modelValue.filterName
          ? this.modelValue.filterName.type
          : null;
      },
    },

    methods: {
      clearFilterValue() {
        this.filterValue = null;
      },
    },
  };
</script>
