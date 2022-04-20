<template>
  <span>
    <Toast data-cy="observable-action-error" />
    <span
      class="treenode-text leaf-element"
      :style="style"
      @click="filterByObservable(observable)"
      >{{ displayValue }}
    </span>
    <Button
      data-cy="copy-to-clipboard-button"
      v-if="showCopyToClipboard"
      role="button"
      icon="pi pi-copy"
      class="p-button-rounded p-button-secondary p-button-outlined p-button-sm leaf-element"
      @click="copyToClipboard(observable.value)"
    />
    <span v-if="showActionsMenu && itemsFiltered.length">
      <Button
        data-cy="show-actions-menu-button"
        role="button"
        icon="pi pi-ellipsis-h"
        type="button"
        class="p-button-rounded p-button-secondary p-button-outlined p-button-sm leaf-element"
        @click="toggle"
      />
      <Menu
        id="overlayMenu"
        ref="menu"
        :model="(itemsFiltered as unknown as MenuItem[])"
        :popup="true"
      >
        <template #item="{ item }">
          <li
            class="p-menuitem"
            @click="itemClick($event, item as observableAction)"
          >
            <span role="menuitem" class="p-menuitem-link">
              <span :class="['p-menuitem-icon', item.icon]"></span>
              <span class="p-menuitem-text">{{ item.label }}</span>
            </span>
          </li>
        </template>
      </Menu>
      <component
        :is="component"
        :name="`${component}`"
        :observable="observable"
      ></component>
    </span>
    <span v-if="showTags && observable.tags.length" class="leaf-element">
      <NodeTagVue
        v-for="tag in observable.tags"
        :key="tag.uuid"
        :tag="tag"
      ></NodeTagVue
    ></span>
  </span>
</template>

<script setup lang="ts">
  import NodeTagVue from "@/components/Node/NodeTag.vue";

  import {
    defineProps,
    computed,
    PropType,
    ref,
    inject,
    onMounted,
    shallowRef,
  } from "vue";

  import { useRouter } from "vue-router";
  import Menu from "primevue/menu";
  import MenuItem from "primevue/menu";
  import Button from "primevue/button";

  import {
    observableActionSection,
    observableTreeRead,
  } from "@/models/observable";
  import type { observableAction } from "@/models/observable";
  import { useFilterStore } from "@/stores/filter";
  import { copyToClipboard } from "@/etc/helpers";
  import { useModalStore } from "@/stores/modal";
  import Toast from "primevue/toast";
  import { useToast } from "primevue/usetoast";

  import { useAlertStore } from "@/stores/alert";

  const filterStore = useFilterStore();
  const router = useRouter();

  const config = inject("config") as Record<string, any>;
  const toast = useToast();

  const toggle = (event: unknown) => {
    menu.value.toggle(event);
  };

  const menu = ref();
  const style = ref();
  const component = shallowRef();
  const items = ref<observableAction[]>([]); // todo fix
  const modalStore = useModalStore();
  const alertStore = useAlertStore();

  onMounted(() => {
    if (props.observable.type.value in config.observables.observableMetadata) {
      items.value = [
        ...config.observables.commonObservableActions,
        ...(config.observables.observableMetadata[props.observable.type.value]
          .actions
          ? config.observables.observableMetadata[props.observable.type.value]
              .actions
          : []),
      ];

      if (
        config.observables.observableMetadata[props.observable.type.value].style
      ) {
        style.value =
          config.observables.observableMetadata[
            props.observable.type.value
          ].style;
      }
    } else {
      items.value = config.observables.commonObservableActions;
    }
  });

  const showError = (args: {
    item: observableAction;
    detail: string | unknown;
  }) => {
    toast.add({
      severity: "error",
      summary: `'${args.item.label}' Failed`,
      detail: args.detail,
      life: 6000,
    });
  };

  const itemClick = async (
    $originalEvent: unknown,
    item: observableAction | observableActionSection,
  ) => {
    if (!("items" in item)) {
      if (item.type == "modal") {
        if ("modal" in item) {
          component.value = item.modal;
          modalStore.open(item.modal);
        } else {
          showError({
            item: item,
            detail: "No modal has been configured for this action.",
          });
        }
      } else if (item.type == "command") {
        if (item.command) {
          try {
            await item.command(props.observable);
            alertStore.requestReload = true; // update in the future to be more extendable
          } catch (e: unknown) {
            showError({
              item: item,
              detail: e,
            });
          }
        } else {
          showError({
            item: item,
            detail: "No command has been configured for this action.",
          });
        }
      } else if (item.type == "url") {
        console.log("blah");
        if ("url" in item) {
          window.location = item.url as unknown as Location;
        } else {
          showError({
            item: item,
            detail: "No URL has been configured for this action.",
          });
        }
      }
    }
    toggle($originalEvent);
  };

  const itemsFiltered = computed(() => {
    return items.value.filter((item) => {
      if (item.requirements) {
        return item.requirements(props.observable);
      } else {
        return true;
      }
    });
  });

  const props = defineProps({
    observable: {
      type: Object as PropType<observableTreeRead>,
      required: true,
    },
    showCopyToClipboard: { type: Boolean, required: false, default: true },
    showActionsMenu: { type: Boolean, required: false, default: true },
    showTags: { type: Boolean, required: false, default: true },
  });

  const displayValue = computed(() => {
    let type = null;
    let value = null;

    try {
      if (
        props.observable.nodeMetadata &&
        props.observable.nodeMetadata.display
      ) {
        if (props.observable.nodeMetadata.display.type) {
          type =
            props.observable.nodeMetadata.display.type +
            " (" +
            props.observable.type.value +
            ")";
        } else {
          type = props.observable.type.value;
        }

        if (props.observable.nodeMetadata.display.value) {
          value = props.observable.nodeMetadata.display.value;
        } else {
          value = props.observable.value;
        }
      } else {
        throw new Error("No observable display metadata given");
      }
    } catch (error) {
      type = props.observable.type.value;
      value = props.observable.value;
    }

    return type + ": " + value;
  });

  function filterByObservable(obs: observableTreeRead) {
    filterStore.bulkSetFilters({
      nodeType: "alerts",
      filters: {
        observable: {
          category: obs.type,
          value: obs.value,
        },
      },
    });
    router.replace({
      path: "/manage_alerts",
    });
  }
</script>
<style scoped>
  .treenode-text:hover {
    cursor: pointer;
    text-decoration: underline;
    font-weight: bold;
  }
</style>
