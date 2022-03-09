<!-- EventURLSummary.vue -->
<!-- A simple list of all URLs contained in the given event uuid or open event (whichever is given) -->

<template>
  <Listbox
    v-model="selectedURL"
    :options="urlObservables"
    option-value="value"
    option-label="value"
    data-key="uuid"
    empty-message="This event doesn't have any URL observables."
    @change="copyToClipboard(selectedURL)"
  />
</template>

<script setup>
  import { defineProps, ref, onBeforeMount } from "vue";
  import Listbox from "primevue/listbox";
  import { Alert } from "@/services/api/alert";
  import { NodeTree } from "@/services/api/nodeTree";
  import { copyToClipboard } from "@/etc/helpers";

  const props = defineProps({
    eventUuid: { type: String, required: true },
  });

  const selectedURL = ref(null);
  const urlObservables = ref([]);

  onBeforeMount(async () => {
    const observables = await getAllObservables();
    getURLObservables(observables);
  });

  const getAllObservables = async () => {
    const allAlerts = await Alert.readAllPages({
      eventUuid: props.eventUuid,
      sort: "event_time|asc",
    });

    const allObservables = await NodeTree.readNodesOfNodeTree(
      allAlerts.map((alert) => alert.uuid),
      "observable",
    );
    return allObservables;
  };

  const getURLObservables = (allObservables) => {
    urlObservables.value = allObservables.filter(
      (observable) => observable.type.value == "url",
    );

    urlObservables.value = urlObservables.value.sort((a, b) => {
      if (a.type.value === b.type.value) {
        return a.value < b.value ? -1 : 1;
      } else {
        return a.type.value < b.type.value ? -1 : 1;
      }
    });
  };
</script>
