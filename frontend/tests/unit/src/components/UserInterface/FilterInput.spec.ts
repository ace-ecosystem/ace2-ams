import { createTestingPinia, TestingOptions } from "@pinia/testing";

import FilterInput from "@/components/UserInterface/FilterInput.vue";
import { mount } from "@vue/test-utils";
import { filterTypes } from "@/etc/constants";
import { useObservableTypeStore } from "@/stores/observableType";
import { useUserStore } from "@/stores/user";
import { observableTypeRead } from "@/models/observableType";
import { userRead } from "@/models/user";

const FILTERS_STUB = [
  {
    name: "name",
    label: "Name",
    type: filterTypes.INPUT_TEXT,
  },
  {
    name: "owner",
    label: "Owner",
    type: filterTypes.SELECT,
    store: useUserStore,
    optionLabel: "displayName",
    optionValue: "username",
  },
  {
    name: "observable",
    label: "Observable",
    store: useObservableTypeStore,
    type: filterTypes.CATEGORIZED_VALUE,
  },
  {
    name: "tags",
    label: "Tags",
    type: filterTypes.CHIPS,
  },
  {
    name: "observable_types",
    label: "Observable Types",
    type: filterTypes.MULTISELECT,
  },
  {
    name: "timeAfter",
    label: "After",
    type: filterTypes.DATE,
  },
];

const USERS_STUB: userRead[] = [
  {
    defaultAlertQueue: { description: null, uuid: "1", value: "default" },
    displayName: "Test Analyst",
    email: "analyst@test.com",
    enabled: true,
    roles: [],
    timezone: "UTC",
    username: "test analyst",
    uuid: "1",
  },
  {
    defaultAlertQueue: { description: null, uuid: "1", value: "default" },
    displayName: "Test Analyst2",
    email: "analyst2@test.com",
    enabled: true,
    roles: [],
    timezone: "UTC",
    username: "test analyst2",
    uuid: "2",
  },
];
const OBSERVABLE_TYPES_STUB: observableTypeRead[] = [
  {
    description: null,
    uuid: "1",
    value: "file",
  },
  {
    description: null,
    uuid: "2",
    value: "ipv4",
  },
];

function factory(
  filter: {
    filterName: string | null;
    filterValue: Record<string, string> | null;
  },
  options?: TestingOptions,
) {
  const wrapper = mount(FilterInput, {
    props: {
      modelValue: filter,
    },
    global: {
      plugins: [createTestingPinia(options)],
      provide: {
        filterType: "alerts",
        availableFilters: FILTERS_STUB,
      },
    },
  });

  return { wrapper };
}

describe("FilterInput setup w/o set filter", () => {
  it("renders", () => {
    const { wrapper } = factory({ filterName: null, filterValue: null });

    expect(wrapper.exists()).toBe(true);
  });

  it("sets up data correctly", () => {
    const { wrapper } = factory({ filterName: null, filterValue: null });

    expect(wrapper.vm.filterName).toEqual(FILTERS_STUB[0]);
    expect(wrapper.vm.filterValue).toBeNull();
  });
});

describe("FilterInput setup w/ set filter", () => {
  it("renders", () => {
    const { wrapper } = factory({
      filterName: "owner",
      filterValue: {
        displayName: "Test Analyst",
        username: "test analyst",
      },
    });

    expect(wrapper.exists()).toBe(true);
  });

  it("sets up data correctly", () => {
    const { wrapper } = factory({
      filterName: "owner",
      filterValue: {
        displayName: "Test Analyst",
        username: "test analyst",
      },
    });

    const userStore = useUserStore();
    userStore.items = USERS_STUB;

    expect(wrapper.vm.filterName).toEqual(FILTERS_STUB[1]);
    expect(wrapper.vm.filterOptions).toEqual(USERS_STUB);
    expect(wrapper.vm.filterValue).toEqual({
      displayName: "Test Analyst",
      username: "test analyst",
    });
  });
});

