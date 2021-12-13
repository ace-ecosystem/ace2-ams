// Modal manager that handles opening/closing of modals
// Allows modal components to be (cleanly) called from buttons in parent component, as well as opening a modal from a modal
// Ex. Disposition > Save to Event
// Credit to: https://xon5.medium.com/a-vue-modal-manager-via-vuex-1ae530c8649

import { defineStore } from "pinia";

export const useModalStore = defineStore({
  id: "modalStore",

  state: () => ({
    openModals: [] as string[],
  }),

  getters: {
    active(): string | null {
      return this.openModals.length > 0 ? this.openModals[0] : null;
    },
  },

  actions: {
    open(name: string) {
      this.openModals.unshift(name);
    },

    close(name: string) {
      this.openModals = this.openModals.filter((n) => n !== name);
    },
  },
});
