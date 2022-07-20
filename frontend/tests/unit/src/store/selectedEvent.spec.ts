import { describe, it, beforeEach, expect } from "vitest";
import { useSelectedEventStore } from "@/stores/selectedEvent";
import { createCustomPinia } from "@tests/unitHelpers";

createCustomPinia();

const store = useSelectedEventStore();

describe("selectedEvent Getters", () => {
  beforeEach(() => {
    store.$reset();
  });

  it("multipleSelected will return true when multiple events are selected", () => {
    store.selected = ["id1", "id2"];

    expect(store.multipleSelected).toStrictEqual(true);
  });

  it("will have multipleSelected return false when one or fewer events are selected", () => {
    store.selected = ["id1"];

    expect(store.multipleSelected).toStrictEqual(false);
  });

  it("will have anySelected return true when any events are selected", () => {
    store.selected = ["id1"];

    expect(store.anySelected).toStrictEqual(true);
  });

  it("will have anySelected return false when no events are selected", () => {
    expect(store.anySelected).toStrictEqual(false);
  });
});

describe("selectedEvent Actions", () => {
  it("will add a given string to the selected list upon the select action", () => {
    store.select("id1");

    expect(store.selected.length).toStrictEqual(1);
    expect(store.selected[0]).toStrictEqual("id1");
  });

  it("will remove a given string from the selected list upon the unselect action", () => {
    store.selected = ["id1", "id2"];

    expect(store.selected.length).toStrictEqual(2);
    store.unselect("id1");
    expect(store.selected.length).toStrictEqual(1);
    expect(store.selected[0]).toStrictEqual("id2");
  });

  it("will add a list of strings to the selected list upon the selected action", () => {
    store.selectAll(["id1", "id2", "id3"]);

    expect(store.selected.length).toStrictEqual(3);
    expect(store.selected[0]).toStrictEqual("id1");
    expect(store.selected[1]).toStrictEqual("id2");
    expect(store.selected[2]).toStrictEqual("id3");
  });

  it("will remove all from the selected list upon the unselectAll action", () => {
    store.selected = ["id1", "id2", "id3"];

    expect(store.selected.length).toStrictEqual(3);
    store.unselectAll();
    expect(store.selected.length).toStrictEqual(0);
  });
});
