import { describe, it, beforeEach, expect } from "vitest";
import { useModalStore } from "@/stores/modal";
import { createCustomPinia } from "@tests/unitHelpers";

createCustomPinia();

const store = useModalStore();

describe("modal Getters", () => {
  beforeEach(() => {
    store.$reset();
  });

  it("will return null when there is no open/active modal", () => {
    expect(store.active).toStrictEqual(null);
  });

  it("will return the name of the currently active modal (first in the list)", () => {
    store.openModals = ["modal1", "modal2"];

    expect(store.active).toStrictEqual("modal1");
  });
});

describe("modal Actions", () => {
  beforeEach(() => {
    store.$reset();
  });

  it("will add a new modal to the front of the open list upon the open action", () => {
    expect(store.openModals.length).toStrictEqual(0);
    store.open("modal1");
    expect(store.openModals.length).toStrictEqual(1);
    expect(store.openModals[0]).toStrictEqual("modal1");
    store.open("modal2");
    expect(store.openModals.length).toStrictEqual(2);
    expect(store.openModals[0]).toStrictEqual("modal2");
  });
  it("will remove the given modal from the open list upon the close action", () => {
    store.openModals = ["modal1"];

    expect(store.openModals.length).toStrictEqual(1);
    store.close("modal1");
    expect(store.openModals.length).toStrictEqual(0);
  });
});
