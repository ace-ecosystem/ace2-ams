<!-- Toolbar containing all event-related actions, such as Assign, Comment, etc. -->

<template>
  <div>
    <div v-if="error" class="p-col">
      <Message severity="error" @close="handleError">{{ error }}</Message>
    </div>
  </div>
  <Toolbar id="EventActionToolbar" style="overflow-x: auto">
    <template #start>
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
        :disabled="!selectedEventStore.anySelected"
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

  import { useEventStore } from "@/stores/event";
  import { useEventTableStore } from "@/stores/eventTable";
  import { useAuthStore } from "@/stores/auth";
  import { useModalStore } from "@/stores/modal";
  import { useSelectedEventStore } from "@/stores/selectedEvent";

  const eventStore = useEventStore();
  const eventTableStore = useEventTableStore();
  const authStore = useAuthStore();
  const modalStore = useModalStore();
  const selectedEventStore = useSelectedEventStore();

  const props = defineProps({
    page: { type: String, required: true },
  });

  const error = ref(null);

  const open = (name) => {
    modalStore.open(name);
  };

  async function takeOwnership() {
    try {
      const updateData = selectedEventStore.selected.map((uuid) => ({
        uuid: uuid,
        owner: authStore.user.username,
      }));

      await eventStore.update(updateData);
    } catch (err) {
      error.value = err.message;
    }
    if (!error.value) {
      requestReload();
    }
  }

  function requestReload() {
    if (props.page == "Manage Events") {
      eventTableStore.requestReload = true;
    } else if (props.page == "View Event") {
      eventStore.requestReload = true;
    }
  }

  const handleError = () => {
    error.value = null;
  };
</script>
