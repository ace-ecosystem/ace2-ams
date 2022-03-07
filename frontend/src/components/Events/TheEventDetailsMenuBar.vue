<!-- EventDetailsMenuBar.vue -->
<!-- Menu bar containing various options for the event details page, ranging from actions such as commenting, tagging, closing, etc. -->
<!-- to controlling what section of event details is currently displayed -->

<template>
  <MegaMenu v-if="eventStore.open" :model="menuItems" />
  <CommentModal name="CommentModal" @request-reload="requestReload" />
  <AssignModal name="AssignModal" @request-reload="requestReload" />
  <TagModal
    name="TagModal"
    reload-object="node"
    @request-reload="requestReload"
  />
  <EditEventModal
    :name="`EditEventModal-${props.eventUuid}`"
    :event-uuid="props.eventUuid"
    @request-reload="requestReload"
  />
</template>

<script setup>
  import { ref, defineProps, computed, watch, defineEmits } from "vue";

  import MegaMenu from "primevue/megamenu";

  import { useAuthStore } from "@/stores/auth";
  import { useEventStore } from "@/stores/event";
  import { useModalStore } from "@/stores/modal";
  import { useSelectedEventStore } from "@/stores/selectedEvent";

  import AssignModal from "@/components/Modals/AssignModal.vue";
  import CommentModal from "@/components/Modals/CommentModal.vue";
  import EditEventModal from "@/components/Modals/EditEventModal.vue";
  import TagModal from "@/components/Modals/TagModal.vue";

  const authStore = useAuthStore();
  const eventStore = useEventStore();
  const modalStore = useModalStore();
  const selectedStore = useSelectedEventStore();

  const props = defineProps({
    eventUuid: { type: String, required: true },
  });

  const emit = defineEmits(["sectionClicked"]);

  const error = ref();

  const open = (name) => {
    modalStore.open(name);
  };

  const requestReload = () => {
    eventStore.requestReload = true;
  };

  async function takeOwnership() {
    try {
      const updateData = selectedStore.selected.map((uuid) => ({
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

  const analysisMenuItems = computed(() => {
    let analysisMenuItems = [];
    if (eventStore.open) {
      analysisMenuItems = eventStore.open.analysisTypes.map((analysisType) => ({
        label: analysisType,
        command: () => {
          emit("sectionClicked", analysisType);
        },
      }));
    }
    return {
      label: "Analysis",
      icon: "pi pi-fw pi-chart-bar",
      items: [
        [
          {
            label: "Analysis Details",
            items: analysisMenuItems,
          },
        ],
      ],
    };
  });

  const defaultItems = ref([
    {
      label: "Actions",
      icon: "pi pi-fw pi-cog",
      items: [
        [
          {
            label: "Edit",
            items: [
              {
                label: "Comment",
                command: () => {
                  open("CommentModal");
                },
              },
              {
                label: "Take Ownership",
                command: () => {
                  takeOwnership();
                },
              },
              {
                label: "Assign",
                command: () => {
                  open("AssignModal");
                },
              },
              {
                label: "Add Tags",
                command: () => {
                  open("TagModal");
                },
              },
              {
                label: "Edit Event",
                command: () => {
                  open(`EditEventModal-${props.eventUuid}`);
                },
              },
            ],
          },
        ],
        [
          {
            label: "Management",
            items: [
              { label: "Close Event" },
              { label: "TIP Actions", disabled: true },
            ],
          },
        ],
      ],
    },
    {
      label: "Information",
      icon: "pi pi-fw pi-info-circle",
      items: [
        [
          {
            label: "Event Details",
            items: [
              {
                label: "Event Summary",
                command: () => {
                  emit("sectionClicked", "Event Summary");
                },
              },
              {
                label: "Alert Summary",
                command: () => {
                  emit("sectionClicked", "Alert Summary");
                },
              },
              {
                label: "Detection Summary",
                command: () => {
                  emit("sectionClicked", "Detection Summary");
                },
                disabled: true,
              },
              {
                label: "URL Summary",
                command: () => {
                  emit("sectionClicked", "URL Summary");
                },
              },
              {
                label: "Observable Summary",
                command: () => {
                  emit("sectionClicked", "Observable Summary");
                },
              },
            ],
          },
        ],
      ],
    },
  ]);

  const menuItems = ref([...defaultItems.value, analysisMenuItems.value]);
  // For whatever reason, PrimeVue menu objects will not auto-reload using a computed value
  // So we have to manually update menuItems using a watcher instead
  watch(eventStore, () => {
    menuItems.value = [...defaultItems.value, analysisMenuItems.value];
  });
</script>
