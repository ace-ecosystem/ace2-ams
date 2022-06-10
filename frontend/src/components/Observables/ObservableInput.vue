<template>
  <span v-if="type == 'file'" name="observable-file-upload">
    <FileUpload
      mode="basic"
      class="inputfield"
      :multiple="multiAdd"
      :choose-label="fileUploadLabel"
    >
    </FileUpload>
  </span>
  <span v-else>
    <InputText
      v-if="!multiAdd"
      v-model="value"
      :placeholder="placeholder"
      :class="styleClasses"
      type="text"
    ></InputText>
    <Textarea
      v-else
      v-model="value"
      :placeholder="placeholder"
      :class="styleClasses"
    ></Textarea>
    <small v-if="!inputIsValid" class="p-error">{{ type }} is malformed</small>
  </span>
</template>
<script setup lang="ts">
  import { defineEmits, defineProps, computed, ref, watch, inject } from "vue";

  import FileUpload from "primevue/fileupload";
  import InputText from "primevue/inputtext";
  import Textarea from "primevue/textarea";

  const config = inject("config") as Record<string, any>;

  const emit = defineEmits(["update:observableValue", "update:invalid"]);

  const props = defineProps({
    observableValue: {
      type: String,
      required: false,
      default: undefined,
    },
    invalid: {
      type: Boolean,
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

  const value = ref(props.observableValue);

  const styleClasses = computed(() => {
    if (!inputIsValid.value) {
      return ["inputfield", "p-invalid"];
    }
    return ["inputfield"];
  });

  const fileUploadLabel = computed(() => {
    if (!props.multiAdd) {
      return "Choose";
    }
    return "Choose multiple";
  });

  const inputIsValid = computed(() => {
    if (value.value == null || value.value.length == 0) {
      return true;
    }
    if (observableMetadata.value.validator) {
      return observableMetadata.value.validator(value.value);
    }
    return true;
  });

  const placeholder = computed(() => {
    if (observableMetadata.value.placeholder && !props.multiAdd) {
      return observableMetadata.value.placeholder;
    } else if (props.multiAdd) {
      return "Enter a comma or newline-delimited list of values";
    } else {
      return "Enter a value";
    }
  });

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
    emit("update:observableValue", value);
    if (inputIsValid.value) {
      emit("update:invalid", false);
    } else {
      emit("update:invalid", true);
    }
  });
</script>
