import { useEventTableStore } from "@/stores/eventTable";
import { useModalStore } from "@/stores/modal";
import EventTableCell from "@/components/Events/EventTableCell.vue";
import { shallowMount, VueWrapper } from "@vue/test-utils";
import PrimeVue from "primevue/config";
import { createTestingPinia, TestingOptions } from "@pinia/testing";

import { createRouterMock, injectRouterMock } from "vue-router-mock";

function factory(
  piniaOptions: TestingOptions = {},
  data = { name: "event" },
  field = "name",
) {
  const router = createRouterMock();
  injectRouterMock(router);

  const wrapper: VueWrapper<any> = shallowMount(EventTableCell, {
    global: {
      plugins: [createTestingPinia(piniaOptions), PrimeVue],
    },
    props: {
      data: data,
      field: field,
    },
  });

  const eventTableStore = useEventTableStore();
  const modalStore = useModalStore();

  return { wrapper, modalStore, eventTableStore };
}

describe("EventTableCell", () => {
  it("renders", async () => {
    const { wrapper } = factory();
    expect(wrapper.exists()).toBe(true);
  });
  it("correctly formats a given date object into string", () => {
    const { wrapper } = factory();
    let result = wrapper.vm.formatDateTime(null);
    expect(result).toEqual("None");
    result = wrapper.vm.formatDateTime(new Date("2022-01-24"));
    expect(result).toEqual("1/24/2022, 12:00:00 AM");
  });
  it("correctly formats a given uuid object into the correct path", () => {
    const { wrapper } = factory();
    const result = wrapper.vm.getEventLink("uuid1");
    expect(result).toEqual("/event/uuid1");
  });
  it("correctly joins an array of strings using joinStringArray", () => {
    const { wrapper } = factory();
    const result = wrapper.vm.joinStringArray(["stringA", "stringB"]);
    expect(result).toEqual("stringA, stringB");
  });
  it("correctly opens a given modal on open", () => {
    const { wrapper, modalStore } = factory({ stubActions: false });

    expect(modalStore.openModals).toEqual([]);
    wrapper.vm.open("TestModal");
    expect(modalStore.openModals).toEqual(["TestModal"]);
  });
  it("sets the eventTableStore requestReload property to true on requestReload", () => {
    const { wrapper, eventTableStore } = factory({ stubActions: false });

    expect(eventTableStore.requestReload).toBeFalsy();
    wrapper.vm.requestReload();
    expect(eventTableStore.requestReload).toBeTruthy();
  });
});
