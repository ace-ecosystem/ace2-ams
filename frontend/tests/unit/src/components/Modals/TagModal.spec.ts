import TagModal from "@/components/Modals/TagModal.vue";
import { TestingOptions } from "@pinia/testing";
import { mount } from "@vue/test-utils";
import PrimeVue from "primevue/config";
import nock from "nock";

import myNock from "@unit/services/api/nock";
import { useModalStore } from "@/stores/modal";
import { useUserStore } from "@/stores/user";
import { createCustomPinia } from "@unit/helpers";

function factory(options?: TestingOptions) {
  const wrapper = mount(TagModal, {
    attachTo: document.body,
    global: {
      plugins: [createCustomPinia(options), PrimeVue],
      provide: { nodeType: "alerts" },
    },
    props: { name: "TagModal" },
  });

  const modalStore = useModalStore();
  const userStore = useUserStore();

  return { wrapper, modalStore, userStore };
}

describe("TagModal.vue", () => {
  afterEach(() => {
    nock.cleanAll();
  });

  it("renders", () => {
    const { wrapper } = factory();

    expect(wrapper.exists()).toBe(true);
  });
  it("has the correctly assigned name 'TagModal'", () => {
    const { wrapper } = factory();

    expect(wrapper.vm.name).toEqual("TagModal");
  });

  it("will clear the 'error' property when handleError is called", () => {
    const { wrapper } = factory();

    wrapper.vm.error = "Call failed";

    expect(wrapper.vm.error).toEqual("Call failed");
    wrapper.vm.handleError();
    expect(wrapper.vm.error).toBeNull();
  });

  it("will remove the TagModal from open modals store and clear newTags on close", () => {
    const { wrapper } = factory();

    wrapper.vm.newTags = ["tag1", "tag2"];
    wrapper.vm.modalStore.open("TagModal");

    wrapper.vm.close();

    expect(wrapper.vm.modalStore.openModals).toStrictEqual([]);
  });

  it("correctly computes in allowSubmit whether the submit button should be enabled'", () => {
    const { wrapper } = factory();

    // No alerts selected and no value set
    wrapper.vm.selectedStore.selected = [];
    wrapper.vm.newTags = [];
    expect(wrapper.vm.allowSubmit).toBeFalsy();
    // Alerts selected and no value set
    wrapper.vm.selectedStore.selected = ["1", "2"];
    wrapper.vm.newTags = [];
    expect(wrapper.vm.allowSubmit).toBeFalsy();
    // No alerts selected and value set
    wrapper.vm.selectedStore.selected = [];
    wrapper.vm.newTags = ["tag1", "tag2"];
    expect(wrapper.vm.allowSubmit).toBeFalsy();
    // Alerts selected and value set
    wrapper.vm.selectedStore.selected = ["1", "2"];
    wrapper.vm.newTags = ["tag1", "tag2"];
    expect(wrapper.vm.allowSubmit).toBeTruthy();
  });

  it("will readAll available tags and add their values to storeTagValues on loadTags", async () => {
    myNock
      .get("/node/tag/?offset=0")
      .twice()
      .reply(200, { items: [{ value: "tag1" }, { value: "tag3" }] });

    const { wrapper } = factory({ stubActions: false });
    await wrapper.vm.loadTags();

    expect(wrapper.vm.storeTagValues).toEqual(["tag1", "tag3"]);
  });

  it("will create any non-existing tags and reload the new set on createTags", async () => {
    myNock
      .get("/node/tag/?offset=0")
      .once()
      .reply(200, { items: [{ value: "tag1" }, { value: "tag3" }] });
    myNock
      .get("/node/tag/?offset=0")
      .once()
      .reply(200, {
        items: [{ value: "tag1" }, { value: "tag2" }, { value: "tag3" }],
      });
    myNock.post("/node/tag/", { value: "tag2" }).reply(200);

    const { wrapper } = factory({ stubActions: false });
    await wrapper.vm.loadTags();
    expect(wrapper.vm.storeTagValues).toEqual(["tag1", "tag3"]);

    wrapper.vm.storeTagValues = ["tag1", "tag3"];
    await wrapper.vm.createTags(["tag2"]);

    expect(wrapper.vm.storeTagValues).toEqual(["tag1", "tag2", "tag3"]);
  });

  it("will correctly return whether storeTagValues includes a tag on tagExists", () => {
    const { wrapper } = factory();

    wrapper.vm.storeTagValues = ["tag1", "tag3"];

    expect(wrapper.vm.tagExists("tag1")).toBeTruthy();
    expect(wrapper.vm.tagExists("tag2")).toBeFalsy();
  });

  it("will create a list of tag values given a list of tag objects", () => {
    const { wrapper } = factory();

    const res = wrapper.vm.tagValues([{ value: "tag1" }, { value: "tag3" }]);

    expect(res).toEqual(["tag1", "tag3"]);
  });

  it("will add an existing tag value to the newTags list on addExistingTag", () => {
    const { wrapper } = factory();

    wrapper.vm.addExistingTag({ value: { value: "tag1" } });

    expect(wrapper.vm.newTags).toEqual(["tag1"]);
  });

  it("will correctly combine existing alert tags with new tags on newNodeTags", () => {
    myNock
      .get("/node/tag/?offset=0")
      .twice()
      .reply(200, { items: [{ value: "tag1" }, { value: "tag3" }] });
    const { wrapper } = factory({ stubActions: false });

    wrapper.vm.tableStore.visibleQueriedItems = [
      { uuid: "uuid1", tags: [] },
      { uuid: "uuid2", tags: [{ value: "tag1" }] },
    ];

    const res1 = wrapper.vm.newNodeTags("uuid1", ["tag2", "tag3"]);
    const res2 = wrapper.vm.newNodeTags("uuid2", ["tag2", "tag3"]);
    const res3 = wrapper.vm.newNodeTags("uuid3", ["tag2", "tag3"]);

    expect(res1).toEqual(["tag2", "tag3"]);
    expect(res2).toEqual(["tag1", "tag2", "tag3"]);
    expect(res3).toEqual(["tag2", "tag3"]);
  });

  it("will close the modal when addTags has successfully finished", async () => {
    myNock
      .get("/node/tag/?offset=0")
      .once()
      .reply(200, { items: [{ value: "tag1" }, { value: "tag3" }] });
    myNock
      .get("/node/tag/?offset=0")
      .once()
      .reply(200, {
        items: [{ value: "tag1" }, { value: "tag2" }, { value: "tag3" }],
      });
    myNock.post("/node/tag/", { value: "tag2" }).reply(200);
    myNock.options("/alert/").reply(200, "Success");
    myNock
      .patch("/alert/", [
        { uuid: "uuid1", tags: ["tag1", "tag2"] },
        { uuid: "uuid2", tags: ["tag1", "tag1", "tag2"] },
      ])
      .reply(200, "Success");

    const { wrapper } = factory({ stubActions: false });

    // Set the selected alert
    wrapper.vm.selectedStore.selected = ["uuid1", "uuid2"];

    // Set data
    wrapper.vm.storeTagValues = ["tag1", "tag3"];
    wrapper.vm.newTags = ["tag1", "tag2"];
    wrapper.vm.tableStore.visibleQueriedItems = [
      { uuid: "uuid1", tags: [] },
      { uuid: "uuid2", tags: [{ value: "tag1" }] },
    ];

    expect(wrapper.vm.modalStore.openModals).toStrictEqual([]);
    wrapper.vm.modalStore.open("TagModal");
    expect(wrapper.vm.modalStore.openModals).toStrictEqual(["TagModal"]);
    await wrapper.vm.addTags();
    expect(wrapper.vm.newTags).toEqual([]);
    expect(wrapper.vm.modalStore.openModals).toStrictEqual([]);
    expect(wrapper.emitted("requestReload")).toBeTruthy();
  });

  it("will not close the modal and will set the 'error' property when addTags fails", async () => {
    myNock
      .get("/node/tag/?offset=0")
      .once()
      .reply(200, { items: [{ value: "tag1" }, { value: "tag3" }] });
    myNock
      .get("/node/tag/?offset=0")
      .once()
      .reply(200, {
        items: [{ value: "tag1" }, { value: "tag2" }, { value: "tag3" }],
      });
    myNock.post("/node/tag/", { value: "tag2" }).reply(200);
    const updateAlert = myNock
      .options("/alert/")
      .reply(200, "Success")
      .patch("/alert/")
      .reply(403, "Unauthorized");

    const { wrapper } = factory({ stubActions: false });
    await wrapper.vm.loadTags();

    wrapper.vm.selectedStore.selected = ["uuid1", "uuid2"];
    wrapper.vm.storeTagValues = ["tag1", "tag3"];
    wrapper.vm.newTags = ["tag1", "tag2"];
    wrapper.vm.tableStore.visibleQueriedItems = [
      { uuid: "uuid1", tags: [] },
      { uuid: "uuid2", tags: [{ value: "tag1" }] },
    ];

    expect(wrapper.vm.modalStore.openModals).toStrictEqual([]);
    wrapper.vm.modalStore.open("TagModal");
    expect(wrapper.vm.modalStore.openModals).toStrictEqual(["TagModal"]);
    await wrapper.vm.addTags();
    // TODO: Figure out why this no longer works
    // expect(updateAlert.isDone()).toBe(true);
    expect(wrapper.vm.error).toEqual("Request failed with status code 403");
    expect(wrapper.vm.newTags).toEqual(["tag1", "tag2"]);
    expect(wrapper.vm.modalStore.openModals).toStrictEqual(["TagModal"]);
    expect(wrapper.emitted("requestReload")).toBeFalsy();
  });
});
