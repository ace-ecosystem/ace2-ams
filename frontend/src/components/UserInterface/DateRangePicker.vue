<template>
  <!--      DATE PICKER OPTIONS  -->
  <Button icon="pi pi-calendar" @click="toggleOptionsMenu" />
  <OverlayPanel ref="op">
    <div class="p-d-flex">
      <Dropdown v-model="currentRangeFilter" :options="rangeFilterOptions" />
    </div>
    <div class="p-d-flex p-flex-column p-jc-center">
      <div class="p-mb-2">
        <Button label="Today" class="p-button-sm" @click="setRange(TODAY)" />
      </div>
      <div class="p-mb-2">
        <Button
          label="Yesterday"
          class="p-button-sm"
          @click="setRange(YESTERDAY)"
        />
      </div>
      <div class="p-mb-2">
        <Button
          label="Last 7 Days"
          class="p-button-sm"
          @click="setRange(LAST_SEVEN)"
        />
      </div>
      <div class="p-mb-2">
        <Button
          label="Last 30 Days"
          class="p-button-sm"
          @click="setRange(LAST_THIRTY)"
        />
      </div>
      <div class="p-mb-2">
        <Button
          label="Last 60 Days"
          class="p-button-sm"
          @click="setRange(LAST_SIXTY)"
        />
      </div>
      <div class="p-mb-2">
        <Button
          label="This Month"
          class="p-button-sm"
          @click="setRange(THIS_MONTH)"
        />
      </div>
      <div class="p-mb-2">
        <Button
          label="Last Month"
          class="p-button-sm"
          @click="setRange(LAST_MONTH)"
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
</template>

<script>
  import { mapActions } from "vuex";

  import Dropdown from "primevue/dropdown";
  import Button from "primevue/button";
  import OverlayPanel from "primevue/overlaypanel";

  import InputText from "primevue/inputtext";
  import Tooltip from "primevue/tooltip";
  import { DatePicker } from "v-calendar";

  export default {
    name: "DateRangePicker",
    components: {
      Button,
      DatePicker,
      Dropdown,
      InputText,
      OverlayPanel,
    },

    directives: {
      tooltip: Tooltip,
    },

    inject: ["filterType", "rangeFilterOptions", "rangeFilters"],

    data() {
      return {
        currentRangeFilter: this.rangeFilterOptions[0],
        TODAY: "today",
        YESTERDAY: "yesterday",
        LAST_SEVEN: "last_seven",
        LAST_THIRTY: "last_thirty",
        LAST_SIXTY: "last_sixty",
        THIS_MONTH: "this_month",
        LAST_MONTH: "last_month",
      };
    },

    computed: {
      filters() {
        return this.$store.getters[`filters/${this.filterType}`];
      },
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

      dateSelect(event, filterName) {
        if (event == null) {
          return;
        }
        this.setFilter({
          filterType: this.filterType,
          filterName: filterName,
          filterValue: event,
        });
      },

      clearDate(filterName) {
        this.unsetFilter({
          filterType: this.filterType,
          filterName: filterName,
        });
      },

      setRange(rangeType) {
        const today = new Date();
        let startDate = null;
        let endDate = null;
        let pastDate = null;
        switch (rangeType) {
          case this.TODAY:
            startDate = new Date();
            endDate = new Date();
            break;
          case this.YESTERDAY:
            pastDate = today.getDate() - 1;
            startDate = new Date(today.setDate(pastDate));
            endDate = new Date(today.setDate(pastDate));
            break;
          case this.LAST_SEVEN:
            pastDate = today.getDate() - 7;
            startDate = new Date(today.setDate(pastDate));
            endDate = new Date();
            break;
          case this.LAST_THIRTY:
            pastDate = today.getDate() - 30;
            startDate = new Date(today.setDate(pastDate));
            endDate = new Date();
            break;
          case this.LAST_SIXTY:
            pastDate = today.getDate() - 60;
            startDate = new Date(today.setDate(pastDate));
            endDate = new Date();
            break;
          case this.THIS_MONTH:
            pastDate = today.getMonth();
            startDate = new Date(today.setMonth(pastDate));
            startDate.setDate(1);
            endDate = new Date();
            break;
          case this.LAST_MONTH:
            pastDate = today.getMonth() - 1;
            startDate = new Date(today.setMonth(pastDate));
            endDate = new Date(today.setMonth(pastDate + 1));
            startDate.setDate(1);
            endDate.setDate(0); // 0 will set the date to the last day of the previous month
            break;
          default:
            break;
        }
        // Set start and end date times to capture entierty of each day
        startDate.setHours(0, 0, 0);
        endDate.setHours(23, 59, 59);
        this.dateSelect(startDate, this.startFilter);
        this.dateSelect(endDate, this.endfilter);
      },
    },

    toggleOptionsMenu(event) {
      this.$refs.op.toggle(event);
    },
  };
</script>
