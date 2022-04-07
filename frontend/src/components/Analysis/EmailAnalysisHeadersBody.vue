<!-- EmailAnalysis.vue -->

<template>
  <div v-if="isLoading">Loading...</div>
  <div v-else-if="emailHeadersBodyRes">
    <span>
      <h5>
        Email Details
        <router-link :to="`/alert/${emailHeadersBodyRes.alertUuid}`" exact
          >(Alert)</router-link
        >
      </h5>
    </span>
    <Panel id="email-headers-panel" header="Headers" :toggleable="true">
      <div style="width: 100%">
        <pre>{{ emailHeadersBodyRes.headers }}</pre>
      </div>
    </Panel>
    <br />
    <Panel id="email-body-panel" header="Body" :toggleable="true">
      <div class="flex">
        <div
          v-if="emailHeadersBodyRes.bodyText?.length"
          id="body-text"
          class="panel-content"
        >
          <h5>Body Text</h5>
          <pre>{{ emailHeadersBodyRes.bodyText }}</pre>
        </div>
        <Divider
          v-if="emailHeadersBodyRes.bodyHtml && emailHeadersBodyRes.bodyText"
          id="divider"
          layout="vertical"
        />
        <div
          v-if="emailHeadersBodyRes.bodyHtml?.length"
          id="body-html"
          class="panel-content"
        >
          <h5>Body HTML</h5>
          <pre class="pre-panel">{{ emailHeadersBodyRes.bodyHtml }}</pre>
        </div>
      </div>
    </Panel>
  </div>
  <div v-else-if="error">
    <div>Couldn't load email details: {{ error }}</div>
  </div>
</template>

<script setup lang="ts">
  import { onMounted, ref, defineProps } from "vue";

  import Panel from "primevue/panel";
  import Divider from "primevue/divider";

  import { Event } from "@/services/api/event";
  import { emailHeadersBody } from "@/models/eventSummaries";

  const props = defineProps({
    eventUuid: { type: String, required: true },
  });
  const isLoading = ref(false);
  const error = ref<string>();
  const emailHeadersBodyRes = ref<emailHeadersBody>();

  onMounted(async () => {
    isLoading.value = true;
    try {
      emailHeadersBodyRes.value = await Event.readEmailHeadersAndBody(
        props.eventUuid,
      );
    } catch (e: unknown) {
      if (typeof e === "string") {
        error.value = e;
      } else if (e instanceof Error) {
        error.value = e.message;
      }
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
