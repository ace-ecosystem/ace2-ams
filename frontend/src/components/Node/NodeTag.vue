<template>
  <Chip
    ><span class="p-chip-text" style="cursor: pointer" @click="filterByTags">{{
      tag.value
    }}</span></Chip
  >
</template>

<script setup>
  import Chip from "primevue/chip";

  import { defineProps, inject } from "vue";
  import { useRouter } from "vue-router";
  const router = useRouter();
  const filterType = inject("filterType");

  const props = defineProps({
    tag: { type: Object, required: true },
  });

  function filterByTags() {
    // Determine what page to route to, right now only option is alerts - Manage Alerts
    const route = filterType == "alerts" ? "/manage_alerts" : null;
    if (route) {
      // Route to given page with query for filtering by this tag's value
      router.replace({ path: route, query: { tags: props.tag.value } });
    }
  }
</script>
