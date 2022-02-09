import DispositionModal from "@/components/Modals/DispositionModal.vue";
import { createTestingPinia, TestingOptions } from "@pinia/testing";
import { mount } from "@vue/test-utils";
import PrimeVue from "primevue/config";
import nock from "nock";

import myNock from "@unit/services/api/nock";
import { useAlertDispositionStore } from "@/stores/alertDisposition";
import { useAlertStore } from "@/stores/alert";
import { useAlertTableStore } from "@/stores/alertTable";
import { useModalStore } from "@/stores/modal";
import { useSelectedAlertStore } from "@/stores/selectedAlert";

function factory(options?: TestingOptions) {
  const wrapper = mount(DispositionModal, {
    attachTo: document.body,
    global: {
      plugins: [createTestingPinia(options), PrimeVue],
      stubs: { SaveToEventModal: true },
    },
    props: { name: "DispositionModal" },
  });

  const alertDispositionStore = useAlertDispositionStore();
  const alertStore = useAlertStore();
  const alertTableStore = useAlertTableStore();
  const modalStore = useModalStore();
  const selectedAlertStore = useSelectedAlertStore();

  return {
    alertDispositionStore,
    alertStore,
    alertTableStore,
    modalStore,
    selectedAlertStore,
    wrapper,
  };
}

