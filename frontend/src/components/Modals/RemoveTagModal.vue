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
    objectStores,
    objectSelectedStores,
    objectTableStores,
  } from "@/stores/index";
  import { useAuthStore } from "@/stores/auth";
  import { useModalStore } from "@/stores/modal";
  import { useMetadataTagStore } from "@/stores/metadataTag";
  import { metadataTagRead } from "@/models/metadataTag";
  import { observableTreeRead } from "@/models/observable";
  import { useObservableStore } from "@/stores/observable";

  const props = defineProps({
    name: { type: String, required: true },
    reloadObject: { type: String, required: true },
    objectType: {
      type: String as PropType<"alerts" | "events" | "observable">,
      required: true,
    },
    observable: {
      type: Object as PropType<observableTreeRead>,
      required: false,
      default: undefined,
    },
  });

  let objectStore: any;
  let tableStore: any;
  let selectedStore: any;
  if (!(props.objectType === "observable")) {
    objectStore = objectStores[props.objectType]();
    selectedStore = objectSelectedStores[props.objectType]();
    tableStore = objectTableStores[props.objectType]();
  }

  const authStore = useAuthStore();
  const modalStore = useModalStore();
  const metadataTagStore = useMetadataTagStore();

  const emit = defineEmits(["requestReload"]);

  const formTagValues = ref<string[]>([]);
  const tagOptions = ref<metadataTagRead[]>([]);
  const error = ref<string>();
  const isLoading = ref(false);

  const initTagOptions = async () => {
    if (props.objectType === "observable" && props.observable) {
      tagOptions.value = props.observable.tags;
    } else if (props.reloadObject == "object") {
      tagOptions.value = objectStore.open.tags;
    } else {
      try {
        await metadataTagStore.readAll();
        tagOptions.value = metadataTagStore.allItems;
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
      if (props.objectType == "observable") {
        await removeObservableTags();
      } else {
        await removeTagsFromObservable();
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

  const removeTagsFromObservable = async () => {
    const updateData = selectedStore.selected.map((uuid: any) => ({
      uuid: uuid,
      tags: deduped([
        ...existingTagValues(uuid),
        ...formTagValues.value,
      ]).filter((tag) => !formTagValues.value.includes(tag)),
      historyUsername: authStore.user.username,
    }));

    await objectStore.update(updateData);
  };

  const existingTagValues = (uuid: string) => {
    let tags: metadataTagRead[] = [];
    if (props.reloadObject == "table") {
      const object = tableStore.visibleQueriedItemById(uuid);
      tags = object ? object.tags : [];
    } else if (props.reloadObject == "object") {
      tags = objectStore.open.tags;
    }
    return tags.map((tag) => tag.value);
  };

  const removeObservableTags = async () => {
    const observableStore = useObservableStore();

    if (props.observable) {
      await observableStore.update(props.observable.uuid, {
        tags: deduped([
          ...props.observable.tags.map((tag) => tag.value),
          ...formTagValues.value,
        ]).filter((tag) => !formTagValues.value.includes(tag)),
        historyUsername: authStore.user.username,
      });
    }
  };

  interface tagEvent {
    value: metadataTagRead;
  }
  function addExistingTagToForm(tagEvent: tagEvent) {
    // Add an existing tag to the list of tags to be added
    formTagValues.value.push(tagEvent.value.value);
  }

  const allowSubmit = computed(() => {
    if (props.objectType == "observable") {
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
