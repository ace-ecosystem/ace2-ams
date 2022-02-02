<!-- AlertTableCell.vue -->
<!-- Contains logic and functionality to display field-specific data in TheAlertTable -->

<template>
  <!-- Alert Name -->
  <div v-if="props.field === 'name'">
    <!-- Name w/ Link to Alert -->
    <span class="p-m-1" data-cy="alertName">
      <router-link :to="getAlertLink(props.data)">{{
        props.data.name
      }}</router-link></span
    >
    <br />
    <!-- Alert Tags -->
    <span data-cy="tags">
      <NodeTagVue
        v-for="tag in getAllAlertTags(props.data)"
        :key="tag.uuid"
        :tag="tag"
      ></NodeTagVue>
    </span>
    <!-- Alert comments -->
    <span v-if="props.data.comments">
      <pre
        v-for="comment in props.data.comments"
        :key="comment.uuid"
        class="p-mr-2 comment"
        >{{ formatComment(comment) }}</pre
      >
    </span>
  </div>

  <!-- Alert Time Property -->
  <span v-else-if="props.field.includes('Time')">
    {{ formatDateTime(props.data[props.field]) }}</span
  >

  <!-- Everything else -->
  <span v-else> {{ props.data[props.field] }}</span>
</template>

<script setup>
  import { defineProps } from "vue";

  import NodeTagVue from "@/components/Node/NodeTag.vue";

  import { getAllAlertTags, getAlertLink } from "@/etc/helpers";

  const props = defineProps({
    data: { type: Object, required: true },
    field: { type: String, required: true },
  });

  const formatComment = (comment) => {
    return `(${comment.user.displayName}) ${comment.value}`;
  };

  const formatDateTime = (dateTime) => {
    if (dateTime) {
      const d = new Date(dateTime);
      return d.toLocaleString("en-US", { timeZone: "UTC" });
    }

    return "None";
  };
</script>

<style>
  .link-text:hover {
    cursor: pointer;
    text-decoration: underline;
    font-weight: bold;
  }
</style>
