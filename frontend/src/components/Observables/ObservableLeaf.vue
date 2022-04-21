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
      v-if="showCopyToClipboard"
      data-cy="copy-to-clipboard-button"
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
            @click="itemClick($event, item as observableActionSubTypes)"
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
        :name="componentName"
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
  import {
    computed,
    defineProps,
    inject,
    onMounted,
    PropType,
    ref,
    shallowRef,
  } from "vue";
  import { useRouter } from "vue-router";

  import { useToast } from "primevue/usetoast";
  import Button from "primevue/button";
  import Menu from "primevue/menu";
  import MenuItem from "primevue/menu";
  import Toast from "primevue/toast";

  import type CSS from "csstype";

  import NodeTagVue from "@/components/Node/NodeTag.vue";

  import {
    observableActionCommand,
    observableActionModal,
    observableActionSection,
    observableActionUrl,
    observableTreeRead,
  } from "@/models/observable";
  import type { observableActionSubTypes } from "@/models/observable";
  import { copyToClipboard } from "@/etc/helpers";
  import { useAlertStore } from "@/stores/alert";
  import { useFilterStore } from "@/stores/filter";
  import { useModalStore } from "@/stores/modal";

  const config = inject("config") as Record<string, any>;

  const props = defineProps({
    observable: {
      type: Object as PropType<observableTreeRead>,
      required: true,
    },
    showCopyToClipboard: { type: Boolean, required: false, default: true },
    showActionsMenu: { type: Boolean, required: false, default: true },
    showTags: { type: Boolean, required: false, default: true },
  });

  const alertStore = useAlertStore();
  const filterStore = useFilterStore();
  const modalStore = useModalStore();
  const toast = useToast();
  const router = useRouter();

  const component = shallowRef();
  const menu = ref();
  const items = ref<observableActionSubTypes[]>([]); // todo fix
  const style = ref<CSS.Properties>();
  const observableType = ref<string>(props.observable.type.value);
  const componentName = ref<string>();

  onMounted(() => {
    const observableMetadata = config.observables.observableMetadata;
    const commonObservableActions = config.observables.commonObservableActions;
    items.value = commonObservableActions;

    // Check whether there is specific metadata config for this observable type
    if (observableType.value in observableMetadata) {
      // If so, add any available actions
      if (
        observableMetadata[observableType.value].actions &&
        observableMetadata[observableType.value].actions.length
      ) {
        items.value = [
          ...items.value,
          ...observableMetadata[observableType.value].actions,
        ];
      }

      // And use any configured styling
      if (observableMetadata[observableType.value].style) {
        style.value = observableMetadata[observableType.value].style;
      }
    }
  });

  const itemsFiltered = computed(() => {
    return items.value.filter((item) => {
      if (item.requirements) {
        return item.requirements(props.observable);
      } else {
        return true;
      }
    });
  });

  const displayValue = computed(() => {
    let type = observableType.value;
    let value = props.observable.value;
    const metadata = props.observable.nodeMetadata;

    if (metadata && metadata.display) {
      if (metadata.display.type) {
        type = `${metadata.display.type} (${observableType.value})`;
      }

      if (metadata.display.value) {
        value = metadata.display.value;
      }
    }

    return `${type}: ${value}`;
  });

  const itemClick = async (
    $originalEvent: unknown,
    item: observableActionSubTypes | observableActionSection,
  ) => {
    if (!isObservableActionSection(item)) {
      if (item.type == "modal") {
        handleModalItemClicked(item);
      } else if (item.type == "command") {
        await handleCommandItemClicked(item);
      } else if (item.type == "url") {
        handleUrlItemClicked(item);
      }
    }
    toggle($originalEvent);
  };

  const isObservableActionSection = (
    item: observableActionSubTypes | observableActionSection,
  ): item is observableActionSection => {
    return "items" in item;
  };

  const handleModalItemClicked = (item: observableActionModal) => {
    component.value = item.modal;
    componentName.value = item.modalName;
    modalStore.open(item.modalName);
  };

  const handleCommandItemClicked = async (item: observableActionCommand) => {
    try {
      await item.command(props.observable);
      if (item.reloadPage) {
        alertStore.requestReload = true; // update in the future to be more extendable
      }
    } catch (e: unknown) {
      if (typeof e === "string") {
        showError({
          item: item,
          detail: e,
        });
      } else if (e instanceof Error) {
        showError({
          item: item,
          detail: e.message,
        });
      }
    }
  };

  const handleUrlItemClicked = (item: observableActionUrl) => {
    window.location = item.url as unknown as Location;
  };

  const filterByObservable = (obs: observableTreeRead) => {
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
  };

  const showError = (args: {
    item: observableActionSubTypes;
    detail: string;
  }) => {
    toast.add({
      severity: "error",
      summary: `'${args.item.label}' Failed`,
      detail: args.detail,
      life: 6000,
    });
  };

  const toggle = (event: unknown) => {
    menu.value.toggle(event);
  };
</script>
<style scoped>
  .treenode-text:hover {
    cursor: pointer;
    text-decoration: underline;
    font-weight: bold;
  }
</style>
