import TheEventDetailsMenuBar from "@/components/Events/TheEventDetailsMenuBar.vue";
import { flushPromises, shallowMount, VueWrapper } from "@vue/test-utils";
import { TestingOptions } from "@pinia/testing";
import { createRouterMock, injectRouterMock } from "vue-router-mock";
import { createCustomPinia } from "@unit/helpers";
import myNock from "@unit/services/api/nock";

import { useFilterStore } from "@/stores/filter";
import { defineEmits } from "vue";

import { expect } from "vitest";
import { eventReadFactory } from "../../../../mocks/events";

function factory(options: TestingOptions = {}, eventUuid = "uuid1") {
  const router = createRouterMock();
  injectRouterMock(router);

  const wrapper: VueWrapper<any> = shallowMount(TheEventDetailsMenuBar, {
    global: {
      plugins: [createCustomPinia(options)],
      provide: { nodeType: "events" },
    },
    props: {
      eventUuid: eventUuid,
    },
  });

  const filterStore = useFilterStore();

  return { wrapper, filterStore };
}

const noAnalysisItems = {
  label: "Analysis",
  icon: "pi pi-fw pi-chart-bar",
  items: [
    [
      {
        label: "Analysis Details",
        items: [],
      },
    ],
  ],
};

describe("EventAlertsTable", () => {
  it("renders", () => {
    const { wrapper } = factory();
    expect(wrapper.exists()).toBe(true);
  });

  it("sets eventStore requestReload to true on requestReload", () => {
    const { wrapper } = factory();
    expect(wrapper.vm.eventStore.requestReload).toBeFalsy();
    wrapper.vm.requestReload();
    expect(wrapper.vm.eventStore.requestReload).toBeTruthy();
  });

  it("correcty computes analysisMenuItems based on open event analysisTypes", () => {
    const { wrapper } = factory();
    // When there is no set open event, there will be no analysis details items
    expect(wrapper.vm.analysisMenuItems).toEqual(noAnalysisItems);
    // When there is an open event that has no analysis items
    wrapper.vm.eventStore.open = eventReadFactory();
    expect(wrapper.vm.analysisMenuItems).toEqual(noAnalysisItems);
    // When there is an open event that does have analysis items
    wrapper.vm.eventStore.open = eventReadFactory({
      analysisTypes: ["analysisTypeA", "analysisTypeB"],
    });
    expect(wrapper.vm.analysisMenuItems.items[0][0].items).toHaveLength(2);
    expect(wrapper.vm.analysisMenuItems.items[0][0].items[0].label).toEqual(
      "analysisTypeA",
    );
    expect(wrapper.vm.analysisMenuItems.items[0][0].items[1].label).toEqual(
      "analysisTypeB",
    );
  });

  it("updates menuItems when the eventStore changes", async () => {
    const { wrapper } = factory();
    wrapper.vm.eventStore.open = eventReadFactory();
    expect(wrapper.vm.menuItems).toEqual([
      ...wrapper.vm.defaultItems,
      noAnalysisItems,
    ]);
    wrapper.vm.eventStore.open = eventReadFactory({
      analysisTypes: ["analysisTypeA", "analysisTypeB"],
    });
    await wrapper.vm.$nextTick();
    await flushPromises();
    expect(wrapper.vm.menuItems[2].items[0][0].items).toHaveLength(2);
    expect(wrapper.vm.menuItems[2].items[0][0].items[0].label).toEqual(
      "analysisTypeA",
    );
    expect(wrapper.vm.menuItems[2].items[0][0].items[1].label).toEqual(
      "analysisTypeB",
    );
  });

  it("opens a given modal when the open function is called", () => {
    const { wrapper } = factory({
      stubActions: false,
    });

    expect(wrapper.vm.modalStore.openModals).toStrictEqual([]);
    wrapper.vm.open("modal1");
    expect(wrapper.vm.modalStore.openModals).toStrictEqual(["modal1"]);
  });

  it("updates ownership of selected node to current user and requests eventStore reload when Take Ownership clicked", async () => {
    myNock.options("/event/").reply(200).patch("/event/").reply(403);
    const { wrapper } = factory();
    wrapper.vm.authStore.user = { username: "testingUser" };
    wrapper.vm.selectedStore.selected = ["uuid1"];
    await wrapper.vm.takeOwnership();
    // this will still be truthy bc it's in the same component as requestReload()
    expect(wrapper.vm.eventStore.update).toHaveBeenNthCalledWith(1, [
      { owner: "testingUser", uuid: "uuid1" },
    ]);
    expect(wrapper.vm.eventStore.requestReload).toBeTruthy();
  });

  it("sets the error and does not request reload if takeOwnership fails", async () => {
    myNock.options("/event/").reply(200).patch("/event/").reply(403);

    const { wrapper } = factory({
      stubActions: false,
    });

    wrapper.vm.authStore.user = { username: "testingUser" };
    wrapper.vm.selectedStore.selected = ["uuid1"];

    await wrapper.vm.takeOwnership();
    expect(wrapper.vm.error).toEqual("Request failed with status code 403");
    // this will still be truthy bc it's in the same component as requestReload()
    expect(wrapper.vm.eventStore.requestReload).toBeFalsy();
  });
});
