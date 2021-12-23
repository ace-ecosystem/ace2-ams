import CommentModal from "@/components/Modals/CommentModal.vue";
import { createTestingPinia, TestingOptions } from "@pinia/testing";
import { mount } from "@vue/test-utils";
import PrimeVue from "primevue/config";
import nock from "nock";

import myNock from "@unit/services/api/nock";
import { useModalStore } from "@/stores/modal";
import { useSelectedAlertStore } from "@/stores/selectedAlert";
import { useUserStore } from "@/stores/user";

function factory(options?: TestingOptions) {
  const wrapper = mount(CommentModal, {
    attachTo: document.body,
    global: {
      plugins: [createTestingPinia(options), PrimeVue],
    },
    props: { name: "CommentModal" },
  });

  const modalStore = useModalStore();
  const selectedAlertStore = useSelectedAlertStore();
  const userStore = useUserStore();

  return { wrapper, modalStore, selectedAlertStore, userStore };
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

    // Set the selected user
    wrapper.vm.authStore.user = { username: "Alice" };

    // Set the new comment value
    wrapper.vm.newComment = "test comment";

    expect(wrapper.vm.commentData).toEqual({
      user: "Alice",
      value: "test comment",
    });
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

    expect(wrapper.vm.newComment).toBeNull();
    expect(wrapper.vm.modalStore.openModals).toStrictEqual([]);
  });

  it("will close the modal when addComment has successfully finished", async () => {
    const { wrapper } = factory({ stubActions: false });

    // Set the selected alert
    wrapper.vm.selectedAlertStore.selected = ["1", "2"];

    // Set the selected user
    wrapper.vm.authStore.user = { username: "Alice" };

    // Set the new comment value
    wrapper.vm.newComment = "test comment";

    // Mock the update alert API call
    myNock
      .post("/node/comment/", {
        user: "Alice",
        value: "test comment",
        node_uuid: "1",
      })
      .reply(201, "Success");
    myNock
      .post("/node/comment/", {
        user: "Alice",
        value: "test comment",
        node_uuid: "2",
      })
      .reply(201, "Success");

    expect(wrapper.vm.modalStore.openModals).toStrictEqual([]);
    wrapper.vm.modalStore.open("CommentModal");
    expect(wrapper.vm.modalStore.openModals).toStrictEqual(["CommentModal"]);
    await wrapper.vm.addComment();
    expect(wrapper.vm.newComment).toBeNull();
    expect(wrapper.vm.modalStore.openModals).toStrictEqual([]);
    expect(wrapper.vm.alertTableStore.requestReload).toBeTruthy();
  });

  it("will not close the modal and will set the 'error' property when assignUser fails", async () => {
    const { wrapper } = factory({ stubActions: false });

    // Set the selected alert
    wrapper.vm.selectedAlertStore.selected = ["1", "2"];

    // Set the selected user
    wrapper.vm.authStore.user = { username: "Alice" };

    // Set the new comment value
    wrapper.vm.newComment = "test comment";
    // Mock the update alert API call
    const updateAlert = myNock
      .post("/node/comment/", {
        user: "Alice",
        value: "test comment",
        node_uuid: "1",
      })
      .reply(403, "Failed");

    expect(wrapper.vm.modalStore.openModals).toStrictEqual([]);
    wrapper.vm.modalStore.open("CommentModal");
    expect(wrapper.vm.modalStore.openModals).toStrictEqual(["CommentModal"]);
    await wrapper.vm.addComment();
    expect(updateAlert.isDone()).toBe(true);
    expect(wrapper.vm.error).toEqual("Request failed with status code 403");
    expect(wrapper.vm.newComment).toEqual("test comment");
    expect(wrapper.vm.modalStore.openModals).toStrictEqual(["CommentModal"]);
    expect(wrapper.vm.alertTableStore.requestReload).toBeFalsy();
  });
});
