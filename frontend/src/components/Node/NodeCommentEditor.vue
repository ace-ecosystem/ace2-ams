<template>
  <div class="formgrid grid flex align-content-center">
    <div class="field col-fixed">
      <div class="p-listbox p-component">
        <div class="p-listbox-list-wrapper">
          <ul class="p-listbox-list">
            <li v-if="!comments.length" class="p-listbox-item">
              No comments found.
            </li>
            <li
              v-for="comment in comments"
              :key="comment.uuid"
              :class="[
                'p-listbox-item',
                { 'p-highlight': comment.uuid == editingCommentUuid },
              ]"
            >
              <span>
                <NodeComment :comment="comment" :include-time="true" />
                <Button
                  data-cy="edit-comment-button"
                  icon="pi pi-pencil"
                  class="p-button-rounded p-button-text pi-button-sm"
                  @click="openEditCommentPanel(comment)"
                />
              </span>
            </li>
          </ul>
        </div>
      </div>
    </div>
  </div>

  <div
    v-if="editCommentPanelOpen"
    data-cy="edit-comment-panel"
    class="formgrid grid flex align-content-center"
  >
    <div class="field col-fixed">
      <InputText
        v-model="editingCommentValue"
        data-cy="updated-comment-value"
      />
    </div>
    <div class="field col-fixed">
      <Button
        icon="pi pi-times"
        data-cy="close-edit-comment-panel"
        @click="closeEditCommentPanel"
      />
    </div>
    <div class="field col-fixed">
      <Button
        icon="pi pi-check"
        data-cy="save-comment-button"
        @click="saveModelComment"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
  import { defineProps, ref, defineEmits, PropType } from "vue";

  import Button from "primevue/button";
  import InputText from "primevue/inputtext";
  import NodeComment from "@/components/Node/NodeComment.vue";
  import { nodeCommentRead } from "@/models/nodeComment";

  const props = defineProps({
    modelValue: { type: Array as PropType<nodeCommentRead[]>, required: true },
  });

  const emit = defineEmits(["update:modelValue"]);

  const comments = ref<nodeCommentRead[]>(props.modelValue);
  const editingCommentValue = ref<string>();
  const editingCommentUuid = ref<string>();
  const editCommentPanelOpen = ref(false);

  const openEditCommentPanel = (comment: nodeCommentRead) => {
    editingCommentValue.value = comment.value;
    editingCommentUuid.value = comment.uuid;
    editCommentPanelOpen.value = true;
  };

  const closeEditCommentPanel = () => {
    editCommentPanelOpen.value = false;
    editingCommentValue.value = undefined;
    editingCommentUuid.value = undefined;
  };

  const saveModelComment = () => {
    const modelCommentIndex = comments.value.findIndex(
      (comment) => comment.uuid === editingCommentUuid.value,
    );
    if (modelCommentIndex != -1 && editingCommentValue.value) {
      comments.value[modelCommentIndex].value = editingCommentValue.value;
      emit("update:modelValue", comments.value);
      closeEditCommentPanel();
    }
  };
</script>
