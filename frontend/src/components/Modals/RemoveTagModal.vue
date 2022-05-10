<!-- RemoveTagModal.vue -->
<!-- 'Remove Tag' action modal, agnostic to what is being tagged -->

<template>
  <BaseModal :name="name" header="Remove Tag(s)" @show="initTagOptions">
    <div>
      <div v-if="error" class="p-col">
        <Message severity="error" @close="handleError">{{ error }}</Message>
      </div>
    </div>
    <span class="p-fluid">
      <Chips v-model="formTagValues" data-cy="chips-container" />
      <Dropdown
        :options="tagOptions"
        option-label="value"
        :filter="true"
        placeholder="Select from existing tags"
        filter-placeholder="Search tags"
        @change="addExistingTagToForm($event as unknown as tagEvent)"
      />
    </span>
    <template #footer>
      <Button
        label="Nevermind"
        icon="pi pi-times"
        class="p-button-text"
        @click="close"
      />
      <Button
        data-cy="remove-button"
        label="Remove"
        icon="pi pi-check"
        :disabled="!allowSubmit"
        @click="removeTags"
      />
    </template>
  </BaseModal>
</template>

<script setup lang="ts">
  import { computed, defineEmits, defineProps, ref, PropType } from "vue";

  import Button from "primevue/button";
  import Message from "primevue/message";
  import Chips from "primevue/chips";
  import Dropdown from "primevue/dropdown";

  import BaseModal from "@/components/Modals/BaseModal.vue";

  import {
    nodeStores,
    nodeSelectedStores,
    nodeTableStores,
  } from "@/stores/index";
  import { useModalStore } from "@/stores/modal";
  import { useNodeTagStore } from "@/stores/nodeTag";
  import { nodeTagRead } from "@/models/nodeTag";
  import { observableTreeRead } from "@/models/observable";
  import { useObservableStore } from "@/stores/observable";

  const props = defineProps({
    name: { type: String, required: true },
    reloadObject: { type: String, required: true },
    nodeType: {
      type: String as PropType<"alerts" | "events" | "observable">,
      required: true,
    },
    observable: {
      type: Object as PropType<observableTreeRead>,
      required: false,
      default: undefined,
    },
  });

  let nodeStore: any;
  let tableStore: any;
  let selectedStore: any;
  if (!(props.nodeType === "observable")) {
    nodeStore = nodeStores[props.nodeType]();
    selectedStore = nodeSelectedStores[props.nodeType]();
    tableStore = nodeTableStores[props.nodeType]();
  }

  const modalStore = useModalStore();
  const nodeTagStore = useNodeTagStore();

  const emit = defineEmits(["requestReload"]);

  const formTagValues = ref<string[]>([]);
  const tagOptions = ref<nodeTagRead[]>([]);
  const error = ref<string>();
  const isLoading = ref(false);

  const initTagOptions = async () => {
    if (props.nodeType === "observable" && props.observable) {
      tagOptions.value = props.observable.tags;
    } else if (props.reloadObject == "node") {
      tagOptions.value = nodeStore.open.tags;
    } else {
      try {
        await nodeTagStore.readAll();
        tagOptions.value = nodeTagStore.allItems;
      } catch (e: unknown) {
        if (typeof e === "string") {
          error.value = e;
        } else if (e instanceof Error) {
          error.value = e.message;
        }
      }
    }
  };

  async function removeTags() {
    isLoading.value = true;
    try {
      if (props.nodeType == "observable") {
        await removeObservableTags();
      } else {
        await removeNodeTags();
      }
    } catch (e: unknown) {
      if (typeof e === "string") {
        error.value = e;
      } else if (e instanceof Error) {
        error.value = e.message;
      }
    }

    isLoading.value = false;
    if (!error.value) {
      close();
      emit("requestReload");
    }
  }

  const removeNodeTags = async () => {
    const updateData = selectedStore.selected.map((uuid: any) => ({
      uuid: uuid,
      tags: deduped([
        ...existingNodeTagValues(uuid),
        ...formTagValues.value,
      ]).filter((tag) => !formTagValues.value.includes(tag)),
    }));

    await nodeStore.update(updateData);
  };

  const existingNodeTagValues = (uuid: string) => {
    let nodeTags: nodeTagRead[] = [];
    if (props.reloadObject == "table") {
      const node = tableStore.visibleQueriedItemById(uuid);
      nodeTags = node ? node.tags : [];
    } else if (props.reloadObject == "node") {
      nodeTags = nodeStore.open.tags;
    }
    return nodeTags.map((tag) => tag.value);
  };

  const removeObservableTags = async () => {
    const observableStore = useObservableStore();

    if (props.observable) {
      await observableStore.update(props.observable.uuid, {
        tags: deduped([
          ...props.observable.tags.map((tag) => tag.value),
          ...formTagValues.value,
        ]).filter((tag) => !formTagValues.value.includes(tag)),
      });
    }
  };

  interface tagEvent {
    value: nodeTagRead;
  }
  function addExistingTagToForm(tagEvent: tagEvent) {
    // Add an existing tag to the list of tags to be added
    formTagValues.value.push(tagEvent.value.value);
  }

  const allowSubmit = computed(() => {
    if (props.nodeType == "observable") {
      return formTagValues.value.length;
    }
    return selectedStore.selected.length && formTagValues.value.length;
  });

  const deduped = (arr: string[]) => {
    return [...new Set(arr)];
  };

  const handleError = () => {
    error.value = undefined;
    close();
  };

  function close() {
    formTagValues.value = [];
    modalStore.close(props.name);
  }
</script>
