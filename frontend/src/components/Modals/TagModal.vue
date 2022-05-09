<!-- TagModal.vue -->
<!-- 'Tag' action modal, agnostic to what is being tagged -->

<template>
  <BaseModal :name="name" header="Add Tags" @show="loadAllExistingTags">
    <div>
      <div v-if="error" class="p-col">
        <Message severity="error" @close="handleError">{{ error }}</Message>
      </div>
    </div>
    <span class="p-fluid">
      <Chips v-model="formTagValues" data-cy="chips-container" />
      <Dropdown
        :options="nodeTagStore.allItems"
        option-label="value"
        :filter="true"
        placeholder="Select from existing tags"
        filter-placeholder="Search tags"
        @change="addExistingTag($event as unknown as tagEvent)"
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
        label="Add"
        icon="pi pi-check"
        :disabled="!allowSubmit"
        @click="createAndAddTags"
      />
    </template>
  </BaseModal>
</template>

<script setup lang="ts">
  import {
    computed,
    defineEmits,
    defineProps,
    ref,
    inject,
    PropType,
  } from "vue";

  import Button from "primevue/button";
  import Message from "primevue/message";
  import Chips from "primevue/chips";
  import Dropdown from "primevue/dropdown";

  import BaseModal from "@/components/Modals/BaseModal.vue";

  import { NodeTag } from "@/services/api/nodeTag";
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
  let selected: string[];
  if (!(props.nodeType === "observable")) {
    nodeStore = nodeStores[props.nodeType]();
    selected = nodeSelectedStores[props.nodeType]().selected;
    tableStore = nodeTableStores[props.nodeType]();
  }

  const modalStore = useModalStore();
  const nodeTagStore = useNodeTagStore();

  const emit = defineEmits(["requestReload"]);

  const formTagValues = ref<string[]>([]);
  const existingTagValues = ref<string[]>([]);
  const error = ref<string>();
  const isLoading = ref(false);

  async function loadAllExistingTags() {
    await nodeTagStore.readAll();
    existingTagValues.value = nodeTagStore.allItems.map((tag) => tag.value);
  }

  async function createAndAddTags() {
    isLoading.value = true;
    try {
      await createNewTags();
      if (props.nodeType == "observable") {
        await addObservableTags();
      } else {
        await addNodeTags();
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

  const addNodeTags = async () => {
    const updateData = selected.map((uuid) => ({
      uuid: uuid,
      tags: deduped([...existingNodeTagValues(uuid), ...formTagValues.value]),
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

  const addObservableTags = async () => {
    const observableStore = useObservableStore();

    if (props.observable) {
      await observableStore.update(props.observable.uuid, {
        tags: deduped([
          ...props.observable.tags.map((tag) => tag.value),
          ...formTagValues.value,
        ]),
      });
    }
  };

  const createNewTags = async () => {
    for (const tag of uniqueNewTags.value) {
      await NodeTag.create({ value: tag });
    }
    await loadAllExistingTags();
  };

  const uniqueNewTags = computed(() => {
    return deduped(formTagValues.value).filter(
      (tag) => !existingTagValues.value.includes(tag),
    );
  });

  interface tagEvent {
    value: nodeTagRead;
  }
  function addExistingTag(tagEvent: tagEvent) {
    // Add an existing tag to the list of tags to be added
    formTagValues.value.push(tagEvent.value.value);
  }

  const allowSubmit = computed(() => {
    if (props.nodeType == "observable") {
      return formTagValues.value.length;
    }
    return selected.length && formTagValues.value.length;
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
