<template>
  <span class="tag">
    <Tag rounded
      ><span class="tag"> {{ props.type }}: {{ props.value }} </span></Tag
    >
  </span>
</template>

<script setup lang="ts">
  import Tag from "primevue/tag";

  import { defineProps } from "vue";

  const props = defineProps({
    type: { type: String, required: true },
    value: { type: String, required: true },
  });
</script>
<style>
  .tag {
    padding: 2px;
  }
</style>
