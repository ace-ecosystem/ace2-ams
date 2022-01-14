<!-- ManageEvents.vue -->

<template>
  <br />
  <TheEventActionToolbar page="Manage Events" />
  <br />
  <TheFilterToolbar id="FilterToolbar" />
  <br />
  <div id="EventsTable" class="card">
    <TheEventsTable />
  </div>
</template>

<script setup>
  import { onMounted, provide, watch } from "vue";

  import {
    eventFilters,
    eventRangeFilters,
    filterTypes,
  } from "@/etc/constants";

  import TheEventActionToolbar from "@/components/Events/TheEventActionToolbar.vue";
  import TheFilterToolbar from "@/components/Filters/TheFilterToolbar";
  import TheEventsTable from "@/components/Events/TheEventsTable";
  import { useRoute, useRouter } from "vue-router";

  import { useFilterStore } from "@/stores/filter";
  import { populateCommonStores, isValidDate } from "@/etc/helpers";

  const route = useRoute();
  const router = useRouter();

  provide("availableFilters", eventFilters);
  provide("filterType", "events");
  provide("rangeFilters", eventRangeFilters);

  const filterStore = useFilterStore();

  onMounted(async () => {
    if (Object.keys(route.query).length) {
      // Will need to load common stores in order to find filter values
      await populateCommonStores();
      loadRouteQuery();
    }
  });

  watch(route, () => {
    if (Object.keys(route.query).length) {
      loadRouteQuery();
    }
  });

  function loadRouteQuery() {
    // load filters given in route
    loadFilters();
    // Reload page to clear URL params
    router.push("/manage_events");
  }

  function loadFilters() {
    const parsedFilters = {};

    // parse each filter
    for (const filterName in route.query) {
      // first get the filter object so you can validate the filter exists and use its metadata
      let filterNameObject = eventFilters.find((filter) => {
        return filter.name === filterName;
      });
      filterNameObject = filterNameObject ? filterNameObject : null;

      // if the filter doesn't exist, skip it
      if (!filterNameObject) {
        continue;
      }

      let filterValueUnparsed = route.query[filterName]; // the filter value from URL
      // format filterValueUnparsed for GUI if method available
      if (filterNameObject.parseFormattedFilterString) {
        filterValueUnparsed = filterNameObject.parseFormattedFilterString(
          route.query[filterName],
        );
      }

      // use correct property for determinining equality (default is 'value')
      const filterValueProperty = filterNameObject.valueProperty
        ? filterNameObject.valueProperty
        : "value";

      // load the filter options store if available
      let store = null; // store that may be used to find filter value object
      if (filterNameObject.store) {
        store = filterNameObject.store();
      }

      let filterValueParsed = null; // the target filter value, might be an Object, Array, Date, or string
      // based on the filter type, parse/format the filter value
      switch (filterNameObject.type) {
        case filterTypes.MULTISELECT:
          // look up each array item in store, add to filter value
          filterValueParsed = [];
          if (store) {
            for (const value of filterValueUnparsed) {
              const valueObject = store.allItems.find((element) => {
                return element[filterValueProperty] === value;
              });
              if (valueObject) {
                filterValueParsed.push(valueObject);
              }
            }
          }
          filterValueParsed = filterValueParsed.length
            ? filterValueParsed
            : null;
          break;

        case filterTypes.CHIPS:
          // array of strings, handled in parseFormattedFilterString
          filterValueParsed = filterValueUnparsed;
          break;

        case filterTypes.SELECT:
          // look item up in store
          if (store) {
            filterValueParsed = store.allItems.find((element) => {
              return element[filterValueProperty] === filterValueUnparsed;
            });
          }
          break;

        case filterTypes.DATE:
          // Date string, handled in parseFormattedFilterString
          filterValueParsed = isValidDate(filterValueUnparsed)
            ? filterValueUnparsed
            : null;
          break;

        case filterTypes.INPUT_TEXT:
          // does not need parsing
          filterValueParsed = filterValueUnparsed;
          break;

        case filterTypes.CATEGORIZED_VALUE:
          // look up category value in store, sub-value stays untouched
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

        // Unsupported filter types will be ignored
        default:
          console.log(
            `Unsupported filter type found: ${filterNameObject.type}`,
          );
          continue;
      }

      // If filter value was successfully parsed add it to the new filter object
      if (filterValueParsed) {
        parsedFilters[filterName] = filterValueParsed;
      }
    }

    // Set filters in store (evemts will auto-reload)
    filterStore.bulkSetFilters({
      filterType: "events",
      filters: parsedFilters,
    });
  }
</script>
