import { defineStore } from "pinia";

import { useAuthStore } from "./auth";

export const useCurrentUserSettingsStore = defineStore({
  id: "currentUserSettingsStore",

  state: () => {
    const authStore = useAuthStore();
    return {
      queues: {
        alerts: authStore.user.defaultAlertQueue,
        events: authStore.user.defaultEventQueue,
      },
    };
  },
});
