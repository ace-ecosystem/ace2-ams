import { defineStore } from "pinia";
import { userRead } from "@/models/user";
import { User } from "@/services/api/user";

export const useUserStore = defineStore({
  id: "userStore",

  state: () => ({
    items: [] as userRead[],
  }),

  getters: {
    allItems(): userRead[] {
      return this.items;
    },
  },

  actions: {
    async readAll() {
      this.items = await User.readAll();
    },
  },
});
