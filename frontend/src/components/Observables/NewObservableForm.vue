<template>
  <div id="observables-list">
    <div class="formgrid grid">
      <div class="field col-2 px-1">
        <label for="observable-time">Time (UTC)</label>
      </div>
      <div class="field col-2 px-1">
        <label for="observable-type">Type</label>
      </div>
      <div class="field col-3 px-1">
        <label for="observable-value">Value</label>
      </div>
      <div class="field col-3 px-1">
        <label for="observable-directives">Directives</label>
      </div>
      <div class="field col-1">
        <Button
          v-if="observablesListEmpty"
          id="add-observable-empty"
          icon="pi pi-plus"
          class="p-button-rounded inputfield"
          @click="addFormObservable"
        />
      </div>
    </div>
    <div
      v-for="(observable, index) in observablesCopy"
      :key="index"
      name="observable-input"
      class="p-col-12"
    >
      <div class="formgrid grid">
        <div class="field col-2 px-1">
          <DatePicker
            v-model="observablesCopy[index].time"
            mode="dateTime"
            class="inputfield w-16rem"
            is24hr
            timezone="UTC"
          >
            <template #default="{ inputValue, inputEvents }">
              <div class="p-inputgroup">
                <InputText
                  name="observable-time"
                  class="inputfield w-16rem"
                  type="text"
                  :value="inputValue"
                  placeholder="No time selected"
                  v-on="inputEvents"
                />
              </div>
            </template>
          </DatePicker>
        </div>
        <div class="field col-2 px-1">
          <Dropdown
            v-model="observablesCopy[index].type"
            name="observable-type"
            class="inputfield w-full"
            option-label="value"
            option-value="value"
            :options="observableTypeStore.items"
          />
        </div>
        <div class="field px-1" name="observable-value">
          <span class="inputfield">
            <span style="display: inline">
              <ObservableInput
                v-model:observableValue="observablesCopy[index].value"
                v-model:invalid="observablesCopy[index].invalid"
                :multi-add="observablesCopy[index].multiAdd"
                :type="observablesCopy[index].type"
              ></ObservableInput>
            </span>
            <span>
              <Button icon="pi pi-list" @click="toggleMultiObservable(index)" />
            </span>
          </span>
        </div>
        <div class="field col-3 px-1">
          <MultiSelect
            v-model="observablesCopy[index].directives"
            name="observable-directives"
            placeholder="No directives selected"
            class="inputfield w-full"
            option-label="value"
            option-value="value"
            :options="nodeDirectiveStore.items"
          />
        </div>
        <div class="field col-1">
          <Button
            name="delete-observable"
            icon="pi pi-times"
            class="inputfield"
            @click="deleteFormObservable(index)"
          />
        </div>
        <div class="field col-1">
          <Button
            v-if="isLastObservable(index)"
            id="add-observable"
            label="Add"
            icon="pi pi-plus"
            class="p-button-rounded inputfield"
            @click="addFormObservable"
          />
        </div>
      </div>
    </div>
  </div>
</template>
<script setup lang="ts">
  import {
    computed,
    defineProps,
    defineEmits,
    PropType,
    onMounted,
    ref,
    watch,
  } from "vue";

  import Button from "primevue/button";
  import Dropdown from "primevue/dropdown";
  import InputText from "primevue/inputtext";
  import MultiSelect from "primevue/multiselect";

  import ObservableInput from "@/components/Observables/ObservableInput.vue";
  import { DatePicker } from "v-calendar";

  import { useObservableTypeStore } from "@/stores/observableType";
  import { useNodeDirectiveStore } from "@/stores/nodeDirective";

  const emit = defineEmits(["update:modelValue"]);

  interface formObservable {
    time?: Date;
    type: string;
    multiAdd: boolean;
    invalid: boolean;
    value: any;
    directives?: string[];
  }

  const props = defineProps({
    modelValue: {
      type: Array as PropType<formObservable[]>,
      required: true,
    },
  });

  const observablesCopy = ref<formObservable[]>(props.modelValue);
  const observableTypeStore = useObservableTypeStore();
  const nodeDirectiveStore = useNodeDirectiveStore();

  onMounted(() => {
    // observablesCopy.value = props.modelValue;
    if (!observablesCopy.value.length) {
      addFormObservable();
    }
  });

  const observablesListEmpty = computed(() => {
    return !observablesCopy.value.length;
  });

  const lastObservableIndex = computed(() => {
    return observablesCopy.value.length - 1;
  });

  const deleteFormObservable = (index: number) => {
    observablesCopy.value.splice(index, 1);
  };

  const isLastObservable = (index: number) => {
    return index == lastObservableIndex.value;
  };
  const addFormObservable = () => {
    observablesCopy.value.push({
      time: undefined,
      type: "file",
      multiAdd: false,
      invalid: false,
      value: undefined,
      directives: [],
    });
  };

  const toggleMultiObservable = (index: number) => {
    observablesCopy.value[index].multiAdd =
      !observablesCopy.value[index].multiAdd;
  };

  watch(observablesCopy, () => {
    emit("update:modelValue", observablesCopy);
  });
</script>
