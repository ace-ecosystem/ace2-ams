<template>
  <span class="tag">
    <Tag rounded
      ><span class="tag" style="cursor: pointer" @click="filterByTags">{{
        tag.value
      }}</span></Tag
    >
  </span>
</template>

<script setup lang="ts">
  import Tag from "primevue/tag";

  import { defineProps, inject, PropType } from "vue";
  import { useRouter } from "vue-router";
  import { useFilterStore } from "@/stores/filter";
  import { metadataTagRead } from "@/models/metadataTag";

  const router = useRouter();
  const nodeType = inject("nodeType") as "alerts" | "events";
  const nodeRoutes = {
    alerts: "/manage_alerts",
    events: "/manage_events",
  };

  const filterStore = useFilterStore();

  const props = defineProps({
    tag: { type: Object as PropType<metadataTagRead>, required: true },
    overrideNodeType: {
      type: String as PropType<"alerts" | "events">,
      required: false,
      default: null,
    },
  });

  function filterByTags() {
    const preferredNodeType = props.overrideNodeType
      ? props.overrideNodeType
      : nodeType;
    const route = nodeRoutes[preferredNodeType];
    if (route) {
      filterStore.bulkSetFilters({
        nodeType: preferredNodeType,
        filters: {
          tags: { included: [[props.tag.value]], notIncluded: [] },
        },
      });
      // Route to given page with query for filtering by this tag's value
      router.replace({ path: route });
    }
  }
</script>
<style>
  .tag {
    padding: 2px;
  }
</style>
