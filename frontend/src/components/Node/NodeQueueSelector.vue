<template>
  <div data-cy="event-queue-selector">
    <Dropdown
      v-model="preferredQueue"
      :options="queueStore.items"
      option-label="value"
      style="margin-right: 2%"
      @change="updateUserSettings"
    ></Dropdown>
  </div>
</template>

<script setup>
  import Dropdown from "primevue/dropdown";

  import { useCurrentUserSettingsStore } from "@/stores/currentUserSettings";
  import { useQueueStore } from "@/stores/queue";
  import { defineProps, ref, watchEffect } from "vue";

  const queueStore = useQueueStore();

  const props = defineProps({
    nodeQueue: { type: String, required: true },
  });

  const currentUserSettingsStore = useCurrentUserSettingsStore();
  const preferredQueue = ref();

  if (props.nodeQueue === "alerts") {
    preferredQueue.value = currentUserSettingsStore.queues.alerts;
  } else if (props.nodeQueue === "events") {
    preferredQueue.value = currentUserSettingsStore.queues.events;
  }

  const updateUserSettings = () => {
    if (props.nodeQueue === "alerts") {
      currentUserSettingsStore.queues.alerts = preferredQueue.value;
    } else if (props.nodeQueue === "events") {
      currentUserSettingsStore.queues.events = preferredQueue.value;
    }
  };
</script>
