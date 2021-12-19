import AlertTree from "../../../../../src/components/Alerts/AlertTree.vue";
import { mount, VueWrapper } from "@vue/test-utils";
import { createTestingPinia } from "@pinia/testing";
import {
  mockAlertReadFirstAppearances,
  mockAlertTreeFirstAppearances,
  mockAnalysisRead,
} from "../../../../mockData/alert";
import { useAlertStore } from "@/stores/alert";
import router from "@/router";

describe("AlertTree.vue", () => {
  const pinia = createTestingPinia({ stubActions: false });
  const alertStore = useAlertStore();
  alertStore.openAlert = mockAlertReadFirstAppearances;

  const wrapper: VueWrapper<any> = mount(AlertTree, {
    props: {
      items: mockAlertTreeFirstAppearances,
    },
    global: {
      plugins: [router, pinia],
      stubs: { NodeTagVue: true },
    },
  });

  it("renders", () => {
    expect(wrapper.exists()).toBe(true);
  });

  it("will correctly populate array of expanded status on generateExpandedStatus", () => {
    const itemsStub = [
      { firstAppearance: true },
      { firstAppearance: false },
      { firstAppearance: true },
    ];
    const itemsExpandedStatus = wrapper.vm.generateExpandedStatus(itemsStub);
    expect(itemsExpandedStatus).toEqual([true, false, true]);
  });

  it("will correctly return the expanded status for a given item index", () => {
    expect(wrapper.vm.nodeExpanded(0)).toEqual(true);
  });

  it("will correctly toggle the expanded status for a given item index", () => {
    wrapper.vm.toggleNodeExpanded(0);
    expect(wrapper.vm.itemsExpandedStatus).toEqual([false, true]);
    wrapper.vm.toggleNodeExpanded(1);
    expect(wrapper.vm.itemsExpandedStatus).toEqual([false, false]);
    wrapper.vm.toggleNodeExpanded(1);
    expect(wrapper.vm.itemsExpandedStatus).toEqual([false, true]);
    wrapper.vm.toggleNodeExpanded(0);
    expect(wrapper.vm.itemsExpandedStatus).toEqual([true, true]);
  });

  it("will correctly return the toggle icon class for a given item index", () => {
    wrapper.vm.toggleNodeExpanded(0);
    expect(wrapper.vm.toggleIcon(0)).toEqual([
      "p-tree-toggler-icon pi pi-fw",
      { "pi-chevron-down": false, "pi-chevron-right": true },
    ]);
    wrapper.vm.toggleNodeExpanded(0);
    expect(wrapper.vm.toggleIcon(0)).toEqual([
      "p-tree-toggler-icon pi pi-fw",
      { "pi-chevron-down": true, "pi-chevron-right": false },
    ]);
  });

  it("will correctly generate route for a given analysis item", () => {
    wrapper.vm.openAlertId = "alertUuid";
    const route = wrapper.vm.viewAnalysisRoute({ uuid: "itemUuid" });
    expect(route).toStrictEqual({
      name: "View Analysis",
      params: { alertId: "alertUuid", analysisID: "itemUuid" },
    });
  });

  it("will correctly return a given item's 'Name' on treeItemName", () => {
    let name = wrapper.vm.treeItemName(mockAnalysisRead);
    expect(name).toEqual("File Analysis");
    name = wrapper.vm.treeItemName({
      nodeType: "observable",
      type: { value: "test_type" },
      value: "test",
    });
    expect(name).toEqual("test_type: test");
  });

  it("will correctly return whether a given item is 'analysis' on isAnalysis", () => {
    let isAnalysis = wrapper.vm.isAnalysis(mockAnalysisRead);
    expect(isAnalysis).toEqual(true);
    isAnalysis = wrapper.vm.isAnalysis({
      nodeType: "observable",
      type: { value: "test_type" },
      value: "test",
    });
    expect(isAnalysis).toEqual(false);
  });
  it("will correctly return whether a given item is an 'observable' on isObservable", () => {
    let isObservable = wrapper.vm.isObservable(mockAnalysisRead);
    expect(isObservable).toEqual(false);
    isObservable = wrapper.vm.isObservable({
      nodeType: "observable",
      type: { value: "test_type" },
      value: "test",
    });
    expect(isObservable).toEqual(true);
  });
  it("will correctly generate a given item's style classes", () => {
    let containerClass = wrapper.vm.containerClass({ children: ["not_empty"] });
    expect(containerClass).toEqual([
      "p-treenode",
      { "p-treenode-leaf": false },
    ]);
    containerClass = wrapper.vm.containerClass({ children: [] });
    expect(containerClass).toEqual(["p-treenode", { "p-treenode-leaf": true }]);
  });
  it("will correctly return whether a given item has tags", () => {
    let hasTags = wrapper.vm.hasTags({});
    expect(hasTags).toEqual(false);
    hasTags = wrapper.vm.hasTags({ tags: [] });
    expect(hasTags).toBeFalsy();
    hasTags = wrapper.vm.hasTags({ tags: ["not_empty"] });
    expect(hasTags).toBeTruthy();
  });
});
