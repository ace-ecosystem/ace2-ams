<!-- TagModal.vue -->
<!-- 'Tag' action modal, agnostic to what is being tagged -->

<template>
  <BaseModal :name="name" header="Add Tags" @show="loadTags">
    <div>
      <div v-if="error" class="p-col">
        <Message severity="error" @close="handleError">{{ error }}</Message>
      </div>
    </div>
    <span class="p-fluid">
      <Chips v-model="newTags" data-cy="chips-container" />
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
        @click="addTags"
      />
    </template>
  </BaseModal>
</template>

<script setup lang="ts">
  import { computed, defineEmits, defineProps, ref, inject } from "vue";

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

  const nodeType = inject("nodeType") as "alerts" | "events";

  const nodeStore = nodeStores[nodeType]();
  const tableStore = nodeTableStores[nodeType]();
  const selectedStore = nodeSelectedStores[nodeType]();
  const modalStore = useModalStore();
  const nodeTagStore = useNodeTagStore();

  const emit = defineEmits(["requestReload"]);

  const props = defineProps({
    name: { type: String, required: true },
    reloadObject: { type: String, required: true },
  });

  const newTags = ref<string[]>([]);
  const storeTagValues = ref<string[]>([]);
  const error = ref<string>();
  const isLoading = ref(false);

  async function loadTags() {
    await nodeTagStore.readAll();
    storeTagValues.value = tagValues(nodeTagStore.allItems);
  }

  async function addTags() {
    isLoading.value = true;
    try {
      await createTags(newTags.value);

      const updateData = selectedStore.selected.map((uuid) => ({
        uuid: uuid,
        tags: newNodeTags(uuid, newTags.value),
      }));

      await nodeStore.update(updateData);
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

  function newNodeTags(uuid: string, tags: string[]) {
    let nodeTags: nodeTagRead[] = [];
    if (props.reloadObject == "table") {
      const node = tableStore.visibleQueriedItemById(uuid);
      nodeTags = node ? node.tags : [];
    } else if (props.reloadObject == "node") {
      nodeTags = nodeStore.open.tags;
    }
    return [...tagValues(nodeTags), ...tags];
  }

  async function createTags(tags: string[]) {
    for (const tag of tags) {
      if (!tagExists(tag)) {
        await NodeTag.create({ value: tag });
        await loadTags();
      }
    }
  }

  function tagExists(tagValue: string) {
    return storeTagValues.value.includes(tagValue);
  }

  function tagValues(tags: nodeTagRead[]) {
    let values = [];
    for (const tag of tags) {
      values.push(tag.value);
    }
    return values;
  }

  interface tagEvent {
    value: nodeTagRead;
  }
  function addExistingTag(tagEvent: tagEvent) {
    // Add an existing tag to the list of tags to be added
    newTags.value.push(tagEvent.value.value);
  }

  const allowSubmit = computed(() => {
    return selectedStore.anySelected && newTags.value.length;
  });

  const handleError = () => {
    error.value = undefined;
    close();
  };

  function close() {
    newTags.value = [];
    modalStore.close(props.name);
  }
</script>
