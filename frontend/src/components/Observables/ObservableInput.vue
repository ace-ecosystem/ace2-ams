<template>
  <FileUpload
    v-if="type == 'file'"
    mode="basic"
    class="inputfield"
  ></FileUpload>
  <span v-else>
    <InputText
      v-if="!multiAdd"
      v-model="value"
      placeholder="Enter a value"
      class="inputfield"
      type="text"
    ></InputText>
    <Textarea
      v-else
      v-model="value"
      placeholder="Enter a comma or newline-delimited list of values"
      class="inputfield"
    ></Textarea>
  </span>
</template>
<script setup lang="ts">
  import {
    defineEmits,
    defineProps,
    computed,
    ref,
    watch,
    inject,
    PropType,
  } from "vue";

  import FileUpload from "primevue/fileupload";
  import InputText from "primevue/inputtext";
  import Textarea from "primevue/textarea";

  const config = inject("config") as Record<string, any>;

  const emit = defineEmits(["update:modelValue"]);

  const props = defineProps({
    modelValue: {
      type: null as PropType<string | null>,
      required: true,
    },
    multiAdd: {
      type: Boolean,
      required: true,
    },
    type: {
      type: String,
      required: true,
    },
  });

  const value = ref(props.modelValue);

  const observableMetadata = computed(() => {
    const observableMetadata = config.observables.observableMetadata;

    // Check whether there is specific metadata config for this observable type
    if (props.type in observableMetadata) {
      // If so, add any available actions
      return observableMetadata[props.type];
    }
    return {};
  });

  watch(value, () => {
    emit("update:modelValue", value);
  });
</script>
