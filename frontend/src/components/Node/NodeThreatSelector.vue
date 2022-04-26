<template>
  <Toast data-cy="toast-error" />
  <div class="formgrid grid flex align-content-center">
    <div class="field col-fixed">
      <Listbox
        v-model="selectedThreats"
        :options="nodeThreatStore.allItems"
        :multiple="true"
        option-label="value"
        list-style="max-height:100px"
        @change="updateModelValue"
      >
        <template #option="slotProps">
          <span class="align-items-center flex">
            <span style="width: 150px">
              {{ slotProps.option.value }}
            </span>
            <i
              v-tooltip.top="{
                value: formatThreatTypes(slotProps.option.types),
              }"
              class="pi pi-info-circle"
            />

            <Button
              v-tooltip.top="'Edit'"
              data-cy="edit-threat-button"
              icon="pi pi-pencil"
              class="p-button-rounded p-button-text pi-button-sm"
              @click="openEditThreatPanel(slotProps.option)"
            />
          </span>
        </template>
      </Listbox>
    </div>
    <div class="field col-fixed align-items-center flex">
      <Button
        icon="pi pi-plus"
        data-cy="new-threat-button"
        label="New"
        @click="openEditThreatPanel(null)"
      ></Button>
    </div>
  </div>

  <div
    v-if="showEditThreat"
    class="formgrid grid flex align-content-center"
    data-cy="edit-threat-panel"
  >
    <div class="field col-fixed" style="width: 150px">
      <InputText
        v-model="newThreatName"
        data-cy="threat-name"
        placeholder="My new threat"
        :disabled="editingExistingThreat"
      ></InputText>
    </div>
    <div class="field col-fixed" style="width: 150px">
      <MultiSelect
        v-model="newThreatTypes"
        data-cy="threat-types"
        append-to="self"
        :options="nodeThreatTypeStore.allItems"
        option-label="value"
        :show-toggle-all="false"
      ></MultiSelect>
    </div>
    <div class="field col-fixed">
      <Button
        :icon="editThreatCloseIcon"
        data-cy="close-edit-threat-panel-button"
        @click="closeEditThreatPanel"
      />
    </div>
    <div class="field col-fixed">
      <Button
        icon="pi pi-check"
        :disabled="!newThreatName || !newThreatTypes.length"
        data-cy="save-threat-button"
        @click="submitNewThreat"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
  import {
    computed,
    defineProps,
    ref,
    defineEmits,
    onMounted,
    PropType,
  } from "vue";

  import Button from "primevue/button";
  import InputText from "primevue/inputtext";
  import Listbox from "primevue/listbox";
  import MultiSelect from "primevue/multiselect";
  import Toast from "primevue/toast";
  import { useToast } from "primevue/usetoast";

  import { useNodeThreatStore } from "@/stores/nodeThreat";
  import { useNodeThreatTypeStore } from "@/stores/nodeThreatType";
  import { nodeThreatTypeRead } from "@/models/nodeThreatType";
  import { nodeThreatRead } from "@/models/nodeThreat";

  const nodeThreatStore = useNodeThreatStore();
  const nodeThreatTypeStore = useNodeThreatTypeStore();
  const toast = useToast();

  const props = defineProps({
    modelValue: { type: Array as PropType<nodeThreatRead[]>, required: true },
    queue: { type: String, required: true },
  });

  const emit = defineEmits(["update:modelValue"]);

  const editingExistingThreat = ref(false);
  const editingExistingThreatUuid = ref<string>();
  const newThreatName = ref<string>();
  const newThreatTypes = ref<nodeThreatTypeRead[]>([]);
  const selectedThreats = ref<nodeThreatRead[]>(props.modelValue);
  const showEditThreat = ref(false);

  const formatThreatTypes = (threatTypes: nodeThreatTypeRead[]) => {
    return threatTypes.map((x) => x.value).join(", ");
  };

  const closeEditThreatPanel = () => {
    newThreatName.value = undefined;
    newThreatTypes.value = [];
    editingExistingThreat.value = false;
    editingExistingThreatUuid.value = undefined;
    showEditThreat.value = false;
  };

  const openEditThreatPanel = (threat: nodeThreatRead | null) => {
    showEditThreat.value = true;
    if (threat) {
      editingExistingThreat.value = true;
      editingExistingThreatUuid.value = threat.uuid;
      newThreatName.value = threat.value;
      // Preselect any threat types that already belong to the current threat
      // that also exist in the nodeThreatTypeStore
      newThreatTypes.value = nodeThreatTypeStore.allItems.filter(
        (threatTypeOption) =>
          threat.types.some(
            (threatType) => threatType.value === threatTypeOption.value,
          ),
      );
    } else {
      editingExistingThreat.value = false;
    }
  };

  const submitNewThreat = async () => {
    try {
      if (editingExistingThreat.value && editingExistingThreatUuid.value) {
        await nodeThreatStore.update(editingExistingThreatUuid.value, {
          types: newThreatTypes.value.map((x) => x.value),
        });
      } else if (newThreatName.value) {
        await nodeThreatStore.create({
          value: newThreatName.value,
          queues: [props.queue],
          types: newThreatTypes.value.map((x) => x.value),
        });
      }
    } catch (e: unknown) {
      if (typeof e === "string") {
        showError({
          detail: e,
        });
      } else if (e instanceof Error) {
        showError({
          detail: e.message,
        });
      }
    }

    closeEditThreatPanel();
  };

  const updateModelValue = (event: any) => {
    emit("update:modelValue", event.value);
  };

  const editThreatCloseIcon = computed(() => {
    if (editingExistingThreat.value) {
      return "pi pi-times";
    } else {
      return "pi pi-trash";
    }
  });

  const showError = (args: { detail: string }) => {
    toast.add({
      severity: "error",
      summary: "Action Failed",
      detail: args.detail,
      life: 6000,
    });
  };

  onMounted(async () => {
    await nodeThreatStore.readAll();
  });
</script>
