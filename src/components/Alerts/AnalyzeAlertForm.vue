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
                <label for="alert-date">Alert Datetime</label>
                <Calendar
                  id="alert-date"
                  v-model="alertDate"
                  class="inputfield w-full"
                  :show-time="true"
                  :show-seconds="true"
                />
              </div>
            </div>
            <div class="formgrid grid">
              <div class="field col-4">
                <label for="timezone">Timezone</label>
                <Dropdown
                  id="timezone"
                  v-model="timezone"
                  class="inputfield w-full"
                  :options="timezones"
                />
              </div>
            </div>
            <div class="formgrid grid">
              <div class="field col-4">
                <label for="type">Alert Type</label>
                <Dropdown
                  id="type"
                  v-model="alertType"
                  class="inputfield w-full"
                  :options="alertTypes"
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
                  v-model="alertQueue"
                  class="inputfield w-full"
                  :options="alertQueues"
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
          <div id="observables-list">
            <div class="formgrid grid">
              <div class="field col-2 px-1">
                <label for="observable-time">Time</label>
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
                  icon="pi pi-plus"
                  class="p-button-rounded inputfield"
                  @click="addFormObservable"
                />
              </div>
            </div>
            <div
              v-for="(observable, index) in observables"
              :key="observable.index"
              class="p-col-12"
            >
              <div class="formgrid grid">
                <div class="field col-2 px-1">
                  <Calendar
                    id="observable-time"
                    v-model="observables[index].time"
                    placeholder="No time selected"
                    class="inputfield w-full"
                    :show-time="true"
                    :show-seconds="true"
                  />
                </div>
                <div class="field col-2 px-1">
                  <Dropdown
                    id="observable-type"
                    v-model="observables[index].type"
                    class="inputfield w-full"
                    option-label="value"
                    option-value="value"
                    :options="observableTypes"
                  />
                </div>
                <div class="field col-3 px-1">
                  <FileUpload
                    v-if="observables[index].type == 'file'"
                    mode="basic"
                    class="inputfield w-full"
                  ></FileUpload>
                  <div v-else class="p-inputgroup">
                    <InputText
                      v-if="!observables[index].multiAdd"
                      id="observable-value"
                      v-model="observables[index].value"
                      placeholder="Enter a value"
                      class="inputfield w-full"
                      type="text"
                    ></InputText>
                    <Textarea
                      v-else
                      id="observable-value"
                      v-model="observables[index].value"
                      placeholder="Enter a comma or newline-delimited list of values"
                      class="inputfield w-full"
                    ></Textarea>
                    <Button
                      icon="pi pi-list"
                      @click="toggleMultiObservable(index)"
                    />
                  </div>
                </div>
                <div class="field col-3 px-1">
                  <MultiSelect
                    id="observable-directives"
                    v-model="observables[index].directives"
                    placeholder="No directives selected"
                    class="inputfield w-full"
                    :options="directives"
                  />
                </div>
                <div class="field col-1">
                  <Button
                    icon="pi pi-times"
                    class="inputfield"
                    @click="deleteFormObservable(index)"
                  />
                </div>
                <div class="field col-1">
                  <Button
                    v-if="isLastObservable(index)"
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
      </Card>

      <br />
    </TabPanel>
  </TabView>
  <div class="pl-3">
    <SplitButton
      label="Analyze!"
      :loading="alertCreateLoading"
      :disabled="showContinueButton"
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

