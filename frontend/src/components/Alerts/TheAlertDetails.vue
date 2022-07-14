<template>
  <Message v-if="error" severity="error" data-cy="error-banner">{{
    error
  }}</Message>
  <Panel
    data-cy="alert-url-domain-summary"
    header="Alert Details"
    :toggleable="true"
    :collapsed="true"
  >
    <component :is="currentComponent" v-if="currentComponent"></component>
    <div v-else>
      {{ prettyAlertDetails }}
    </div>
  </Panel>

</template>
<script setup lang="ts">
  import Panel from "primevue/panel";
  import Message from "primevue/message";
  import { useAlertStore } from "@/stores/alert";
  import { findClosestMatchingString } from "@/etc/helpers";

  import { ref, inject, computed, shallowRef, onMounted } from "vue";

  const config = inject("config") as {
    alerts: { alertDetailsComponents: Record<string, any> };
  };
  const alertStore = useAlertStore();

  const error = ref<string>();
  const currentComponent = shallowRef();
  const componentMapping = {
    ...config.alerts.alertDetailsComponents,
  };

  onMounted(() => {
    initPage();
  });

  function initPage() {
    if (alertStore.open) {
      const matchingKey = findClosestMatchingString(
        Object.keys(componentMapping),
        alertStore.open.type.value,
      );
      if (matchingKey) {
        currentComponent.value = componentMapping[matchingKey];
      } else {
        currentComponent.value = undefined;
      }
    }
  }

  const prettyAlertDetails = computed(() => {
    if (alertStore.open && alertStore.open.rootAnalysis.details) {
      return JSON.stringify(alertStore.open.rootAnalysis.details, null, 4);
    }
    return "No alert details available.";
  });
</script>
