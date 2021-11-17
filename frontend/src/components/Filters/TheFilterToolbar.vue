<!-- TheFilterToolbar.vue -->
<!-- A toolbar containing buttons/inputs to display/change applied filters for a given set of items (ex. alerts or events) -->

<template>
  <Toolbar style="overflow-x: auto">
    <!--      DATE PICKER -->
    <template #left>
      <DatePicker
        v-model="eventTimeAfterDate"
        mode="dateTime"
        is24hr
        @update:model-value="dateSelect($event, EVENT_TIME_AFTER_FILTER)"
        @update:model-value.delete="dateSelect(null)"
      >
        <template #default="{ inputValue, inputEvents }">
          <div class="p-inputgroup">
            <InputText
              v-tooltip.top="{
                value: eventTimeAfterUTC,
                disabled: !eventTimeAfterUTC,
              }"
              type="text"
              :value="inputValue"
              placeholder="The beginning of time"
              v-on="inputEvents"
            />
            <Button
              icon="pi pi-times"
              class="p-button-outlined p-button-secondary"
              @click="clearDate(EVENT_TIME_AFTER_FILTER)"
            />
          </div>
        </template>
      </DatePicker>
      to
      <DatePicker
        v-model="eventTimeBeforeDate"
        mode="dateTime"
        is24hr
        @update:model-value="dateSelect($event, EVENT_TIME_BEFORE_FILTER)"
        @update:model-value.delete="dateSelect(null)"
      >
        <template #default="{ inputValue, inputEvents }">
          <div class="p-inputgroup">
            <InputText
              v-tooltip.top="{
                value: eventTimeBeforeUTC,
                disabled: !eventTimeBeforeUTC,
              }"
              type="text"
              :value="inputValue"
              placeholder="Now"
              v-on="inputEvents"
            />
            <Button
              icon="pi pi-times"
              class="p-button-outlined p-button-secondary"
              @click="clearDate(EVENT_TIME_BEFORE_FILTER)"
            />
          </div>
        </template>
      </DatePicker>
      <!--      EDIT FILTERS -->
      <Button
        type="button"
        icon="pi pi-filter"
        label="Edit"
        class="p-button-outlined p-m-1"
        style="float: right"
        @click="open('EditFilterModal')"
      />
      <EditFilterModal />
    </template>
    <!--    TODO: SHOW APPLIED FILTERS -->
    <template #right>
      <!--      CLEAR FILTERS-->
      <Button
        type="button"
        icon="pi pi-filter-slash"
        label="Clear"
        class="p-button-outlined p-m-1"
        @click="clearFilters"
      />
      <!--      RESET FILTERS-->
      <Button
        type="button"
        icon="pi pi-refresh"
        label="Reset"
        class="p-button-outlined p-m-1"
        @click="resetFilters"
      />
    </template>
  </Toolbar>
</template>

<script>
  import {
    EVENT_TIME_AFTER_FILTER,
    EVENT_TIME_BEFORE_FILTER,
  } from "@/etc/constants";

  import { mapActions, mapGetters } from "vuex";

  import Button from "primevue/button";
  import Toolbar from "primevue/toolbar";
  import InputText from "primevue/inputtext";
  import Tooltip from "primevue/tooltip";
  import { DatePicker } from "v-calendar";

  import EditFilterModal from "@/components/Modals/FilterModal";

  export default {
    name: "TheFilterToolbar",
    components: {
      Button,
      DatePicker,
      EditFilterModal,
      InputText,
      Toolbar,
    },

    directives: {
      tooltip: Tooltip,
    },

    computed: {
      ...mapGetters({
        filters: "filters/filters",
      }),
      EVENT_TIME_AFTER_FILTER() {
        return EVENT_TIME_AFTER_FILTER;
      },
      EVENT_TIME_BEFORE_FILTER() {
        return EVENT_TIME_BEFORE_FILTER;
      },
      eventTimeAfterDate() {
        return this.filters[EVENT_TIME_AFTER_FILTER]
          ? this.filters[EVENT_TIME_AFTER_FILTER]
          : null;
      },
      eventTimeBeforeDate() {
        return this.filters[EVENT_TIME_BEFORE_FILTER]
          ? this.filters[EVENT_TIME_BEFORE_FILTER]
          : null;
      },
      eventTimeAfterUTC() {
        return this.eventTimeAfterDate
          ? this.eventTimeAfterDate.toUTCString()
          : null;
      },
      eventTimeBeforeUTC() {
        return this.eventTimeBeforeDate
          ? this.eventTimeBeforeDate.toUTCString()
          : null;
      },
    },

    methods: {
      ...mapActions({
        setFilter: "filters/setFilter",
        unsetFilter: "filters/unsetFilter",
      }),

      clearFilters() {
        this.clearDate(this.EVENT_TIME_AFTER_FILTER);
        this.clearDate(this.EVENT_TIME_BEFORE_FILTER);
      },

      resetFilters() {
        this.clearDate(this.EVENT_TIME_AFTER_FILTER);
        this.clearDate(this.EVENT_TIME_BEFORE_FILTER);
      },

      clearDate(filterType) {
        this.unsetFilter({
          filterType: filterType,
        });
      },

      dateSelect(event, filterType) {
        if (event == null) {
          return;
        }
        this.setFilter({
          filterType: filterType,
          filterValue: event,
        });
      },

      open(name) {
        this.$store.dispatch("modals/open", name);
      },
    },
  };
</script>
