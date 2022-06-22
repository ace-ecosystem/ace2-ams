<!-- AlertTableExpansion.vue -->
<!-- Contains logic and functionality for displaying data in alert row dropdown, currently list of alert's observables -->

<template>
  <div v-if="isLoading" style="flex: 1">
    <ul>
      <li><Skeleton width="30%" data-cy="loading-observable"></Skeleton></li>
      <li><Skeleton width="25%" data-cy="loading-observable"></Skeleton></li>
      <li><Skeleton width="30%" data-cy="loading-observable"></Skeleton></li>
      <li><Skeleton width="25%" data-cy="loading-observable"></Skeleton></li>
    </ul>
  </div>
  <span v-else-if="observablesIsEmpty"
    >No observables exist for this alert.</span
  >
  <ul v-else>
    <!-- List each observable with link to filter -->
    <li v-for="obs of observables" :key="obs.value">
      <span class="link-text" @click="filterByObservable(obs)">{{
        formatObservable(obs)
      }}</span>
      <!-- Display each observable's tags -->
      <MetadataTag v-for="tag of obs.tags" :key="tag.value" :tag="tag" />
      <MetadataTag
        v-for="tag of obs.analysisMetadata.tags"
        :key="tag.value"
        :tag="tag"
      />
      <AlertDispositionTag
        v-for="entry in obs.dispositionHistory"
        :key="entry.disposition"
        style="cursor: pointer"
        :disposition="entry.disposition"
        :disposition-count="entry.count"
        :percent="entry.percent"
        @click="filterByObservableAndDisposition(obs, entry.disposition)"
      ></AlertDispositionTag>
    </li>
  </ul>
</template>

<script setup lang="ts">
  import { computed, defineProps, PropType } from "vue";
  import Skeleton from "primevue/skeleton";

  import { useFilterStore } from "@/stores/filter";
  import { useAlertDispositionStore } from "@/stores/alertDisposition";

  import type CSS from "csstype";

  import AlertDispositionTag from "@/components/Alerts/AlertDispositionTag.vue";
  import MetadataTag from "@/components/Metadata/MetadataTag.vue";

  import { observableInAlertRead } from "@/models/observable";
  import { alertDispositionRead } from "@/models/alertDisposition";

  const alertDispositionStore = useAlertDispositionStore();

  const props = defineProps({
    observables: {
      type: Array as PropType<observableInAlertRead[] | null>,
      required: true,
    },
  });

  const isLoading = computed(() => {
    return props.observables === null;
  });

  const observablesIsEmpty = computed(() => {
    return Array.isArray(props.observables) && !props.observables.length;
  });

  const formatObservable = (observable: observableInAlertRead) => {
    return `${observable.type.value} : ${observable.value}`;
  };

  const filterStore = useFilterStore();
  const filterByObservable = (observable: observableInAlertRead) => {
    filterStore.bulkSetFilters({
      nodeType: "alerts",
      filters: {
        observable: [
          {
            category: observable.type,
            value: observable.value,
          },
        ],
      },
    });
  };

  const filterByObservableAndDisposition = (
    obs: observableInAlertRead,
    disposition: string,
  ) => {
    const dispositionObject = getDispositionObject(disposition);

    filterStore.clearAll({ nodeType: "alerts" });

    if (dispositionObject) {
      filterStore.setFilter({
        nodeType: "alerts",
        filterName: "disposition",
        filterValue: dispositionObject,
      });
    }

    filterStore.setFilter({
      nodeType: "alerts",
      filterName: "observable",
      filterValue: {
        category: obs.type,
        value: obs.value,
      },
    });
  };

  const getDispositionObject = (
    disposition: string,
  ): alertDispositionRead | undefined => {
    if (disposition == "OPEN") {
      return { value: "None" } as alertDispositionRead;
    } else {
      return alertDispositionStore.items.find(
        (item) => item.value == disposition,
      );
    }
  };
</script>

<style>
  .link-text:hover {
    cursor: pointer;
    text-decoration: underline;
    font-weight: bold;
  }
</style>
