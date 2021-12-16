import { defineStore } from "pinia";
import { userRead } from "@/models/user";
import authApi from "@/services/api/auth";

export const useAuthStore = defineStore({
  id: "authStore",

  state: () => ({
    authenticated: false,
    user: null as unknown as userRead,
  }),

  getters: {
    displayName(): string {
      if (this.authenticated && this.user) {
        return this.user.displayName;
      }

      return "Unauthenticated User";
    },

    isAuthenticated(): boolean {
      return this.authenticated;
    },
  },

  actions: {
    async refreshTokens() {
      await authApi
        .refresh()
        .then(() => {
          this.authenticated = true;
        })
        .catch(() => {
          this.authenticated = false;
        });
    },

    setAuthenticated(value: boolean) {
      this.authenticated = value;
    },
  },
});
