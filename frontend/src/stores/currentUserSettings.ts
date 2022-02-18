import { defineStore } from "pinia";

export const useCurrentUserSettingsStore = defineStore({
  id: "currentUserSettingsStore",

  state: () => ({
    preferredEventQueue: null as unknown as boolean,
  }),
});
