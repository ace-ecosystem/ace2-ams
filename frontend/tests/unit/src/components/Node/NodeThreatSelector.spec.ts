import { useNodeThreatTypeStore } from "@/stores/nodeThreatType";
import { nodeThreatReadFactory } from "./../../../../mocks/nodeThreat";
import { genericObjectReadFactory } from "./../../../../mocks/genericObject";
import NodeThreatSelector from "../../../../../src/components/Node/NodeThreatSelector.vue";
import { mount } from "@vue/test-utils";
import { createCustomPinia } from "@unit/helpers";
import Tooltip from "primevue/tooltip";
import PrimeVue from "primevue/config";

import { useNodeThreatStore } from "@/stores/nodeThreat";

function factory() {
  const wrapper = mount(NodeThreatSelector, {
    props: {
      modelValue: [],
    },
    global: {
      plugins: [createCustomPinia(), PrimeVue],
      directives: { tooltip: Tooltip },
    },
  });

  const nodeThreatStore = useNodeThreatStore();
  const nodeThreatTypeStore = useNodeThreatTypeStore();

  return { wrapper, nodeThreatStore, nodeThreatTypeStore };
}

describe("NodeThreatSelector.vue", () => {
  it("renders", () => {
    const { wrapper } = factory();
    expect(wrapper.exists()).toBe(true);
  });
  it("loads nodeThreats when mounted", async () => {
    const { nodeThreatStore } = factory();
    expect(nodeThreatStore.readAll).toHaveBeenCalled();
  });
  it("correctly formats a given array of threat types on formatThreatTypes", () => {
    const { wrapper } = factory();
    const result = wrapper.vm.formatThreatTypes([
      { value: "threatA" },
      { value: "threatB" },
    ]);
    expect(result).toEqual("threatA, threatB");
  });
  it("correctly resets data on closeEditThreatPanel", () => {
    const { wrapper } = factory();
    wrapper.vm.newThreatName = "test";
    wrapper.vm.newThreatTypes = ["test"];
    wrapper.vm.editingExistingThreat = true;
    wrapper.vm.editingExistingThreatUuid = "uuid";
    wrapper.vm.showEditThreat = true;

    wrapper.vm.closeEditThreatPanel();
    expect(wrapper.vm.newThreatName).toBeNull();
    expect(wrapper.vm.newThreatTypes).toEqual([]);
    expect(wrapper.vm.editingExistingThreat).toBeFalsy();
    expect(wrapper.vm.editingExistingThreatUuid).toBeUndefined();
    expect(wrapper.vm.showEditThreat).toBeFalsy();
  });
  it("correctly sets up the EditThreatPanel given an existing threat on openEditThreatPanel", () => {
    const { wrapper, nodeThreatTypeStore } = factory();

    const testThreatTypeA = genericObjectReadFactory({ value: "testThreatA" });
    const testThreatTypeB = genericObjectReadFactory({ value: "testThreatb" });

    nodeThreatTypeStore.items = [testThreatTypeA, testThreatTypeB];

    wrapper.vm.openEditThreatPanel(
      nodeThreatReadFactory({ types: [testThreatTypeB] }),
    );
    expect(wrapper.vm.editingExistingThreat).toBeTruthy();
    expect(wrapper.vm.editingExistingThreatUuid).toEqual("nodeThreat1");
    expect(wrapper.vm.newThreatName).toEqual("nodeThreat");
    expect(wrapper.vm.newThreatTypes).toEqual([testThreatTypeB]);
  });
  it("correctly sets up the EditThreatPanel for a new threat on openEditThreatPanel", () => {
    const { wrapper } = factory();
    wrapper.vm.openEditThreatPanel();
    expect(wrapper.vm.editingExistingThreat).toBeFalsy();
  });
  it("correctly submits a new threat on submitNewThreat", async () => {
    const { wrapper, nodeThreatStore } = factory();

    const testThreatType = genericObjectReadFactory({
      value: "testThreatType",
    });

    wrapper.vm.newThreatName = "threatName";
    wrapper.vm.editingExistingThreat = true;
    wrapper.vm.editingExistingThreatUuid = "uuid";
    wrapper.vm.newThreatTypes = [testThreatType];

    await wrapper.vm.submitNewThreat();
    expect(nodeThreatStore.update).toHaveBeenCalledWith("uuid", {
      types: ["testThreatType"],
    });
    expect(wrapper.vm.newThreatName).toBeNull();
    expect(wrapper.vm.newThreatTypes).toEqual([]);
    expect(wrapper.vm.editingExistingThreat).toBeFalsy();
    expect(wrapper.vm.editingExistingThreatUuid).toBeUndefined();
    expect(wrapper.vm.showEditThreat).toBeFalsy();
  });
  it("correctly submits an updated threat on submitNewThreat", async () => {
    const { wrapper, nodeThreatStore } = factory();

    wrapper.vm.newThreatName = "threatName";
    const testThreatType = genericObjectReadFactory({
      value: "testThreatType",
    });
    wrapper.vm.newThreatTypes = [testThreatType];

    await wrapper.vm.submitNewThreat();
    expect(nodeThreatStore.create).toHaveBeenCalledWith({
      queues: ["external"],
      types: ["testThreatType"],
      value: "threatName",
    });
    expect(wrapper.vm.newThreatName).toBeNull();
    expect(wrapper.vm.newThreatTypes).toEqual([]);
    expect(wrapper.vm.editingExistingThreat).toBeFalsy();
    expect(wrapper.vm.editingExistingThreatUuid).toBeUndefined();
    expect(wrapper.vm.showEditThreat).toBeFalsy();
  });
  it("emits the expected event on updateModelValue", () => {
    const { wrapper } = factory();
    wrapper.vm.updateModelValue({ value: "testEvent" });
    expect(wrapper.emitted("update:modelValue")).toBeTruthy();
  });
  it("correctly computes editThreatCloseIcon value", () => {
    const { wrapper } = factory();
    expect(wrapper.vm.editThreatCloseIcon).toEqual("pi pi-trash");
    wrapper.vm.editingExistingThreat = true;
    expect(wrapper.vm.editThreatCloseIcon).toEqual("pi pi-times");
  });
});
