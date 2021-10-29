<!-- App.vue -->
<!-- Main Entrypoint to the app -->

<template>
  <TheHeader />
  <router-view />
</template>

<script>
  import TheHeader from "@/components/UserInterface/TheHeader";
  import auth from "@/services/api/auth";

  export default {
    components: { TheHeader },

    created() {
      setInterval(() => {
        if (this.$route.name !== "Login") {
          auth.validate().catch(() => {
            console.debug("redirecting to login page");
            this.$router.replace({ name: "Login" });
          });
        }
      }, 60000);
    },
  };
</script>
