<!-- DeleteModal.vue -->
<!-- 'Delete' action modal, agnostic to what type of data is being deleted -->

<template>
  <BaseModal :name="name" header="Update Detection Expiration Time">
    <div>
      <b>Current Expiration Time (UTC)</b>
      <span>{{ observable.expiresOn }}</span>
      <br />
      <span>
        <InputSwitch v-model="neverExpires" /> This observable should never
        expire.
      </span>
      <br />
      <div v-if="!neverExpires">
        <b>New Expiration Time (UTC)</b>
        <Calendar
          v-model="newExpirationTime"
          autocomplete="off"
          :show-time="true"
          :show-seconds="true"
        />
      </div>
    </div>
    <template #footer>
      <Button
        label="Nevermind"
        icon="pi pi-times"
        class="p-button-text"
        @click="close"
      />
      <Button label="Do it!" icon="pi pi-check" @click="update" />
    </template>
  </BaseModal>
</template>

<script setup lang="ts">
  import { defineProps, PropType, ref, onMounted } from "vue";

  import Button from "primevue/button";
  import Calendar from "primevue/calendar";
  import BaseModal from "@/components/Modals/BaseModal.vue";

  import { useModalStore } from "@/stores/modal";
  import { observableRead, observableTreeRead } from "@/models/observable";
  import InputSwitch from "primevue/inputswitch";
  import { ObservableInstance } from "@/services/api/observable";
  import { useAlertStore } from "@/stores/alert";

  const newExpirationTime = ref<Date>();

  const modalStore = useModalStore();
  const neverExpires = ref(false);

  onMounted(() => {
    if (props.observable.expiresOn === null) {
      neverExpires.value = true;
    }
  });

  const props = defineProps({
    name: { type: String, required: true },
    observable: {
      type: Object as PropType<observableTreeRead | observableRead>,
      required: true,
    },
  });

  const alertStore = useAlertStore();

  const update = async () => {
    if (neverExpires.value) {
      await ObservableInstance.update(props.observable.uuid, {
        expiresOn: null,
      });
    } else if (newExpirationTime.value) {
      await ObservableInstance.update(props.observable.uuid, {
        expiresOn: newExpirationTime.value,
      });
    }
    alertStore.requestReload = true;
    close();
  };

  const close = () => {
    if (props.observable.expiresOn === null) {
      neverExpires.value = true;
    }
    newExpirationTime.value = undefined;
    modalStore.close(props.name);
  };
</script>
