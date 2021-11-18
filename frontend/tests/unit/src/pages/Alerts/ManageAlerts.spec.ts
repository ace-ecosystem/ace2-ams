import ManageAlerts from "@/pages/Alerts/ManageAlerts.vue";
import TheAlertActionToolbar from "@/components/Alerts/TheAlertActionToolbar.vue";
import TheFilterToolbar from "@/components/Filters/TheFilterToolbar.vue";
import TheAlertsTable from "@/components/Alerts/TheAlertsTable.vue";
import DateRangePicker from "@/components/UserInterface/DateRangePicker.vue";
import store from "@/store";
import { mount, shallowMount } from "@vue/test-utils";

describe("ManageAlerts.vue", () => {
  const wrapper = mount(ManageAlerts, {
    global: {
      plugins: [store],
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

    const datepicker = wrapper.findComponent(DateRangePicker).vm;
    expect(datepicker.filterType).toEqual("alerts");
    expect(datepicker.rangeFilterOptions).toEqual([
      "Event Time",
      "Insert Time",
      "Dispositioned Time",
    ]);
    expect(datepicker.rangeFilters).toEqual({
      "Event Time": { start: "eventTimeAfter", end: "eventTimeBefore" },
      "Insert Time": { start: "insertTimeAfter", end: "insertTimeBefore" },
      "Dispositioned Time": {
        start: "dispositionedAfter",
        end: "dispositionedBefore",
      },
    });
  });
});
