<!-- TheFilterToolbar.vue -->
<!-- A toolbar containing buttons/inputs to display/change applied filters for a given set of items (ex. alerts or events) -->

<template>
  <Toolbar style="overflow-x: auto">
    <template #left>
      <!--      DATE PICKER -->
      <i class="pi pi-calendar"></i>
      <Calendar
        id="startTimeFilter"
        v-model="startTimeFilterData"
        class="p-m-1"
        :manual-input="true"
        :show-time="true"
        selection-mode="single"
        style="width: 180px"
        @update:model-value="dateSelect($event, 'eventTimeAfter')"
        @update:model-value.delete="dateSelect(null)"
        @month-change="
          monthChange($event, 'eventTimeAfter', startTimeFilterData)
        "
      />
      to
      <Calendar
        id="endTimeFilter"
        v-model="endTimeFilterData"
        class="p-m-1"
        :manual-input="true"
        :show-time="true"
        selection-mode="single"
        style="width: 180px"
        @update:model-value="dateSelect($event, 'eventTimeBefore')"
        @update:model-value.delete="dateSelect(null)"
        @month-change="
          monthChange($event, 'eventTimeBefore', endTimeFilterData)
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
        filters: "filters/setFilters",
      }),
      endTimeFilterData() {
        return this.filters["eventTimeBefore"];
      },
      startTimeFilterData() {
        return this.filters["eventTimeAfter"];
      },
    },

    async created() {
      if (this.endTimeFilterData == null) {
        this.setFilter({
          filterType: "eventTimeBefore",
          filterValue: new Date(),
        });
      }
      if (this.startTimeFilterData == null) {
        this.setFilter({
          filterType: "eventTimeAfter",
          filterValue: new Date(),
        });
      }
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
          filterType: filterName,
          filterValue: event,
        });
      },

      monthChange(event, filterName, oldDate) {
        let updatedDate = new Date(oldDate);
        updatedDate.setMonth(event.month);
        updatedDate.setYear(event.year);
        this.setFilter({
          filterType: filterName,
          filterValue: updatedDate,
        });
      },

      open(name) {
        this.$store.dispatch("modals/open", name);
      },
    },
  };
</script>
