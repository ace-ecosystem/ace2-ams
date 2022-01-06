<!-- ManageAlerts.vue -->

<template>
  <br />
  <TheAlertActionToolbar page="Manage Alerts" />
  <br />
  <TheFilterToolbar id="FilterToolbar" />
  <br />
  <div id="AlertsTable" class="card">
    <TheAlertsTable />
  </div>
</template>

<script setup>
  import { onMounted, watch, ref, provide } from "vue";

  import {
    alertFilters,
    alertRangeFilters,
    filterTypes,
  } from "@/etc/constants";

  import TheAlertActionToolbar from "@/components/Alerts/TheAlertActionToolbar";
  import TheFilterToolbar from "@/components/Filters/TheFilterToolbar";
  import TheAlertsTable from "@/components/Alerts/TheAlertsTable";
  import { useRoute } from "vue-router";

  import { useFilterStore } from "@/stores/filter";
  import { populateCommonStores } from "@/etc/helpers";

  const route = useRoute();

  provide("availableFilters", alertFilters);
  provide("filterType", "alerts");
  provide("rangeFilters", alertRangeFilters);

  const filterStore = useFilterStore();

  onMounted(async () => {
    if (route.query) {
      await populateCommonStores();
      loadFilters();
    }
  });

  function loadFilters() {
    // Need to parse the params here

    const parsedFilters = {};
    // parse each filter
    for (const filterName in route.query) {
      // first get the filter object so you can load the option
      let filterNameObject = alertFilters.find((filter) => {
        return filter.name === filterName;
      });
      filterNameObject = filterNameObject ? filterNameObject : null;
      console.log(filterNameObject);

      if (!filterNameObject) {
        continue;
      }

      let filterValueUnparsed = route.query[filterName];
      let filterValueParsed = null;
      let store = null;

      // format for GUI if available
      if (filterNameObject.formatForGUI) {
        filterValueUnparsed = filterNameObject.formatForGUI(
          route.query[filterName],
        );
      }

      // this is whatever property should be used to determine equality
      const filterValueProperty = filterNameObject.valueProperty
        ? filterNameObject.valueProperty
        : "value";

      // load the filter options store if available
      if (filterNameObject.store) {
        store = filterNameObject.store();
      }

      switch (filterNameObject.type) {
        case filterTypes.MULTISELECT:
          // look up each object in the list
          filterValueParsed = [];
          if (store) {
            for (const value in filterValueUnparsed) {
              filterValueParsed.push   (
                store.allItems.find((element) => {
                  return element[filterValueProperty] === value;
                }),
              );
            }
          }
          break;
        case filterTypes.CHIPS:
          // array of strings
          filterValueParsed = filterValueUnparsed;
          break;
        case filterTypes.SELECT:
          if (store) {
            filterValueParsed = store.allItems.find((element) => {
              return element[filterValueProperty] === filterValueUnparsed;
            });
          }
          break;
        case filterTypes.DATE:
          filterValueParsed = filterValueUnparsed;
          break;
        case filterTypes.INPUT_TEXT:
          filterValueParsed = filterValueUnparsed;
          break;
        case filterTypes.CATEGORIZED_VALUE:
          // look up category, value stays untouched
          if (store) {
            const category = store.allItems.find((element) => {
              return (
                element[filterValueProperty] === filterValueUnparsed.category
              );
            });
            filterValueParsed = {
              category: category,
              value: filterValueUnparsed.value,
            };
          }
          break;
        default:
          continue;
      }

      console.log(filterValueParsed);
      if (filterValueParsed) {
        parsedFilters[filterName] = filterValueParsed;
      }
    }
    filterStore.bulkSetFilters({
      filterType: "alerts",
      filters: parsedFilters,
    });
  }
</script>
