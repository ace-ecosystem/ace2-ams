<template>
  <EventStatusTag
    v-for="entry in observable.matchingEvents"
    :key="entry.status"
    style="cursor: pointer"
    :status="entry.status"
    :status-count="entry.count"
    @click="filterByObservableAndStatus(entry.status)"
  ></EventStatusTag>
</template>

<script setup lang="ts">
  import { defineProps, PropType } from "vue";
  import { useRouter } from "vue-router";

  import EventStatusTag from "@/components/Events/EventStatusTag.vue";
  import { useEventStatusStore } from "@/stores/eventStatus";
  import { useFilterStore } from "@/stores/filter";
  import { eventStatusRead } from "@/models/eventStatus";
  import {
    observableTreeRead,
    observableInAlertRead,
  } from "@/models/observable";

  const router = useRouter();

  const eventStatusStore = useEventStatusStore();
  const filterStore = useFilterStore();

  const props = defineProps({
    observable: {
      type: Object as PropType<observableTreeRead | observableInAlertRead>,
      required: true,
    },
    rerouteToManageEvents: {
      type: Boolean,
      required: true,
    },
  });

  const filterByObservableAndStatus = (status: string) => {
    const statusObject = getStatusObject(status);

    filterStore.clearAll({ objectType: "events" });

    if (statusObject) {
      filterStore.setFilter({
        objectType: "events",
        filterName: "status",
        filterValue: statusObject,
        isIncluded: true,
      });
    }

    filterStore.setFilter({
      objectType: "events",
      filterName: "observable",
      filterValue: {
        category: props.observable.type,
        value: props.observable.value,
      },
      isIncluded: true,
    });

    if (props.rerouteToManageEvents) {
      router.replace({
        path: "/manage_events",
      });
    }
  };

  const getStatusObject = (status: string): eventStatusRead | undefined => {
    return eventStatusStore.items.find((item) => item.value == status);
  };
</script>
