/* eslint-disable vue/attribute-hyphenation */
<!-- TheEventsTable.vue -->
<!-- The table where all currently filtered events are displayed, selected to take action, or link to an individual event page -->

<template>
  <div v-if="props.field === 'name'">
    <span class="p-m-1" data-cy="eventName">
      <router-link :to="getEventLink(props.data.uuid)">{{
        props.data.name
      }}</router-link></span
    >
    <br />
    <span v-if="props.data.comments">
      <pre
        v-for="comment in props.data.comments"
        :key="comment.uuid"
        class="p-mr-2 comment"
        >{{ formatComment(comment) }}</pre
      >
    </span>
  </div>
  <span v-else-if="props.field.includes('Time')">
    {{ formatDateTime(props.data[props.field]) }}</span
  >
  <span v-else-if="Array.isArray(props.data[props.field])">
    {{ joinStringArray(props.data[props.field]) }}
  </span>
  <span v-else> {{ props.data[props.field] }}</span>
</template>

<script setup>
  import { defineProps } from "vue";

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

  const getEventLink = (uuid) => {
    return "/event/" + uuid;
  };

  const joinStringArray = (arr) => {
    return arr.join(", ");
  };
</script>
