import { alertQueueRead } from '@/models/alertQueue';
import { eventQueueRead } from "@/models/eventQueue";
import { defineStore } from "pinia";

export const useCurrentUserSettingsStore = defineStore({
  id: "currentUserSettingsStore",

  state: () => ({
    preferredEventQueue: null as unknown as eventQueueRead,
    preferredAlertQueue: null as unknown as alertQueueRead,
  }),
});
