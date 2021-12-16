import { createTestingPinia } from "@pinia/testing";
import { useModalStore } from "@/stores/modal";

createTestingPinia();

describe("modal Getters", () => {
  it("will return null when there is no open/active modal", () => {
    const store = useModalStore();
    store.$reset();

    expect(store.active).toBeNull();
  });

  it("will return the name of the currently active modal (first in the list)", () => {
    const store = useModalStore();
    store.$reset();

    store.openModals = ["modal1", "modal2"];

    expect(store.active).toBe("modal1");
  });
});

describe("modal Actions", () => {
  it("will add a new modal to the front of the open list upon the open action", () => {
    const store = useModalStore();
    store.$reset();

    expect(store.openModals.length).toBe(0);
    store.open("modal1");
    expect(store.openModals.length).toBe(1);
    expect(store.openModals[0]).toBe("modal1");
    store.open("modal2");
    expect(store.openModals.length).toBe(2);
    expect(store.openModals[0]).toBe("modal2");
  });
  it("will remove the given modal from the open list upon the close action", () => {
    const store = useModalStore();
    store.$reset();

    store.openModals = ["modal1"];

    expect(store.openModals.length).toBe(1);
    store.close("modal1");
    expect(store.openModals.length).toBe(0);
  });
});
