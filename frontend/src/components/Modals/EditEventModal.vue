]
<!-- EditEventModal.vue -->
<!-- Edit various configured properties of an event -->

<template>
  <BaseModal :name="name" header="Edit Event" :style="{ width: '70vw' }">
    <div>
      <div v-if="error" class="p-col">
        <Message severity="error" @close="handleError">{{ error }}</Message>
      </div>
    </div>
    <div v-if="isLoading">Loading...</div>
    <div v-else class="p-grid p-fluid p-formgrid p-grid">
      <div v-for="field of fieldOptions" :key="field.name" class="field grid">
        <label for="field.name" class="col-fixed" style="width: 30%"
          ><span style="font-weight: bold">{{ field.label }}</span></label
        >
        <div class="col">
          <NodeThreatSelector
            v-if="field.name == 'threats'"
            v-model="formFields['threats'].propertyValue"
          ></NodeThreatSelector>
          <NodePropertyInput
            v-else
            id="field.name"
            v-model="formFields[field.name]"
            :fixed-property-type="true"
            :allow-delete="false"
            form-type="edit"
          />
        </div>
      </div>
    </div>
    <template #footer>
      <Button
        label="Nevermind"
        icon="pi pi-times"
        class="p-button-text"
        @click="close"
      />
      <Button label="Save" icon="pi pi-check" @click="saveEvent()" />
    </template>
  </BaseModal>
</template>

<script setup>
  import {
    computed,
    defineEmits,
    defineProps,
    onMounted,
    ref,
    inject,
    watch,
  } from "vue";

  import Button from "primevue/button";
  import Message from "primevue/message";

  import BaseModal from "@/components/Modals/BaseModal";
  import NodePropertyInput from "../Node/NodePropertyInput.vue";
  import NodeThreatSelector from "../Node/NodeThreatSelector.vue";

  import { Event } from "@/services/api/event";
  import { useEventStore } from "@/stores/event";
  import { useModalStore } from "@/stores/modal";
  import { isObject, populateEventStores } from "@/etc/helpers";

  const modalStore = \\
  seModalStore();
  const eventStore = useEventStore();

  const props = defineProps({
    name: { type: String, required: true },
    eventUuid: { type: String, required: true },
  });

  const emit = defineEmits(["requestReload"]);

  const fieldOptions = inject("availableEditFields");

  const error = ref(null);
  const event = ref(null);
  const fieldOptionObjects = ref({});
  const formFields = ref({});
  const isLoading = ref(false);

  onMounted(() => {
    for (const option of fieldOptions) {
      // Create a lookup by field/option name of all the fieldOptionObjects
      fieldOptionObjects.value[option.name] = option;
      // Set up all the form field objects (to be used in NodePropertyInput)
      formFields.value[option.name] = {
        propertyType: option.name,
        propertyValue: null,
      };
    }
  });

  // Load event data only when modal becomes active
  watch(modalStore, async () => {
    if (modalStore.active === props.name) {
      isLoading.value = true;
      try {
        await populateEventStores();
        await resetForm();
      } catch (err) {
        error.value = err.message;
      }
      isLoading.value = false;
    }
  });

  const updateData = computed(() => {
    // All updateData will have the event uuid
    const data = { uuid: props.eventUuid };
    // Add the formatted valueds for all fields in the form
    for (const field in formFields.value) {
      data[field] = formatValue(field, formFields.value[field].propertyValue);
    }
    return [data];
  });

  const resetForm = async () => {
    event.value = await Event.read(props.eventUuid);
    if (event.value) {
    fillFormFields();
    }
  };

  const fillFormFields = () => {
    // Fill in form field values with data from event
    for (const field in formFields.value) {
      formFields.value[field].propertyValue =
        event.value[formFields.value[field].propertyType];
    }
  };

  const saveEvent = async () => {
    isLoading.value = true;

    try {
      await eventStore.update(updateData.value);
    } catch (err) {
      error.value = err.message;
    }

    isLoading.value = false;
    if (!error.value) {
      close();
      emit("requestReload");
    }
  };

  function formatValue(field, value) {
    // If there is a 'valueProperty' available for the field, and the field value
    // Is an object, use that property as a value
    if (fieldOptionObjects.value[field].valueProperty && isObject(value)) {
      return value[fieldOptionObjects.value[field].valueProperty];
      // If the field value is an array, try to build a list of strings using either
      // the valueProperty (if available), or 'value' as the valueProperty as default
    } else if (Array.isArray(value)) {
      let valueProperty = "value";
      if (fieldOptionObjects.value[field].valueProperty) {
        valueProperty = fieldOptionObjects.value[field].valueProperty;
      }
      return value.map((x) => x[valueProperty]);
    }
    // Otherwise return the plain value
    return value;
  }

  const handleError = () => {
    error.value = null;
    close();
  };

  const close = () => {
    modalStore.close(props.name);
  };
</script>
