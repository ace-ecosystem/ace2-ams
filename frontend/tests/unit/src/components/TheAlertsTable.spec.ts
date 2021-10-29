import TheAlertsTable from "@/components/Alerts/TheAlertsTable.vue";
import { mount } from "@vue/test-utils";

describe("TheAlertsTable.vue", () => {
  const wrapper = mount(TheAlertsTable);

  it("renders", () => {
    expect(wrapper.exists()).toBe(true);
  });
});
