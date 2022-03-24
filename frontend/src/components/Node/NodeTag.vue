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
    import { useFilterStore } from "@/stores/filter";
    
  const router = useRouter();
  const nodeType = inject("nodeType");
  const nodeRoutes = {
    alerts: "/manage_alerts",
    events: "/manage_events",
  };

  const filterStore = useFilterStore();

  const props = defineProps({
    tag: { type: Object, required: true },
    overrideNodeType: { type: String, required: false, default: null },
  });

  function filterByTags() {
    const preferredNodeType = props.overrideNodeType
      ? props.overrideNodeType
      : nodeType;
    const route = nodeRoutes[preferredNodeType];
    if (route) {
      filterStore.bulkSetFilters({
        nodeType: nodeType,
        filters: {
          tags: [props.tag.value],
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