<script>
  import { mapActions, mapGetters } from "vuex";

  import Button from "primevue/button";
  import Calendar from "primevue/calendar";
  import Card from "primevue/card";
  import Dropdown from "primevue/dropdown";
  import Fieldset from "primevue/fieldset";
  import FileUpload from "primevue/fileupload";
  import InputText from "primevue/inputtext";
  import Message from "primevue/message";
  import MultiSelect from "primevue/multiselect";
  import SplitButton from "primevue/splitbutton";
  import TabPanel from "primevue/tabpanel";
  import TabView from "primevue/tabview";
  import Textarea from "primevue/textarea";

  import moment from "moment-timezone";

  import ObservableInstance from "@/services/api/observableInstance";

  export default {
    name: "AnalyzeAlertForm",
    components: {
      Button,
      Calendar,
      Card,
      Dropdown,
      Fieldset,
      FileUpload,
      InputText,
      Message,
      MultiSelect,
      SplitButton,
      TabPanel,
      TabView,
      Textarea,
    },
    data() {
      return {
        addingObservables: false,
        alertCreateLoading: false,
        alertDate: null,
        alertDescription: null,
        alertDescriptionAppendString: null,
        alertQueue: null,
        alertType: null,
        errors: [],
        splitButtonOptions: [
          {
            label: "Create multiple alerts",
            icon: "pi pi-copy",
            command: this.submitMultipleAlerts,
          },
        ],
        observables: [],
        showContinueButton: false,
        timezone: null,
        timezones: moment.tz.names(),
      };
    },
    computed: {
      adjustedAlertDate() {
        return this.adjustForTimezone(this.alertDate, this.timezone);
      },
      alertDescriptionFormatted() {
        return `${this.alertDescription}${this.alertDescriptionAppendString}`;
      },
      observablesListEmpty() {
        return !this.observables.length;
      },
      lastObservableIndex() {
        return this.observables.length - 1;
      },
      ...mapGetters({
        openAlert: "alerts/openAlert",
        directives: "nodeDirective/allItems",
        alertTypes: "alertType/allItems",
        alertQueues: "alertQueue/allItems",
        observableTypes: "observableType/allItems",
      }),
    },
    created() {
      this.initData();
      this.initExternalData();
    },
    methods: {
      ...mapActions({
        createAlert: "alerts/createAlert",
        getAllAlertQueue: "alertQueue/getAll",
        getAllAlertType: "alertType/getAll",
        getAllNodeDirective: "nodeDirective/getAll",
        getAllObservableType: "observableType/getAll",
      }),
      initData() {
        this.alertDate = new Date();
        this.alertDescription = "Manual Alert";
        this.alertDescriptionAppendString = "";
        this.alertType = "manual";
        this.alertQueue = "default";
        this.errors = [];
        this.timezone = moment.tz.guess();
        this.observables = [];
        this.addFormObservable();
      },
      async initExternalData() {
        await this.getAllAlertQueue();
        await this.getAllAlertType();
        await this.getAllNodeDirective();
        await this.getAllObservableType();
      },
      adjustForTimezone(datetime, timezone) {
        return moment(datetime).tz(timezone).format();
      },
      // create a single alert that contains all observables currently in the form
      async submitSingleAlert() {
        this.alertCreateLoading = true;
        await this.submitAlert();
        this.alertCreateLoading = false;

        if (this.errors.length) {
          return;
        }

        if (this.observables.length) {
          this.addingObservables = true;
          let observables = this.expandObservablesList();
          observables = observables.map(this.generateSubmissionObservable);
          await this.submitObservables(observables);
          this.addingObservables = false;
        }

        if (this.errors.length) {
          this.showContinueButton = true;
        } else {
          this.routeToNewAlert();
        }
      },
      // create a single alert for each observable currently in the form
      async submitMultipleAlerts() {
        this.alertCreateLoading = true;

        const observables = this.expandObservablesList();
        for (const obs_index in observables) {
          const current_observable = observables[obs_index];

          // Update the alert name with observable value to easily from manage alerts page
          this.alertDescriptionAppendString = ` ${current_observable.value}`;

          await this.submitAlert();
          if (this.errors.length) {
            // If first alert can't be created, bail trying a bunch of times
            return;
          }

          await this.submitObservables([
            this.generateSubmissionObservable(current_observable), // Generate the submission object here so that it has correct alert/analysis UUIDs
          ]);
          // Ignore observable created errors
          this.clearErrors();
        }

        this.alertCreateLoading = false;
        // Routes you to latest alert
        this.routeToNewAlert();
      },
      // Submit alert create object to API to create an alert
      async submitAlert() {
        const alert = {
          alertDescription: this.alertDescriptionFormatted,
          eventTime: this.adjustedAlertDate,
          name: this.alertDescriptionFormatted,
          queue: this.alertQueue,
          type: this.alertType,
        };
        try {
          await this.createAlert(alert);
        } catch (error) {
          this.addError(`alert ${alert.name}`, error);
        }
      },
      // Submit a list of observables to API for latest alert
      async submitObservables(observables) {
        try {
          await ObservableInstance.create(observables, false);
        } catch (error) {
          this.addError("at least one observable", error);
        }
      },
      // Generate a list of all observables (single observables plus expanded multi-observables)
      expandObservablesList() {
        let observables = [];
        for (const obs_index in this.observables) {
          let current_observable = this.observables[obs_index];
          if (current_observable.multiAdd) {
            const splitObservables =
              this.splitMultiObservable(current_observable);
            observables = [...observables, ...splitObservables];
          } else {
            observables.push(current_observable);
          }
        }
        return observables;
      },
      // Given a multi-observable object, expand into a list of single observable objects for each sub-value
      splitMultiObservable(multiObservable) {
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
      },
      // Given an observable object, return a formatted observable instance 'create' object
      generateSubmissionObservable(observable) {
        const submissionObservable = {
          alertUuid: this.openAlert.uuid,
          parentAnalysisUuid: this.openAlert.analysis.uuid,
          type: observable.type,
          value: observable.value,
        };
        if (observable.time) {
          submissionObservable["time"] = this.adjustForTimezone(
            observable.time,
            this.timezone,
          );
        }
        return submissionObservable;
      },
      toggleMultiObservable(index) {
        this.observables[index].multiAdd = !this.observables[index].multiAdd;
      },
      addFormObservable() {
        this.observables.push({
          time: null,
          type: "file",
          multiAdd: false,
          value: null,
          directives: [],
        });
      },
      deleteFormObservable(index) {
        this.observables.splice(index, 1);
      },
      isLastObservable(index) {
        return index == this.lastObservableIndex;
      },
      routeToNewAlert() {
        this.$router.push({ path: `/alert/${this.openAlert.uuid}` });
      },
      addError(object, error) {
        let responseError = null;
        if (error.response) {
          responseError = JSON.stringify(error.response.data);
        }
        this.errors.push({
          content: `Could not create ${object}: ${error} ${responseError}`,
        });
      },
      clearErrors() {
        this.errors = [];
      },
      handleError(index) {
        this.errors.splice(index, 1);
      },
    },
  };
</script>
