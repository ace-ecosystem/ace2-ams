<!-- AlertActionToolbar.vue -->
<!-- Toolbar containing all alert-related actions, such as Disposition, Assign, Comment, etc. -->

<template>
  <div>
    <div v-if="error" class="p-col">
      <Message severity="error" @close="handleError">{{ error }}</Message>
    </div>
  </div>
  <Toolbar id="AlertActionToolbar" style="overflow-x: auto">
    <template #start>
      <!--      DISPOSITION -->
      <Button
        class="p-m-1 p-button-normal p-button-success"
        icon="pi pi-thumbs-up"
        label="Disposition"
        @click="open('DispositionModal')"
      />
      <DispositionModal
        name="DispositionModal"
        @requestReload="requestReload"
      />
      <!--      COMMENT -->
      <Button
        class="p-m-1 p-button-sm"
        icon="pi pi-comment"
        label="Comment"
        @click="open('CommentModal')"
      />
      <CommentModal name="CommentModal" @requestReload="requestReload" />
      <!--      TAKE OWNERSHIP -- NO MODAL -->
      <Button
        class="p-m-1 p-button-sm"
        icon="pi pi-briefcase"
        label="Take Ownership"
        :disabled="!selectedAlertStore.anySelected"
        @click="takeOwnership"
      />
      <!--      ASSIGN -->
      <Button
        class="p-m-1 p-button-sm"
        icon="pi pi-user"
        label="Assign"
        @click="open('AssignModal')"
      />
      <AssignModal name="AssignModal" @requestReload="requestReload" />
      <!--      TAG MODAL -->
      <Button
        class="p-m-1 p-button-sm"
        icon="pi pi-tags"
        label="Tag"
        @click="open('TagModal')"
        @requestReload="requestReload"
      />
      <TagModal name="TagModal" @requestReload="requestReload" />
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
  </Toolbar>
</template>

<script setup>
  import { ref, defineProps } from "vue";

  import Button from "primevue/button";
  import Message from "primevue/message";
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

  const props = defineProps({
    page: { type: String, required: true },
  });

  const error = ref(null);

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
      error.value = err.message;
    }
    if (!error.value) {
      requestReload();
    }
  }

  function requestReload() {
    if (props.page == "Manage Alerts") {
      alertTableStore.requestReload = true;
    } else if (props.page == "View Alert") {
      alertStore.requestReload = true;
    }
  }

  const handleError = () => {
    error.value = null;
  };
</script>
