import Button from "primevue/button";
import OverlayPanel from "primevue/overlaypanel";
import InputText from "primevue/inputtext";
import { DatePicker } from "v-calendar";
import Tooltip from "primevue/tooltip";
import MockDate from "mockdate";
import each from "jest-each";
import { createTestingPinia, TestingOptions } from "@pinia/testing";

import DateRangePicker from "@/components/UserInterface/DateRangePicker.vue";
import { mount, VueWrapper } from "@vue/test-utils";

function factory(options?: TestingOptions) {
  const wrapper: VueWrapper<any> = mount(DateRangePicker, {
    global: {
      plugins: [createTestingPinia(options)],
      directives: { tooltip: Tooltip },
      provide: {
        nodeType: "alerts",
        rangeFilterOptions: ["Example Time", "Other Time"],
        rangeFilters: {
          "Example Time": {
            start: "exampleTimeAfter",
            end: "exampleTimeBefore",
          },
          "Other Time": {
            start: "otherTimeAfter",
            end: "otherTimeBefore",
          },
        },
      },
    },
  });

  return { wrapper };
}

describe("DateRangePicker setup", () => {
  it("renders", () => {
    const { wrapper } = factory();

    expect(wrapper.exists()).toBe(true);
  });

  it("contains expected (on render) components", () => {
    const { wrapper } = factory();

    expect(wrapper.findComponent(Button).exists()).toBe(true);
    expect(wrapper.findComponent(OverlayPanel).exists()).toBe(true);
    expect(wrapper.findComponent(InputText).exists()).toBe(true);
    expect(wrapper.findComponent(DatePicker).exists()).toBe(true);
  });

  it("receives expected injected data", () => {
    const { wrapper } = factory();

    expect(wrapper.vm.nodeType).toEqual("alerts");
    expect(wrapper.vm.rangeFilterOptions).toEqual([
      "Example Time",
      "Other Time",
    ]);
    expect(wrapper.vm.rangeFilters).toEqual({
      "Example Time": {
        start: "exampleTimeAfter",
        end: "exampleTimeBefore",
      },
      "Other Time": {
        start: "otherTimeAfter",
        end: "otherTimeBefore",
      },
    });
  });

  it("contains expected (on render) data", () => {
    const { wrapper } = factory();

    expect(wrapper.vm.currentRangeFilter).toEqual("Example Time");
    expect(wrapper.vm.TODAY).toEqual("today");
    expect(wrapper.vm.YESTERDAY).toEqual("yesterday");
    expect(wrapper.vm.LAST_SEVEN).toEqual("last_seven");
    expect(wrapper.vm.LAST_THIRTY).toEqual("last_thirty");
    expect(wrapper.vm.LAST_SIXTY).toEqual("last_sixty");
    expect(wrapper.vm.THIS_MONTH).toEqual("this_month");
    expect(wrapper.vm.LAST_MONTH).toEqual("last_month");
  });
});

const today = new Date();
const yesterdayDate = today.getDate() - 1;
const yesterday = new Date(today.setDate(yesterdayDate));

describe("DateRangePicker computed properties", () => {
  it("contains expected computed data when no filters are set", () => {
    const { wrapper } = factory();

    expect(wrapper.vm.filters).toEqual({});
    expect(wrapper.vm.startFilter).toEqual("exampleTimeAfter");
    expect(wrapper.vm.endFilter).toEqual("exampleTimeBefore");
    expect(wrapper.vm.startDate).toBeNull();
    expect(wrapper.vm.endDate).toBeNull();
    expect(wrapper.vm.startDateUTC).toBeNull();
    expect(wrapper.vm.endDateUTC).toBeNull();
  });

  it("contains expected computed data when there are filters set", () => {
    const { wrapper } = factory({ stubActions: false });

    const today = new Date();
    const yesterdayDate = today.getDate() - 1;
    const yesterday = new Date(today.setDate(yesterdayDate));

    wrapper.vm.filterStore.setFilter({
      nodeType: "alerts",
      filterName: "exampleTimeAfter",
      filterValue: yesterday,
    });

    wrapper.vm.filterStore.setFilter({
      nodeType: "alerts",
      filterName: "exampleTimeBefore",
      filterValue: today,
    });

    expect(wrapper.vm.filters).toEqual({
      exampleTimeAfter: yesterday,
      exampleTimeBefore: today,
    });
    expect(wrapper.vm.startFilter).toEqual("exampleTimeAfter");
    expect(wrapper.vm.endFilter).toEqual("exampleTimeBefore");
    expect(wrapper.vm.startDate).toEqual(yesterday);
    expect(wrapper.vm.endDate).toEqual(today);
    expect(wrapper.vm.startDateUTC).toEqual(yesterday.toUTCString());
    expect(wrapper.vm.endDateUTC).toEqual(today.toUTCString());
  });
});

