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
  <small v-if="anyObservablesInvalid" class="p-error"
    >Please check observable input</small
  >
  <div class="pl-3">
    <SplitButton
      label="Analyze!"
      :loading="alertCreateLoading"
      :disabled="anyObservablesInvalid"
      :model="splitButtonOptions"
      class="p-button-lg"
      @click="submitSingleAlert"
    />
  </div>
  <Message v-if="addingObservables" severity="info"
    >Alert created, now adding Observables...</Message
  >
  <Message v-if="showContinueButton" severity="info"
    >Oh dear, it looks like some observables couldn't be created... The errors
    below might help explain what went wrong. You can try adding the observables
    again on the next page!</Message
  >
  <Message
    v-for="(error, index) of errors"
    :key="error.content"
    severity="error"
    @close="handleError(index)"
    >{{ error.content }}</Message
  >
  <div class="pl-3">
    <Button
      v-if="showContinueButton"
      label="On with it then..."
      class="p-button-lg"
      @click="routeToNewAlert"
    />
  </div>
</template>

<script setup>
  import { computed, onMounted, ref } from "vue";
  import { useRouter } from "vue-router";

  import Button from "primevue/button";
  import Card from "primevue/card";
  import Dropdown from "primevue/dropdown";
  import Fieldset from "primevue/fieldset";
  import InputText from "primevue/inputtext";
  import Message from "primevue/message";
  import SplitButton from "primevue/splitbutton";
  import TabPanel from "primevue/tabpanel";
  import TabView from "primevue/tabview";
  import { DatePicker } from "v-calendar";

  import NewObservableForm from "@/components/Observables/NewObservableForm.vue";

  import { useAlertStore } from "@/stores/alert";
  import { useQueueStore } from "@/stores/queue";
  import { useAlertTypeStore } from "@/stores/alertType";
  import { useAuthStore } from "@/stores/auth";

  const router = useRouter();

  const alertStore = useAlertStore();
  const alertTypeStore = useAlertTypeStore();
  const authStore = useAuthStore();
  const queueStore = useQueueStore();

  const addingObservables = ref(false);
  const alertCreateLoading = ref(false);
  const alertDate = ref(new Date());
  const alertDescription = ref("Manual Alert");
  const alertDescriptionAppendString = ref("");
  const alertType = ref("manual");
  const queue = ref();
  const errors = ref([]);
  const splitButtonOptions = ref([
    {
      label: "Create multiple alerts",
      icon: "pi pi-copy",
      command: async () => {
        await submitMultipleAlerts();
      },
    },
  ]);
  const observables = ref([]);
  const showContinueButton = ref(false);

  const alertDescriptionFormatted = computed(() => {
    return `${alertDescription.value}${alertDescriptionAppendString.value}`;
  });

  const anyObservablesInvalid = computed(() => {
    const invalid = observables.value.filter((obs) => obs.invalid);
    return invalid.length;
  });

  onMounted(() => {
    initData();
  });

  const addError = (object, error) => {
    let responseError = null;
    if (error.response) {
      responseError = JSON.stringify(error.response.data);
    }
    errors.value.push({
      content: `Could not create ${object}: ${error} ${responseError}`,
    });
  };

  // Generate a list of all observables (single observables plus expanded multi-observables)
  const expandObservablesList = () => {
    let _observables = [];
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
  const generateSubmissionObservable = (observable) => {
    const submissionObservable = {
      type: observable.type,
      value: observable.value,
    };
    if (observable.time) {
      submissionObservable["time"] = observable.time;
    }
    if (observable.directives && observable.directives.length) {
      submissionObservable["directives"] = observable.directives;
    }
    return submissionObservable;
  };

  const handleError = (index) => {
    errors.value.splice(index, 1);
  };

  const initData = () => {
    alertDate.value = new Date();
    alertDescription.value = "Manual Alert";
    alertDescriptionAppendString.value = "";
    alertType.value = alertTypeStore.items.length
      ? alertTypeStore.items[0].value
      : "manual";
    // TODO: This needs to be based on the current user's preferred queue
    queue.value = authStore.user
      ? authStore.user.defaultAlertQueue.value
      : "default";
    errors.value = [];
  };

  const routeToNewAlert = () => {
    router.push({ path: `/alert/${alertStore.open.uuid}` });
  };

  // Given a multi-observable object, expand into a list of single observable objects for each sub-value
  const splitMultiObservable = (multiObservable) => {
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
      };
      splitObservables.push(subObservable);
    }
    return splitObservables;
  };

  // Submit alert create object to API to create an alert
  const submitAlert = async (observables) => {
    const alert = {
      alert: true,
      alertDescription: alertDescriptionFormatted.value,
      eventTime: alertDate.value,
      name: alertDescriptionFormatted.value,
      observables: observables,
      owner: authStore.user.username,
      queue: queue.value,
      type: alertType.value,
    };
    try {
      await alertStore.create(alert);
    } catch (error) {
      addError(`alert ${alert.name}`, error);
    }
  };

  // create a single alert that contains all observables currently in the form
  const submitSingleAlert = async () => {
    if (!errors.value.length && observables.value.length) {
      addingObservables.value = true;
      let _observables = expandObservablesList();

      alertCreateLoading.value = true;
      await submitAlert(_observables.map(generateSubmissionObservable));
      alertCreateLoading.value = false;
      addingObservables.value = false;

      if (errors.value.length) {
        showContinueButton.value = true;
      } else {
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
    // Routes you to latest alert
    routeToNewAlert();
  };
</script>
