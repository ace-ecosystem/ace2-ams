<!-- TagModal.vue -->
<!-- 'Tag' action modal, agnostic to what is being tagged -->

<template>
  <BaseModal :name="name" header="Add Tags">
    <div>
      <div v-if="error" class="p-col">
        <Message severity="error" @close="handleError">{{ error }}</Message>
      </div>
    </div>
    <span class="p-fluid">
      <Chips v-model="newTags" />
      <Dropdown
        :options="nodeTagStore.allItems"
        option-label="value"
        :filter="true"
        placeholder="Select from existing tags"
        filter-placeholder="Search tags"
        @change="addExistingTag"
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

<script setup>
  import { computed, defineEmits, defineProps, onMounted, ref } from "vue";

  import Button from "primevue/button";
  import Message from "primevue/message";
  import Chips from "primevue/chips";
  import Dropdown from "primevue/dropdown";

  import BaseModal from "@/components/Modals/BaseModal";

  import { NodeTag } from "@/services/api/nodeTag";

  import { useAlertStore } from "@/stores/alert";
  import { useAlertTableStore } from "@/stores/alertTable";
  import { useModalStore } from "@/stores/modal";
  import { useNodeTagStore } from "@/stores/nodeTag";
  import { useSelectedAlertStore } from "@/stores/selectedAlert";

  const alertStore = useAlertStore();
  const alertTableStore = useAlertTableStore();
  const modalStore = useModalStore();
  const nodeTagStore = useNodeTagStore();
  const selectedAlertStore = useSelectedAlertStore();

  const emit = defineEmits(["requestReload"]);

  const props = defineProps({
    name: { type: String, required: true },
  });

  const newTags = ref([]);
  const storeTagValues = ref([]);
  const error = ref(null);
  const isLoading = ref(false);

  onMounted(async () => {
    await loadTags();
  });

  async function loadTags() {
    await nodeTagStore.readAll();
    storeTagValues.value = tagValues(nodeTagStore.allItems);
  }

  async function addTags() {
    isLoading.value = true;
    try {
      await createTags(newTags.value);

      const updateData = selectedAlertStore.selected.map((uuid) => ({
        uuid: uuid,
        tags: newAlertTags(uuid, newTags.value),
      }));

      await alertStore.update(updateData);
    } catch (err) {
      error.value = err.message;
    }

    isLoading.value = false;
    if (!error.value) {
      close();
      emit("requestReload");
    }
  }

  function newAlertTags(uuid, tags) {
    const alert = alertTableStore.visibleQueriedAlertById(uuid);
    const alertTags = alert ? alert.tags : [];
    return tagValues(alertTags).concat(tags);
  }

  async function createTags(tags) {
    for (const tag of tags) {
      if (!tagExists(tag)) {
        await NodeTag.create({ value: tag });
        await loadTags();
      }
    }
  }

  function tagExists(tagValue) {
    return storeTagValues.value.includes(tagValue);
  }

  function tagValues(tags) {
    let values = [];
    for (const tag of tags) {
      values.push(tag.value);
    }
    return values;
  }

  function addExistingTag(tagEvent) {
    // Add an existing tag to the list of tags to be added
    newTags.value.push(tagEvent.value.value);
  }

  const allowSubmit = computed(() => {
    return selectedAlertStore.anySelected && newTags.value.length;
  });

  const handleError = () => {
    error.value = null;
    close();
  };

  function close() {
    newTags.value = [];
    modalStore.close(props.name);
  }
</script>
