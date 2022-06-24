<!-- SaveToEvent.vue -->
<!-- 'Save to Event' alert action modal, will close the Disposition Modal that opened it -->

<template>
  <BaseModal
    data-cy="save-to-event-modal"
    :name="name"
    header="Save to Event"
    :style="{ width: '75vw' }"
    @dialog-close="close"
  >
    <div>
      <div v-if="error" data-cy="save-to-event-error" class="p-col">
        <Message severity="error" @close="handleError">{{ error }}</Message>
      </div>
    </div>
    <div v-if="isLoading" style="height: 75vh">
      Loading events, hold on a sec...
    </div>
    <div v-else style="height: 70vh">
      <TabView v-model:activeIndex="selectedEventStatusOption" class="p-m-1">
        <TabPanel key="newEvent" header="NEW">
          <div class="p-m-1 p-grid p-fluid p-formgrid">
            <div class="p-field p-col p-m-1">
              <br />
              <span class="p-float-label">
                <InputText
                  id="newEventName"
                  v-model="newEventName"
                  data-cy="new-event-name"
                  name="newEventName"
                  type="text"
                />
                <label for="newEventName">Event Name</label>
              </span>
              <br />
              <br />
              <span class="p-float-label">
                <Textarea
                  id="newEventComment"
                  v-model="newEventComment"
                  data-cy="new-event-comment"
                  :auto-resize="true"
                  rows="5"
                  cols="30"
                />
                <label for="newEventComment">Event Comment</label>
                <CommentAutocomplete
                  @comment-clicked="recentCommentClicked($event)"
                ></CommentAutocomplete>
              </span>
            </div>
          </div>
        </TabPanel>
        <TabPanel
          v-for="eventType of availableEventStatusOptions"
          :key="eventType.uuid"
          :header="eventType.value"
        >
          <Listbox
            v-if="!newEventSelected"
            v-model="selectedExistingEvent"
            :options="events[eventType.value]"
            :filter="true"
            data-cy="event-options"
            option-label="name"
            filter-placeholder="Search"
            list-style="height: 55vh"
          />
        </TabPanel>
      </TabView>
    </div>
    <template #footer>
      <Button
        data-cy="save-to-event-back-button"
        label="Back"
        icon="pi pi-arrow-left"
        class="p-button-text"
        @click="close"
      />
      <Button
        data-cy="save-to-event-submit-button"
        label="Save"
        icon="pi pi-check"
        :disabled="!allowEventSelectionSubmit"
        @click="saveToEvent"
      />
    </template>
  </BaseModal>
</template>

