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

  // NOTE: This test should use jest.spyOn, but we can't when using Composition functions
  // https://stackoverflow.com/questions/64544061/cannot-spyon-functions-inside-of-vue-3-setup
  // https://forum.vuejs.org/t/vue3-jest-is-there-a-technique-for-testing-composition-functions/106004
  it("will call assignUser when assignUserClicked called and one alert is selected", async () => {
    const { wrapper } = factory({ stubActions: false });

    // Set the selected alert
    wrapper.vm.selectedAlertStore.selected = ["1"];

    // Set the selected user
    wrapper.vm.selectedUser = { username: "Alice" };

    // Mock the update alert API call
    myNock.options("/alert/1").reply(200, "Success");
    const updateAlert = myNock.patch("/alert/1").reply(200, "Success");

    await wrapper.vm.assignUserClicked();
    expect(updateAlert.isDone()).toBe(true);
  });

  // NOTE: This test should use jest.spyOn, but we can't when using Composition functions
  // https://stackoverflow.com/questions/64544061/cannot-spyon-functions-inside-of-vue-3-setup
  // https://forum.vuejs.org/t/vue3-jest-is-there-a-technique-for-testing-composition-functions/106004
  it("will call assignUserMultiple when assignUserClicked called and multiple alerts are selected", async () => {
    const { wrapper } = factory({ stubActions: false });

    // Set the selected alerts
    wrapper.vm.selectedAlertStore.selected = ["1", "2"];

    // Set the selected user
    wrapper.vm.selectedUser = { username: "Alice" };

    // Mock the update alert API calls
    myNock.options("/alert/1").reply(200, "Success");
    const updateAlert1 = myNock.patch("/alert/1").reply(200, "Success");
    myNock.options("/alert/2").reply(200, "Success");
    const updateAlert2 = myNock.patch("/alert/2").reply(200, "Success");

    await wrapper.vm.assignUserClicked();
    expect(updateAlert1.isDone()).toBe(true);
    expect(updateAlert2.isDone()).toBe(true);
  });

  it("will close the modal when assignUser has successfully finished", async () => {
    const { wrapper } = factory({ stubActions: false });

    // Set the selected alert
    wrapper.vm.selectedAlertStore.selected = ["1"];

    // Set the selected user
    wrapper.vm.selectedUser = { username: "Alice" };

    // Mock the update alert API call
    myNock.options("/alert/1").reply(200, "Success");
    myNock.patch("/alert/1").reply(200, "Success");

    expect(wrapper.vm.modalStore.openModals).toStrictEqual([]);
    wrapper.vm.modalStore.open("AssignModal");
    expect(wrapper.vm.modalStore.openModals).toStrictEqual(["AssignModal"]);
    await wrapper.vm.assignUser();
    expect(wrapper.vm.modalStore.openModals).toStrictEqual([]);
  });
  it("will close the modal when assignUserToMultiple has successfully finished", async () => {
    const { wrapper } = factory({ stubActions: false });

    // Set the selected alerts
    wrapper.vm.selectedAlertStore.selected = ["1", "2"];

    // Set the selected user
    wrapper.vm.selectedUser = { username: "Alice" };

    // Mock the update alert API calls
    myNock.options("/alert/1").reply(200, "Success");
    myNock.patch("/alert/1").reply(200, "Success");
    myNock.options("/alert/2").reply(200, "Success");
    myNock.patch("/alert/2").reply(200, "Success");

    expect(wrapper.vm.modalStore.openModals).toStrictEqual([]);
    wrapper.vm.modalStore.open("AssignModal");
    expect(wrapper.vm.modalStore.openModals).toStrictEqual(["AssignModal"]);
    await wrapper.vm.assignUserToMultiple();
    expect(wrapper.vm.modalStore.openModals).toStrictEqual([]);
  });

  it("will not close the modal and will set the 'error' property when assignUser fails", async () => {
    const { wrapper } = factory({ stubActions: false });

    // Set the selected alert
    wrapper.vm.selectedAlertStore.selected = ["1"];

    // Set the selected user
    wrapper.vm.selectedUser = { username: "Alice" };

    // Mock the update alert API call
    const updateAlert = myNock.options("/alert/1").reply(403, "Unauthorized");

    expect(wrapper.vm.modalStore.openModals).toStrictEqual([]);
    wrapper.vm.modalStore.open("AssignModal");
    expect(wrapper.vm.modalStore.openModals).toStrictEqual(["AssignModal"]);
    await wrapper.vm.assignUser();
    expect(updateAlert.isDone()).toBe(true);
    expect(wrapper.vm.error).toEqual("Network Error");
    expect(wrapper.vm.modalStore.openModals).toStrictEqual(["AssignModal"]);
  });

  // TODO: Figure out how best to do the tests that check the failure conditions
  it("will not close the modal and will set the 'error' property when assignUserToMultiple fails", async () => {
    const { wrapper } = factory({ stubActions: false });

    // Set the selected alerts
    wrapper.vm.selectedAlertStore.selected = ["1", "2"];

    // Set the selected user
    wrapper.vm.selectedUser = { username: "Alice" };

    // Mock the update alert API calls
    myNock.options("/alert/1").reply(403, "Unauthorized");
    myNock.options("/alert/2").reply(403, "Unauthorized");

    expect(wrapper.vm.modalStore.openModals).toStrictEqual([]);
    wrapper.vm.modalStore.open("AssignModal");
    expect(wrapper.vm.modalStore.openModals).toStrictEqual(["AssignModal"]);
    await wrapper.vm.assignUserToMultiple();
    expect(wrapper.vm.error).toEqual("Network Error");
    expect(wrapper.vm.modalStore.openModals).toStrictEqual(["AssignModal"]);
  });
});
