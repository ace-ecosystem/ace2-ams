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

  import { useAlertStore } from "@/stores/alert";
  import { useAlertTableStore } from "@/stores/alertTable";
  import { useAuthStore } from "@/stores/auth";
  import { useModalStore } from "@/stores/modal";
  import { useSelectedAlertStore } from "@/stores/selectedAlert";

  const alertStore = useAlertStore();
  const alertTableStore = useAlertTableStore();
  const authStore = useAuthStore();
  const modalStore = useModalStore();
  const selectedAlertStore = useSelectedAlertStore();

  const open = (name) => {
    modalStore.open(name);
  };

  async function takeOwnership() {
    try {
      for (const uuid of selectedAlertStore.selected) {
        await alertStore.update(uuid, {
          owner: authStore.user.username,
        });
      }
    } catch (err) {
      console.log(err);
    }

    alertTableStore.requestReload = true;
  }
</script>
