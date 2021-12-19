<template>
  <Chip
    ><span class="p-chip-text">{{ tag.value }}</span></Chip
  >
</template>

<script setup>
  import Chip from "primevue/chip";

  import { defineProps } from "vue";
  const props = defineProps({
    tag: { type: Object, required: true },
  });
</script>