<script setup lang="ts">
  import { computed, defineEmits, defineProps, ref, watch } from "vue";

  import Button from "primevue/button";
  import InputText from "primevue/inputtext";
  import Listbox from "primevue/listbox";
  import Message from "primevue/message";
  import TabPanel from "primevue/tabpanel";
  import TabView from "primevue/tabview";
  import Textarea from "primevue/textarea";

  import BaseModal from "@/components/Modals/BaseModal.vue";
  import CommentAutocomplete from "@/components/Comments/CommentAutocomplete.vue";

  import { Event } from "@/services/api/event";
  import { EventComment } from "@/services/api/eventComment";
  import { parseEventSummary } from "@/stores/eventTable";

  import { useAlertStore } from "@/stores/alert";
  import { useAuthStore } from "@/stores/auth";
  import { useEventStatusStore } from "@/stores/eventStatus";
  import { useModalStore } from "@/stores/modal";
  import { useSelectedAlertStore } from "@/stores/selectedAlert";
  import { useRecentCommentsStore } from "@/stores/recentComments";

  import { eventRead, eventSummary } from "@/models/event";
  import { eventStatusRead } from "@/models/eventStatus";

  const alertStore = useAlertStore();
  const authStore = useAuthStore();
  const eventStatusStore = useEventStatusStore();
  const modalStore = useModalStore();
  const selectedAlertStore = useSelectedAlertStore();
  const recentCommentsStore = useRecentCommentsStore();

  const props = defineProps({
    name: { type: String, required: true },
  });

  const emit = defineEmits(["saveToEvent"]);

  // TODO, may want to make this configurable in the constants file
  const eventStatusOptions = ["OPEN", "CLOSED"];

  const availableEventStatusOptions = ref<eventStatusRead[]>([]);
  const error = ref<string>();
  const events = ref<Record<string, eventSummary[]>>({});
  const isLoading = ref(false);
  const newEventComment = ref<string>();
  const newEventName = ref<string>();
  const selectedEventStatusOption = ref(1);
  const selectedExistingEvent = ref<eventSummary>();

  const getAvailableEventStatusOptions = () => {
    // Fetch all known event status objects that are configured in eventStatusOptions
    availableEventStatusOptions.value = eventStatusStore.allItems.filter(
      (status) => eventStatusOptions.includes(status.value),
    );

    // Resort our filtered list to match the order of eventStatusOptions
    availableEventStatusOptions.value.sort(function (a, b) {
      return (
        eventStatusOptions.indexOf(a.value) -
        eventStatusOptions.indexOf(b.value)
      );
    });
  };

  const loadEvents = async () => {
    isLoading.value = true;

    getAvailableEventStatusOptions();

    try {
      // Fetch and store all events for each configured status
      for (const status of availableEventStatusOptions.value) {
        events.value[status.value] = await getEventsWithStatus(status);
      }
    } catch (e: unknown) {
      if (typeof e === "string") {
        error.value = e;
      } else if (e instanceof Error) {
        error.value = e.message;
      }
    }

    isLoading.value = false;
  };

  const getEventsWithStatus = async (status: eventStatusRead) => {
    const allEvents = await Event.readAllPages({
      status: [status],
      sort: "created_time|asc",
    });

    return allEvents.map((x) => parseEventSummary(x));
  };

  // Load available events when modal becomes active
  watch(modalStore, async () => {
    if (modalStore.active === props.name) {
      await loadEvents();
    }
  });

  const saveToEvent = async () => {
    let eventUuid: string;

    // If the event doesn't exist, create it
    if (newEventSelected.value) {
      try {
        const newEvent = (await Event.create(
          {
            historyUsername: authStore.user.username,
            name: newEventName.value!,
            queue: authStore.user.defaultEventQueue.value,
            owner: authStore.user.username,
            status: "OPEN",
          },
          true,
        )) as eventRead;
        eventUuid = newEvent.uuid;
      } catch (e: unknown) {
        if (typeof e === "string") {
          error.value = e;
        } else if (e instanceof Error) {
          error.value = e.message;
        }
        return;
      }

      // Add any comments if necessary
      if (commentData.value) {
        const newCommentData = [
          {
            username: authStore.user.username,
            eventUuid: eventUuid,
            ...commentData.value,
          },
        ];

        try {
          await EventComment.create(newCommentData);
        } catch (e: unknown) {
          if (typeof e === "string") {
            if (e.includes("409")) {
              console.warn("Comment already exists!");
            } else {
              error.value = e;
              return;
            }
          } else if (e instanceof Error) {
            if (e.message.includes("409")) {
              console.warn("Comment already exists!");
            } else {
              error.value = e.message;
              return;
            }
          }
        }
        if (newEventComment.value) {
          recentCommentsStore.addComment(newEventComment.value);
        }
      }
    } else {
      eventUuid = selectedExistingEvent.value!.uuid;
    }

    // Update alert(s) eventUuid
    const updateData = selectedAlertStore.selected.map((uuid) => ({
      uuid: uuid,
      eventUuid: eventUuid,
      historyUsername: authStore.user.username,
    }));
    try {
      await alertStore.update(updateData);
    } catch (e: unknown) {
      if (typeof e === "string") {
        error.value = e;
      } else if (e instanceof Error) {
        error.value = e.message;
      }
      return;
    }
    close();
    // This will close the disposition modal
    emit("saveToEvent");
  };

  const allowEventSelectionSubmit = computed(() => {
    return (
      // Alerts must be selected AND
      selectedAlertStore.anySelected &&
      // Existing alert must be selected AND
      ((selectedExistingEvent.value &&
        //  NOT newEventSelected OR
        !newEventSelected.value) ||
        // New Event option must be selected AND

        (newEventSelected.value &&
          // a name for the new event has been given
          Boolean(newEventName.value?.length)))
    );
  });

  const commentData = computed(() => {
    if (!newEventComment.value) {
      return null;
    }
    return {
      user: authStore.user.username,
      value: newEventComment.value,
    };
  });

  const newEventSelected = computed(() => {
    return selectedEventStatusOption.value === 0;
  });

  const recentCommentClicked = (comment: string) => {
    newEventComment.value = comment;
  };

  const handleError = () => {
    error.value = undefined;
  };

  const close = () => {
    selectedEventStatusOption.value = 1;
    selectedExistingEvent.value = undefined;
    newEventComment.value = undefined;
    newEventName.value = "";
    error.value = undefined;
    modalStore.close(props.name);
  };
</script>
