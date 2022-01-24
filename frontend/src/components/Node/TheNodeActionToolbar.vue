<!-- NodeActionToolbar.vue -->
<!-- Toolbar containing all alert-related actions, such as Disposition, Assign, Comment, etc. -->

<template>
  <div>
    <div v-if="error" class="p-col">
      <Message severity="error" @close="handleError">{{ error }}</Message>
    </div>
  </div>
  <Toolbar id="ActionToolbar" style="overflow-x: auto">
    <template #start>
      <slot name="start"></slot>
      <!--      COMMENT -->
      <div v-if="props.comment">
        <Button
          class="p-m-1 p-button-sm"
          icon="pi pi-comment"
          label="Comment"
          @click="open('CommentModal')"
        />
        <CommentModal name="CommentModal" @requestReload="requestReload" />
      </div>
      <!--      TAKE OWNERSHIP -- NO MODAL -->
      <div v-if="props.takeOwnership">
        <Button
          class="p-m-1 p-button-sm"
          icon="pi pi-briefcase"
          label="Take Ownership"
          :disabled="!selectedStore.anySelected"
          @click="takeOwnership"
        />
      </div>
      <!--      ASSIGN -->
      <div v-if="props.assign">
        <Button
          class="p-m-1 p-button-sm"
          icon="pi pi-user"
          label="Assign"
          @click="open('AssignModal')"
        />
        <AssignModal name="AssignModal" @requestReload="requestReload" />
      </div>
      <!--      TAG MODAL -->
      <div v-if="props.tag">
        <Button
          class="p-m-1 p-button-sm"
          icon="pi pi-tags"
          label="Tag"
          @click="open('TagModal')"
          @requestReload="requestReload"
        />
        <TagModal name="TagModal" @requestReload="requestReload" />
      </div>
    </template>
    <template #end>
      <slot name="end"></slot>
    </template>
  </Toolbar>
</template>

<script setup>
  import { ref, defineProps, defineExpose, inject } from "vue";

  import Button from "primevue/button";
  import Message from "primevue/message";
  import Toolbar from "primevue/toolbar";

  import AssignModal from "@/components/Modals/AssignModal";
  import CommentModal from "@/components/Modals/CommentModal";
  import TagModal from "@/components/Modals/TagModal";

  import {
    nodeStores,
    nodeSelectedStores,
    nodeTableStores,
  } from "@/stores/index";
  import { useAuthStore } from "@/stores/auth";
  import { useModalStore } from "@/stores/modal";

  const props = defineProps({
    reloadObject: { type: String, required: true },
    assign: { type: Boolean, default: true },
    comment: { type: Boolean, default: true },
    tag: { type: Boolean, default: true },
    takeOwnership: { type: Boolean, default: true },
  });

  const nodeType = inject("nodeType");

  const nodeStore = nodeStores[nodeType]();
  const tableStore = nodeTableStores[nodeType]();
  const selectedStore = nodeSelectedStores[nodeType]();
  const authStore = useAuthStore();
  const modalStore = useModalStore();

  const error = ref(null);

  const open = (name) => {
    modalStore.open(name);
  };

  async function takeOwnership() {
    try {
      const updateData = selectedStore.selected.map((uuid) => ({
        uuid: uuid,
        owner: authStore.user.username,
      }));

      await nodeStore.update(updateData);
    } catch (err) {
      error.value = err.message;
    }
    if (!error.value) {
      requestReload();
    }
  }

  const requestReload = () => {
    if (props.reloadObject == "table") {
      tableStore.requestReload = true;
    } else if (props.reloadObject == "node") {
      nodeStore.requestReload = true;
    }
  };

  const handleError = () => {
    error.value = null;
  };

  defineExpose({
    requestReload,
  });
</script>
