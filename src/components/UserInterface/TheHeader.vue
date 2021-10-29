<!-- TheHeader.vue -->
<!-- Header / Navigation bar -->

<template>
  <Menubar>
    <template #start>
      <img alt="ACE logo" src="../../assets/logo.jpg" />
      <router-link class="p-m-1" to="/analyze"
        ><Button label="Analyze" class="p-button-raised"
      /></router-link>
      <router-link class="p-m-1" to="/manage_alerts"
        ><Button label="Alerts" class="p-button-raised"
      /></router-link>
      <router-link class="p-m-1" to="/"
        ><Button label="Events" class="p-button-raised"
      /></router-link>
    </template>
    <template #end>
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
    </template>
  </Menubar>
</template>

<script>
  import Menubar from "primevue/menubar";
  import Button from "primevue/button";

  import auth from "@/services/api/auth";

  export default {
    name: "TheHeader",
    components: { Menubar, Button },
    methods: {
      async logout() {
        await auth.logout().catch((error) => {
          throw error;
        });

        this.$router.replace({ name: "Login" });
      },
    },
  };
</script>
