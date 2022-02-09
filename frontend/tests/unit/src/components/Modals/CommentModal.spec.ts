import CommentModal from "@/components/Modals/CommentModal.vue";
import { createTestingPinia, TestingOptions } from "@pinia/testing";
import { mount } from "@vue/test-utils";
import PrimeVue from "primevue/config";
import nock from "nock";

import myNock from "@unit/services/api/nock";
import { useModalStore } from "@/stores/modal";

function factory(options?: TestingOptions) {
  const wrapper = mount(CommentModal, {
    attachTo: document.body,
    global: {
      plugins: [createTestingPinia(options), PrimeVue],
      provide: { nodeType: "alerts" },
    },
    props: { name: "CommentModal" },
  });

  const modalStore = useModalStore();

  return { wrapper, modalStore };
}

describe("CommentModal.vue", () => {
  afterEach(() => {
    nock.cleanAll();
  });

  it("renders", () => {
    const { wrapper } = factory();

    expect(wrapper.exists()).toBe(true);
  });
  it("correctly computes commentData", () => {
    const { wrapper } = factory();

    // Set the new comment value
    wrapper.vm.newComment = "test comment";

    expect(wrapper.vm.commentData).toEqual({
      value: "test comment",
    });
  });
  it("correctly computes in allowSubmit whether the submit button should be enabled'", () => {
    const { wrapper } = factory();

    // No alerts selected and no value set
    wrapper.vm.selectedStore.selected = [];
    wrapper.vm.newComment = "";
    expect(wrapper.vm.allowSubmit).toBeFalsy();
    // Alerts selected and no value set
    wrapper.vm.selectedStore.selected = ["1", "2"];
    wrapper.vm.newComment = "";
    expect(wrapper.vm.allowSubmit).toBeFalsy();
    // No alerts selected and value set
    wrapper.vm.selectedStore.selected = [];
    wrapper.vm.newComment = "test comment";
    expect(wrapper.vm.allowSubmit).toBeFalsy();
    // Alerts selected and value set
    wrapper.vm.selectedStore.selected = ["1", "2"];
    wrapper.vm.newComment = "test comment";
    expect(wrapper.vm.allowSubmit).toBeTruthy();
  });
  it("has the correctly assigned name 'CommentModal'", () => {
    const { wrapper } = factory();

    expect(wrapper.vm.name).toEqual("CommentModal");
  });

  it("will clear the 'error' property when handleError is called", async () => {
    const { wrapper } = factory();

    wrapper.vm.error = "Call failed";

    expect(wrapper.vm.error).toEqual("Call failed");
    wrapper.vm.handleError();
    expect(wrapper.vm.error).toBeNull();
  });

  it("will remove the CommentModal from open modals store and clear newComment on close", async () => {
    const { wrapper } = factory({ stubActions: false });

    wrapper.vm.newComment = "test comment";
    wrapper.vm.modalStore.open("CommentModal");

    wrapper.vm.close();

    expect(wrapper.vm.newComment).toEqual("");
    expect(wrapper.vm.modalStore.openModals).toStrictEqual([]);
  });

  it("will close the modal when addComment has successfully finished", async () => {
    const { wrapper } = factory({ stubActions: false });

    // Set the selected alert
    wrapper.vm.selectedStore.selected = ["1", "2"];

    // Set the new comment value
    wrapper.vm.newComment = "test comment";

    // Mock the update alert API call
    myNock
      .post("/node/comment/", [
        {
          value: "test comment",
          node_uuid: "1",
        },
        {
          value: "test comment",
          node_uuid: "2",
        },
      ])
      .reply(201, "Success");

    expect(wrapper.vm.modalStore.openModals).toStrictEqual([]);
    wrapper.vm.modalStore.open("CommentModal");
    expect(wrapper.vm.modalStore.openModals).toStrictEqual(["CommentModal"]);
    await wrapper.vm.addComment();
    expect(wrapper.vm.newComment).toEqual("");
    expect(wrapper.vm.modalStore.openModals).toStrictEqual([]);
    expect(wrapper.emitted("requestReload")).toBeTruthy();
  });

  it("will not close the modal and will set the 'error' property when assignUser fails", async () => {
    const { wrapper } = factory({ stubActions: false });

    // Set the selected alert
    wrapper.vm.selectedStore.selected = ["1", "2"];

    // Set the new comment value
    wrapper.vm.newComment = "test comment";
    // Mock the update alert API call
    const updateAlert = myNock.post("/node/comment/").reply(403, "Failed");

    expect(wrapper.vm.modalStore.openModals).toStrictEqual([]);
    wrapper.vm.modalStore.open("CommentModal");
    expect(wrapper.vm.modalStore.openModals).toStrictEqual(["CommentModal"]);
    await wrapper.vm.addComment();
    expect(updateAlert.isDone()).toBe(true);
    expect(wrapper.vm.error).toEqual("Request failed with status code 403");
    expect(wrapper.vm.newComment).toEqual("test comment");
    expect(wrapper.vm.modalStore.openModals).toStrictEqual(["CommentModal"]);
    expect(wrapper.emitted("requestReload")).toBeFalsy();
  });
});
