<!-- AlertActionToolbar.vue -->
<!-- Toolbar containing all alert-related actions, such as Disposition, Assign, Comment, etc. -->

<template>
  <Toolbar style="overflow-x: auto">
    <template #left>
      <!--      DISPOSITION -->
      <Button
        class="p-m-1 p-button-normal p-button-success"
        icon="pi pi-thumbs-up"
        label="Disposition"
        @click="open('DispositionModal')"
      />
      <DispositionModal name="DispositionModal" />
      <!--      COMMENT -->
      <Button
        class="p-m-1 p-button-sm"
        icon="pi pi-comment"
        label="Comment"
        @click="open('CommentModal')"
      />
      <CommentModal name="CommentModal" />
      <!--      TAKE OWNERSHIP -- NO MODAL -->
      <Button
        class="p-m-1 p-button-sm"
        icon="pi pi-briefcase"
        label="Take Ownership"
      />
      <!--      ASSIGN -->
      <Button
        class="p-m-1 p-button-sm"
        icon="pi pi-user"
        label="Assign"
        @click="open('AssignModal')"
      />
      <AssignModal name="AssignModal" />
      <!--      TAG MODAL -->
      <Button
        class="p-m-1 p-button-sm"
        icon="pi pi-tags"
        label="Tag"
        @click="open('TagModal')"
      />
      <TagModal />
      <!--      REMEDIATE MODAL -->
      <Button
        class="p-m-1 p-button-sm"
        icon="pi pi-times-circle"
        label="Remediate"
        @click="open('RemediationModal')"
      />
      <RemediationModal />
      <!--      DELETE ALERT -->
      <Button
        class="p-m-1 p-button-sm p-button-danger"
        icon="pi pi-trash"
        label="Delete"
        @click="open('DeleteModal')"
      />
      <DeleteModal name="DeleteModal" />
    </template>
    <template #right>
      <Button icon="pi pi-link" class="p-button-rounded" label="Link" />
    </template>
  </Toolbar>
</template>

<script setup>
  import Button from "primevue/button";
  import Toolbar from "primevue/toolbar";

  import AssignModal from "@/components/Modals/AssignModal";
  import CommentModal from "@/components/Modals/CommentModal";
  import TagModal from "@/components/Modals/TagModal";
  import RemediationModal from "@/components/Modals/RemediateModal";
  import DeleteModal from "@/components/Modals/DeleteModal";
  import DispositionModal from "@/components/Modals/DispositionModal";

  import { useModalStore } from "@/stores/modal";

  const store = useModalStore();

  const open = (name) => {
    store.open(name);
  };
</script>
