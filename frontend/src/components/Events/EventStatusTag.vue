<template>
  <span class="tag" data-cy="event-status-tag">
    <Tag rounded :style="tagStyle"
      ><span class="tag"> Event {{ status }} </span>
      <span v-if="statusCount">({{ statusCount }})</span>
    </Tag>
  </span>
</template>

<script setup lang="ts">
  import { computed, defineProps, inject } from "vue";
  import Tag from "primevue/tag";
  import type CSS from "csstype";

  const config = inject("config") as Record<string, any>;

  const props = defineProps({
    status: {
      type: String,
      required: true,
    },
    statusCount: {
      type: Number,
      default: undefined,
      required: false,
    },
  });

  const tagStyle = computed(() => {
    const style: CSS.Properties = {};

    const statusLowerCase = props.status.toLowerCase();
    if (statusLowerCase in config.events.eventStatusMetadata) {
      style["backgroundColor"] =
        config.events.eventStatusMetadata[statusLowerCase];
    } else {
      style["backgroundColor"] = "white";
      style["color"] = "black";
      style["borderStyle"] = "solid";
      style["borderWidth"] = "thin";
    }
    return style;
  });
</script>
