<!-- TheFilterToolbar.vue -->
<!-- A toolbar containing buttons/inputs to display/change applied filters for a given set of items (ex. alerts or events) -->

<template>
  <Toolbar style="overflow-x: auto">
    <template #left>
      <!--      DATE PICKER -->
      <i class="pi pi-calendar"></i>
      <Calendar
        id="startTimeFilter"
        v-model="eventTimeAfterDate"
        class="p-m-1"
        :manual-input="true"
        :show-time="true"
        selection-mode="single"
        style="width: 180px"
        placeholder="The beginning of time"
        :show-button-bar="true"
        @clear-click="clearDate(eventTimeAfter)"
        @update:model-value="dateSelect($event, eventTimeAfter)"
        @update:model-value.delete="dateSelect(null)"
        @month-change="monthChange($event, eventTimeAfter, eventTimeAfterDate)"
      />
      to
      <Calendar
        id="endTimeFilter"
        v-model="eventTimeBeforeDate"
        class="p-m-1"
        :manual-input="true"
        :show-time="true"
        :show-button-bar="true"
        selection-mode="single"
        style="width: 180px"
        placeholder="Now"
        @clear-click="clearDate(eventTimeBefore)"
        @update:model-value="dateSelect($event, eventTimeBefore)"
        @update:model-value.delete="dateSelect(null)"
        @month-change="
          monthChange($event, eventTimeBefore, eventTimeBeforeDate)
        "
      />
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
      />
      <!--      RESET FILTERS-->
      <Button
        type="button"
        icon="pi pi-refresh"
        label="Reset"
        class="p-button-outlined p-m-1"
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
  import Calendar from "primevue/calendar";
  import Toolbar from "primevue/toolbar";

  import EditFilterModal from "@/components/Modals/FilterModal";

  export default {
    name: "TheFilterToolbar",
    components: { Button, Calendar, EditFilterModal, Toolbar },

    computed: {
      ...mapGetters({
        filters: "filters/filters",
      }),
      eventTimeAfter() {
        return EVENT_TIME_AFTER_FILTER;
      },
      eventTimeBefore() {
        return EVENT_TIME_BEFORE_FILTER;
      },
      eventTimeAfterDate() {
        return this.filters[EVENT_TIME_AFTER_FILTER];
      },
      eventTimeBeforeDate() {
        return this.filters[EVENT_TIME_BEFORE_FILTER];
      },
    },

    methods: {
      ...mapActions({
        setFilter: "filters/setFilter",
        unsetFilter: "filters/unsetFilter",
      }),

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

      monthChange(event, filterType, oldDate) {
        let updatedDate = new Date(oldDate);
        updatedDate.setMonth(event.month);
        updatedDate.setYear(event.year);
        this.setFilter({
          filterType: filterType,
          filterValue: updatedDate,
        });
      },

      open(name) {
        this.$store.dispatch("modals/open", name);
      },
    },
  };
</script>
