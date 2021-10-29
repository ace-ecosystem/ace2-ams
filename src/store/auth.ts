class State {
  isLoggedIn = false;
}

const store = {
  namespaced: true,

  state: new State(),

  getters: {
    // eslint-disable-next-line @typescript-eslint/no-unused-vars
    isLoggedIn: (_: State): boolean =>
      !!sessionStorage.getItem("authenticated"),
  },
};

export default store;
