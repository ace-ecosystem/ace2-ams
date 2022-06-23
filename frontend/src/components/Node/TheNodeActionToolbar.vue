<!-- NodeActionToolbar.vue -->
<!-- Toolbar containing node actions, such as Assign, Comment, Tag, etc. -->

<template>
  <div>
    <div v-if="error" class="p-col">
      <Message severity="error" @close="handleError">{{ error }}</Message>
    </div>
  </div>
  <Toolbar id="ActionToolbar">
    <template #start>
      <slot name="start-left"></slot>
      <!--      TAKE OWNERSHIP -- NO MODAL -->
      <div v-if="props.takeOwnership">
        <Button
          data-cy="take-ownership-button"
          :class="takeOwnershipClasses"
          style="width: 180px"
          icon="pi pi-briefcase"
          :label="takeOwnershipText"
          :disabled="!selectedStore.anySelected"
          @click="takeOwnership"
        />
      </div>
      <!--      COMMENT -->
      <div v-if="props.comment">
        <Button
          data-cy="comment-button"
          class="p-m-1 p-button-sm p-button-secondary p-button-outlined"
          icon="pi pi-comment"
          label="Comment"
          @click="open('CommentModal')"
        />
        <CommentModal name="CommentModal" @request-reload="requestReload" />
      </div>
      <!--      ASSIGN -->
      <div v-if="props.assign">
        <Button
          data-cy="assign-button"
          class="p-m-1 p-button-sm p-button-secondary p-button-outlined"
          icon="pi pi-user"
          label="Assign"
          @click="open('AssignModal')"
        />
        <AssignModal name="AssignModal" @request-reload="requestReload" />
      </div>
      <!--      TAG MODAL -->
      <div v-if="props.tag">
        <Button
          data-cy="tag-button"
          class="p-m-1 p-button-sm p-button-secondary p-button-outlined"
          icon="pi pi-tags"
          label="Tag"
          @click="open('TagModal')"
          @request-reload="requestReload"
        />
        <TagModal
          name="TagModal"
          :node-type="objectType"
          :reload-object="props.reloadObject"
          @request-reload="requestReload"
        />
      </div>
      <!--      REMOVE TAG MODAL -->
      <div v-if="props.removeTag">
        <Button
          data-cy="remove-tag-button"
          class="p-m-1 p-button-sm p-button-secondary p-button-outlined"
          style="width: 142px"
          icon="pi pi-tags"
          label="Remove Tag(s)"
          @click="open('RemoveTagModal')"
          @request-reload="requestReload"
        />
        <RemoveTagModal
          name="RemoveTagModal"
          :node-type="objectType"
          :reload-object="props.reloadObject"
          @request-reload="requestReload"
        />
      </div>
      <slot name="start-right"></slot>
    </template>
    <template #end>
      <slot name="end"></slot>
    </template>
  </Toolbar>
</template>

<script setup lang="ts">
  import {
    ref,
    computed,
    defineProps,
    defineExpose,
    inject,
    PropType,
  } from "vue";

  import Button from "primevue/button";
  import Message from "primevue/message";
  import Toolbar from "primevue/toolbar";

  import AssignModal from "@/components/Modals/AssignModal.vue";
  import CommentModal from "@/components/Modals/CommentModal.vue";
  import TagModal from "@/components/Modals/TagModal.vue";
  import RemoveTagModal from "@/components/Modals/RemoveTagModal.vue";

  import {
    nodeStores,
    nodeSelectedStores,
    nodeTableStores,
  } from "@/stores/index";
  import { useAuthStore } from "@/stores/auth";
  import { useModalStore } from "@/stores/modal";

  const props = defineProps({
    reloadObject: {
      type: String as PropType<"node" | "table">,
      required: true,
    },
    assign: { type: Boolean, default: true },
    comment: { type: Boolean, default: true },
    tag: { type: Boolean, default: true },
    removeTag: { type: Boolean, default: true },
    takeOwnership: { type: Boolean, default: true },
  });

  const objectType = inject("objectType") as "alerts" | "events";

  const nodeStore = nodeStores[objectType]();
  const tableStore = nodeTableStores[objectType]();
  const selectedStore = nodeSelectedStores[objectType]();
  const authStore = useAuthStore();
  const modalStore = useModalStore();

  const error = ref<string>();

  const open = (name: string) => {
    modalStore.open(name);
  };

  async function takeOwnership() {
    try {
      const updateData = selectedStore.selected.map((uuid) => ({
        uuid: uuid,
        owner: authStore.user.username,
        historyUsername: authStore.user.username,
      }));

      await nodeStore.update(updateData);
    } catch (e: unknown) {
      if (typeof e === "string") {
        error.value = e;
      } else if (e instanceof Error) {
        error.value = e.message;
      }
    }
    if (!error.value) {
      requestReload();
    }
  }

  const ownedByCurrentUser = computed(() => {
    if (props.reloadObject == "node" && nodeStore.open) {
      if ("owner" in nodeStore.open) {
        const authStore = useAuthStore();
        return nodeStore.open.owner?.uuid == authStore.user.uuid;
      }
    }
    return false;
  });

  const takeOwnershipText = computed(() => {
    return ownedByCurrentUser.value ? "Assigned to you!" : "Take Ownership";
  });

  const takeOwnershipClasses = computed(() => {
    return ownedByCurrentUser.value
      ? ["p-m-1", "p-button-sm", "p-button-secondary", "p-button-outlined"]
      : ["p-m-1", "p-button-normal", "p-button-secondary"];
  });

  const requestReload = () => {
    if (props.reloadObject == "table") {
      tableStore.requestReload = true;
    } else if (props.reloadObject == "node") {
      nodeStore.requestReload = true;
    }
  };

  const handleError = () => {
    error.value = undefined;
  };

  defineExpose({
    requestReload,
  });
</script>
