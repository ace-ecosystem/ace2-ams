<!-- AlertTableCell.vue -->
<!-- Contains logic and functionality to display field-specific data in TheAlertTable -->

<template>
  <!-- Alert Name -->
  <div v-if="props.field === 'name'">
    <img
      v-if="alertIconPath"
      data-cy="alert-icon"
      src="@/assets/alertIcons/test.png"
    />
    <!-- Name w/ Link to Alert -->
    <span class="p-m-1" data-cy="alertName">
      <router-link :to="getAlertLink(props.data)">{{
        props.data.name
      }}</router-link></span
    >
    <br />
    <!-- Alert Tags -->
    <span data-cy="tags">
      <NodeTagVue
        v-for="tag in getAllAlertTags(props.data)"
        :key="tag.uuid"
        :tag="tag"
      ></NodeTagVue>
    </span>
    <!-- Alert comments -->
    <span v-if="props.data.comments">
      <pre class="p-mr-2 comment"><NodeComment
      v-for="comment in props.data.comments"
      :key="comment.uuid"
      :comment="comment"
    /></pre>
    </span>
  </div>

  <!-- Alert Time Property -->
  <span v-else-if="props.field.includes('Time')">
    {{ formatDateTime(props.data[props.field]) }}</span
  >

  <!-- Alert Comments -->
  <div v-else-if="props.field === 'comments'">
    <span v-if="!props.data.comments.length">None</span>
    <NodeComment
      v-for="comment in props.data.comments"
      v-else
      :key="comment.uuid"
      :comment="comment"
      :include-time="true"
    />
  </div>

  <!-- Everything else -->
  <span v-else> {{ props.data[props.field] }}</span>
</template>

<script setup lang="ts">
  import { defineProps, PropType, inject, computed } from "vue";

  import NodeTagVue from "@/components/Node/NodeTag.vue";
  import NodeComment from "@/components/Node/NodeComment.vue";

  import { alertSummary } from "@/models/alert";
  import { getAllAlertTags, getAlertLink } from "@/etc/helpers";

  const config = inject("config") as Record<string, any>;

  const props = defineProps({
    data: { type: Object as PropType<alertSummary>, required: true },
    field: { type: String as PropType<keyof alertSummary>, required: true },
  });

  const alertIconPath = computed(() => {
    if (config && config.alerts) {
      if (props.data.type in config.alerts.alertIconTypeMapping) {
        return `@/assets/alertIcons/${
          config.alerts.alertIconTypeMapping[props.data.type]
        }`;
      }
    }
    return undefined;
  });

  const formatDateTime = (dateTime: any) => {
    if (typeof dateTime === "string") {
      return dateTime;
    }

    if (dateTime) {
      const d = new Date(dateTime);
      return d.toLocaleString("en-US", { timeZone: "UTC" });
    }

    return "None";
  };
</script>

<style>
  .link-text:hover {
    cursor: pointer;
    text-decoration: underline;
    font-weight: bold;
  }
</style>
