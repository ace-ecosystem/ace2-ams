<template>
  <span class="tag">
    <Tag rounded :style="tagStyle"
      ><span class="tag"> {{ disposition }} </span></Tag
    >
  </span>
</template>

<script setup lang="ts">
  import { computed, defineProps, inject } from "vue";
  import Tag from "primevue/tag";

  const config = inject("config") as Record<string, any>;

  const props = defineProps({
    disposition: {
      type: String,
      required: true,
    },
  });

  const tagStyle = computed(() => {
    const dispositionLowerCase = props.disposition.toLowerCase();
    if (dispositionLowerCase in config.alerts.alertDispositionMetadata) {
      return {
        backgroundColor:
          config.alerts.alertDispositionMetadata[dispositionLowerCase],
      };
    }
    return {
      backgroundColor: "white",
      color: "black",
    };
  });
</script>