describe("FilterInput computed properties w/o set filter", () => {
  it("contains expected computed data when no filters are set (default to an input filter)", () => {
    const { wrapper } = factory({ filterName: null, filterValue: null });

    expect(wrapper.vm.filterOptions).toBeNull();
    expect(wrapper.vm.filterOptionLabel).toEqual("value");
    expect(wrapper.vm.isDate).toBeFalsy();
    expect(wrapper.vm.isCategorizedValue).toBeFalsy();
    expect(wrapper.vm.isChips).toBeFalsy();
    expect(wrapper.vm.isInputText).toBeTruthy();
    expect(wrapper.vm.isDropdown).toBeFalsy();
    expect(wrapper.vm.isMultiSelect).toBeFalsy();
    expect(wrapper.vm.inputType).toEqual(filterTypes.INPUT_TEXT);
  });
});

describe("FilterInput computed properties w/ set filter", () => {
  it("contains expected computed data when select/dropdown filter is set", () => {
    const { wrapper } = factory({ filterName: "owner", filterValue: null });

    const userStore = useUserStore();
    userStore.items = USERS_STUB;

    expect(wrapper.vm.filterOptions).toEqual(USERS_STUB);
    expect(wrapper.vm.filterOptionLabel).toEqual("displayName");
    expect(wrapper.vm.isDate).toBeFalsy();
    expect(wrapper.vm.isCategorizedValue).toBeFalsy();
    expect(wrapper.vm.isChips).toBeFalsy();
    expect(wrapper.vm.isInputText).toBeFalsy();
    expect(wrapper.vm.isDropdown).toBeTruthy();
    expect(wrapper.vm.isMultiSelect).toBeFalsy();
    expect(wrapper.vm.inputType).toEqual(filterTypes.SELECT);
  });

  it("contains expected computed data when categorized value filter is set", () => {
    const { wrapper } = factory({ filterName: "owner", filterValue: null });

    const observableTypeStore = useObservableTypeStore();
    observableTypeStore.items = OBSERVABLE_TYPES_STUB;

    wrapper.vm.filterName = FILTERS_STUB[2];
    wrapper.vm.filterValue = { category: null, value: null };

    expect(wrapper.vm.filterOptions).toEqual(OBSERVABLE_TYPES_STUB);
    expect(wrapper.vm.filterOptionLabel).toEqual("value");
    expect(wrapper.vm.isDate).toBeFalsy();
    expect(wrapper.vm.isCategorizedValue).toBeTruthy();
    expect(wrapper.vm.isChips).toBeFalsy();
    expect(wrapper.vm.isInputText).toBeFalsy();
    expect(wrapper.vm.isDropdown).toBeFalsy();
    expect(wrapper.vm.isMultiSelect).toBeFalsy();
    expect(wrapper.vm.inputType).toEqual(filterTypes.CATEGORIZED_VALUE);
  });

  it("contains expected computed data when chips filter is set", () => {
    const { wrapper } = factory({ filterName: "owner", filterValue: null });

    wrapper.vm.filterName = FILTERS_STUB[3];
    wrapper.vm.filterValue = null;

    expect(wrapper.vm.filterOptions).toBeNull();
    expect(wrapper.vm.filterOptionLabel).toEqual("value");
    expect(wrapper.vm.isDate).toBeFalsy();
    expect(wrapper.vm.isCategorizedValue).toBeFalsy();
    expect(wrapper.vm.isChips).toBeTruthy();
    expect(wrapper.vm.isInputText).toBeFalsy();
    expect(wrapper.vm.isDropdown).toBeFalsy();
    expect(wrapper.vm.isMultiSelect).toBeFalsy();
    expect(wrapper.vm.inputType).toEqual(filterTypes.CHIPS);
  });

  it("contains expected computed data when multiselect filter is set", () => {
    const { wrapper } = factory({ filterName: "owner", filterValue: null });

    wrapper.vm.filterName = FILTERS_STUB[4];
    wrapper.vm.filterValue = null;

    expect(wrapper.vm.filterOptions).toBeNull();
    expect(wrapper.vm.filterOptionLabel).toEqual("value");
    expect(wrapper.vm.isDate).toBeFalsy();
    expect(wrapper.vm.isCategorizedValue).toBeFalsy();
    expect(wrapper.vm.isChips).toBeFalsy();
    expect(wrapper.vm.isInputText).toBeFalsy();
    expect(wrapper.vm.isDropdown).toBeFalsy();
    expect(wrapper.vm.isMultiSelect).toBeTruthy();
    expect(wrapper.vm.inputType).toEqual(filterTypes.MULTISELECT);
  });
  it("contains expected computed data when date filter is set", () => {
    const { wrapper } = factory({ filterName: "owner", filterValue: null });

    wrapper.vm.filterName = FILTERS_STUB[5];
    wrapper.vm.filterValue = null;

    expect(wrapper.vm.filterOptions).toBeNull();
    expect(wrapper.vm.filterOptionLabel).toEqual("value");
    expect(wrapper.vm.isDate).toBeTruthy();
    expect(wrapper.vm.isCategorizedValue).toBeFalsy();
    expect(wrapper.vm.isChips).toBeFalsy();
    expect(wrapper.vm.isInputText).toBeFalsy();
    expect(wrapper.vm.isDropdown).toBeFalsy();
    expect(wrapper.vm.isMultiSelect).toBeFalsy();
    expect(wrapper.vm.inputType).toEqual(filterTypes.DATE);
  });
});

