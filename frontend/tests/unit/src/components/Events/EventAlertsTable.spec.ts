import EventAlertsTable from "@/components/Events/EventAlertsTable.vue";
import { flushPromises, mount, VueWrapper } from "@vue/test-utils";
import { TestingOptions } from "@pinia/testing";
import { createRouterMock, injectRouterMock } from "vue-router-mock";
import { createCustomPinia } from "@unit/helpers";

import { useFilterStore } from "@/stores/filter";

import {
  mockAlertReadA,
  mockAlertReadB,
  mockAlertReadC,
} from "../../../../mocks/alert";
import { Alert } from "@/services/api/alert";

function factory(options: TestingOptions = {}, eventUuid = "uuid1") {
  const router = createRouterMock();
  injectRouterMock(router);

  const wrapper: VueWrapper<any> = mount(EventAlertsTable, {
    global: {
      plugins: [createCustomPinia(options)],
      provide: { nodeType: "events" },
    },
    props: {
      eventUuid: eventUuid,
    },
  });

  const filterStore = useFilterStore();

  return { wrapper, filterStore };
}

describe("EventAlertsTable", () => {
  it("renders", async () => {
    // Mock the API call used to fetch all of the alerts in the event
    vi.spyOn(Alert, "readAllPages").mockResolvedValueOnce([
      mockAlertReadA,
      mockAlertReadB,
      mockAlertReadC,
    ]);

    const { wrapper } = factory();
    expect(wrapper.exists()).toBe(true);
  });

  it("loads list of alerts and can remove selected alerts", async () => {
    // Mock the API call used to fetch all of the alerts in the event
    vi.spyOn(Alert, "readAllPages").mockResolvedValueOnce([
      mockAlertReadA,
      mockAlertReadB,
      mockAlertReadC,
    ]);

    const { wrapper } = factory();

    // The DataTable should not exist at first
    expect(wrapper.find("[data-cy=expandedEvent]").exists()).toBe(false);

    // The loading message should be present
    expect(
      wrapper
        .find("#loading-message")
        .text()
        .includes("Loading alerts, please hold..."),
    ).toBe(true);

    // Wait for the DOM to update
    await wrapper.vm.$nextTick();
    await flushPromises();

    // Now the DataTable should have replaced the loading message
    expect(wrapper.find("#loading-message").exists()).toBe(false);
    expect(wrapper.find("[data-cy=expandedEvent]").exists()).toBe(true);

    // The DataTable should have three rows for the alerts
    let rows = wrapper.findAll("tbody > tr");
    expect(rows.length).toBe(3);

    // Verify the first alert is not currently selected
    const checkbox = rows[0].find(".p-checkbox-box");
    expect(checkbox.attributes("aria-checked")).toBe("false");

    // TODO: This does not actually work... checkbox does not actually get checked.
    // // Click it to select the alert
    // console.log(checkbox.html());
    // await checkbox.find(".p-checkbox-icon").trigger("click");

    // console.log(checkbox.html());
    // expect(checkbox.attributes("aria-checked")).toBe("true");

    // Since "clicking" the checkbox doesn't seem to work, manually add the UUID of
    // the alert to the selectedAlertStore to simulate the click.
    wrapper.vm.selectedAlertStore.select(mockAlertReadA.uuid);

    // Mock the API call used to fetch the new list of alerts in the event
    vi.spyOn(Alert, "readAllPages").mockResolvedValueOnce([
      mockAlertReadB,
      mockAlertReadC,
    ]);

    // Mock the API call use to remove the alert from the event
    vi.spyOn(Alert, "update").mockResolvedValueOnce();

    // Click the Remove Alerts button.
    wrapper.find("[data-cy=remove-alerts-button]").trigger("click");
    await wrapper.vm.$nextTick();
    await flushPromises();

    // The DataTable should now only have two rows for the alerts
    rows = wrapper.findAll("tbody > tr");
    expect(rows.length).toBe(2);
  });
});
