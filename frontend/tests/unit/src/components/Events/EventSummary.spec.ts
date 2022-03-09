import EventSummary from "@/components/Events/EventSummary.vue";
import { shallowMount, VueWrapper } from "@vue/test-utils";
import { TestingOptions } from "@pinia/testing";
import { createCustomPinia } from "@unit/helpers";
import { testConfiguration } from "@/etc/configuration/test/index";
import { eventReadFactory } from "./../../../../mocks/events";
import { expect } from "vitest";
import { genericObjectReadFactory } from "../../../../mocks/genericObject";
import { parseEventSummary } from "../../../../../src/stores/eventTable";

const mockQueue = genericObjectReadFactory({ value: "external" });
const mockEvent = eventReadFactory({
  queue: mockQueue,
});
const mockEventSummary = parseEventSummary(mockEvent);

const stubDate = new Date("2022-03-02T00:00:00.000-05:00");
const mockEventManualTimes = eventReadFactory({
  queue: mockQueue,
  eventTime: stubDate,
  autoEventTime: stubDate,
  alertTime: stubDate,
  autoAlertTime: stubDate,
  ownershipTime: stubDate,
  autoOwnershipTime: stubDate,
  dispositionTime: stubDate,
  autoDispositionTime: stubDate,
  containTime: stubDate,
  remediationTime: stubDate,
});
const mockEventAutoTimes = eventReadFactory({
  queue: mockQueue,
  eventTime: null,
  autoEventTime: stubDate,
  alertTime: null,
  autoAlertTime: stubDate,
  ownershipTime: null,
  autoOwnershipTime: stubDate,
  dispositionTime: null,
  autoDispositionTime: stubDate,
  containTime: null,
  remediationTime: null,
});

function factory(options: TestingOptions = {}, openEvent = null) {
  const wrapper: VueWrapper<any> = shallowMount(EventSummary, {
    global: {
      plugins: [
        createCustomPinia({
          ...options,
          initialState: {
            eventStore: { open: openEvent, requestReload: false },
          },
        }),
      ],
      provide: { config: testConfiguration },
    },
  });

  return { wrapper };
}

describe("EventSummary", () => {
  it("renders", () => {
    const { wrapper } = factory();
    expect(wrapper.exists()).toBe(true);
  });
  it("sets up data onMounted if eventStore.open does not exist", () => {
    const { wrapper } = factory();
    expect(wrapper.vm.eventTableData).toEqual([]);
    expect(wrapper.vm.eventTimes).toEqual([]);
    expect(wrapper.vm.columns).toEqual([]);
    expect(wrapper.vm.columnOptions).toEqual([]);
    expect(wrapper.vm.selectedColumns).toEqual([]);
  });
  it("sets up data onMounted if eventStore.open exists", () => {
    const { wrapper } = factory({}, mockEvent);
    expect(wrapper.vm.eventTableData).toEqual([mockEventSummary]);
    expect(wrapper.vm.eventTimes).toHaveLength(6);
    expect(wrapper.vm.columns).toEqual(
      testConfiguration.events.eventQueueColumnMappings["external"],
    );
    expect(wrapper.vm.columnOptions).toHaveLength(12);
    expect(wrapper.vm.selectedColumns).toHaveLength(6);
  });
  it.each([
    [
      mockEventManualTimes,
      stubDate,
      stubDate,
      stubDate,
      stubDate,
      stubDate,
      stubDate,
    ],
    [mockEventAutoTimes, stubDate, stubDate, stubDate, stubDate, "TBD", "TBD"],
  ])(
    "sets up eventTimes in initData based on times in event",
    (
      event,
      expectedEventTime,
      expectedAlertTime,
      expectedOwnershipTime,
      expectedDispositionTime,
      expectedContainTime,
      expectedRemediationTime,
    ) => {
      const { wrapper } = factory({}, event);
      expect(wrapper.vm.eventTimes).toHaveLength(6);
      expect(wrapper.vm.eventTimes[0].label).toEqual("Event");
      expect(wrapper.vm.eventTimes[0].datetime).toEqual(expectedEventTime);
      expect(wrapper.vm.eventTimes[1].label).toEqual("Alert");
      expect(wrapper.vm.eventTimes[1].datetime).toEqual(expectedAlertTime);
      expect(wrapper.vm.eventTimes[2].label).toEqual("Ownership");
      expect(wrapper.vm.eventTimes[2].datetime).toEqual(expectedOwnershipTime);
      expect(wrapper.vm.eventTimes[3].label).toEqual("Disposition");
      expect(wrapper.vm.eventTimes[3].datetime).toEqual(
        expectedDispositionTime,
      );
      expect(wrapper.vm.eventTimes[4].label).toEqual("Contain");
      expect(wrapper.vm.eventTimes[4].datetime).toEqual(expectedContainTime);
      expect(wrapper.vm.eventTimes[5].label).toEqual("Remediation");
      expect(wrapper.vm.eventTimes[5].datetime).toEqual(
        expectedRemediationTime,
      );
    },
  );
  it("correctly computes timelineEvents", () => {
    const { wrapper } = factory({}, mockEvent);
    expect(wrapper.vm.timelineEvents).toEqual(wrapper.vm.eventTimes);
  });
  it("correctly returns a formatted time on formatDatetime", () => {
    const { wrapper } = factory();
    const res1 = wrapper.vm.formatDatetime("TBD");
    expect(res1).toEqual("TBD");
    const res2 = wrapper.vm.formatDatetime(stubDate);
    expect(res2).toEqual("3/2/2022, 5:00:00 AM");
  });
  it("correctly resets selectedColumns in resetColumns", () => {
    const { wrapper } = factory({}, mockEvent);
    wrapper.vm.selectedColumns = [];
    expect(wrapper.vm.selectedColumns).toEqual([]);
    wrapper.vm.resetColumns();
    expect(wrapper.vm.selectedColumns).toHaveLength(6);
  });
});
