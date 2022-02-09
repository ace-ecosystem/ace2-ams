]
<!-- AssignModal.vue -->
<!-- 'Assign' alert action modal -->

<template>
  <BaseModal :name="name" header="Edit Event" :style="{ width: '45vw' }">
    <div>
      <div v-if="error" class="p-col">
        <Message severity="error" @close="handleError">{{ error }}</Message>
      </div>
    </div>
    <div v-if="isLoading">Loading...</div>
    <div v-else class="p-grid p-fluid p-formgrid p-grid">
      <div v-for="field of fieldOptions" :key="field.name" class="field grid">
        <label for="field.name" class="col-fixed" style="width: 100px">{{
          field.label
        }}</label>
        <div class="col">
          <FilterInput
            id="field.name"
            v-model="formFields[field.name]"
            :fixed-filter-name="true"
            :allow-delete="false"
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
      <Button
        label="Save"
        icon="pi pi-check"
        :disabled="!allowSave"
        @click="saveEvent()"
      />
    </template>
  </BaseModal>
</template>

<script setup>
  import {
    computed,
    defineProps,
    ref,
    defineEmits,
    watch,
    onMounted,
  } from "vue";

  import Button from "primevue/button";
  import Message from "primevue/message";

  import BaseModal from "@/components/Modals/BaseModal";

  import { useModalStore } from "@/stores/modal";
  import { useEventStore } from "@/stores/event";
  import FilterInput from "../Filters/FilterInput.vue";

  import { Event } from "@/services/api/event";

  const props = defineProps({
    name: { type: String, required: true },
    eventUuid: { type: String, required: true },
  });

  const fieldOptions = [
    {
      label: "Name",
      name: "name",
    },
    {
      label: "Owner",
      name: "owner",
    },
    {
      label: "Status",
      name: "status",
    },
    {
      label: "Event Type",
      name: "type",
    },
    {
      label: "Vectors",
      name: "vectors",
    },
    {
      label: "Severity",
      name: "riskLevel",
    },
    {
      label: "Prevention Tools",
      name: "preventionTools",
    },
    {
      label: "Comments",
      name: "comments",
    },
    {
      label: "Threat Actors",
      name: "threatActors",
    },
    {
      label: "Threats",
      name: "threats",
    },
  ];

  const formFields = ref({});

  onMounted(() => {
    for (const option of fieldOptions) {
      formFields.value[option.name] = {
        filterName: option.name,
        filterValue: null,
      };
    }
  });

  const isLoading = ref(false);

  const emit = defineEmits(["requestReload"]);

  const eventStore = useEventStore();
  const modalStore = useModalStore();

  import { useNodeThreatStore } from "@/stores/nodeThreat";
import NodeThreatSelector from "../Node/NodeThreatSelector.vue";
  const nodeThreatStore = useNodeThreatStore();

  const newThreats = ref([])
  const eventThreats = computed(() => {
    return [...nodeThreatStore.allItems, ...newThreats.value]
  });

  const showEditThreat = ref(false)
  const toggleShowEditThreat = () => {
    showEditThreat.value = !showEditThreat.value;
  }

  const error = ref(null);
  const event = ref(null);

  // Load event data when modal becomes active
  watch(modalStore, async () => {
    if (modalStore.active === props.name) {
      await nodeThreatStore.readAll();
      isLoading.value = true;
      await resetForm();
      isLoading.value = false;
    }
  });

  const resetForm = async () => {
    event.value = await Event.read(props.eventUuid);
    fillFormFields();
  };

  const fillFormFields = () => {
    for (const field in formFields.value) {
      formFields.value[field].filterValue =
        event.value[formFields.value[field].filterName];
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

  const updateData = computed(() => {
    return {
      uuid: props.event.uuid,
    };
  });

  const allowSave = computed(() => {
    return false;
  });

  const handleError = () => {
    error.value = null;
    close();
  };

  const close = () => {
    modalStore.close(props.name);
  };
</script>
