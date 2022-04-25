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
    nodeQueue: {
      type: String as PropType<"alerts" | "events">,
      required: true,
    },
  });

  const preferredQueue = ref();

  if (props.nodeQueue === "alerts") {
    preferredQueue.value = currentUserSettingsStore.queues.alerts;
  } else if (props.nodeQueue === "events") {
    preferredQueue.value = currentUserSettingsStore.queues.events;
  }

  const updateUserSettings = () => {
    if (props.nodeQueue === "alerts") {
      currentUserSettingsStore.queues.alerts = preferredQueue.value;
      filterStore.setFilter({
        nodeType: "alerts",
        filterName: "queue",
        filterValue: preferredQueue.value,
      });
    } else if (props.nodeQueue === "events") {
      currentUserSettingsStore.queues.events = preferredQueue.value;
      filterStore.setFilter({
        nodeType: "events",
        filterName: "queue",
        filterValue: preferredQueue.value,
      });
    }
  };
</script>
