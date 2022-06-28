<template>
  <TabView>
    <TabPanel key="basic" header="Basic">
      <Card>
        <template #title>Alert Details </template>
        <template #content>
          <div class="formgrid grid">
            <div class="field col-4">
              <InputText
                id="description"
                v-model="alertDescription"
                placeholder="Alert Description"
                class="inputfield w-full"
                type="text"
              ></InputText>
            </div>
          </div>

          <br />

          <Fieldset legend="Advanced" :toggleable="true" :collapsed="true">
            <div class="formgrid grid">
              <div class="field col-4">
                <label for="alert-date">Alert Datetime (UTC)</label>
                <DatePicker
                  v-model="alertDate"
                  mode="dateTime"
                  class="inputfield w-16rem"
                  is24hr
                  timezone="UTC"
                >
                  <template #default="{ inputValue, inputEvents }">
                    <div class="p-inputgroup">
                      <InputText
                        data-cy="alert-date"
                        class="inputfield w-16rem"
                        type="text"
                        :value="inputValue"
                        placeholder="Enter a date!"
                        v-on="inputEvents"
                      />
                    </div>
                  </template>
                </DatePicker>
              </div>
            </div>
            <div class="formgrid grid">
              <div class="field col-4">
                <label for="type">Alert Type</label>
                <Dropdown
                  id="type"
                  v-model="alertType"
                  class="inputfield w-full"
                  :options="alertTypeStore.items"
                  option-label="value"
                  option-value="value"
                />
              </div>
            </div>
            <div class="formgrid grid">
              <div class="field col-4">
                <label for="queue">Queue</label>
                <Dropdown
                  id="queue"
                  v-model="queue"
                  class="inputfield w-full"
                  :options="queueStore.items"
                  option-label="value"
                  option-value="value"
                />
              </div>
            </div>
          </Fieldset>
        </template>
      </Card>

      <br />

      <Card>
        <template #title>Observables </template>
        <template #content>
          <NewObservableForm v-model="observables"></NewObservableForm>
        </template>
      </Card>

      <br />
    </TabPanel>
  </TabView>
  <small v-if="formContainsInvalidObservables" class="p-error"
    >Please check observable input</small
  >
  <div class="pl-3">
    <Button
      v-tooltip="'Create a new alert for each observable'"
      label="Submit Multiple Alerts"
      :loading="alertCreateLoading"
      :disabled="
        formContainsInvalidObservables || !formContainsMultipleObservables
      "
      class="p-button-lg p-button-outlined m-1"
      icon="pi pi-question-circle"
      icon-pos="right"
      @click="submitMultipleAlerts"
    />
    <Button
      label="Submit Alert"
      :loading="alertCreateLoading"
      :disabled="formContainsInvalidObservables"
      class="p-button-lg m-1"
      @click="submitSingleAlert"
    />
  </div>
  <Message
    v-for="(error, index) of errors"
    :key="error"
    severity="error"
    @close="handleError(index)"
    >{{ error }}</Message
  >
</template>

