import { genericObjectReadFactory } from "./../../../../mocks/genericObject";
import TheEventsTable from "@/components/Events/TheEventsTable.vue";
import { shallowMount, VueWrapper } from "@vue/test-utils";
import PrimeVue from "primevue/config";
import { TestingOptions } from "@pinia/testing";

import { createRouterMock, injectRouterMock } from "vue-router-mock";
import { createCustomPinia } from "../../helpers";

import { useAuthStore } from "@/stores/auth";
import { useCurrentUserSettingsStore } from "@/stores/currentUserSettings";
import { useFilterStore } from "@/stores/filter";
import { userReadFactory } from "../../../../mocks/user";

import { testConfiguration } from "@/etc/configuration/test/index";

import { expect } from "vitest";

function factory(options?: TestingOptions) {
  const router = createRouterMock();
  injectRouterMock(router);

  const testingPinia = createCustomPinia(options);

  const authStore = useAuthStore();
  authStore.user = userReadFactory();

  const wrapper: VueWrapper<any> = shallowMount(TheEventsTable, {
    global: {
      plugins: [testingPinia, PrimeVue],
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
    const defaultQueue = genericObjectReadFactory({ value: "external" });

    currentUserSettingsStore.queues.events = defaultQueue;
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
  it("will call setColumns when currentUserSettingsStore.queues.events changes", async () => {
    const { wrapper, currentUserSettingsStore, filterStore } = factory();
    const defaultQueue = genericObjectReadFactory({ value: "external" });

    currentUserSettingsStore.queues.events = defaultQueue;

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
    const defaultQueue = genericObjectReadFactory({ value: "external" });

    currentUserSettingsStore.queues.alerts = defaultQueue;

    await wrapper.vm.$nextTick();

    expect(wrapper.vm.preferredEventQueue).toStrictEqual(null);
    expect(wrapper.vm.columns).toHaveLength(0);
    expect(filterStore.setFilter).toHaveBeenCalledTimes(0);
    expect(wrapper.vm.key).toStrictEqual(0);
  });
});
