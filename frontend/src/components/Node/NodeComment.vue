<template>
  <span>
    {{ formatComment(props.comment) }}
  </span>
  <br v-if="props.includeLineBreak" />
</template>

<script setup lang="ts">
  import { prettyPrintDateTime } from "@/etc/helpers";
  import { nodeCommentRead } from "@/models/nodeComment";
  import { defineProps, PropType } from "vue";

  const props = defineProps({
    comment: { type: Object as PropType<nodeCommentRead>, required: true },
    includeTime: { type: Boolean, required: false, default: false },
    includeLineBreak: { type: Boolean, required: false, default: true },
  });

  const formatComment = (comment: nodeCommentRead) => {
    if (props.includeTime) {
      return `${prettyPrintDateTime(comment.insertTime)} (${
        comment.user.displayName
      }) ${comment.value}`;
    }
    return `(${comment.user.displayName}) ${comment.value}`;
  };
</script>
