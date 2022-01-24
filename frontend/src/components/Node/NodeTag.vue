<template>
  <span class="tag">
    <Tag rounded
      ><span class="tag" style="cursor: pointer" @click="filterByTags">{{
        tag.value
      }}</span></Tag
    >
  </span>
</template>

<script setup>
  import Tag from "primevue/tag";

  import { defineProps, inject } from "vue";
  import { useRouter } from "vue-router";
  const router = useRouter();
  const nodeType = inject("nodeType");

  const props = defineProps({
    tag: { type: Object, required: true },
  });

  function filterByTags() {
    // Determine what page to route to, right now only option is alerts - Manage Alerts
    const nodeRoutes = {
      alerts: "/manage_alerts",
      events: "/manage_events",
    };
    const route = nodeRoutes[nodeType];
    if (route) {
      // Route to given page with query for filtering by this tag's value
      router.replace({ path: route, query: { tags: props.tag.value } });
    }
  }
</script>
<style>
  .tag {
    padding: 2px;
  }
</style>
