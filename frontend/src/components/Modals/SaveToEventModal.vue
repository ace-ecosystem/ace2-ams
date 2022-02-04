<!-- SaveToEvent.vue -->
<!-- 'Save to Event' alert action modal, will close the Disposition Modal that opened it -->

<template>
  <BaseModal :name="name" header="Save to Event" :style="{ width: '75vw' }">
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
                  :auto-resize="true"
                  rows="5"
                  cols="30"
                />
                <label for="newEventComment">Disposition Comment</label>
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
            option-label="name"
            filter-placeholder="Search"
            list-style="height: 55vh"
          />
        </TabPanel>
      </TabView>
    </div>
    <template #footer>
      <Button
        label="Back"
        icon="pi pi-arrow-left"
        class="p-button-text"
        @click="close"
      />
      <Button
        label="Save"
        icon="pi pi-check"
        :disabled="!allowEventSelectionSubmit"
        @click="saveToEvent"
      />
    </template>
  </BaseModal>
</template>

<script setup>
  import { computed, defineEmits, defineProps, ref, watch } from "vue";

  import Button from "primevue/button";
  import InputText from "primevue/inputtext";
  import Listbox from "primevue/listbox";
  import TabPanel from "primevue/tabpanel";
  import TabView from "primevue/tabview";
  import Textarea from "primevue/textarea";

  import BaseModal from "@/components/Modals/BaseModal";

  import { Event } from "@/services/api/event";
  import { NodeComment } from "@/services/api/nodeComment";
  import { parseEventSummary } from "@/stores/eventTable";

  import { useAlertStore } from "@/stores/alert";
  import { useAuthStore } from "@/stores/auth";
  import { useEventStatusStore } from "@/stores/eventStatus";
  import { useModalStore } from "@/stores/modal";
  import { useSelectedAlertStore } from "@/stores/selectedAlert";

  const alertStore = useAlertStore();
  const authStore = useAuthStore();
  const eventStatusStore = useEventStatusStore();
  const modalStore = useModalStore();
  const selectedAlertStore = useSelectedAlertStore();

  const props = defineProps({
    name: { type: String, required: true },
  });

  const emit = defineEmits(["saveToEvent"]);

  const eventStatusOptions = ["OPEN", "CLOSED"];

  const availableEventStatusOptions = ref([]);
  const events = ref({});
  const isLoading = ref(false);
  const newEventComment = ref(null);
  const newEventName = ref("");
  const selectedEventStatusOption = ref(1);
  const selectedExistingEvent = ref(null);

  const loadEvents = async () => {
    isLoading.value = true;

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

    // Fetch and store all events for each configured status
    for (const status of availableEventStatusOptions.value) {
      events.value[status.value] = await getEventsWithStatus(status);
    }

    isLoading.value = false;
  };

  const getEventsWithStatus = async (status) => {
    const allEvents = await Event.readAllPages({
      status: status,
      sort: "created_time|asc",
    });

    return allEvents.map((x) => parseEventSummary(x));
  };

  // Load available events when modal becomes active
  watch(modalStore, () => {
    if (modalStore.active === props.name) {
      loadEvents();
    }
  });

  const saveToEvent = async () => {
    let eventUuid = null;

    // If the event doesn't exist, create it
    if (newEventSelected.value) {
      const newEvent = await Event.create(
        {
          name: newEventName.value,
          queue: authStore.user.defaultEventQueue.value,
          owner: authStore.user.username,
          status: "OPEN",
        },
        true,
      );
      eventUuid = newEvent.uuid;
    } else {
      eventUuid = selectedExistingEvent.value.uuid;
    }

    // Update alert(s) eventUuid
    await alertStore.update(
      selectedAlertStore.selected.map((uuid) => ({
        uuid: uuid,
        eventUuid: eventUuid,
      })),
    );

    // Add any comments if necessary
    if (commentData.value) {
      try {
        await NodeComment.create(
          selectedAlertStore.selected.map((uuid) => ({
            nodeUuid: uuid,
            ...commentData.value,
          })),
        );
      } catch (err) {
        if ("409" in err) {
          console.warning("Comment already exists!");
        }
      }
    }

    close();
    // This will close the disposition modal
    emit("saveToEvent");
  };

  const allowEventSelectionSubmit = computed(() => {
    return (
      // Alerts must be selected AND
      useSelectedAlertStore.anySelected &&
      // Existing alert must be selected OR
      (Boolean(selectedExistingEvent.value) ||
        // New Event option must be selected AND
        (Boolean(newEventSelected.value) &&
          // a name for the new event has been given
          newEventName.value &&
          newEventName.value.length))
    );
  });

  const commentData = computed(() => {
    if (!newEventComment.value) {
      return null;
    }
    return {
      user: authStore.user ? authStore.user.username : null,
      value: newEventComment.value,
    };
  });

  const newEventSelected = computed(() => {
    return selectedEventStatusOption.value === 0;
  });

  const close = () => {
    selectedExistingEvent.value = null;
    events.value = [
      { title: "Open", events: ["event1", "event2"] },
      { title: "Closed", events: ["event3", "event4"] },
    ];
    newEventComment.value = null;
    newEventName.value = null;
    modalStore.close(props.name);
  };
</script>
