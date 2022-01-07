import ManageAlerts from "@/pages/Alerts/ManageAlerts.vue";
import TheAlertActionToolbar from "@/components/Alerts/TheAlertActionToolbar.vue";
import TheFilterToolbar from "@/components/Filters/TheFilterToolbar.vue";
import TheAlertsTable from "@/components/Alerts/TheAlertsTable.vue";
import DateRangePicker from "@/components/UserInterface/DateRangePicker.vue";
import { mount, VueWrapper } from "@vue/test-utils";
import { createTestingPinia } from "@pinia/testing";
import Tooltip from "primevue/tooltip";
import { createRouterMock, injectRouterMock, getRouter } from "vue-router-mock";

describe("ManageAlerts.vue", () => {
  const router = createRouterMock({
    initialLocation: "/manage_alerts",
  });

  injectRouterMock(router);
  // getRouter().setParams({ alertID: "uuid1", analysisID: "uuid2" });

  const wrapper = mount(ManageAlerts, {
    global: {
      plugins: [createTestingPinia({ stubActions: false })],
      directives: { tooltip: Tooltip },
      stubs: ["TheAlertsTable"],
    },
  });
  it("renders", () => {
    expect(wrapper.exists()).toBe(true);
  });

  it("contains expected components", () => {
    expect(wrapper.findComponent(TheAlertActionToolbar).exists()).toBe(true);
    expect(wrapper.findComponent(TheFilterToolbar).exists()).toBe(true);
    expect(wrapper.findComponent(TheAlertsTable).exists()).toBe(true);
  });

  it("provides the correct data to be injected", () => {
    // All of the data provided by the ManageAlerts component is injected into the DateRangePicker child component
    // We can therefore find it and check its data for all the injected data

    const datepicker = wrapper.findComponent(DateRangePicker) as VueWrapper<any>;
    expect(datepicker.vm.filterType).toEqual("alerts");
    expect(datepicker.vm.rangeFilterOptions).toEqual([
      "Event Time",
      "Insert Time",
      "Disposition Time",
    ]);
    expect(datepicker.vm.rangeFilters).toEqual({
      "Event Time": { start: "eventTimeAfter", end: "eventTimeBefore" },
      "Insert Time": { start: "insertTimeAfter", end: "insertTimeBefore" },
      "Disposition Time": {
        start: "dispositionedAfter",
        end: "dispositionedBefore",
      },
    });
  });
});
