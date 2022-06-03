<!-- EventDetailsMenuBar.vue -->
<!-- Menu bar containing various options for the event details page, ranging from actions such as commenting, tagging, closing, etc. -->
<!-- to controlling what section of event details is currently displayed -->

<template>
  <MegaMenu
    v-if="eventStore.open"
    :model="menuItems"
    data-cy="event-details-menu"
  />
  <CommentModal name="CommentModal" @request-reload="requestReload" />
  <AssignModal name="AssignModal" @request-reload="requestReload" />
  <TagModal
    name="TagModal"
    reload-object="node"
    node-type="events"
    @request-reload="requestReload"
  />
  <EditEventModal
    :name="`EditEventModal-${props.eventUuid}`"
    :event-uuid="props.eventUuid"
    @request-reload="requestReload"
  />
</template>

<script setup lang="ts">
  import { ref, defineProps, computed, watch, defineEmits, inject } from "vue";

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

  const analysisModuleComponents = inject("analysisModuleComponents") as Record<
    string,
    unknown
  >;

  const props = defineProps({
    eventUuid: { type: String, required: true },
  });

  const emit = defineEmits(["sectionClicked"]);

  const error = ref<string>();

  const open = (name: string) => {
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
        historyUsername: authStore.user.username,
      }));

      await eventStore.update(updateData);
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

  const formatAnalysisType = (analysisType: string) => {
    return analysisType.split(" - ")[0];
  };

  interface menuItem {
    label: string;
    command: () => void;
    disabled?: boolean;
  }

  const analysisMenuItems = computed(() => {
    let analysisMenuItems: menuItem[] = [];
    let processed: string[] = [];
    if (eventStore.open) {
      analysisMenuItems = eventStore.open.analysisTypes
        .filter((analysisType) => {
          let analysisTypeFormatted = formatAnalysisType(analysisType);
          if (
            analysisTypeFormatted in analysisModuleComponents && // Filter out analysis modules that don't have configured components
            !processed.includes(analysisTypeFormatted) //  OR that have already been added to the list
          ) {
            processed.push(analysisTypeFormatted);
            return true;
          }
        })
        .map((analysisType) => {
          let analysisTypeFormatted = formatAnalysisType(analysisType);
          return {
            label: analysisTypeFormatted,
            command: () => {
              emit("sectionClicked", analysisTypeFormatted);
            },
          };
        });
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
              },
              {
                label: "URL Summary",
                command: () => {
                  emit("sectionClicked", "URL Summary");
                },
              },
              {
                label: "URL Domain Summary",
                command: () => {
                  emit("sectionClicked", "URL Domain Summary");
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
