import { useSelectedAlertStore } from "@/stores/selectedAlert";
import { createCustomPinia } from "@unit/helpers";

createCustomPinia();

const store = useSelectedAlertStore();

describe("selectedAlert Getters", () => {
  beforeEach(() => {
    store.$reset();
  });

  it("multipleSelected will return true when multiple alerts are selected", () => {
    store.selected = ["id1", "id2"];

    expect(store.multipleSelected).toBe(true);
  });

  it("will have multipleSelected return false when one or fewer alerts are selected", () => {
    store.selected = ["id1"];

    expect(store.multipleSelected).toBe(false);
  });

  it("will have anySelected return true when any alerts are selected", () => {
    store.selected = ["id1"];

    expect(store.anySelected).toBe(true);
  });

  it("will have anySelected return false when no alerts are selected", () => {
    expect(store.anySelected).toBe(false);
  });
});

describe("selectedAlert Actions", () => {
  it("will add a given string to the selected list upon the select action", () => {
    store.select("id1");

    expect(store.selected.length).toBe(1);
    expect(store.selected[0]).toBe("id1");
  });

  it("will remove a given string from the selected list upon the unselect action", () => {
    store.selected = ["id1", "id2"];

    expect(store.selected.length).toBe(2);
    store.unselect("id1");
    expect(store.selected.length).toBe(1);
    expect(store.selected[0]).toBe("id2");
  });

  it("will add a list of strings to the selected list upon the selected action", () => {
    store.selectAll(["id1", "id2", "id3"]);

    expect(store.selected.length).toBe(3);
    expect(store.selected[0]).toBe("id1");
    expect(store.selected[1]).toBe("id2");
    expect(store.selected[2]).toBe("id3");
  });

  it("will remove all from the selected list upon the unselectAll action", () => {
    store.selected = ["id1", "id2", "id3"];

    expect(store.selected.length).toBe(3);
    store.unselectAll();
    expect(store.selected.length).toBe(0);
  });
});
