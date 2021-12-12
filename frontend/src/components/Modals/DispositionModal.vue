<!-- DispositionModal.vue -->
<!-- 'Disposition' alert action modal, contains trigger to open SaveToEvent modal -->

<template>
  <BaseModal :name="name" header="Set Disposition">
    <div class="p-m-1 p-grid p-fluid p-formgrid p-grid">
      <div class="p-field p-col">
        <div
          v-for="disposition of dispositions"
          :key="disposition"
          class="p-field-radiobutton p-inputgroup"
        >
          <RadioButton
            :id="disposition"
            v-model="newDisposition"
            name="disposition"
            :value="disposition"
          />
          <label :for="disposition">{{ disposition }}</label>
        </div>
      </div>
      <div class="p-field p-col">
        <Textarea
          v-model="dispositionComment"
          :auto-resize="true"
          rows="5"
          cols="30"
          placeholder="Add a comment..."
        />
        <Dropdown
          v-model="dispositionComment"
          :options="suggestedComments"
          :show-clear="true"
          placeholder="Select from a past comment"
        />
      </div>
    </div>
    <template #footer>
      <Button label="Save" class="p-button-outlined" @click="close" />
      <Button
        v-if="showAddToEventButton"
        label="Save to Event"
        class="p-button-raised"
        @click="open('SaveToEventModal')"
      />
    </template>
    <!--  SAVE TO EVENT  -->
    <template #child>
      <SaveToEventModal @save-to-event="close" />
    </template>
  </BaseModal>
</template>

<script setup>
  import { computed, defineProps, ref } from "vue";

  import Button from "primevue/button";
  import Dropdown from "primevue/dropdown";
  import RadioButton from "primevue/radiobutton";
  import Textarea from "primevue/textarea";

  import BaseModal from "@/components/Modals/BaseModal";
  import SaveToEventModal from "@/components/Modals/SaveToEventModal";

  import { useModalStore } from "@/stores/modal";

  const modalStore = useModalStore();

  const props = defineProps({
    name: { type: String, required: true },
  });

  const newDisposition = ref(null);
  const dispositions = ref([
    "FALSE_POSITIVE",
    "WEAPONIZATION",
    "COMMAND_AND_CONTROL",
  ]);
  const dispositionComment = ref(null);
  const elevated_dispositions = ref(["COMMAND_AND_CONTROL"]);
  const suggestedComments = ref(["this is an old comment", "and another"]);

  const showAddToEventButton = computed(() => {
    // Only show add to event button if selected disposition is an 'elevated' disposition
    return elevated_dispositions.value.includes(newDisposition.value);
  });

  const close = () => {
    modalStore.close(props.name);
  };

  const open = (name) => {
    modalStore.open(name);
  };
</script>
