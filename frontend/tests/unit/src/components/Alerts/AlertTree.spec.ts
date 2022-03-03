import AlertTree from "@/components/Alerts/AlertTree.vue";
import { mount, VueWrapper } from "@vue/test-utils";
import { TestingOptions } from "@pinia/testing";
import { mockAlert, mockAnalysisRead } from "../../../../mocks/alert";
import { createRouterMock, injectRouterMock } from "vue-router-mock";
import { useAlertStore } from "@/stores/alert";
import { createCustomPinia } from "@unit/helpers";

describe("AlertTree.vue", () => {
  function factory(options?: TestingOptions) {
    const router = createRouterMock();
    injectRouterMock(router);

    const pinia = createCustomPinia(options);
    const alertStore = useAlertStore();
    alertStore.open = mockAlert;

    const wrapper: VueWrapper<any> = mount(AlertTree, {
      props: {
        items: mockAlert.children,
      },
      global: {
        plugins: [pinia],
        stubs: { NodeTagVue: true },
      },
    });

    return { wrapper, alertStore, router };
  }

  it("renders", () => {
    const { wrapper } = factory();

    expect(wrapper.exists()).toBe(true);
  });

  it("will correctly populate array of expanded status on generateExpandedStatus", () => {
    const { wrapper } = factory();

    const itemsStub = [
      { firstAppearance: true },
      { firstAppearance: false },
      { firstAppearance: true },
    ];
    const itemsExpandedStatus = wrapper.vm.generateExpandedStatus(itemsStub);
    expect(itemsExpandedStatus).toEqual([true, false, true]);
  });

  it("will correctly return the expanded status for a given item index", () => {
    const { wrapper } = factory();

    expect(wrapper.vm.nodeExpanded(0)).toEqual(true);
  });

  it("will correctly toggle the expanded status for a given item index", () => {
    const { wrapper } = factory();

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
    const { wrapper } = factory();

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
    const { wrapper } = factory();

    wrapper.vm.openAlertId = "alertUuid";
    const route = wrapper.vm.viewAnalysisRoute({ uuid: "itemUuid" });
    expect(route).toStrictEqual({
      name: "View Analysis",
      params: { alertId: "alertUuid", analysisID: "itemUuid" },
    });
  });

  it("will correctly return a given item's 'Name' on treeItemName", () => {
    const { wrapper } = factory();

    // Analysis
    let name = wrapper.vm.treeItemName(mockAnalysisRead);
    expect(name).toEqual("File Analysis");

    // Basic observable
    name = wrapper.vm.treeItemName({
      nodeType: "observable",
      type: { value: "test_type" },
      value: "test",
    });
    expect(name).toEqual("test_type: test");

    // 'Styled' observable type
    name = wrapper.vm.treeItemName({
      nodeType: "observable",
      type: { value: "test_type" },
      value: "test",
      nodeMetadata: { display: { type: "Special Type" } },
    });
    expect(name).toEqual("Special Type (test_type): test");

    // 'Styled' observable value
    name = wrapper.vm.treeItemName({
      nodeType: "observable",
      type: { value: "test_type" },
      value: "test",
      nodeMetadata: { display: { value: "Special Value" } },
    });
    expect(name).toEqual("test_type: Special Value");

    // nodeMetadata field but no 'display' field
    name = wrapper.vm.treeItemName({
      nodeType: "observable",
      type: { value: "test_type" },
      value: "test",
      nodeMetadata: {},
    });
    expect(name).toEqual("test_type: test");
  });

  it("will correctly return whether a given item is 'analysis' on isAnalysis", () => {
    const { wrapper } = factory();

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
    const { wrapper } = factory();

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
    const { wrapper } = factory();

    let containerClass = wrapper.vm.containerClass({ children: ["not_empty"] });
    expect(containerClass).toEqual([
      "p-treenode",
      { "p-treenode-leaf": false },
    ]);
    containerClass = wrapper.vm.containerClass({ children: [] });
    expect(containerClass).toEqual(["p-treenode", { "p-treenode-leaf": true }]);
  });
  it("will correctly return whether a given item has tags", () => {
    const { wrapper } = factory();

    let hasTags = wrapper.vm.hasTags({});
    expect(hasTags).toEqual(false);
    hasTags = wrapper.vm.hasTags({ tags: [] });
    expect(hasTags).toBeFalsy();
    hasTags = wrapper.vm.hasTags({ tags: ["not_empty"] });
    expect(hasTags).toBeTruthy();
  });
  it("will route the manage alerts page with correctly observable query when filterByObservable is called with a given observable", async () => {
    const { wrapper, router } = factory();

    const observable = {
      nodeType: "observable",
      type: { value: "test_type" },
      value: "test",
    };
    wrapper.vm.filterByObservable(observable);
    expect(router.currentRoute.value.fullPath).toEqual(
      "/manage_alerts?observable=test_type|test",
    );
  });
});
