import { defineStore } from "pinia";
import { userRead } from "@/models/user";

export const useAuthStore = defineStore({
  id: "authStore",

  state: () => ({
    user: null as unknown as userRead,
  }),

  getters: {
    isAuthenticated(): boolean {
      return !!this.user;
    },
  },
});
