<template>
  <span class="tag">
    <Tag rounded :style="tagStyle"
      ><span class="tag"> {{ disposition }} </span>
      <span v-if="percent">{{ percent }}% </span>
      <span v-if="dispositionCount">({{ dispositionCount }})</span>
    </Tag>
  </span>
</template>

<script setup lang="ts">
  import { computed, defineProps, inject } from "vue";
  import Tag from "primevue/tag";
  import type CSS from "csstype";

  const config = inject("config") as Record<string, any>;

  const props = defineProps({
    disposition: {
      type: String,
      required: true,
    },
    dispositionCount: {
      type: Number,
      default: undefined,
      required: false,
    },
    percent: {
      type: Number,
      default: undefined,
      required: false,
    },
  });

  const tagStyle = computed(() => {
    const style: CSS.Properties = {};

    const dispositionLowerCase = props.disposition.toLowerCase();
    if (dispositionLowerCase in config.alerts.alertDispositionMetadata) {
      style["backgroundColor"] =
        config.alerts.alertDispositionMetadata[dispositionLowerCase];
    } else {
      style["backgroundColor"] = "white";
      style["color"] = "black";
      style["borderStyle"] = "solid";
      style["borderWidth"] = "thin";
    }
    return style;
  });
</script>
