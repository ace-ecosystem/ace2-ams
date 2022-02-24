import { createApp } from "vue";
import App from "@/App.vue";
import { createPinia } from "pinia";
import PrimeVue from "primevue/config";
import Tooltip from "primevue/tooltip";

import router from "@/router";
import { axiosRefresh } from "@/services/api/axios";

import "primeflex/primeflex.css";
import "primeicons/primeicons.css";
import "primevue/resources/primevue.min.css";
import "primevue/resources/themes/saga-blue/theme.css";

import "camelcase-keys";
import "snakecase-keys";

import { configuration } from "@/etc/configuration/index";
import { testConfiguration } from "@/etc/configuration/test/index";

const testingModeEnabled = import.meta.env.VITE_TESTING;
export const config =
  testingModeEnabled === "yes" ? testConfiguration : configuration;

(async () => {
  const app = createApp(App).use(createPinia());

  await axiosRefresh().catch(() => {
    console.error("Must reauthenticate");
  });

  app.use(router).use(PrimeVue);

  app.directive("tooltip", Tooltip);

  app.mount("#app");
})();
