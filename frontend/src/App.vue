<!-- App.vue -->
<!-- Main Entrypoint to the app -->

<template>
  <TheHeader />
  <router-view />
</template>

<script>
  import { mapActions, mapState } from "pinia";

  import TheHeader from "@/components/UserInterface/TheHeader";
  import authApi from "@/services/api/auth";
  import { alertQueueStore } from "@/stores/alertQueue";
  import { alertTypeStore } from "@/stores/alertType";
  import { useAuthStore } from "@/stores/auth";
  import { useNodeDirectiveStore } from "@/stores/nodeDirective";
  import { useObservableTypeStore } from "@/stores/observableType";
  import { useUserStore } from "@/stores/user";

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

      // If the user is authenticated, populate the stores with items from the
      // API that will be used throughout the application.
      if (this.isAuthenticated) {
        const promises = [];

        promises.push(this.readAllAlertQueues());
        promises.push(this.readAllAlertTypes());
        promises.push(this.readAllNodeDirectives());
        promises.push(this.readAllObservableTypes());
        promises.push(this.readAllUsers());

        await Promise.all(promises).catch((error) => {
          throw error;
        });
      }
    },

    methods: {
      ...mapActions(alertQueueStore, { readAllAlertQueues: "readAll" }),
      ...mapActions(alertTypeStore, { readAllAlertTypes: "readAll" }),
      ...mapActions(useNodeDirectiveStore, {
        readAllNodeDirectives: "readAll",
      }),
      ...mapActions(useObservableTypeStore, {
        readAllObservableTypes: "readAll",
      }),
      ...mapActions(useUserStore, { readAllUsers: "readAll" }),
    },
  };
</script>
