<template>
  <span class="p-float-label">
    <AutoComplete
      v-model="selected"
      :suggestions="filteredComments"
      :dropdown="true"
      :disabled="!recentCommentStore.recentComments.length"
      force-selection
      auto-highlight
      @complete="searchComment($event)"
      @item-select="itemSelect($event.value)"
    >
      <template #item="slotProps">
        <div>
          <span class="ml-2">{{ slotProps.item }}</span>
          <span
            class="delete-comment"
            style="float: right"
            @click="removeComment(slotProps.item)"
            ><span class="pi pi-times"></span
          ></span>
        </div>
      </template>
    </AutoComplete>
    <label v-if="recentCommentStore.recentComments.length" for="autocomplete"
      >Choose a recent comment</label
    >
    <label v-if="!recentCommentStore.recentComments.length" for="autocomplete"
      >No recent comments available</label
    >
  </span>
</template>
<script setup lang="ts">
  import { ref, defineEmits, watch } from "vue";

  import AutoComplete from "primevue/autocomplete";

  import { useRecentCommentsStore } from "@/stores/recentComments";
  const emit = defineEmits(["commentClicked"]);
  const selected = ref<string>();
  const recentCommentStore = useRecentCommentsStore();
  const filteredComments = ref<string[]>();

  const searchComment = (event: { query: string }) => {
    setTimeout(() => {
      if (!event.query.trim().length) {
        filteredComments.value = [...recentCommentStore.recentComments];
      } else {
        filteredComments.value = recentCommentStore.recentComments.filter(
          (comment) => {
            return comment.toLowerCase().startsWith(event.query.toLowerCase());
          },
        );
      }
    }, 250);
  };

  watch(recentCommentStore, () => {
    if (
      selected.value &&
      !recentCommentStore.recentComments.includes(selected.value)
    ) {
      selected.value = undefined;
    }
  });

  const itemSelect = (comment: string) => {
    if (
      selected.value &&
      recentCommentStore.recentComments.includes(selected.value)
    ) {
      emit("commentClicked", comment);
    }
    selected.value = undefined;
  };

  const removeComment = (comment: string) => {
    recentCommentStore.removeComment(comment);
    if (filteredComments.value) {
      filteredComments.value = filteredComments.value.filter(
        (c) => c != comment,
      );
    }
  };
</script>
