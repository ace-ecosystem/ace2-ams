<!-- TagModal.vue -->
<!-- 'Tag' action modal, agnostic to what is being tagged -->

<template>
  <BaseModal :name="name" header="Add Tags">
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
      <Button label="Add" icon="pi pi-check" @click="addTags" />
    </template>
  </BaseModal>
</template>

<script setup>
  import { defineProps, onMounted, ref } from "vue";

  import Button from "primevue/button";
  import Chips from "primevue/chips";
  import Dropdown from "primevue/dropdown";

  import BaseModal from "@/components/Modals/BaseModal";

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

  import { NodeTag } from "@/services/api/nodeTag";

  const props = defineProps({
    name: { type: String, required: true },
  });

  const error = ref(null);
  const isLoading = ref(false);
  const newTags = ref([]);
  const storeTagValues = ref([]);

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
      for (const uuid of selectedAlertStore.selected) {
        const alert = alertTableStore.visibleQueriedAlertById(uuid);
        await alertStore.update(uuid, {
          tags: tagValues(alert.tags).concat(newTags.value),
        });
      }
    } catch (err) {
      error.value = err.message || "Something went wrong!";
    }

    isLoading.value = false;
    if (!error.value) {
      close();
    }
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

  function addExistingTag(event) {
    // Add an existing tag to the list of tags to be added
    newTags.value.push(event.value.value);
  }
  
  function close() {
    newTags.value = [];
    modalStore.close(props.name);
  }
</script>
