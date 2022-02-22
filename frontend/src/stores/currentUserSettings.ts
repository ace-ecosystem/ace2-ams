import { eventQueueRead } from "@/models/eventQueue";
import { defineStore } from "pinia";

export const useCurrentUserSettingsStore = defineStore({
  id: "currentUserSettingsStore",

  state: () => ({
    preferredEventQueue: null as unknown as eventQueueRead,
  }),
});
