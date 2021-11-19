import Button from "primevue/button";
import OverlayPanel from "primevue/overlaypanel";
import InputText from "primevue/inputtext";
import { DatePicker } from "v-calendar";
import MockDate from "mockdate";
import each from "jest-each";

import DateRangePicker from "@/components/UserInterface/DateRangePicker.vue";
import store from "@/store";
import { mount, VueWrapper } from "@vue/test-utils";
import { createStore } from "vuex";

describe("DateRangePicker setup", () => {
  const wrapper = mount(DateRangePicker, {
    global: {
      plugins: [store],
      provide: {
        filterType: "alerts",
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

  it("renders", () => {
    expect(wrapper.exists()).toBe(true);
  });

  it("contains expected (on render) components", () => {
    expect(wrapper.findComponent(Button).exists()).toBe(true);
    expect(wrapper.findComponent(OverlayPanel).exists()).toBe(true);
    expect(wrapper.findComponent(InputText).exists()).toBe(true);
    expect(wrapper.findComponent(DatePicker).exists()).toBe(true);
  });

  it("receives expected injected data", () => {
    expect(wrapper.vm.filterType).toEqual("alerts");
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
  const wrapper = mount(DateRangePicker, {
    global: {
      plugins: [store],
      provide: {
        filterType: "alerts",
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

  it("contains expected computed data when no filters are set", () => {
    expect(wrapper.vm.filters).toEqual({});
    expect(wrapper.vm.startFilter).toEqual("exampleTimeAfter");
    expect(wrapper.vm.endfilter).toEqual("exampleTimeBefore");
    expect(wrapper.vm.startDate).toBeNull();
    expect(wrapper.vm.endDate).toBeNull();
    expect(wrapper.vm.startDateUTC).toBeNull();
    expect(wrapper.vm.endDateUTC).toBeNull();
  });

  it("contains expected computed data when there are filters set", () => {
    const today = new Date();
    const yesterdayDate = today.getDate() - 1;
    const yesterday = new Date(today.setDate(yesterdayDate));

    store.dispatch("filters/setFilter", {
      filterType: "alerts",
      filterName: "exampleTimeAfter",
      filterValue: yesterday,
    });
    store.dispatch("filters/setFilter", {
      filterType: "alerts",
      filterName: "exampleTimeBefore",
      filterValue: today,
    });

    expect(wrapper.vm.filters).toEqual({
      exampleTimeAfter: yesterday,
      exampleTimeBefore: today,
    });
    expect(wrapper.vm.startFilter).toEqual("exampleTimeAfter");
    expect(wrapper.vm.endfilter).toEqual("exampleTimeBefore");
    expect(wrapper.vm.startDate).toEqual(yesterday);
    expect(wrapper.vm.endDate).toEqual(today);
    expect(wrapper.vm.startDateUTC).toEqual(yesterday.toUTCString());
    expect(wrapper.vm.endDateUTC).toEqual(today.toUTCString());
  });
});

describe("DateRangePicker watchers", () => {
  const wrapper = mount(DateRangePicker, {
    global: {
      plugins: [store],
      provide: {
        filterType: "alerts",
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

  it("clears currently set time filters when currentRangeFilter is modified", async () => {
    store.dispatch("filters/setFilter", {
      filterType: "alerts",
      filterName: "exampleTimeAfter",
      filterValue: yesterday,
    });
    store.dispatch("filters/setFilter", {
      filterType: "alerts",
      filterName: "exampleTimeBefore",
      filterValue: today,
    });

    expect(wrapper.vm.filters).toEqual({
      exampleTimeAfter: yesterday,
      exampleTimeBefore: today,
    });

    wrapper.setData({
      currentRangeFilter: "Other Time",
    });
    await wrapper.vm.$nextTick();

    expect(wrapper.vm.filters).toEqual({});
  });
});

describe("DateRangePicker methods", () => {
  let actions: {
      setFilter: jest.Mock<any, any>;
      unsetFilter: jest.Mock<any, any>;
    },
    store,
    wrapper: VueWrapper<any>;

  beforeEach(() => {
    actions = {
      setFilter: jest.fn(),
      unsetFilter: jest.fn(),
    };
    store = createStore({
      modules: {
        filters: {
          namespaced: true,
          getters: {
            alerts: () => {
              return {};
            },
          },
          actions: actions,
        },
      },
    });

    wrapper = mount(DateRangePicker, {
      global: {
        plugins: [store],
        provide: {
          filterType: "alerts",
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
  });

  it("correctly maps vuex actions", () => {
    wrapper.vm.setFilter();
    expect(actions.setFilter).toHaveBeenCalled();
    wrapper.vm.unsetFilter();
    expect(actions.unsetFilter).toHaveBeenCalled();
  });

  it("calls setFilter with correct arguments when dateSelect is called", () => {
    wrapper.vm.dateSelect(today, "exampleTimeAfter");
    expect(actions.setFilter.mock.calls).toHaveLength(1);
    expect(actions.setFilter.mock.calls[0][1]).toEqual({
      filterType: "alerts",
      filterName: "exampleTimeAfter",
      filterValue: today,
    });
  });

  it("calls unsetFilter with correct arguments when clearDate is called", () => {
    wrapper.vm.clearDate("exampleTimeAfter");
    expect(actions.unsetFilter.mock.calls).toHaveLength(1);
    expect(actions.unsetFilter.mock.calls[0][1]).toEqual({
      filterType: "alerts",
      filterName: "exampleTimeAfter",
    });
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
      MockDate.set(new Date(1997, 2, 2));
      wrapper.vm.setRange(option);
      expect(actions.setFilter.mock.calls).toHaveLength(2);
      expect(actions.setFilter.mock.calls[0][1]).toEqual({
        filterType: "alerts",
        filterName: "exampleTimeAfter",
        filterValue: startDate,
      });
      expect(actions.setFilter.mock.calls[1][1]).toEqual({
        filterType: "alerts",
        filterName: "exampleTimeBefore",
        filterValue: endDate,
      });
      actions.setFilter.mockReset();
      MockDate.reset();
    },
  );
});
