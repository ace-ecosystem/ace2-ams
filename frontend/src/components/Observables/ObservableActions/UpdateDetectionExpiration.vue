<!-- UpdateDetectionExpiration.vue -->
<!-- 'UpdateDetectionExpiration' action modal, allows user to update an observables FAQueue expiration datetime -->

<template>
  <BaseModal :name="name" header="Update Detection Expiration Time">
    <Message v-if="error" severity="error" data-cy="error-banner">{{
      error
    }}</Message>
    <div>
      <b>Current Expiration Time (UTC)</b>
      <span>{{ currentExpirationTime }}</span>
      <br />
      <span>
        <InputSwitch v-model="neverExpires" role="switch" /> This observable
        should never expire.
      </span>
      <br />
      <div v-if="!neverExpires">
        <b>New Expiration Time (UTC)</b>
        <Calendar
          v-model="newExpirationTime"
          data-cy="new-exipration-time-input"
          placeholder="Enter a valid date"
          autocomplete="off"
          :show-time="true"
          :show-seconds="true"
        />
      </div>
    </div>
    <template #footer>
      <Button
        role="button"
        label="Nevermind"
        icon="pi pi-times"
        class="p-button-text"
        @click="close"
      />
      <Button
        label="Do it!"
        icon="pi pi-check"
        role="button"
        :disabled="disabled"
        @click="update"
      />
    </template>
  </BaseModal>
</template>

<script setup lang="ts">
  import { defineProps, computed, PropType, ref, onMounted } from "vue";

  import Button from "primevue/button";
  import Calendar from "primevue/calendar";
  import BaseModal from "@/components/Modals/BaseModal.vue";

  import { useModalStore } from "@/stores/modal";
  import { observableRead, observableTreeRead } from "@/models/observable";
  import InputSwitch from "primevue/inputswitch";
  import { ObservableInstance } from "@/services/api/observable";
  import { useAlertStore } from "@/stores/alert";
  import Message from "primevue/message";

  const newExpirationTime = ref<Date>();
  const currentExpirationTime = ref<string>();

  const modalStore = useModalStore();
  const neverExpires = ref(false);
  const error = ref<string>();

  onMounted(() => {
    if (props.observable.expiresOn === null) {
      neverExpires.value = true;
    } else {
      currentExpirationTime.value = props.observable.expiresOn.toUTCString();
    }
  });

  const props = defineProps({
    name: { type: String, required: true },
    observable: {
      type: Object as PropType<observableTreeRead | observableRead>,
      required: true,
    },
  });

  const disabled = computed(() => {
    return !(neverExpires.value || newExpirationTime.value != null);
  });

  const alertStore = useAlertStore();

  const update = async () => {
    let newValue = neverExpires.value ? null : newExpirationTime.value;
    try {
      await ObservableInstance.update(props.observable.uuid, {
        expiresOn: newValue,
      });
      alertStore.requestReload = true;
      close();
    } catch (e: unknown) {
      if (typeof e === "string") {
        error.value = e;
      } else if (e instanceof Error) {
        error.value = e.message;
      }
    }
  };

  const close = () => {
    if (props.observable.expiresOn === null) {
      neverExpires.value = true;
    }
    newExpirationTime.value = undefined;
    modalStore.close(props.name);
  };
</script>
