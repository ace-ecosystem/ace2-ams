import AssignModal from "@/components/Modals/AssignModal.vue";
import { createTestingPinia, TestingOptions } from "@pinia/testing";
import { mount } from "@vue/test-utils";
import PrimeVue from "primevue/config";
import nock from "nock";

import myNock from "@unit/services/api/nock";
import { useModalStore } from "@/stores/modal";
import { useSelectedAlertStore } from "@/stores/selectedAlert";
import { useUserStore } from "@/stores/user";

function factory(options?: TestingOptions) {
  const wrapper = mount(AssignModal, {
    attachTo: document.body,
    global: {
      plugins: [createTestingPinia(options), PrimeVue],
    },
    props: { name: "AssignModal" },
  });

  const modalStore = useModalStore();
  const selectedAlertStore = useSelectedAlertStore();
  const userStore = useUserStore();

  return { wrapper, modalStore, selectedAlertStore, userStore };
}

describe("AssignModal.vue", () => {
  afterEach(() => {
    nock.cleanAll();
  });

  it("renders", () => {
    const { wrapper } = factory();

    expect(wrapper.exists()).toBe(true);
  });
  it("has the correctly assigned name 'AssignModal'", () => {
    const { wrapper } = factory();

    expect(wrapper.vm.name).toEqual("AssignModal");
  });

  it("will clear the 'error' property when handleError is called", async () => {
    const { wrapper } = factory();

    wrapper.vm.error = "Call failed";

    expect(wrapper.vm.error).toEqual("Call failed");
    wrapper.vm.handleError();
    expect(wrapper.vm.error).toBeNull();
  });

  it("will remove the AssignModal from open modals store and clear selectedUser on close", async () => {
    const { wrapper } = factory({ stubActions: false });

    wrapper.vm.selectedUser = { username: "Alice" };
    wrapper.vm.modalStore.open("AssignModal");

    wrapper.vm.close();

    expect(wrapper.vm.selectedUser).toBeNull();
    expect(wrapper.vm.modalStore.openModals).toStrictEqual([]);
  });

  it("will close the modal when assignUser has successfully finished", async () => {
    const { wrapper } = factory({ stubActions: false });

    // Set the selected alert
    wrapper.vm.selectedAlertStore.selected = ["1", "2"];

    // Set the selected user
    wrapper.vm.selectedUser = { username: "Alice" };

    // Mock the update alert API call
    myNock.options("/alert/1").reply(200, "Success");
    myNock.patch("/alert/1").reply(200, "Success");
    myNock.options("/alert/2").reply(200, "Success");
    myNock.patch("/alert/2").reply(200, "Success");

    expect(wrapper.vm.modalStore.openModals).toStrictEqual([]);
    wrapper.vm.modalStore.open("AssignModal");
    expect(wrapper.vm.modalStore.openModals).toStrictEqual(["AssignModal"]);
    await wrapper.vm.assignUser();
    expect(wrapper.vm.selectedUser).toBeNull();
    expect(wrapper.vm.modalStore.openModals).toStrictEqual([]);
    expect(wrapper.vm.alertTableStore.requestReload).toBeTruthy();
  });

  it("will not close the modal and will set the 'error' property when assignUser fails", async () => {
    const { wrapper } = factory({ stubActions: false });

    // Set the selected alert
    wrapper.vm.selectedAlertStore.selected = ["1"];

    // Set the selected user
    wrapper.vm.selectedUser = { username: "Alice" };

    // Mock the update alert API call
    const updateAlert = myNock
      .options("/alert/1")
      .reply(200, "Success")
      .patch("/alert/1")
      .reply(403, "Unauthorized");

    expect(wrapper.vm.modalStore.openModals).toStrictEqual([]);
    wrapper.vm.modalStore.open("AssignModal");
    expect(wrapper.vm.modalStore.openModals).toStrictEqual(["AssignModal"]);
    await wrapper.vm.assignUser();
    expect(updateAlert.isDone()).toBe(true);
    expect(wrapper.vm.error).toEqual("Request failed with status code 403");
    expect(wrapper.vm.selectedUser).toEqual({ username: "Alice" });
    expect(wrapper.vm.modalStore.openModals).toStrictEqual(["AssignModal"]);
    expect(wrapper.vm.alertTableStore.requestReload).toBeFalsy();
  });
});
