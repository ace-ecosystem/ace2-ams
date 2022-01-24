import ManageAlerts from "@/pages/Alerts/ManageAlerts.vue";
import TheAlertActionToolbar from "@/components/Alerts/TheAlertActionToolbar.vue";
import TheFilterToolbar from "@/components/Filters/TheFilterToolbar.vue";
import TheAlertsTable from "@/components/Alerts/TheAlertsTable.vue";
import DateRangePicker from "@/components/UserInterface/DateRangePicker.vue";
import { mount, VueWrapper } from "@vue/test-utils";
import { createTestingPinia, TestingOptions } from "@pinia/testing";
import Tooltip from "primevue/tooltip";
import { createRouterMock, injectRouterMock } from "vue-router-mock";
import { useFilterStore } from "@/stores/filter";
import { useModalStore } from "@/stores/modal";
import * as helpers from "@/etc/helpers";

function factory(
  initialLocation = "/manage_alerts",
  piniaOptions?: TestingOptions,
) {
  const router = createRouterMock({
    initialLocation: initialLocation,
  });
  injectRouterMock(router);

  const wrapper = mount(ManageAlerts, {
    global: {
      plugins: [createTestingPinia(piniaOptions)],
      directives: { tooltip: Tooltip },
      stubs: ["TheAlertsTable", "TagModal", "FilterChipContainer"],
    },
  });

  const filterStore = useFilterStore();
  const modalStore = useModalStore();

  return { wrapper, filterStore, modalStore, router };
}

describe("ManageAlerts.vue", () => {
  it("renders", () => {
    const { wrapper } = factory();
    expect(wrapper.exists()).toBe(true);
  });

  it("contains expected components", () => {
    const { wrapper } = factory();

    expect(wrapper.findComponent(TheAlertActionToolbar).exists()).toBe(true);
    expect(wrapper.findComponent(TheFilterToolbar).exists()).toBe(true);
    expect(wrapper.findComponent(TheAlertsTable).exists()).toBe(true);
  });

  it("will not add any filters that cannot be found", () => {
    jest
      .spyOn(helpers, "populateCommonStores")
      .mockImplementationOnce(() => Promise.resolve());
    factory("/manage_alerts?fake_filter=blah");
    const filterStore = useFilterStore();

    expect(Object.keys(filterStore.alerts).length).toBeFalsy();
  });

  it("will parse given filters, set them in the filterStore, and reload on loadRouteQuery", async () => {
    jest
      .spyOn(helpers, "populateCommonStores")
      .mockImplementationOnce(() => Promise.resolve());
    const { wrapper, filterStore, router } = factory(
      "/manage_alerts?tags=tagA,tagB",
      {
        stubActions: false,
      },
    );

    await wrapper.vm.$nextTick();
    expect(filterStore.alerts).toEqual({
      tags: ["tagA", "tagB"],
    });

    // should route you back to /manage_alerts when done
    expect(router.currentRoute.value.fullPath).toEqual("/manage_alerts");
  });

  it("executes loadRouteQuery when route changes", async () => {
    jest
      .spyOn(helpers, "populateCommonStores")
      .mockImplementationOnce(() => Promise.resolve());
    const { wrapper, filterStore, router } = factory("/manage_alerts", {
      stubActions: false,
    });

    await wrapper.vm.$nextTick();
    expect(filterStore.alerts).toEqual({});

    // push new route with query
    router.push("/manage_alerts?tags=tagA,tagB");
    await wrapper.vm.$nextTick();
    expect(filterStore.alerts).toEqual({
      tags: ["tagA", "tagB"],
    });

    // should route you back to /manage_alerts when done
    expect(router.currentRoute.value.fullPath).toEqual("/manage_alerts");
  });

  it("will attempt to load common stores if url parameters are provided", async () => {
    const spy = jest
      .spyOn(helpers, "populateCommonStores")
      .mockImplementationOnce(() => Promise.resolve());
    factory("/manage_alerts?fake_filter=blah");
    expect(spy).toHaveBeenCalled();
  });
});
