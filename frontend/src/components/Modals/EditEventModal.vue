]
<!-- EditEventModal.vue -->
<!-- Edit various configured properties of an event -->

<template>
  <BaseModal
    :name="name"
    header="Edit Event"
    :style="{ width: '70vw' }"
    data-cy="edit-event-modal"
  >
    <div>
      <div v-if="error" class="p-col">
        <Message severity="error" @close="handleError">{{ error }}</Message>
      </div>
    </div>
    <div v-if="isLoading">Loading...</div>
    <div v-else-if="event" class="p-grid p-fluid p-formgrid p-grid">
      <div v-for="field of fieldOptions" :key="field.name" class="field grid">
        <label for="field.name" class="col-fixed" style="width: 30%"
          ><span style="font-weight: bold">{{ field.label }}</span></label
        >
        <div class="col" :data-cy="`event-${field.name}-field`">
          <NodeThreatSelector
            v-if="field.name == 'threats'"
            v-model="formFields['threats'].propertyValue"
          ></NodeThreatSelector>
          <NodeCommentEditor
            v-else-if="field.name == 'comments'"
            v-model="formFields['comments'].propertyValue"
          ></NodeCommentEditor>
          <NodePropertyInput
            v-else
            id="field.name"
            v-model="formFields[field.name]"
            :queue="event.queue.value"
            :fixed-property-type="true"
            :allow-delete="false"
            form-type="edit"
          />
        </div>
      </div>
    </div>
    <template #footer>
      <Button
        data-cy="nevermind-edit-event-button"
        label="Nevermind"
        icon="pi pi-times"
        class="p-button-text"
        @click="close"
      />
      <Button
        label="Save"
        icon="pi pi-check"
        data-cy="save-edit-event-button"
        @click="saveEvent()"
      />
    </template>
  </BaseModal>
</template>

<script setup lang="ts">
  import { computed, defineEmits, defineProps, ref, inject, watch } from "vue";

  import Button from "primevue/button";
  import Message from "primevue/message";

  import BaseModal from "@/components/Modals/BaseModal.vue";
  import NodePropertyInput from "@/components/Node/NodePropertyInput.vue";
  import NodeThreatSelector from "@/components/Node/NodeThreatSelector.vue";

  import { Event } from "@/services/api/event";
  import { useEventStore } from "@/stores/event";
  import { useModalStore } from "@/stores/modal";
  import { isObject } from "@/etc/validators";
  import NodeCommentEditor from "@/components/Node/NodeCommentEditor.vue";
  import { NodeComment } from "@/services/api/nodeComment";
  import { eventRead, eventUpdate } from "@/models/event";
  import { propertyOption } from "@/models/base";
  import { nodeCommentRead } from "@/models/nodeComment";

  const modalStore = useModalStore();
  const eventStore = useEventStore();

  const props = defineProps({
    name: { type: String, required: true },
    eventUuid: { type: String, required: true },
  });

  const emit = defineEmits(["requestReload"]);

  const availableEditFields = inject("availableEditFields") as Record<
    string,
    propertyOption[]
  >;

  const error = ref<string>();
  const event = ref<eventRead>();
  const originalEvent = ref<eventRead>();
  const fieldOptionObjects = ref<Record<keyof eventUpdate, propertyOption>>({});
  const formFields = ref<
    Record<keyof eventUpdate, { propertyType: string; propertyValue: unknown }>
  >({});
  const isLoading = ref<boolean>(false);

  // Load event data only when modal becomes active
  watch(modalStore, async () => {
    if (modalStore.active === props.name) {
      await initializeData();
    }
  });

  const fieldOptions = computed(() => {
    if (event.value) {
      return availableEditFields[event.value.queue.value];
    } else {
      return [];
    }
  });

  const updateData = computed((): eventUpdate[] => {
    if (!event.value) {
      return [];
    }
    // All updateData will have the event uuid
    const data: eventUpdate = { uuid: props.eventUuid };
    // Add the formatted valueds for all fields in the form
    for (const field in formFields.value) {
      if (formFields.value[field].propertyValue !== event.value[field]) {
        data[field] = formatValue(field, formFields.value[field].propertyValue);
      }
    }
    return [data];
  });

  const fetchEvent = async () => {
    event.value = await Event.read(props.eventUuid);
    originalEvent.value = JSON.parse(JSON.stringify(event.value));
  };

  const initializeData = async () => {
    isLoading.value = true;
    try {
      await fetchEvent();
      if (!event.value) {
        throw new Error("Event data not saved to local store");
      }
      if (!(event.value.queue.value in availableEditFields)) {
        throw new Error(
          `Could not load settings for this event queue: ${event.value.queue.value}`,
        );
      }

      for (const option of availableEditFields[event.value.queue.value]) {
        // Create a lookup by field/option name of all the fieldOptionObjects
        fieldOptionObjects.value[option.name] = option;
        // Set up all the form field objects (to be used in NodePropertyInput)
        formFields.value[option.name] = {
          propertyType: option.name,
          propertyValue: null,
        };
      }

      await resetForm();
    } catch (e: unknown) {
      if (typeof e === "string") {
        error.value = `Could not load event data: ${e}`;
      } else if (e instanceof Error) {
        error.value = `Could not load event data: ${e.message}`;
      }
    }
    isLoading.value = false;
  };

  const resetForm = async () => {
    if (event.value) {
      fillFormFields();
    }
  };

  const fillFormFields = () => {
    if (!event.value) {
      return;
    }
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
      if ("comments" in formFields.value) {
        await saveEventComments();
      }
    } catch (e: unknown) {
      if (typeof e === "string") {
        error.value = `Could not update event: ${e}`;
      } else if (e instanceof Error) {
        error.value = `Could not update event: ${e.message}`;
      }
    }

    isLoading.value = false;
    if (!error.value) {
      close();
      emit("requestReload");
    }
  };

  const saveEventComments = async () => {
    for (const comment of formFields.value["comments"]
      .propertyValue as nodeCommentRead[]) {
      const commentChanged = originalEvent.value?.comments.find(
        (originalComment) =>
          originalComment.uuid == comment.uuid &&
          originalComment.value != comment.value,
      );
      if (commentChanged) {
        await NodeComment.update(comment.uuid, {
          uuid: comment.uuid,
          value: comment.value,
        });
      }
    }
  };

  function formatValue(field: keyof eventUpdate, value: unknown) {
    // If the field value is an array, try to build a list of strings using either
    // the valueProperty (if available), or 'value' as the valueProperty as default
    if (Array.isArray(value)) {
      let valueProperty = "value";
      if (fieldOptionObjects.value[field].valueProperty) {
        valueProperty = fieldOptionObjects.value[field].valueProperty as string;
      }
      return value.map((x) => (x[valueProperty] ? x[valueProperty] : x));
    } else if (
      isObject(value) &&
      fieldOptionObjects.value[field].valueProperty
    ) {
      // If there is a 'valueProperty' available for the field, and the field value
      // Is an object, use that property as a value
      return value[fieldOptionObjects.value[field].valueProperty as string];
    }
    // Otherwise return the plain value
    return value;
  }

  const handleError = () => {
    error.value = undefined;
    close();
  };

  const close = () => {
    modalStore.close(props.name);
  };
</script>
