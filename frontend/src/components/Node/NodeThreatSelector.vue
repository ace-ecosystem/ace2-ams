<template>
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
        data-cy="threat-name"
        v-model="newThreatName"
        placeholder="My new threat"
        :disabled="editingExistingThreat"
      ></InputText>
    </div>
    <div class="field col-fixed" style="width: 150px">
      <MultiSelect
        data-cy="threat-types"
        append-to="self"
        v-model="newThreatTypes"
        :options="nodeThreatTypeStore.allItems"
        option-label="value"
        :show-toggle-all="false"
      ></MultiSelect>
    </div>
    <div class="field col-fixed">
      <Button
        :icon="editThreatCloseIcon"
        @click="closeEditThreatPanel"
        data-cy="close-edit-threat-panel-button"
      />
    </div>
    <div class="field col-fixed">
      <Button
        icon="pi pi-check"
        @click="submitNewThreat"
        data-cy="save-threat-button"
      />
    </div>
  </div>
</template>

<script setup>
  import { computed, defineProps, ref, defineEmits, onMounted } from "vue";

  import Button from "primevue/button";
  import InputText from "primevue/inputtext";
  import Listbox from "primevue/listbox";
  import MultiSelect from "primevue/multiselect";

  import { useNodeThreatStore } from "@/stores/nodeThreat";
  import { useNodeThreatTypeStore } from "@/stores/nodeThreatType";

  const nodeThreatStore = useNodeThreatStore();
  const nodeThreatTypeStore = useNodeThreatTypeStore();

  const props = defineProps({
    modelValue: { type: Array, required: true },
  });

  const emit = defineEmits(["update:modelValue"]);

  const editingExistingThreat = ref(false);
  const editingExistingThreatUuid = ref();
  const newThreatName = ref(null);
  const newThreatTypes = ref([]);
  const selectedThreats = ref(props.modelValue);
  const showEditThreat = ref(false);

  const formatThreatTypes = (threatTypes) => {
    return threatTypes.map((x) => x.value).join(", ");
  };

  const closeEditThreatPanel = () => {
    newThreatName.value = null;
    newThreatTypes.value = [];
    editingExistingThreat.value = false;
    editingExistingThreatUuid.value = undefined;
    showEditThreat.value = false;
  };

  const openEditThreatPanel = (threat) => {
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
    if (editingExistingThreat.value) {
      await nodeThreatStore.update(editingExistingThreatUuid.value, {
        types: newThreatTypes.value.map((x) => x.value),
      });
    } else {
      await nodeThreatStore.create({
        value: newThreatName.value,
        // TODO: This needs to be based on the current user's preferred queue
        queues: ["external"],
        types: newThreatTypes.value.map((x) => x.value),
      });
    }
    closeEditThreatPanel();
  };

  const updateModelValue = (event) => {
    emit("update:modelValue", event.value);
  };

  const editThreatCloseIcon = computed(() => {
    if (editingExistingThreat.value) {
      return "pi pi-times";
    } else {
      return "pi pi-trash";
    }
  });

  onMounted(async () => {
    await nodeThreatStore.readAll();
  });
</script>
