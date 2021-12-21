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
        @click="takeOwnership"
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
      <TagModal name="TagModal" />
      <!--      REMEDIATE MODAL -->
      <Button
        class="p-m-1 p-button-sm"
        icon="pi pi-times-circle"
        label="Remediate"
        disabled
        @click="open('RemediationModal')"
      />
      <RemediationModal />
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
  import DispositionModal from "@/components/Modals/DispositionModal";

  import { useAlertTableStore } from "@/stores/alertTable";
  const alertTableStore = useAlertTableStore();

  import { useAuthStore } from "@/stores/auth";
  const authStore = useAuthStore();

  import { useModalStore } from "@/stores/modal";
  import { useAlertStore } from "@/stores/alert";
  import { useSelectedAlertStore } from "@/stores/selectedAlert";

  const alertStore = useAlertStore();
  const selectedAlertStore = useSelectedAlertStore();

  const store = useModalStore();

  const open = (name) => {
    store.open(name);
  };

  async function takeOwnership() {
    for (const uuid of selectedAlertStore.selected) {
      await alertStore.update(uuid, {
        owner: authStore.user.username,
      });
            alertTableStore.requestReload = true;

    }
  }
</script>
