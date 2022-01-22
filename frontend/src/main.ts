import { createApp } from "vue";
import App from "@/App.vue";
import { createPinia } from "pinia";
import PrimeVue from "primevue/config";
import Tooltip from "primevue/tooltip";

import router from "@/router";
import { axiosRefresh } from "@/services/api/axios";
import { useAuthStore } from "@/stores/auth";

import "primeflex/primeflex.css";
import "primeicons/primeicons.css";
import "primevue/resources/primevue.min.css";
import "primevue/resources/themes/saga-blue/theme.css";

import "camelcase-keys";
import "snakecase-keys";

declare global {
  interface Window {
    Cypress: any;
    authStore: any;
  }
}

(async () => {
  const app = createApp(App).use(createPinia());

  // If the application is running under Cypress, set the authStore in the
  // window so that it can be accessed by the tests. This is needed when
  // Cypress signs in programatically instead of via the actual login page.
  // Parts of the application rely on the authenticated user that the login
  // page sets in the authStore.
  if (window.Cypress) {
    const authStore = useAuthStore();
    window.authStore = authStore;
  }

  await axiosRefresh().catch(() => {
    console.error("Must reauthenticate");
  });

  app.use(router).use(PrimeVue);

  app.directive("tooltip", Tooltip);

  app.mount("#app");
})();