describe("DispositionModal.vue", () => {
  afterEach(() => {
    nock.cleanAll();
  });

  it("renders", () => {
    const { wrapper } = factory();

    expect(wrapper.exists()).toBe(true);
  });

  it("opens a modal when the open function is called", () => {
    const { wrapper } = factory({ stubActions: false });

    expect(wrapper.vm.modalStore.openModals).toStrictEqual([]);
    wrapper.vm.open("modal1");
    expect(wrapper.vm.modalStore.openModals).toStrictEqual(["modal1"]);
  });

  it("correctly computes in allowSubmit whether the submit button should be enabled'", () => {
    const { wrapper } = factory();

    // No alerts selected and no value set
    wrapper.vm.selectedAlertStore.selected = [];
    wrapper.vm.newDisposition = null;
    expect(wrapper.vm.allowSubmit).toBeFalsy();
    // Alerts selected and no value set
    wrapper.vm.selectedAlertStore.selected = ["1", "2"];
    wrapper.vm.newDisposition = null;
    expect(wrapper.vm.allowSubmit).toBeFalsy();
    // No alerts selected and value set
    wrapper.vm.selectedAlertStore.selected = [];
    wrapper.vm.newDisposition = { value: "low disposition", rank: 1 };
    expect(wrapper.vm.allowSubmit).toBeFalsy();
    // Alerts selected and value set
    wrapper.vm.selectedAlertStore.selected = ["1", "2"];
    wrapper.vm.newDisposition = { value: "low disposition", rank: 1 };
    expect(wrapper.vm.allowSubmit).toBeTruthy();
  });

  it("correctly computes showAddToEventButton", () => {
    const { wrapper } = factory();

    wrapper.vm.newDisposition = { value: "high disposition", rank: 2 };
    expect(wrapper.vm.showAddToEventButton).toBeTruthy();

    wrapper.vm.newDisposition = { value: "low disposition", rank: 1 };
    expect(wrapper.vm.showAddToEventButton).toBeFalsy();
  });
  it("has the correctly assigned name 'DispositionModal'", () => {
    const { wrapper } = factory();

    expect(wrapper.vm.name).toEqual("DispositionModal");
  });

  it("correctly computes commentData", () => {
    const { wrapper } = factory();

    // Set the new comment value
    wrapper.vm.dispositionComment = "test comment";

    expect(wrapper.vm.commentData).toEqual({
      value: "test comment",
    });
  });

  it("will clear the 'error' property when handleError is called", async () => {
    const { wrapper } = factory();

    wrapper.vm.error = "Call failed";

    expect(wrapper.vm.error).toEqual("Call failed");
    wrapper.vm.handleError();
    expect(wrapper.vm.error).toBeNull();
  });

  it("will remove the DispositionModal from open modals store and clear newDisposition and dispositionComment on close", async () => {
    const { wrapper } = factory({ stubActions: false });

    wrapper.vm.newDisposition = { value: "low disposition", rank: 1 };
    wrapper.vm.dispositionComment = "test comment";
    wrapper.vm.modalStore.open("DispositionModal");

    wrapper.vm.close();

    expect(wrapper.vm.newDisposition).toBeNull();
    expect(wrapper.vm.dispositionComment).toBeNull();
    expect(wrapper.vm.modalStore.openModals).toStrictEqual([]);
  });

  it("will close the modal when setDisposition has successfully finished", async () => {
    const { wrapper } = factory({ stubActions: false });

    // Set the selected alert
    wrapper.vm.selectedAlertStore.selected = ["1", "2"];

    // Set the new disposition / comment values
    wrapper.vm.newDisposition = { value: "low disposition", rank: 1 };
    wrapper.vm.dispositionComment = "test comment";

    // Mock the update alert API calls
    myNock.options("/alert/").reply(200, "Success");
    myNock
      .patch("/alert/", [
        { uuid: "1", disposition: "low disposition" },
        { uuid: "2", disposition: "low disposition" },
      ])
      .reply(200, "Success");
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
    wrapper.vm.modalStore.open("DispositionModal");
    expect(wrapper.vm.modalStore.openModals).toStrictEqual([
      "DispositionModal",
    ]);
    await wrapper.vm.setDisposition();
    expect(wrapper.vm.newDisposition).toBeNull();
    expect(wrapper.vm.dispositionComment).toBeNull();
    expect(wrapper.vm.modalStore.openModals).toStrictEqual([]);
    expect(wrapper.emitted("requestReload")).toBeTruthy();
  });

  it("will close the modal when setDisposition has successfully finished (no dispositionComment)", async () => {
    const { wrapper } = factory({ stubActions: false });

    // Set the selected alert
    wrapper.vm.selectedAlertStore.selected = ["1", "2"];

    // Set the new disposition / comment values
    wrapper.vm.newDisposition = { value: "low disposition", rank: 1 };

    // Mock the update alert API calls
    myNock.options("/alert/").reply(200, "Success");
    myNock
      .patch("/alert/", [
        { uuid: "1", disposition: "low disposition" },
        { uuid: "2", disposition: "low disposition" },
      ])
      .reply(200, "Success");

    expect(wrapper.vm.modalStore.openModals).toStrictEqual([]);
    wrapper.vm.modalStore.open("DispositionModal");
    expect(wrapper.vm.modalStore.openModals).toStrictEqual([
      "DispositionModal",
    ]);
    await wrapper.vm.setDisposition();
    expect(wrapper.vm.newDisposition).toBeNull();
    expect(wrapper.vm.dispositionComment).toBeNull();
    expect(wrapper.vm.modalStore.openModals).toStrictEqual([]);
    expect(wrapper.emitted("requestReload")).toBeTruthy();
  });

  it("will not close the modal and will set the 'error' property when setDisposition fails", async () => {
    const { wrapper } = factory({ stubActions: false });

    // Set the selected alert
    wrapper.vm.selectedAlertStore.selected = ["1", "2"];

    // Set the new disposition / comment values
    wrapper.vm.newDisposition = { value: "low disposition", rank: 1 };
    wrapper.vm.dispositionComment = "test comment";

    // Mock the update alert API call
    myNock.options("/alert/").reply(200, "Success");
    const updateAlert = myNock.patch("/alert/").reply(403, "Failure");

    expect(wrapper.vm.modalStore.openModals).toStrictEqual([]);
    wrapper.vm.modalStore.open("DispositionModal");
    expect(wrapper.vm.modalStore.openModals).toStrictEqual([
      "DispositionModal",
    ]);
    await wrapper.vm.setDisposition();
    expect(updateAlert.isDone()).toBe(true);
    expect(wrapper.vm.error).toEqual("Request failed with status code 403");
    expect(wrapper.vm.newDisposition).toEqual({
      value: "low disposition",
      rank: 1,
    });
    expect(wrapper.vm.dispositionComment).toEqual("test comment");
    expect(wrapper.vm.modalStore.openModals).toStrictEqual([
      "DispositionModal",
    ]);
    expect(wrapper.emitted("requestReload")).toBeFalsy();
  });

  it("will ignore an error in setDisposition if it is a 409 (duplicate comment)", async () => {
    const { wrapper } = factory({ stubActions: false });

    // Set the selected alert
    wrapper.vm.selectedAlertStore.selected = ["1", "2"];

    // Set the new disposition / comment values
    wrapper.vm.newDisposition = { value: "low disposition", rank: 1 };
    wrapper.vm.dispositionComment = "test comment";

    // Mock the update alert API call
    myNock.options("/alert/").reply(200, "Success");
    myNock
      .patch("/alert/", [
        { uuid: "1", disposition: "low disposition" },
        { uuid: "2", disposition: "low disposition" },
      ])
      .reply(200, "Success");

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
      .reply(409, "Duplicate comment");

    expect(wrapper.vm.modalStore.openModals).toStrictEqual([]);
    wrapper.vm.modalStore.open("DispositionModal");
    expect(wrapper.vm.modalStore.openModals).toStrictEqual([
      "DispositionModal",
    ]);
    await wrapper.vm.setDisposition();
    expect(wrapper.vm.newDisposition).toBeNull();
    expect(wrapper.vm.dispositionComment).toBeNull();
    expect(wrapper.vm.modalStore.openModals).toStrictEqual([]);
    expect(wrapper.emitted("requestReload")).toBeTruthy();
  });
});
