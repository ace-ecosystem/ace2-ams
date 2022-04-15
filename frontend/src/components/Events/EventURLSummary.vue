<!-- EventURLSummary.vue -->
<!-- A simple list of all URLs contained in the given alert UUIDs -->

<template>
  <Message v-if="error" severity="error" data-cy="error-banner">{{
    error
  }}</Message>
  <Listbox
    v-model="selectedURL"
    :options="sortedUrlObservables"
    option-value="value"
    option-label="value"
    data-key="uuid"
    empty-message="This event doesn't have any URL observables."
    data-cy="url-observable-listbox"
    @change="copyToClipboard(selectedURL)"
  />
</template>

<script setup lang="ts">
  import { defineProps, ref, onMounted, PropType } from "vue";

  import Listbox from "primevue/listbox";
  import Message from "primevue/message";

  import { NodeTree } from "@/services/api/nodeTree";
  import { copyToClipboard } from "@/etc/helpers";
  import { observableRead } from "@/models/observable";

  const props = defineProps({
    eventAlertUuids: { type: Array as PropType<string[]>, required: true },
  });

  const error = ref<string>();
  const selectedURL = ref(null);
  const sortedUrlObservables = ref<observableRead[]>([]);

  onMounted(async () => {
    const observables = await getAllObservables();
    sortedUrlObservables.value = getURLObservables(observables);
  });

  const getAllObservables = async () => {
    try {
      const allObservables = await NodeTree.readNodesOfNodeTree(
        props.eventAlertUuids,
        "observable",
      );
      return allObservables as unknown as observableRead[];
    } catch (e: unknown) {
      if (typeof e === "string") {
        error.value = e;
      } else if (e instanceof Error) {
        error.value = e.message;
      }
      return [];
    }
  };

  const getURLObservables = (allObservables: observableRead[]) => {
    const urlObservables = allObservables.filter(
      (observable) => observable.type.value == "url",
    );

    return urlObservables.sort((a, b) => {
      if (a.type.value === b.type.value) {
        return a.value < b.value ? -1 : 1;
      } else {
        return a.type.value < b.type.value ? -1 : 1;
      }
    });
  };
</script>
