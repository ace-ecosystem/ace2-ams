<!-- AlertTableCell.vue -->
<!-- Contains logic and functionality to display field-specific data in TheAlertTable -->

<template>
  <!-- Alert Name -->
  <div v-if="props.field === 'name'">
    <!-- Name w/ Link to Alert -->
    <span class="p-m-1" data-cy="alertName">
      <router-link :to="getAlertLink(props.data.uuid)">{{
        props.data.name
      }}</router-link></span
    >
    <br />
    <!-- Alert Tags -->
    <span data-cy="tags">
      <NodeTagVue
        v-for="tag in getAllTags(props.data)"
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
      return d.toLocaleString("en-US");
    }

    return "None";
  };

  const getAlertLink = (uuid) => {
    return "/alert/" + uuid;
  };

  const getAllTags = (alert) => {
    const allTags = alert.tags.concat(alert.childTags);

    // Return a sorted and deduplicated list of the tags based on the tag UUID.
    return [...new Map(allTags.map((v) => [v.uuid, v])).values()].sort((a, b) =>
      a.value > b.value ? 1 : -1,
    );
  };
</script>

<style>
  .link-text:hover {
    cursor: pointer;
    text-decoration: underline;
    font-weight: bold;
  }
</style>
