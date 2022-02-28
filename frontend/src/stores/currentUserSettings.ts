import { useAuthStore } from "./auth";
import { defineStore } from "pinia";

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