<script setup lang="ts">
  import { computed, onMounted, ref } from "vue";
  import { useRouter } from "vue-router";

  import { alertCreate } from "@/models/alert";
  import { observableCreate } from "@/models/observable";

  import Button from "primevue/button";
  import Card from "primevue/card";
  import Dropdown from "primevue/dropdown";
  import Fieldset from "primevue/fieldset";
  import InputText from "primevue/inputtext";
  import Message from "primevue/message";
  import TabPanel from "primevue/tabpanel";
  import TabView from "primevue/tabview";
  import { DatePicker } from "v-calendar";

  import NewObservableForm from "@/components/Observables/NewObservableForm.vue";

  import { useAlertStore } from "@/stores/alert";
  import { useQueueStore } from "@/stores/queue";
  import { useAlertTypeStore } from "@/stores/alertType";
  import { useAuthStore } from "@/stores/auth";

  interface formObservable {
    time?: Date;
    type: string;
    multiAdd: boolean;
    invalid: boolean;
    value: any;
    directives: string[];
  }

  const router = useRouter();

  const alertStore = useAlertStore();
  const alertTypeStore = useAlertTypeStore();
  const authStore = useAuthStore();
  const queueStore = useQueueStore();

  const alertCreateLoading = ref(false);
  const alertDate = ref(new Date());
  const alertDescription = ref("Manual Alert");
  const alertDescriptionAppendString = ref("");
  const errors = ref<string[]>([]);
  const observables = ref<formObservable[]>([]);
  const alertType = ref<string>("manual");
  const queue = ref<string>("default");

  // Initialize form data with store data or default values
  onMounted(() => {
    if (alertTypeStore.items.length) {
      alertType.value = alertTypeStore.items[0].value;
    }
    if (authStore.user) {
      queue.value = authStore.user.defaultAlertQueue.value;
    }
  });

  // Return true if any observables are invalid
  const formContainsInvalidObservables = computed(() => {
    return observables.value.some((obs) => obs.invalid);
  });

  // Return true if there are multiple observables (more than one in list OR one in list and multiAdd is true)
  const formContainsMultipleObservables = computed(() => {
    if (observables.value.length > 1) {
      return true;
    }
    return observables.value.some((obs) => obs.multiAdd);
  });

  // Generate a list of all observables (single observables plus expanded multi-observables)
  const expandObservablesList = (): formObservable[] => {
    let _observables: formObservable[] = [];
    for (const observable of observables.value) {
      if (observable.multiAdd) {
        const splitObservables = splitMultiObservable(observable);
        _observables = [..._observables, ...splitObservables];
      } else {
        _observables.push(observable);
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
      analysisMetadata: [],
      // historyUsername: authStore.user.username,
    };

    if (submissionObservable.analysisMetadata) {
      if (observable.time) {
        submissionObservable.analysisMetadata.push({
          type: "time",
          value: observable.time as unknown as string,
        });
      }

      if (observable.directives) {
        for (const directive of observable.directives) {
          submissionObservable.analysisMetadata.push({
            type: "directive",
            value: directive,
          });
        }
      }
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
        multiAdd: multiObservable.multiAdd,
        invalid: multiObservable.invalid,
        directives: multiObservable.directives,
      };
      splitObservables.push(subObservable);
    }
    return splitObservables;
  };

  // Submit alert create object to API to create an alert
  const submitAlert = async (observables: observableCreate[]) => {
    const alertName = `${alertDescription.value}${alertDescriptionAppendString.value}`;

    const alert: alertCreate = {
      alert: true,
      alertDescription: alertName,
      eventTime: alertDate.value,
      name: alertName,
      observables: observables,
      owner: authStore.user.username,
      queue: queue.value,
      type: alertType.value,
      // historyUsername: authStore.user.username,
    };
    try {
      await alertStore.create(alert);
    } catch (e: unknown) {
      if (typeof e === "string") {
        errors.value.push(e);
      } else if (e instanceof Error) {
        errors.value.push(e.message);
      }
    }
  };

  // create a single alert that contains all observables currently in the form
  const submitSingleAlert = async () => {
    if (!errors.value.length && observables.value.length) {
      let _observables = expandObservablesList();

      alertCreateLoading.value = true;
      await submitAlert(_observables.map(generateSubmissionObservable));
      alertCreateLoading.value = false;

      if (!errors.value.length) {
        routeToNewAlert();
      }
    }
  };

  // create a single alert for each observable currently in the form
  const submitMultipleAlerts = async () => {
    alertCreateLoading.value = true;

    const _observables = expandObservablesList();
    for (const obs_index in _observables) {
      const current_observable = _observables[obs_index];

      // Update the alert name with observable value to easily from manage alerts page
      alertDescriptionAppendString.value = ` ${current_observable.value}`;

      await submitAlert([generateSubmissionObservable(current_observable)]);

      if (errors.value.length) {
        // If first alert can't be created, bail trying a bunch of times
        return;
      }
    }

    alertCreateLoading.value = false;
    routeToNewAlert();
  };

  // Reroute to new alert page
  const routeToNewAlert = () => {
    router.push({ path: `/alert/${alertStore.open.uuid}` });
  };

  // Remove error at given position from errors array
  const handleError = (index: number) => {
    errors.value.splice(index, 1);
  };
</script>
