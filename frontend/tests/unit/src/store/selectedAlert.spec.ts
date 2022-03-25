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

    expect(store.multipleSelected).to.equal(true);
  });

  it("will have multipleSelected return false when one or fewer alerts are selected", () => {
    store.selected = ["id1"];

    expect(store.multipleSelected).to.equal(false);
  });

  it("will have anySelected return true when any alerts are selected", () => {
    store.selected = ["id1"];

    expect(store.anySelected).to.equal(true);
  });

  it("will have anySelected return false when no alerts are selected", () => {
    expect(store.anySelected).to.equal(false);
  });
});

describe("selectedAlert Actions", () => {
  it("will add a given string to the selected list upon the select action", () => {
    store.select("id1");

    expect(store.selected.length).to.equal(1);
    expect(store.selected[0]).to.equal("id1");
  });

  it("will remove a given string from the selected list upon the unselect action", () => {
    store.selected = ["id1", "id2"];

    expect(store.selected.length).to.equal(2);
    store.unselect("id1");
    expect(store.selected.length).to.equal(1);
    expect(store.selected[0]).to.equal("id2");
  });

  it("will add a list of strings to the selected list upon the selected action", () => {
    store.selectAll(["id1", "id2", "id3"]);

    expect(store.selected.length).to.equal(3);
    expect(store.selected[0]).to.equal("id1");
    expect(store.selected[1]).to.equal("id2");
    expect(store.selected[2]).to.equal("id3");
  });

  it("will remove all from the selected list upon the unselectAll action", () => {
    store.selected = ["id1", "id2", "id3"];

    expect(store.selected.length).to.equal(3);
    store.unselectAll();
    expect(store.selected.length).to.equal(0);
  });
});
