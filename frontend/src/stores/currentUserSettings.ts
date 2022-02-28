import { defineStore } from "pinia";

import { useAuthStore } from "./auth";

export const useCurrentUserSettingsStore = defineStore({
  id: "currentUserSettingsStore",

  state: () => {
    const authStore = useAuthStore();
    return {
      preferredEventQueue: authStore.user.defaultEventQueue,
      preferredAlertQueue: authStore.user.defaultAlertQueue,
    };
  },
});