describe("DateRangePicker watchers", () => {
  it("clears currently set time filters when currentRangeFilter is modified", async () => {
    const { wrapper } = factory({ stubActions: false });

    wrapper.vm.filterStore.setFilter({
      nodeType: "alerts",
      filterName: "exampleTimeAfter",
      filterValue: yesterday,
    });

    wrapper.vm.filterStore.setFilter({
      nodeType: "alerts",
      filterName: "exampleTimeBefore",
      filterValue: today,
    });

    expect(wrapper.vm.filters).toEqual({
      exampleTimeAfter: yesterday,
      exampleTimeBefore: today,
    });

    wrapper.vm.currentRangeFilter = "Other Time";
    await wrapper.vm.$nextTick();

    expect(wrapper.vm.filters).toEqual({});
  });
});

describe("DateRangePicker methods", () => {
  it("calls setFilter when dateSelect is called", () => {
    const { wrapper } = factory({ stubActions: false });

    wrapper.vm.dateSelect(today, "exampleTimeAfter");

    expect(wrapper.vm.filterStore.alerts).toEqual({
      exampleTimeAfter: today,
    });
  });

  it("calls unsetFilter when clearDate is called", () => {
    const { wrapper } = factory({ stubActions: false });

    wrapper.vm.dateSelect(today, "exampleTimeAfter");
    expect(wrapper.vm.filterStore.alerts).toEqual({
      exampleTimeAfter: today,
    });

    wrapper.vm.clearDate("exampleTimeAfter");
    expect(wrapper.vm.filterStore.alerts).toEqual({});
  });

  each([
    [
      "today",
      new Date(1997, 2, 2, 0, 0, 0, 0),
      new Date(1997, 2, 2, 23, 59, 59, 0),
    ],
    [
      "yesterday",
      new Date(1997, 2, 1, 0, 0, 0, 0),
      new Date(1997, 2, 1, 23, 59, 59, 0),
    ],
    [
      "last_seven",
      new Date(1997, 1, 23, 0, 0, 0, 0),
      new Date(1997, 2, 2, 23, 59, 59, 0),
    ],
    [
      "last_thirty",
      new Date(1997, 0, 31, 0, 0, 0, 0),
      new Date(1997, 2, 2, 23, 59, 59, 0),
    ],
    [
      "last_sixty",
      new Date(1997, 0, 1, 0, 0, 0, 0),
      new Date(1997, 2, 2, 23, 59, 59, 0),
    ],
    [
      "this_month",
      new Date(1997, 2, 1, 0, 0, 0, 0),
      new Date(1997, 2, 2, 23, 59, 59, 0),
    ],
    [
      "last_month",
      new Date(1997, 1, 1, 0, 0, 0, 0),
      new Date(1997, 1, 28, 23, 59, 59, 0),
    ],
  ]).it(
    "sets date range to the correct range option '%s'",
    (option, startDate, endDate) => {
      const { wrapper } = factory({ stubActions: false });

      MockDate.set(new Date(1997, 2, 2));
      wrapper.vm.setRange(option);

      expect(wrapper.vm.filterStore.alerts).toEqual({
        exampleTimeAfter: startDate,
        exampleTimeBefore: endDate,
      });
    },
  );
});