describe("FilterInput methods", () => {
  // beforeEach(() => {
  //   wrapper.vm.filterName = FILTERS_STUB[0];
  //   wrapper.vm.filterValue = null;
  // });

  it("executes updatedCategorizedValueObject as expected", () => {
    const { wrapper } = factory({ filterName: null, filterValue: null });

    wrapper.vm.filterName = FILTERS_STUB[2];
    wrapper.vm.filterValue = {
      category: OBSERVABLE_TYPES_STUB[0],
      value: null,
    };

    let result = wrapper.vm.updatedCategorizedValueObject(
      "category",
      OBSERVABLE_TYPES_STUB[1],
    );
    expect(result).toEqual({ category: OBSERVABLE_TYPES_STUB[1], value: null });
    result = wrapper.vm.updatedCategorizedValueObject("value", "0.0.0.0");
    expect(result).toEqual({
      category: OBSERVABLE_TYPES_STUB[0],
      value: "0.0.0.0",
    });
  });

  it("executes clearFilterValue as expected", () => {
    const { wrapper } = factory({ filterName: null, filterValue: null });

    wrapper.vm.filterValue = "test";
    wrapper.vm.clearFilterValue();
    expect(wrapper.vm.filterValue).toBeNull();

    wrapper.vm.filterName = FILTERS_STUB[2];
    const observableTypeStore = useObservableTypeStore();
    observableTypeStore.items = OBSERVABLE_TYPES_STUB;

    wrapper.vm.clearFilterValue();
    expect(wrapper.vm.filterValue).toEqual({
      category: OBSERVABLE_TYPES_STUB[0],
      value: null,
    });
  });

  it("executes getFilterNameObject as expected", () => {
    const { wrapper } = factory({ filterName: null, filterValue: null });

    let result = wrapper.vm.getFilterNameObject("tags");
    expect(result).toEqual(FILTERS_STUB[3]);
    result = wrapper.vm.getFilterNameObject("made up");
    expect(result).toBeNull();
    result = wrapper.vm.getFilterNameObject(null);
    expect(result).toEqual(FILTERS_STUB[0]);
  });

  it("executes updateValue as expected", async () => {
    const { wrapper } = factory({ filterName: null, filterValue: null });

    await wrapper.vm.$nextTick();

    wrapper.vm.updateValue("filterName", FILTERS_STUB[1]);
    await wrapper.vm.$nextTick();
    let result = wrapper.emitted()["update:modelValue"][1];
    expect(result).toEqual([{ filterName: "owner", filterValue: null }]);

    wrapper.vm.updateValue("filterValue", "hello!");
    await wrapper.vm.$nextTick();
    result = wrapper.emitted()["update:modelValue"][2];
    expect(result).toEqual([{ filterName: "name", filterValue: "hello!" }]);
  });
});
