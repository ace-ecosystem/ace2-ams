import TagModal from "@/components/Modals/TagModal.vue";
import { createTestingPinia, TestingOptions } from "@pinia/testing";
import { mount } from "@vue/test-utils";
import PrimeVue from "primevue/config";
import nock from "nock";

import myNock from "@unit/services/api/nock";
import { useModalStore } from "@/stores/modal";
import { useSelectedAlertStore } from "@/stores/selectedAlert";
import { useUserStore } from "@/stores/user";

function factory(options?: TestingOptions) {
  const wrapper = mount(TagModal, {
    attachTo: document.body,
    global: {
      plugins: [createTestingPinia(options), PrimeVue],
    },
    props: { name: "TagModal" },
  });

  const modalStore = useModalStore();
  const selectedAlertStore = useSelectedAlertStore();
  const userStore = useUserStore();

  return { wrapper, modalStore, selectedAlertStore, userStore };
}

describe("TagModal.vue", () => {
  afterEach(() => {
    nock.abortPendingRequests();
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

    wrapper.vm.storeTagValues = ["tag1", "tag3"];
    wrapper.vm.createTags(["tag2"]);

    await wrapper.vm.loadTags();

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

  it("will correctly combine existing alert tags with new tags on newAlertTags", () => {
    myNock
      .get("/node/tag/?offset=0")
      .twice()
      .reply(200, { items: [{ value: "tag1" }, { value: "tag3" }] });
    const { wrapper } = factory({ stubActions: false });

    wrapper.vm.alertTableStore.visibleQueriedAlerts = [
      { uuid: "uuid1", tags: [] },
      { uuid: "uuid2", tags: [{ value: "tag1" }] },
    ];

    const res1 = wrapper.vm.newAlertTags("uuid1", ["tag2", "tag3"]);
    const res2 = wrapper.vm.newAlertTags("uuid2", ["tag2", "tag3"]);
    const res3 = wrapper.vm.newAlertTags("uuid3", ["tag2", "tag3"]);

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
    myNock.options("/alert/uuid1").reply(200, "Success");
    myNock
      .patch("/alert/uuid1", '{"tags":["tag1","tag2"]}')
      .reply(200, "Success");
    myNock.options("/alert/uuid2").reply(200, "Success");
    myNock
      .patch("/alert/uuid2", '{"tags":["tag1","tag1","tag2"]}')
      .reply(200, "Success");

    const { wrapper } = factory({ stubActions: false });

    // Set the selected alert
    wrapper.vm.selectedAlertStore.selected = ["uuid1", "uuid2"];

    // Set data
    wrapper.vm.storeTagValues = ["tag1", "tag3"];
    wrapper.vm.newTags = ["tag1", "tag2"];
    wrapper.vm.alertTableStore.visibleQueriedAlerts = [
      { uuid: "uuid1", tags: [] },
      { uuid: "uuid2", tags: [{ value: "tag1" }] },
    ];

    expect(wrapper.vm.modalStore.openModals).toStrictEqual([]);
    wrapper.vm.modalStore.open("TagModal");
    expect(wrapper.vm.modalStore.openModals).toStrictEqual(["TagModal"]);
    await wrapper.vm.addTags();
    expect(wrapper.vm.newTags).toEqual([]);
    expect(wrapper.vm.modalStore.openModals).toStrictEqual([]);
    expect(wrapper.vm.alertTableStore.requestReload).toBeTruthy();
  });

  it("will not close the modal and will set the 'error' property when assignUser fails", async () => {
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
      .options("/alert/uuid1")
      .reply(200, "Success")
      .patch("/alert/uuid1")
      .reply(403, "Unauthorized");

    const { wrapper } = factory({ stubActions: false });

    wrapper.vm.selectedAlertStore.selected = ["uuid1", "uuid2"];
    wrapper.vm.storeTagValues = ["tag1", "tag3"];
    wrapper.vm.newTags = ["tag1", "tag2"];
    wrapper.vm.alertTableStore.visibleQueriedAlerts = [
      { uuid: "uuid1", tags: [] },
      { uuid: "uuid2", tags: [{ value: "tag1" }] },
    ];

    expect(wrapper.vm.modalStore.openModals).toStrictEqual([]);
    wrapper.vm.modalStore.open("TagModal");
    expect(wrapper.vm.modalStore.openModals).toStrictEqual(["TagModal"]);
    await wrapper.vm.addTags();
    expect(updateAlert.isDone()).toBe(true);
    expect(wrapper.vm.error).toEqual("Request failed with status code 403");
    expect(wrapper.vm.newTags).toEqual(["tag1", "tag2"]);
    expect(wrapper.vm.modalStore.openModals).toStrictEqual(["TagModal"]);
    expect(wrapper.vm.alertTableStore.requestReload).toBeFalsy();
  });
});
