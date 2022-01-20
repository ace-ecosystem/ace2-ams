<!-- TheAlertsTable.vue -->
<!-- The table where all currently filtered alerts are displayed, selected to take action, or link to an individual alert page -->

<template>
  <TheNodeTable
    :columns="columns"
    :column-select="true"
    :export-c-s-v="true"
    :keyword-search="true"
    :reset-table="true"
    :row-expansion="true"
    @row-expand="getObservables($event.data.uuid)"
    @row-collapse="clearObservables($event.data.uuid)"
  >
    <template #rowCell="{ data, col }">
      <!-- Alert Name -->
      <div v-if="col.field === 'name'">
        <!-- Name w/ Link to Alert -->
        <span class="p-m-1" data-cy="alertName">
          <router-link :to="getAlertLink(data.uuid)">{{
            data.name
          }}</router-link></span
        >
        <br />
        <!-- Alert Tags -->
        <span data-cy="tags">
          <NodeTagVue
            v-for="tag in getAllTags(data)"
            :key="tag.uuid"
            :tag="tag"
          ></NodeTagVue>
        </span>
        <!-- Alert comments -->
        <span v-if="data.comments">
          <pre
            v-for="comment in data.comments"
            :key="comment.uuid"
            class="p-mr-2 comment"
            >{{ formatComment(comment) }}</pre
          >
        </span>
      </div>

      <!-- Alert Time Property -->
      <span v-else-if="col.field.includes('Time')">
        {{ formatDateTime(data[col.field]) }}</span
      >

      <!-- Everything else -->
      <span v-else> {{ data[col.field] }}</span>
    </template>

    <!-- Row Expansion -->
    <template #rowExpansion="{ data }">
      <ul>
        <!-- List each observable with link to filter -->
        <li v-for="obs of observablesByAlertUuid[data.uuid]" :key="obs.value">
          <span class="link-text" @click="filterByObservable(obs)">{{
            formatObservable(obs)
          }}</span>
          <!-- Display each observable's -->
          <NodeTagVue v-for="tag of obs.tags" :key="tag.value" :tag="tag" />
        </li>
      </ul>
    </template>
  </TheNodeTable>
</template>

<script setup>
  import { ref } from "vue";

  import NodeTagVue from "../Node/NodeTag.vue";
  import TheNodeTable from "../Node/TheNodeTable";

  import { NodeTree } from "@/services/api/nodeTree";

  const columns = ref([
    { field: "dispositionTime", header: "Dispositioned Time", default: false },
    { field: "insertTime", header: "Insert Time", default: false },
    { field: "eventTime", header: "Event Time", default: true },
    { field: "name", header: "Name", default: true },
    { field: "owner", header: "Owner", default: true },
    { field: "disposition", header: "Disposition", default: true },
    { field: "dispositionUser", header: "Dispositioned By", default: false },
    { field: "queue", header: "Queue", default: false },
    { field: "type", header: "Type", default: false },
  ]);

  const formatComment = (comment) => {
    return `(${comment.user.displayName}) ${comment.value}`;
  };

  const formatDateTime = (dateTime) => {
    if (dateTime) {
      const d = new Date(dateTime);
      return d.toLocaleString("en-US");
    }

    return "None";
  };

  const formatObservable = (observable) => {
    return `${observable.type.value} : ${observable.value}`;
  };

  const getAlertLink = (uuid) => {
    return "/alert/" + uuid;
  };

  const getAllTags = (alert) => {
    const allTags = alert.tags.concat(alert.childTags);

    // Return a sorted and deduplicated list of the tags based on the tag UUID.
    return [...new Map(allTags.map((v) => [v.uuid, v])).values()].sort((a, b) =>
      a.value > b.value ? 1 : -1,
    );
  };

  const observablesByAlertUuid = ref({});
  const getObservables = async (uuid) => {
    const observables = await NodeTree.readNodesOfNodeTree(
      [uuid],
      "observable",
    );

    observablesByAlertUuid.value[uuid] = observables.sort((a, b) => {
      if (a.type.value === b.type.value) {
        return a.value < b.value ? -1 : 1;
      } else {
        return a.type.value < b.type.value ? -1 : 1;
      }
    });
  };
  const clearObservables = (uuid) => {
    delete observablesByAlertUuid.value[uuid];
  };

  import { useFilterStore } from "@/stores/filter";
  const filterStore = useFilterStore();
  const filterByObservable = (observable) => {
    filterStore.bulkSetFilters({
      nodeType: "alerts",
      filters: {
        observable: {
          category: observable.type,
          value: observable.value,
        },
      },
    });
  };
</script>

<style>
  .link-text:hover {
    cursor: pointer;
    text-decoration: underline;
    font-weight: bold;
  }
</style>
