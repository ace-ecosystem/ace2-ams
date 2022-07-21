<!-- TheHeader.vue -->
<!-- Header / Navigation bar -->

<template>
  <Menubar>
    <template #start>
      <img alt="ACE logo" src="../../assets/logo.jpg" />
      <span v-if="authStore.isAuthenticated" name="logged-in-links">
        <router-link class="p-m-1" to="/analyze"
          ><Button label="Analyze" class="p-button-raised"
        /></router-link>
        <router-link class="p-m-1" to="/manage_alerts"
          ><Button label="Alerts" class="p-button-raised"
        /></router-link>
        <router-link class="p-m-1" to="/manage_events"
          ><Button label="Events" class="p-button-raised"
        /></router-link>
      </span>
    </template>
    <template #end>
      <span v-if="authStore.isAuthenticated" name="logged-in-buttons">
        <Button icon="pi pi-bell" class="p-button-rounded p-m-1" />
        <router-link to="/"
          ><Button icon="pi pi-cog" class="p-button-rounded p-m-1"
        /></router-link>
        <Button icon="pi pi-user" class="p-button-rounded p-m-1" />
        <router-link :to="{ name: 'Login' }">
          <Button
            icon="pi pi-sign-out"
            class="p-button-rounded p-m-1"
            @click="logout"
        /></router-link>
      </span>
    </template>
  </Menubar>
</template>

<script setup lang="ts">
  import { useRouter } from "vue-router";

  import Menubar from "primevue/menubar";
  import Button from "primevue/button";

  import { useAuthStore } from "@/stores/auth";

  import authApi from "@/services/api/auth";

  const router = useRouter();

  const authStore = useAuthStore();

  async function logout() {
    await authApi.logout().catch((error) => {
      throw error;
    });

    router.replace({ name: "Login" });
  }
</script>
