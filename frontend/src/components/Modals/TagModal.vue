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
        :options="tagStore.allItems"
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
  import { computed, defineEmits, defineProps, ref, PropType } from "vue";

  import Button from "primevue/button";
  import Message from "primevue/message";
  import Chips from "primevue/chips";
  import Dropdown from "primevue/dropdown";

  import BaseModal from "@/components/Modals/BaseModal.vue";

  import { Tag } from "@/services/api/tag";
  import {
    nodeStores,
    nodeSelectedStores,
    nodeTableStores,
  } from "@/stores/index";
  import { useAuthStore } from "@/stores/auth";
  import { useModalStore } from "@/stores/modal";
  import { useTagStore } from "@/stores/tag";
  import { tagRead } from "@/models/tag";
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

  const authStore = useAuthStore();
  const modalStore = useModalStore();
  const tagStore = useTagStore();

  const emit = defineEmits(["requestReload"]);

  const formTagValues = ref<string[]>([]);
  const error = ref<string>();
  const isLoading = ref(false);

  async function loadAllExistingTags() {
    await tagStore.readAll();
  }

  async function createAndAddTags() {
    isLoading.value = true;
    try {
      if (uniqueNewTags.value.length) {
        await createNewTags();
      }
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
    const updateData = selectedStore.selected.map((uuid: any) => ({
      uuid: uuid,
      tags: deduped([...getExistingTagValues(uuid), ...formTagValues.value]),
    }));

    await nodeStore.update(updateData);
  };

  const getExistingTagValues = (uuid: string) => {
    let tags: tagRead[] = [];
    if (props.reloadObject == "table") {
      const node = tableStore.visibleQueriedItemById(uuid);
      tags = node ? node.tags : [];
    } else if (props.reloadObject == "node") {
      tags = nodeStore.open.tags;
    }
    return tags.map((tag) => tag.value);
  };

  const addObservableTags = async () => {
    const observableStore = useObservableStore();

    if (props.observable) {
      await observableStore.update(props.observable.uuid, {
        tags: deduped([
          ...props.observable.permanentTags.map((tag) => tag.value),
          ...formTagValues.value,
        ]),
        historyUsername: authStore.user.username,
      });
    }
  };

  const createNewTags = async () => {
    for (const tag of uniqueNewTags.value) {
      await Tag.create({ value: tag });
    }
    await loadAllExistingTags();
  };

  const uniqueNewTags = computed(() => {
    return deduped(formTagValues.value).filter(
      (tag) => !existingTagValues.value.includes(tag),
    );
  });

  const existingTagValues = computed(() => {
    return tagStore.allItems.map((tag) => tag.value);
  });

  interface tagEvent {
    value: tagRead;
  }
  function addExistingTag(tagEvent: tagEvent) {
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
