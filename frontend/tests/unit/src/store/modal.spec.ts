import { useModalStore } from "@/stores/modal";
import { createCustomPinia } from "@unit/helpers";

createCustomPinia();

const store = useModalStore();

describe("modal Getters", () => {
  beforeEach(() => {
    store.$reset();
  });

  it("will return null when there is no open/active modal", () => {
    expect(store.active).to.equal(null);
  });

  it("will return the name of the currently active modal (first in the list)", () => {
    store.openModals = ["modal1", "modal2"];

    expect(store.active).to.equal("modal1");
  });
});

describe("modal Actions", () => {
  beforeEach(() => {
    store.$reset();
  });

  it("will add a new modal to the front of the open list upon the open action", () => {
    expect(store.openModals.length).to.equal(0);
    store.open("modal1");
    expect(store.openModals.length).to.equal(1);
    expect(store.openModals[0]).to.equal("modal1");
    store.open("modal2");
    expect(store.openModals.length).to.equal(2);
    expect(store.openModals[0]).to.equal("modal2");
  });
  it("will remove the given modal from the open list upon the close action", () => {
    store.openModals = ["modal1"];

    expect(store.openModals.length).to.equal(1);
    store.close("modal1");
    expect(store.openModals.length).to.equal(0);
  });
});
