<!-- EventTableCell.vue -->
<!-- Contains logic and functionality to display field-specific data in TheEventTable -->

<template>
  <!-- Event Name -->
  <div v-if="props.field === 'name'">
    <span class="p-m-1" data-cy="eventName">
      <router-link :to="getEventLink(props.data.uuid)">{{
        props.data.name
      }}</router-link></span
    >
    <!-- Event Tags -->
    <span v-if="props.showTags" data-cy="tags">
      <NodeTagVue
        v-for="tag in props.data.tags"
        :key="tag.uuid"
        :tag="tag"
      ></NodeTagVue>
    </span>
    <br />
    <!-- Event Comments -->
    <span v-if="props.data.comments" data-cy="comments">
      <pre class="p-mr-2 comment"><NodeComment
      v-for="comment in props.data.comments"
      :key="comment.uuid"
      :comment="comment"
    /></pre>
    </span>
  </div>
  <!-- Event Time fields -->
  <span v-else-if="props.field.includes('Time')">
    {{ formatDateTime(props.data[props.field]) }}</span
  >
  <!-- Any event property that uses a list -->
  <span v-else-if="Array.isArray(props.data[props.field])">
    <span v-if="props.data[props.field].length">
      {{ joinStringArray(props.data[props.field]) }}
    </span>
    <span v-else> None </span>
  </span>
  <!-- Edit event cell -->
  <span v-else-if="props.field === 'edit'">
    <Button
      data-cy="edit-event-button"
      class="p-button-sm"
      icon="pi pi-pencil"
      @click="open(editEventModalName)"
    />
    <EditEventModal
      :id="props.data.uuid"
      :name="`EditEventModal-${props.data.uuid}`"
      :event-uuid="props.data.uuid"
      @request-reload="requestReload"
    />
  </span>
  <!-- All other columns -->
  <span v-else> {{ props.data[props.field] }}</span>
</template>

<script setup lang="ts">
  import { computed, defineProps, PropType } from "vue";
  import Button from "primevue/button";

  import NodeTagVue from "@/components/Node/NodeTag.vue";
  import NodeComment from "@/components/Node/NodeComment.vue";
  import EditEventModal from "@/components/Modals/EditEventModal.vue";

  import { useModalStore } from "@/stores/modal";
  import { useEventTableStore } from "@/stores/eventTable";
  import { eventSummary } from "@/models/event";

  const eventTableStore = useEventTableStore();
  const modalStore = useModalStore();

  const props = defineProps({
    data: { type: Object as PropType<eventSummary>, required: true },
    field: {
      type: String as PropType<keyof eventSummary | "edit">,
      required: true,
    },
    showTags: { type: Boolean, required: false, default: true },
  });

  const editEventModalName = computed(() => {
    return `EditEventModal-${props.data.uuid}`;
  });

  const formatDateTime = (dateTime: string) => {
    if (dateTime) {
      const d = new Date(dateTime);
      return d.toLocaleString("en-US", { timeZone: "UTC" });
    }

    return "None";
  };

  const getEventLink = (uuid: string) => {
    return "/event/" + uuid;
  };

  const joinStringArray = (arr: string[]) => {
    return arr.join(", ");
  };

  const requestReload = () => {
    eventTableStore.requestReload = true;
  };

  const open = (name: string) => {
    modalStore.open(name);
  };
</script>
