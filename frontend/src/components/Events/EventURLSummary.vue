<!-- EventURLSummary.vue -->
<!-- A simple list of all URLs contained in the given alert UUIDs -->

<template>
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

<script setup>
  import { defineProps, ref, onMounted } from "vue";
  import Listbox from "primevue/listbox";
  import { NodeTree } from "@/services/api/nodeTree";
  import { copyToClipboard } from "@/etc/helpers";

  const props = defineProps({
    eventAlertUuids: { type: Array, required: true },
  });

  const selectedURL = ref(null);
  const sortedUrlObservables = ref([]);

  onMounted(async () => {
    const observables = await getAllObservables();
    sortedUrlObservables.value = getURLObservables(observables);
  });

  const getAllObservables = async () => {
    const allObservables = await NodeTree.readNodesOfNodeTree(
      props.eventAlertUuids,
      "observable",
    );
    return allObservables;
  };

  const getURLObservables = (allObservables) => {
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
