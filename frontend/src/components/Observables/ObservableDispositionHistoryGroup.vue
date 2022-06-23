<template>
  <AlertDispositionTag
    v-for="entry in observable.dispositionHistory"
    :key="entry.disposition"
    style="cursor: pointer"
    :disposition="entry.disposition"
    :disposition-count="entry.count"
    :percent="entry.percent"
    @click="filterByObservableAndDisposition(entry.disposition)"
  ></AlertDispositionTag>
</template>

<script setup lang="ts">
  import { defineProps, PropType } from "vue";
  import { useRouter } from "vue-router";

  import AlertDispositionTag from "@/components/Alerts/AlertDispositionTag.vue";
  import { useAlertDispositionStore } from "@/stores/alertDisposition";
  import { useFilterStore } from "@/stores/filter";
  import { alertDispositionRead } from "@/models/alertDisposition";
  import {
    observableTreeRead,
    observableInAlertRead,
  } from "@/models/observable";

  const router = useRouter();

  const alertDispositionStore = useAlertDispositionStore();
  const filterStore = useFilterStore();

  const props = defineProps({
    observable: {
      type: Object as PropType<observableTreeRead | observableInAlertRead>,
      required: true,
    },
    rerouteToManageAlerts: {
      type: Boolean,
      required: true,
    },
  });

  const filterByObservableAndDisposition = (disposition: string) => {
    const dispositionObject = getDispositionObject(disposition);

    filterStore.clearAll({ objectType: "alerts" });

    if (dispositionObject) {
      filterStore.setFilter({
        objectType: "alerts",
        filterName: "disposition",
        filterValue: dispositionObject,
      });
    }

    filterStore.setFilter({
      objectType: "alerts",
      filterName: "observable",
      filterValue: {
        category: props.observable.type,
        value: props.observable.value,
      },
    });
    if (props.rerouteToManageAlerts) {
      router.replace({
        path: "/manage_alerts",
      });
    }
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
