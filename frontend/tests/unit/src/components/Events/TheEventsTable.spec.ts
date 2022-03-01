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

import { expect } from "vitest";
import { userReadFactory } from "../../../../mocks/user";

function factory(options?: TestingOptions) {
  const router = createRouterMock();
  injectRouterMock(router);

  const wrapper: VueWrapper<any> = shallowMount(TheEventsTable, {
    global: {
      plugins: [
        createCustomPinia({
          ...options,
          initialState: {
            authStore: {
              user: userReadFactory({
                defaultAlertQueue: genericObjectReadFactory({
                  value: "external",
                }),
                defaultEventQueue: genericObjectReadFactory({
                  value: "external",
                }),
              }),
            },
          },
        }),
        PrimeVue,
      ],
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
    const defaultQueue = genericObjectReadFactory({ value: "external" });

    // these will be set up on mount
    expect(wrapper.vm.columns).toStrictEqual(
      testConfiguration.events.eventQueueColumnMappings.external,
    );
    expect(wrapper.vm.key).toStrictEqual(1);
    expect(wrapper.vm.preferredEventQueue).toStrictEqual(defaultQueue);
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
    expect(wrapper.vm.key).toStrictEqual(3);
  });
  it("will call setColumns when currentUserSettingsStore.preferredEventQueue changes", async () => {
    const { wrapper, currentUserSettingsStore, filterStore } = factory({
      stubActions: false,
    });
    const newQueue = genericObjectReadFactory({ value: "internal" });

    currentUserSettingsStore.queues.events = newQueue;

    await wrapper.vm.$nextTick();
    await wrapper.vm.$nextTick();

    expect(wrapper.vm.preferredEventQueue).toStrictEqual(newQueue);
    expect(wrapper.vm.columns).toHaveLength(13);
    expect(filterStore.setFilter).toHaveBeenCalledWith({
      nodeType: "events",
      filterName: "queue",
      filterValue: newQueue,
    });
    expect(wrapper.vm.key).toStrictEqual(2);
  });
  it("will not update anything if currentUserSettingsStore updates, but doesn't include preferredEventQueue", async () => {
    const { wrapper, currentUserSettingsStore, filterStore } = factory();
    const defaultQueue = genericObjectReadFactory({ value: "external" });
    const newQueue = genericObjectReadFactory({ value: "internal" });

    currentUserSettingsStore.queues.alerts = newQueue;

    await wrapper.vm.$nextTick();

    expect(wrapper.vm.preferredEventQueue).toStrictEqual(defaultQueue);
    expect(wrapper.vm.columns).toHaveLength(13);
    expect(filterStore.setFilter).toHaveBeenCalledTimes(1);
    expect(wrapper.vm.key).toStrictEqual(1);
  });
});
