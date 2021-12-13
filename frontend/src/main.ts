import { createApp } from "vue";
import App from "@/App.vue";
import { createPinia } from "pinia";
import PrimeVue from "primevue/config";
import Tooltip from "primevue/tooltip";

import router from "@/router";
import { useAuthStore } from "./stores/auth";

import "primeflex/primeflex.css";
import "primeicons/primeicons.css";
import "primevue/resources/primevue.min.css";
import "primevue/resources/themes/saga-blue/theme.css";

import "camelcase-keys";
import "snakecase-keys";

(async () => {
  const app = createApp(App).use(createPinia());

  const authStore = useAuthStore();
  await authStore.refreshTokens();

  app.use(router).use(PrimeVue);

  app.directive("tooltip", Tooltip);

  app.mount("#app");
})();
