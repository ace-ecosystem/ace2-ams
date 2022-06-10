<!-- AddObservableModal.vue -->
<!-- 'AddObservable' modal, meant specifically for adding observables to an alert -->
<!-- As of right now, this will only work when adding an observable to a single, currently open alert. -->

<template>
  <BaseModal :name="name" header="Add Observable(s)">
    <div>
      <div v-if="error" class="p-col">
        <Message severity="error" @close="handleError">{{ error }}</Message>
      </div>
    </div>
    <div>
      <NewObservableForm v-model="observables"></NewObservableForm>
    </div>
    <template #footer>
      <Button
        label="Actually, nevermind"
        icon="pi pi-times"
        class="p-button-text"
        @click="close"
      />
      <Button
        label="Add!"
        icon="pi pi-check"
        :loading="isLoading"
        @click="addObservables"
      />
    </template>
  </BaseModal>
</template>

<script setup lang="ts">
  import { defineProps, defineEmits, ref } from "vue";

  import Button from "primevue/button";
  import Message from "primevue/message";

  import BaseModal from "@/components/Modals/BaseModal.vue";
  import NewObservableForm from "@/components/Observables/NewObservableForm.vue";

  import { ObservableInstance } from "@/services/api/observable";
  import { useModalStore } from "@/stores/modal";
  import { observableCreate } from "@/models/observable";

  import { useAuthStore } from "@/stores/auth";
  import { useAlertStore } from "@/stores/alert";

  const props = defineProps({
    name: { type: String, required: true },
  });

  interface formObservable {
    time?: Date;
    type: string;
    multiAdd?: boolean;
    value: string;
    directives?: string[];
  }
  const emit = defineEmits(["requestReload"]);

  const authStore = useAuthStore();
  const alertStore = useAlertStore();
  const modalStore = useModalStore();

  const observables = ref<formObservable[]>([]);
  const isLoading = ref(false);

  const error = ref<string>();

  const addObservables = async () => {
    isLoading.value = true;

    const _observables: observableCreate[] = expandObservablesList().map(
      generateSubmissionObservable,
    );

    try {
      // for (const obs of _observables) {
        await ObservableInstance.create(_observables);
      // }
    } catch (e: unknown) {
      if (typeof e === "string") {
        error.value = e;
      } else if (e instanceof Error) {
        error.value = e.message;
      }
    }
    isLoading.value = false;
    if (!error.value) {
      close();
      emit("requestReload");
    }
  };

  // Generate a list of all observables (single observables plus expanded multi-observables)
  const expandObservablesList = () => {
    let _observables: formObservable[] = [];
    for (const obs_index in observables.value) {
      let current_observable = observables.value[obs_index];
      if (current_observable.multiAdd) {
        const splitObservables = splitMultiObservable(current_observable);
        _observables = [..._observables, ...splitObservables];
      } else {
        _observables.push(current_observable);
      }
    }
    return _observables;
  };

  // Given an observable object, return a formatted observable instance 'create' object
  const generateSubmissionObservable = (
    observable: formObservable,
  ): observableCreate => {
    const submissionObservable: observableCreate = {
      type: observable.type,
      value: observable.value,
      parentAnalysisUuid: alertStore.open.rootAnalysisUuid,
      historyUsername: authStore.user.username,
    };
    if (observable.time) {
      submissionObservable["time"] = observable.time;
    }
    return submissionObservable;
  };

  // Given a multi-observable object, expand into a list of single observable objects for each sub-value
  const splitMultiObservable = (multiObservable: formObservable) => {
    // Determine split character -- can be newline or comma
    let splitValues = [];
    var containsNewline = /\r?\n/.exec(multiObservable.value);
    if (containsNewline) {
      splitValues = multiObservable.value.split(/\r?\n/);
    } else {
      splitValues = multiObservable.value.split(",");
    }
    // Split and return new list
    const splitObservables = [];
    for (const index in splitValues) {
      const subObservable = {
        type: multiObservable.type,
        value: splitValues[index],
        time: multiObservable.time,
      };
      splitObservables.push(subObservable);
    }
    return splitObservables;
  };

  const handleError = () => {
    error.value = undefined;
  };

  const close = () => {
    modalStore.close(props.name);
  };
</script>
