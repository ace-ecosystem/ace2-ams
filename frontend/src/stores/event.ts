import { defineStore } from "pinia";
import { eventRead, eventUpdate } from "@/models/event";
import { Event } from "@/services/api/event";
import { UUID } from "@/models/base";

export const useEventStore = defineStore({
  id: "eventStore",

  state: () => ({
    open: null as unknown as eventRead,

    // whether the event should be reloaded
    requestReload: false,
  }),

  actions: {
    async read(uuid: UUID) {
      await Event.read(uuid)
        .then((event) => {
          this.open = event;
        })
        .catch((error) => {
          throw error;
        });
    },

    async update(data: eventUpdate[]) {
      // once we get around to updating events, we will need to update the base api service to have a
      // 'getAfterUpdate' option like there is for 'create'
      // then we can reset the open/queried event(s)
      await Event.update(data).catch((error) => {
        throw error;
      });
    },
  },
});
