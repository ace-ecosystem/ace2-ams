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
    class="formgrid grid flex align-content-center"
  >
    <div class="field col-fixed">
      <InputText v-model="editingCommentValue"></InputText>
    </div>
    <div class="field col-fixed">
      <Button icon="pi pi-times" @click="closeEditCommentPanel" />
    </div>
    <div class="field col-fixed">
      <Button icon="pi pi-check" @click="saveModelComment" />
    </div>
  </div>
</template>

<script setup>
  import { defineProps, ref, defineEmits } from "vue";

  import Button from "primevue/button";
  import InputText from "primevue/inputtext";
  import NodeComment from "../Node/NodeComment.vue";

  const props = defineProps({
    modelValue: { type: Array, required: true },
  });

  const emit = defineEmits(["update:modelValue"]);

  const comments = ref(props.modelValue);
  const editingCommentValue = ref(null);
  const editingCommentUuid = ref(null);
  const editCommentPanelOpen = ref(false);

  const openEditCommentPanel = (comment) => {
    editingCommentValue.value = comment.value;
    editingCommentUuid.value = comment.uuid;
    editCommentPanelOpen.value = true;
  };

  const closeEditCommentPanel = () => {
    editCommentPanelOpen.value = false;
    editingCommentValue.value = null;
    editingCommentUuid.value = null;
  };

  const saveModelComment = () => {
    const modelCommentIndex = comments.value.findIndex(
      (comment) => comment.uuid === editingCommentUuid.value,
    );
    comments.value[modelCommentIndex].value = editingCommentValue.value;
    emit("update:modelValue", comments.value);
    closeEditCommentPanel();
  };
</script>
