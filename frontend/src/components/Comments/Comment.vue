<template>
  <span>
    {{ formatComment(props.comment) }}
  </span>
  <br v-if="props.includeLineBreak" />
</template>

<script setup lang="ts">
  import { prettyPrintDateTime } from "@/etc/helpers";
  import { commentRead } from "@/models/comment";
  import { defineProps, PropType } from "vue";

  const props = defineProps({
    comment: { type: Object as PropType<commentRead>, required: true },
    includeTime: { type: Boolean, required: false, default: false },
    includeLineBreak: { type: Boolean, required: false, default: true },
  });

  const formatComment = (comment: commentRead) => {
    if (props.includeTime) {
      return `${prettyPrintDateTime(comment.insertTime)} (${
        comment.user.displayName
      }) ${comment.value}`;
    }
    return `(${comment.user.displayName}) ${comment.value}`;
  };
</script>
