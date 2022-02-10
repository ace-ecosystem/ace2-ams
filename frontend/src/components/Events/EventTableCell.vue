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
    <span data-cy="tags">
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
    {{ joinStringArray(props.data[props.field]) }}
  </span>
  <!-- Edit event cell -->
  <span v-else-if="props.field === 'edit'">
    <Button
      data-cy="disposition-button"
      class="p-button-sm"
      icon="pi pi-pencil"
      @click="open(`EditEventModal-${props.data.uuid}`)"
    />
    <EditEventModal
      :id="props.data.uuid"
      :name="`EditEventModal-${props.data.uuid}`"
      :event-uuid="props.data.uuid"
      @requestReload="requestReload"
    />
  </span>
  <!-- All other columns -->
  <span v-else> {{ props.data[props.field] }}</span>
</template>

<script setup>
  import { defineProps } from "vue";
  import Button from "primevue/button";

  import NodeTagVue from "../Node/NodeTag.vue";
  import NodeComment from "../Node/NodeComment.vue";
  import EditEventModal from "../Modals/EditEventModal.vue";

  import { useModalStore } from "@/stores/modal";
  import { useEventTableStore } from "@/stores/eventTable";

  const eventTableStore = useEventTableStore();
  const modalStore = useModalStore();

  const props = defineProps({
    data: { type: Object, required: true },
    field: { type: String, required: true },
  });

  const formatDateTime = (dateTime) => {
    if (dateTime) {
      const d = new Date(dateTime);
      return d.toLocaleString("en-US");
    }

    return "None";
  };

  const getEventLink = (uuid) => {
    return "/event/" + uuid;
  };

  const joinStringArray = (arr) => {
    return arr.join(", ");
  };

  const requestReload = () => {
    eventTableStore.requestReload = true;
  };

  const open = (name) => {
    modalStore.open(name);
  };
</script>
