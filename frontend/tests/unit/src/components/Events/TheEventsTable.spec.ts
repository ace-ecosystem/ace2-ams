import { genericObjectReadFactory } from "./../../../../mocks/genericObject";
import TheEventsTable from "@/components/Events/TheEventsTable.vue";
import { shallowMount, VueWrapper } from "@vue/test-utils";
import PrimeVue from "primevue/config";
import { TestingOptions } from "@pinia/testing";

import { createRouterMock, injectRouterMock } from "vue-router-mock";
import { createCustomPinia } from "../../helpers";

import { useCurrentUserSettingsStore } from "../../../../../src/stores/currentUserSettings";
import { useFilterStore } from "../../../../../src/stores/filter";

import { testConfiguration } from "@/etc/configuration/test/index";

import { vitest, expect } from "vitest";

function factory(options?: TestingOptions) {
  const router = createRouterMock();
  injectRouterMock(router);

  const wrapper: VueWrapper<any> = shallowMount(TheEventsTable, {
    global: {
      plugins: [createCustomPinia(options), PrimeVue],
      provide: {
        config: testConfiguration,
      },
    },
  });

  const currentUserSettingsStore = useCurrentUserSettingsStore();
  const filterStore = useFilterStore();

  return { wrapper, currentUserSettingsStore, filterStore };
}

// DATA/CREATION
describe("TheEventsTable data/creation", () => {
  it("renders", async () => {
    const { wrapper } = factory();
    expect(wrapper.exists()).toBe(true);
  });

  it("initializes data as expected", () => {
    const { wrapper } = factory();
    expect(wrapper.vm.columns).toStrictEqual([]);
    expect(wrapper.vm.key).toStrictEqual(0);
    expect(wrapper.vm.preferredEventQueue).toStrictEqual(null);
  });

  it("will set columns and filter based on current user's preferred queue and increase the table key", async () => {
    const { wrapper, currentUserSettingsStore, filterStore } = factory();
    const defaultQueue = genericObjectReadFactory({ value: "default" });

    currentUserSettingsStore.preferredEventQueue = defaultQueue;
    wrapper.vm.setColumns();

    await wrapper.vm.$nextTick();

    expect(wrapper.vm.preferredEventQueue).toStrictEqual(defaultQueue);
    expect(wrapper.vm.columns).toHaveLength(13);
    expect(filterStore.setFilter).toHaveBeenCalledWith({
      nodeType: "events",
      filterName: "queue",
      filterValue: defaultQueue,
    });
    expect(wrapper.vm.key).toStrictEqual(1);
  });
  it("will call setColumns when currentUserSettingsStore.preferredEventQueue changes", async () => {
    const { wrapper, currentUserSettingsStore, filterStore } = factory();
    const defaultQueue = genericObjectReadFactory({ value: "default" });

    currentUserSettingsStore.preferredEventQueue = defaultQueue;

    await wrapper.vm.$nextTick();

    expect(wrapper.vm.preferredEventQueue).toStrictEqual(defaultQueue);
    expect(wrapper.vm.columns).toHaveLength(13);
    expect(filterStore.setFilter).toHaveBeenCalledWith({
      nodeType: "events",
      filterName: "queue",
      filterValue: defaultQueue,
    });
    expect(wrapper.vm.key).toStrictEqual(1);
  });
  it("will not update anything if currentUserSettingsStore updates, but doesn't include preferredEventQueue", async () => {
    const { wrapper, currentUserSettingsStore, filterStore } = factory();
    const defaultQueue = genericObjectReadFactory({ value: "default" });

    currentUserSettingsStore.preferredAlertQueue = defaultQueue;

    await wrapper.vm.$nextTick();

    expect(wrapper.vm.preferredEventQueue).toStrictEqual(null);
    expect(wrapper.vm.columns).toHaveLength(0);
    expect(filterStore.setFilter).toHaveBeenCalledTimes(0);
    expect(wrapper.vm.key).toStrictEqual(0);
  });
});
