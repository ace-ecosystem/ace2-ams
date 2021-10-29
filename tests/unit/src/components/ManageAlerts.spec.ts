import ManageAlerts from "@/pages/Alerts/ManageAlerts.vue";
import TheAlertActionToolbar from "@/components/Alerts/TheAlertActionToolbar.vue";
import TheFilterToolbar from "@/components/Filters/TheFilterToolbar.vue";
import TheAlertsTable from "@/components/Alerts/TheAlertsTable.vue";
import { shallowMount } from "@vue/test-utils";

describe("ManageAlerts.vue", () => {
  const wrapper = shallowMount(ManageAlerts);
  it("renders", () => {
    expect(wrapper.exists()).toBe(true);
  });

  it("contains expected components", () => {
    expect(wrapper.findComponent(TheAlertActionToolbar).exists()).toBe(true);
    expect(wrapper.findComponent(TheFilterToolbar).exists()).toBe(true);
    expect(wrapper.findComponent(TheAlertsTable).exists()).toBe(true);
  });
});
