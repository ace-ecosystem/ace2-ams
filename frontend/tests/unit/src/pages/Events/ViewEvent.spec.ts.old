import { createCustomPinia } from "@unit/helpers";
import { createRouterMock, getRouter, injectRouterMock } from "vue-router-mock";
import { eventReadFactory } from "../../../../mocks/events";
import { expect } from "vitest";
import { flushPromises, shallowMount, VueWrapper } from "@vue/test-utils";
import { testConfiguration } from "@/etc/configuration/test/index";
import { TestingOptions } from "@pinia/testing";
import { useEventStore } from "@/stores/event";
import { useSelectedEventStore } from "@/stores/selectedEvent";
import AnalysisDetailsBaseVue from "@/components/Analysis/AnalysisDetailsBase.vue";
import EventSummaryVue from "@/components/Events/EventSummary.vue";
import myNock from "@unit/services/api/nock";
import nock from "nock";
import ViewEvent from "@/pages/Events/ViewEvent.vue";

const mockEvent = eventReadFactory();

function factory(options?: TestingOptions) {
  myNock.get("/event/uuid1").reply(200, mockEvent);
  const router = createRouterMock({
    initialLocation: "/event/uuid1",
  });

  injectRouterMock(router);
  getRouter().setParams({ eventID: "uuid1" });

  const wrapper: VueWrapper<any> = shallowMount(ViewEvent, {
    global: {
      provide: {
        config: testConfiguration,
      },
      plugins: [createCustomPinia(options)],
    },
  });

  return {
    wrapper,
  };
}

describe("ViewEvent.vue", () => {
  afterAll(async () => {
    nock.cleanAll();
  });

  it("renders", async () => {
    const { wrapper } = factory();
    expect(wrapper.exists()).toBe(true);
  });
  it("reloads open event on reloadPage", async () => {
    const { wrapper } = factory();

    const eventStore = useEventStore();
    await wrapper.vm.reloadPage();
    expect(eventStore.read).toHaveBeenCalledTimes(2);
  });
  it("reloads open event when eventStore requestReload is set to true", async () => {
    factory();
    const eventStore = useEventStore();
    eventStore.requestReload = true;
    await flushPromises();
    expect(eventStore.read).toHaveBeenCalledTimes(2);
  });
  it("selects open event and fetches given eventID on initPage", async () => {
    const { wrapper } = factory({ stubActions: false });

    myNock.get("/event/uuid1").reply(200, mockEvent);
    const selectedEventStore = useSelectedEventStore();
    const eventStore = useEventStore();
    await wrapper.vm.initPage("uuid1");
    expect(selectedEventStore.selected).toEqual(["uuid1"]);
    expect(eventStore.open).toEqual(JSON.parse(JSON.stringify(mockEvent)));
  });
  it("unselects all selected events when umounted", async () => {
    const { wrapper } = factory({ stubActions: false });

    myNock.get("/event/uuid1").reply(200, mockEvent);
    const selectedEventStore = useSelectedEventStore();
    await wrapper.vm.initPage("uuid1");
    expect(selectedEventStore.selected).toEqual(["uuid1"]);
    wrapper.unmount();
    expect(selectedEventStore.selected).toEqual([]);
  });
  it("sets the current section and current component on updateSection using config", () => {
    const { wrapper } = factory();

    myNock.get("/event/uuid1").reply(200, mockEvent);

    expect(wrapper.vm.currentSection).toEqual("Event Summary");
    expect(wrapper.vm.currentComponent).toEqual(EventSummaryVue);
    wrapper.vm.updateSection("Unknown section");
    expect(wrapper.vm.currentSection).toEqual("Unknown section");
    expect(wrapper.vm.currentComponent).toEqual(AnalysisDetailsBaseVue);
    wrapper.vm.updateSection("Event Summary");
    expect(wrapper.vm.currentSection).toEqual("Event Summary");
    expect(wrapper.vm.currentComponent).toEqual(EventSummaryVue);
  });
});
