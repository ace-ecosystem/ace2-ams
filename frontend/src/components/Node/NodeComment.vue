<template>
  <span>
    {{ formatComment(props.comment) }}
  </span>
  <br v-if="props.lineBreak" />
</template>

<script setup>
  import { defineProps } from "vue";

  const props = defineProps({
    comment: { type: Object, required: true },
    includeTime: { type: Boolean, required: false, default: false },
    lineBreak: { type: Boolean, required: false, default: true },
  });

  const formatComment = (comment) => {
    if (props.includeTime) {
      const d = new Date(comment.insertTime);
      return `${d.toLocaleString("en-US")} (${comment.user.displayName}) ${
        comment.value
      }`;
    }
    return `(${comment.user.displayName}) ${comment.value}`;
  };
</script>
