<!-- AnalysisDetailsBase.vue -->
<!-- Base/Details component for analysis details -->

<template>
  <span> Basic Analysis </span>
  <br />
  <span> {{ props.section }} </span>
</template>

<script setup>
  import { defineProps } from "vue";

  const props = defineProps({
    section: { type: String, required: true },
  });
</script>
