<!-- EmailAnalysis.vue -->

<template>
  <h5>Email Details</h5>
  <div v-if="isLoading">Loading...</div>
  <div v-else-if="emailHeadersBody">
    <Panel header="Headers" :toggleable="true">
      <div style="width: 100%">
        <pre>{{ emailHeadersBody.headers }}</pre>
      </div>
    </Panel>
    <br />
    <Panel header="Body" :toggleable="true">
      <div class="flex">
        <div v-if="emailHeadersBody.bodyText" class="panel-content">
          <h5>Body Text</h5>
          <pre>{{ emailHeadersBody.bodyText }}</pre>
        </div>
        <Divider layout="vertical" />
        <div v-if="emailHeadersBody.bodyHtml" class="panel-content">
          <h5>Body HTML</h5>
          <pre class="pre-panel">{{ emailHeadersBody.bodyHtml }}</pre>
        </div>
      </div>
    </Panel>
  </div>
  <div v-else>
    <div>Couldn't load email details: {{ error }}</div>
  </div>
</template>

<script setup>
  import { onMounted, ref, defineProps } from "vue";

  import Panel from "primevue/panel";
  import Divider from "primevue/divider";

  import { Event } from "@/services/api/event";

  const props = defineProps({
    eventUuid: { type: String, required: true },
  });
  const isLoading = ref(false);
  const error = ref(null);
  const emailHeadersBody = ref(null);

  onMounted(async () => {
    isLoading.value = true;
    try {
      emailHeadersBody.value = await Event.readEmailHeadersAndBody(
        props.eventUuid,
      );
    } catch (error) {
      error.value = error.message;
    }
    isLoading.value = false;
  });
</script>

<style scoped>
  .panel-content {
    width: 100%;
    max-height: 800px;
  }

  pre {
    white-space: pre-wrap;
    overflow-y: auto;
    max-height: 600px;
  }
</style>
