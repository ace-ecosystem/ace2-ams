<!-- TheFilterToolbar.vue -->
<!-- A toolbar containing buttons/inputs to display/change applied filters for a given set of items (ex. alerts or events) -->

<template>
  <Toolbar style="overflow-x: auto">
    <template #left>
      <!--      DATE PICKER OPTIONS  -->
      <Button icon="pi pi-calendar" @click="toggle" />
      <OverlayPanel ref="op">
        <div class="p-d-flex">
          <Dropdown
            v-model="currentRangeFilter"
            :options="rangeFilterOptions"
          />
        </div>
        <div class="p-d-flex p-flex-column p-jc-center">
          <div class="p-mb-2">
            <Button
              label="Today"
              class="p-button-sm"
              @click="setRange('today')"
            />
          </div>
          <div class="p-mb-2">
            <Button
              label="Yesterday"
              class="p-button-sm"
              @click="setRange('yesterday')"
            />
          </div>
          <div class="p-mb-2">
            <Button
              label="Last 7 Days"
              class="p-button-sm"
              @click="setRange('last_seven')"
            />
          </div>
          <div class="p-mb-2">
            <Button
              label="Last 30 Days"
              class="p-button-sm"
              @click="setRange('last_thirty')"
            />
          </div>
          <div class="p-mb-2">
            <Button
              label="Last 60 Days"
              class="p-button-sm"
              @click="setRange('last_sixty')"
            />
          </div>
          <div class="p-mb-2">
            <Button
              label="This Month"
              class="p-button-sm"
              @click="setRange('this_month')"
            />
          </div>
          <div class="p-mb-2">
            <Button
              label="Last Month"
              class="p-button-sm"
              @click="setRange('last_month')"
            />
          </div>
        </div>
      </OverlayPanel>

      <!--      DATE PICKERS -->
      <DatePicker
        v-model="startDate"
        mode="dateTime"
        is24hr
        @update:model-value="dateSelect($event, startFilter)"
        @update:model-value.delete="dateSelect(null)"
      >
        <template #default="{ inputValue, inputEvents }">
          <div class="p-inputgroup">
            <InputText
              v-tooltip.top="{
                value: startDateUTC,
                disabled: !startDateUTC,
              }"
              type="text"
              :value="inputValue"
              placeholder="The beginning of time"
              v-on="inputEvents"
            />
            <Button
              icon="pi pi-times"
              class="p-button-outlined p-button-secondary"
              @click="clearDate(startFilter)"
            />
          </div>
        </template>
      </DatePicker>
      to
      <DatePicker
        v-model="endDate"
        mode="dateTime"
        is24hr
        @update:model-value="dateSelect($event, endfilter)"
        @update:model-value.delete="dateSelect(null)"
      >
        <template #default="{ inputValue, inputEvents }">
          <div class="p-inputgroup">
            <InputText
              v-tooltip.top="{
                value: endDateUTC,
                disabled: !endDateUTC,
              }"
              type="text"
              :value="inputValue"
              placeholder="Now"
              v-on="inputEvents"
            />
            <Button
              icon="pi pi-times"
              class="p-button-outlined p-button-secondary"
              @click="clearDate(endfilter)"
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
    INSERT_TIME_AFTER_FILTER,
    INSERT_TIME_BEFORE_FILTER,
    DISPOSITIONED_AFTER_FILTER,
    DISPOSITIONED_BEFORE_FILTER,
  } from "@/etc/constants";

  import { mapActions, mapGetters } from "vuex";

  import Dropdown from "primevue/dropdown";
  import Button from "primevue/button";
  import Toolbar from "primevue/toolbar";
  import OverlayPanel from "primevue/overlaypanel";

  import InputText from "primevue/inputtext";
  import Tooltip from "primevue/tooltip";
  import { DatePicker } from "v-calendar";

  import EditFilterModal from "@/components/Modals/FilterModal";

  export default {
    name: "TheFilterToolbar",
    components: {
      Button,
      DatePicker,
      Dropdown,
      EditFilterModal,
      InputText,
      Toolbar,
      OverlayPanel,
    },

    directives: {
      tooltip: Tooltip,
    },

    data() {
      return {
        currentRangeFilter: "Event Time",
        rangeFilterOptions: ["Event Time", "Insert Time", "Dispositioned Time"],
        rangeFilters: {
          "Event Time": {
            start: EVENT_TIME_AFTER_FILTER,
            end: EVENT_TIME_BEFORE_FILTER,
          },
          "Insert Time": {
            start: INSERT_TIME_AFTER_FILTER,
            end: INSERT_TIME_BEFORE_FILTER,
          },
          "Dispositioned Time": {
            start: DISPOSITIONED_AFTER_FILTER,
            end: DISPOSITIONED_BEFORE_FILTER,
          },
        },
      };
    },

    computed: {
      ...mapGetters({
        filters: "filters/filters",
      }),
      startFilter() {
        return this.rangeFilters[this.currentRangeFilter].start;
      },
      endfilter() {
        return this.rangeFilters[this.currentRangeFilter].end;
      },
      startDate() {
        return this.filters[this.startFilter]
          ? this.filters[this.startFilter]
          : null;
      },
      endDate() {
        return this.filters[this.endfilter]
          ? this.filters[this.endfilter]
          : null;
      },
      startDateUTC() {
        return this.startDate ? this.startDate.toUTCString() : null;
      },
      endDateUTC() {
        return this.endDate ? this.endDate.toUTCString() : null;
      },
    },

    watch: {
      currentRangeFilter: function (_newValue, oldValue) {
        this.clearDate(this.rangeFilters[oldValue].start);
        this.clearDate(this.rangeFilters[oldValue].end);
      },
    },

    methods: {
      ...mapActions({
        setFilter: "filters/setFilter",
        unsetFilter: "filters/unsetFilter",
      }),

      clearFilters() {
        this.clearDate(this.startFilter);
        this.clearDate(this.endfilter);
      },

      resetFilters() {
        this.clearDate(this.startFilter);
        this.clearDate(this.endfilter);
      },

      clearDate(filterType) {
        this.unsetFilter({
          filterType: filterType,
        });
      },

      toggle(event) {
        this.$refs.op.toggle(event);
      },

      setRange(rangeType) {
        const today = new Date();
        let startDate = null;
        let endDate = null;
        let pastDate = null;
        switch (rangeType) {
          case "today":
            startDate = new Date();
            endDate = new Date();
            break;
          case "yesterday":
            pastDate = today.getDate() - 1;
            startDate = new Date(today.setDate(pastDate));
            endDate = new Date(today.setDate(pastDate));
            break;
          case "last_seven":
            pastDate = today.getDate() - 7;
            startDate = new Date(today.setDate(pastDate));
            endDate = new Date();
            break;
          case "last_thirty":
            pastDate = today.getDate() - 30;
            startDate = new Date(today.setDate(pastDate));
            endDate = new Date();
            break;
          case "last_sixty":
            pastDate = today.getDate() - 60;
            startDate = new Date(today.setDate(pastDate));
            endDate = new Date();
            break;
          case "this_month":
            pastDate = today.getMonth();
            startDate = new Date(today.setMonth(pastDate));
            startDate.setDate(1);
            endDate = new Date();
            break;
          case "last_month":
            pastDate = today.getMonth() - 1;
            startDate = new Date(today.setMonth(pastDate));
            endDate = new Date(today.setMonth(pastDate + 1));
            startDate.setDate(1);
            endDate.setDate(0);
            break;
          default:
            break;
        }
        startDate.setHours(0, 0, 0);
        endDate.setHours(23, 59, 59);
        this.dateSelect(startDate, this.startFilter);
        this.dateSelect(endDate, this.endfilter);
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
        console.log(this.startDateUserTimezone);
        this.$store.dispatch("modals/open", name);
      },
    },
  };
</script>
