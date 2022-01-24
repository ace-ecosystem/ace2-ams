<template>
  <!-- Event Name -->
  <div v-if="props.field === 'name'">
    <span class="p-m-1" data-cy="eventName">
      <router-link :to="getEventLink(props.data.uuid)">{{
        props.data.name
      }}</router-link></span
    >
    <!-- Event Tags -->
    <span data-cy="tags">
      <NodeTagVue
        v-for="tag in props.data.tags"
        :key="tag.uuid"
        :tag="tag"
      ></NodeTagVue>
    </span>
    <br />
    <!-- Event Comments -->
    <span v-if="props.data.comments">
      <pre
        v-for="comment in props.data.comments"
        :key="comment.uuid"
        class="p-mr-2 comment"
        >{{ formatComment(comment) }}</pre
      >
    </span>
  </div>
  <!-- Event Time fields -->
  <span v-else-if="props.field.includes('Time')">
    {{ formatDateTime(props.data[props.field]) }}</span
  >
  <!-- Any event property that uses a list -->
  <span v-else-if="Array.isArray(props.data[props.field])">
    {{ joinStringArray(props.data[props.field]) }}
  </span>
  <!-- All other columns -->
  <span v-else> {{ props.data[props.field] }}</span>
</template>

<script setup>
  import { defineProps } from "vue";
  import NodeTagVue from "../Node/NodeTag.vue";

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
