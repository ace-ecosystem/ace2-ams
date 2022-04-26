<template>
  <span>
    {{ formatComment(props.comment) }}
  </span>
  <br v-if="props.includeLineBreak" />
</template>

<script setup lang="ts">
  import { nodeCommentRead } from "@/models/nodeComment";
  import { defineProps, PropType } from "vue";

  const props = defineProps({
    comment: { type: Object as PropType<nodeCommentRead>, required: true },
    includeTime: { type: Boolean, required: false, default: false },
    includeLineBreak: { type: Boolean, required: false, default: true },
  });

  const formatComment = (comment: nodeCommentRead) => {
    if (props.includeTime) {
      const d = new Date(comment.insertTime);
      return `${d.toLocaleString("en-US")} (${comment.user.displayName}) ${
        comment.value
      }`;
    }
    return `(${comment.user.displayName}) ${comment.value}`;
  };
</script>
