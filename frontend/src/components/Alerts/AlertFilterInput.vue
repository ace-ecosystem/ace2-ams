/* eslint-disable vue/no-mutating-props */
<template>
  <Dropdown
    v-model="modelValue.filterName"
    :options="alertFilters"
    option-label="label"
    type="text"
    @change="
      $emit('update:modelValue', {
        filterName: $event.value,
        filterValue: modelValue.filterValue,
      })
    "
  />
  <InputText
    v-model="modelValue.filterValue"
    type="text"
    @input="
      $emit('update:modelValue', {
        filterName: modelValue.filterName,
        filterValue: $event.target.value,
      })
    "
  ></InputText>
  <Button
    name="delete-filter"
    icon="pi pi-times"
    class="inputfield"
    @click="$emit('deleteFormFilter')"
  />
</template>

<script>
  import { alertFilters } from "@/etc/constants";
  import { mapActions } from "vuex";
  import InputText from "primevue/inputtext";

  import Button from "primevue/button";
  import Dropdown from "primevue/dropdown";

  import BaseModal from "@/components/Modals/BaseModal";

  export default {
    name: "AlertFilterInput",
    components: { Button, Dropdown, InputText },

    inject: ["filterType", "rangeFilterOptions", "rangeFilters"],

    props: ["modelValue"],
    emits: ["update:modelValue", "deleteFormFilter"],

    computed: {
      alertFilters() {
        return alertFilters;
      },
    },
  };
</script>
