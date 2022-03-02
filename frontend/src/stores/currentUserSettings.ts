import { defineStore } from "pinia";

import { useAuthStore } from "./auth";

export const useCurrentUserSettingsStore = defineStore({
  id: "currentUserSettingsStore",

  state: () => {
    const authStore = useAuthStore();
    return {
      queues: {
        alerts: authStore.user ? authStore.user.defaultAlertQueue : null,
        events: authStore.user ? authStore.user.defaultEventQueue : null,
      },
    };
  },
});
