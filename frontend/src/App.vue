<!-- App.vue -->
<!-- Main Entrypoint to the app -->

<template>
  <TheHeader />
  <router-view />
</template>

<script>
  import { mapState } from "pinia";

  import TheHeader from "@/components/UserInterface/TheHeader";

  import { populateCommonStores } from "@/etc/helpers";
  import authApi from "@/services/api/auth";
  import { useAuthStore } from "@/stores/auth";

  export default {
    components: { TheHeader },

    computed: {
      ...mapState(useAuthStore, ["isAuthenticated"]),
    },

    async created() {
      // Create a 60s interval to check if the user is still authenticated.
      // If they are not authenticated, kick them back to the Login page.
      setInterval(() => {
        if (this.$route.name !== "Login") {
          authApi.validate().catch(() => {
            console.debug("redirecting to login page");
            this.$router.replace({ name: "Login" });
          });
        }
      }, 60000);

      // If the user is authenticated, some of the stores with items
      // from the API that will be used throughout the application.
      if (this.isAuthenticated) {
        await populateCommonStores();
      }
    },
  };
</script>
