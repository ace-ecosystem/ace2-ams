<!-- App.vue -->
<!-- Main Entrypoint to the app -->

<template>
  <TheHeader />
  <router-view />
</template>

<script setup>
  import { onBeforeMount } from "vue";
  import { useRoute, useRouter } from "vue-router";

  import TheHeader from "@/components/UserInterface/TheHeader";
  import {
    populateCommonStores,
    dateParser,
    setUserDefaults,
  } from "@/etc/helpers";
  import authApi from "@/services/api/auth";
  import { useAuthStore } from "@/stores/auth";
  import { useFilterStore } from "@/stores/filter";

  const authStore = useAuthStore();

  onBeforeMount(async () => {
    const route = useRoute();
    const router = useRouter();

    // Create a 60s interval to check if the user is still authenticated.
    // If they are not authenticated, kick them back to the Login page.
    setInterval(async () => {
      if (route.name !== "Login") {
        await authApi.validate().catch(() => {
          console.debug("redirecting to login page");
          router.replace({ name: "Login" });
        });
      }
    }, 60000);

    // If the user is authenticated, load their most recent filters from
    // localStorage and populate some of the stores with items from
    // the API that will be used throughout the application.
    if (authStore.isAuthenticated) {
      const filterStore = useFilterStore();
      filterStore.$state = JSON.parse(
        localStorage.getItem("aceFilters"),
        dateParser,
      );

      await populateCommonStores();
      setUserDefaults();
    }
  });
</script>
