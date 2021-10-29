import AssignModal from "@/components/Modals/AssignModal.vue";
import { flushPromises, mount } from "@vue/test-utils";
import store, { testVars } from "@unit/components/mockStore";
import PrimeVue from "primevue/config";

describe("AssignModal.vue", () => {
  afterEach(() => {
    store.commit("users/addItems", []);
    store.commit("selectedAlerts/UNSELECTALL");
    store.commit("modals/CLOSE", "AssignModal");
    wrapper.setData({
      selectedUser: null,
      error: null,
    });
    jest.clearAllMocks();
    testVars.errorCondition = false;
  });

  const wrapper = mount(AssignModal, {
    attachTo: document.body,
    global: {
      plugins: [store, PrimeVue],
    },
  });
  it("renders", () => {
    expect(wrapper.exists()).toBe(true);
  });
  it("has a true 'isOpen' property after dispatching the open action and false when it is closed", async () => {
    expect(wrapper.vm.isOpen).toBe(false);
    await store.dispatch("modals/open", "AssignModal");
    expect(wrapper.vm.isOpen).toBe(true);
    wrapper.vm.close();
    expect(wrapper.vm.isOpen).toBe(false);
  });
  it("has the correctly assigned name 'AssignModal'", () => {
    expect(wrapper.vm.name).toEqual("AssignModal");
  });
  it("will set the 'users' property when loadUsers is called and completed successfully", async () => {
    // Should be empty to start
    expect(wrapper.vm.users).toEqual([]);
    await wrapper.vm.loadUsers();
    expect(wrapper.vm.users).toEqual(["Alice", "Bob"]);
  });
  it("has a true 'isLoading' property when loadUsers is called and is not completed", async () => {
    // Should be empty to start
    expect(wrapper.vm.users).toEqual([]);
    expect(wrapper.vm.isLoading).toBe(false);
    // Don't await here so we can check the loading value
    wrapper.vm.loadUsers();
    expect(wrapper.vm.isLoading).toBe(true);
    await flushPromises();
    expect(wrapper.vm.isLoading).toBe(false);
    expect(wrapper.vm.users).toEqual(["Alice", "Bob"]);
  });
  it("will set the 'error' property when loadUsers is called and fails", async () => {
    testVars.errorCondition = true;
    // Should be empty to start
    expect(wrapper.vm.users).toEqual([]);
    await wrapper.vm.loadUsers();
    expect(wrapper.vm.error).toEqual("Call failed");
    // And empty after still
    expect(wrapper.vm.users).toEqual([]);
  });
  it("will have an updated 'selectedAlerts' property when an alert is selected", async () => {
    expect(wrapper.vm.selectedAlerts).toEqual([]);
    await store.dispatch("selectedAlerts/select", "Alert1");
    expect(wrapper.vm.selectedAlerts).toEqual(["Alert1"]);
  });
  it("will have a true 'selectedAlerts' property when any alert is selected", async () => {
    expect(wrapper.vm.anyAlertsSelected).toEqual(false);
    await store.dispatch("selectedAlerts/select", "Alert1");
    expect(wrapper.vm.anyAlertsSelected).toEqual(true);
  });
  it("will have a true 'multipleAlertsSelected' property only when more than one alert is selected", async () => {
    expect(wrapper.vm.multipleAlertsSelected).toEqual(false);
    await store.dispatch("selectedAlerts/select", "Alert1");
    expect(wrapper.vm.multipleAlertsSelected).toEqual(false);
    await store.dispatch("selectedAlerts/select", "Alert2");
    expect(wrapper.vm.multipleAlertsSelected).toEqual(true);
  });
  it("will clear the 'error' property when handleError is called", async () => {
    testVars.errorCondition = true;
    await wrapper.vm.loadUsers();
    expect(wrapper.vm.error).toEqual("Call failed");
    wrapper.vm.handleError();
    expect(wrapper.vm.error).toBeNull();
  });
  it("will call assignUserMultiple when assignUserClicked called and multiple alerts are selected", async () => {
    await store.dispatch("selectedAlerts/select", "Alert1");
    await wrapper.setData({ selectedUser: "Alice" });
    const assignUser = jest.spyOn(wrapper.vm, "assignUser");
    const assignUserToMultiple = jest.spyOn(wrapper.vm, "assignUserToMultiple");
    wrapper.vm.assignUserClicked();
    expect(assignUserToMultiple).not.toHaveBeenCalled();
    expect(assignUser).toHaveBeenCalled();
  });
  it("will call assignUser when assignUserClicked called and one alert is selected", async () => {
    await store.dispatch("selectedAlerts/selectAll", ["Alert1", "Alert2"]);
    await wrapper.setData({ selectedUser: "Bob" });
    const assignUser = jest.spyOn(wrapper.vm, "assignUser");
    const assignUserToMultiple = jest.spyOn(wrapper.vm, "assignUserToMultiple");
    wrapper.vm.assignUserClicked();
    expect(assignUser).not.toHaveBeenCalled();
    expect(assignUserToMultiple).toHaveBeenCalled();
  });
  it("will close the modal when assignUser has successfully finished", async () => {
    expect(wrapper.vm.isOpen).toBe(false);
    await store.dispatch("modals/open", "AssignModal");
    expect(wrapper.vm.isOpen).toBe(true);
    await wrapper.vm.assignUser();
    expect(wrapper.vm.isOpen).toBe(false);
  });
  it("will close the modal when assignUserToMultiple has successfully finished", async () => {
    expect(wrapper.vm.isOpen).toBe(false);
    await store.dispatch("modals/open", "AssignModal");
    expect(wrapper.vm.isOpen).toBe(true);
    await wrapper.vm.assignUserToMultiple();
    expect(wrapper.vm.isOpen).toBe(false);
  });
  it("will not close the modal and will set the 'error' property when assignUser fails", async () => {
    testVars.errorCondition = true;
    expect(wrapper.vm.isOpen).toBe(false);
    await store.dispatch("modals/open", "AssignModal");
    expect(wrapper.vm.isOpen).toBe(true);
    await wrapper.vm.assignUser();
    expect(wrapper.vm.error).toEqual("Call failed");
    expect(wrapper.vm.isOpen).toBe(true);
  });
  it("will not close the modal and will set the 'error' property when assignUserToMultiple fails", async () => {
    testVars.errorCondition = true;
    expect(wrapper.vm.isOpen).toBe(false);
    await store.dispatch("modals/open", "AssignModal");
    expect(wrapper.vm.isOpen).toBe(true);
    await wrapper.vm.assignUserToMultiple();
    expect(wrapper.vm.error).toEqual("Call failed");
    expect(wrapper.vm.isOpen).toBe(true);
  });
});
