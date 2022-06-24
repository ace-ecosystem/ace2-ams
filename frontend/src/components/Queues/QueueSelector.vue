<template>
  <div data-cy="event-queue-selector">
    <span class="p-float-label">
      <Dropdown
        id="queue-dropdown"
        v-model="preferredQueue"
        :options="queueStore.items"
        option-label="value"
        style="margin-right: 2%"
        @change="updateUserSettings"
      />
      <label for="queue-dropdown">Queue</label>
    </span>
  </div>
</template>

<script setup lang="ts">
  import { defineProps, ref, PropType } from "vue";

  import Dropdown from "primevue/dropdown";

  import { useCurrentUserSettingsStore } from "@/stores/currentUserSettings";
  import { useFilterStore } from "@/stores/filter";
  import { useQueueStore } from "@/stores/queue";

  const currentUserSettingsStore = useCurrentUserSettingsStore();
  const filterStore = useFilterStore();
  const queueStore = useQueueStore();

  const props = defineProps({
    objectQueue: {
      type: String as PropType<"alerts" | "events">,
      required: true,
    },
  });

  const preferredQueue = ref();

  if (props.objectQueue === "alerts") {
    preferredQueue.value = currentUserSettingsStore.queues.alerts;
  } else if (props.objectQueue === "events") {
    preferredQueue.value = currentUserSettingsStore.queues.events;
  }

  const updateUserSettings = () => {
    if (props.objectQueue === "alerts") {
      currentUserSettingsStore.queues.alerts = preferredQueue.value;
      filterStore.unsetFilter({ objectType: "alerts", filterName: "queue" });
      filterStore.setFilter({
        objectType: "alerts",
        filterName: "queue",
        filterValue: preferredQueue.value,
      });
    } else if (props.objectQueue === "events") {
      currentUserSettingsStore.queues.events = preferredQueue.value;
      filterStore.unsetFilter({ objectType: "events", filterName: "queue" });
      filterStore.setFilter({
        objectType: "events",
        filterName: "queue",
        filterValue: preferredQueue.value,
      });
    }
  };
</script>
