import { defineStore } from "pinia";

export const useRecentCommentsStore = defineStore({
  id: "recentCommentsStore",

  state: () => ({
    recentComments: JSON.parse(
      localStorage.getItem("aceComments") || "[]",
    ) as string[],
  }),

  actions: {
    addComment(comment: string) {
      // push to the front if the comment is already in the list
      if (this.recentComments.includes(comment)) {
        this.recentComments = this.recentComments.filter((c) => c != comment);
      }
      if (this.recentComments.length == 10) {
        this.recentComments.pop();
      }
      this.recentComments.unshift(comment);
      localStorage.setItem("aceComments", JSON.stringify(this.recentComments));
    },

    removeComment(comment: string) {
      this.recentComments = this.recentComments.filter((c) => c != comment);
      localStorage.setItem("aceComments", JSON.stringify(this.recentComments));
    },
  },
});
