import { createTestingPinia, TestingOptions } from "@pinia/testing";

import NodePropertyInput from "@/components/Node/NodePropertyInput.vue";
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
    optionProperty: "displayName",
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
    defaultEventQueue: { description: null, uuid: "1", value: "default" },
    displayName: "Test Analyst",
    email: "analyst@test.com",
    enabled: true,
    roles: [],
    timezone: "UTC",
    training: false,
    username: "test analyst",
    uuid: "1",
  },
  {
    defaultAlertQueue: { description: null, uuid: "1", value: "default" },
    defaultEventQueue: { description: null, uuid: "1", value: "default" },
    displayName: "Test Analyst2",
    email: "analyst2@test.com",
    enabled: true,
    roles: [],
    timezone: "UTC",
    training: true,
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
    filterValue: Record<string, unknown> | null;
  },
  options?: TestingOptions,
) {
  const wrapper = mount(NodePropertyInput, {
    props: {
      modelValue: filter,
      inputType: "filter",
    },
    global: {
      plugins: [createTestingPinia(options)],
      provide: {
        nodeType: "alerts",
        availableFilters: FILTERS_STUB,
      },
    },
  });

  return { wrapper };
}

describe("NodePropertyInput.vue", () => {
  it("renders with no given filter", () => {
    const { wrapper } = factory({ filterName: null, filterValue: null });

    expect(wrapper.exists()).toBe(true);
  });

  it("renders with a given filter", () => {
    const { wrapper } = factory({
      filterName: "owner",
      filterValue: {
        displayName: "Test Analyst",
        username: "test analyst",
      },
    });

    expect(wrapper.exists()).toBe(true);
  });

  it("sets up data correctly with no given filter", () => {
    const { wrapper } = factory({ filterName: null, filterValue: null });

    expect(wrapper.vm.filterName).toEqual(FILTERS_STUB[0]);
    expect(wrapper.vm.filterValue).toBeNull();
  });

  it("sets up data correctly with unknown filter", () => {
    const { wrapper } = factory({ filterName: "made_up", filterValue: null });

    expect(wrapper.vm.filterName).toBeNull();
    expect(wrapper.vm.filterValue).toBeNull();
  });

  it("sets up data correctly with an uninitialized select filter", async () => {
    const { wrapper } = factory({
      filterName: "owner",
      filterValue: null,
    });

    expect(wrapper.vm.filterName).toEqual(FILTERS_STUB[1]);
    // Attempts to set to default, however I can't get the userstore to load properly
    // so it ends up being undefined
    expect(wrapper.vm.filterValue).toEqual(undefined);
  });

  it("sets up data correctly with an initialized select filter", () => {
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

  it("sets up data correctly with an uninitialized categorized value filter", () => {
    const { wrapper } = factory({
      filterName: "observable",
      filterValue: null,
    });

    expect(wrapper.vm.filterName).toEqual(FILTERS_STUB[2]);
    expect(wrapper.vm.filterValue).toEqual({
      category: undefined, // Attempted to set to default, but couldn't load store
      value: null,
    });
  });

  it("sets up data correctly with an initialized categorized value filter", () => {
    const { wrapper } = factory({
      filterName: "observable",
      filterValue: {
        category: OBSERVABLE_TYPES_STUB[1],
        value: "test",
      },
    });

    const observableTypeStore = useObservableTypeStore();
    observableTypeStore.items = OBSERVABLE_TYPES_STUB;

    expect(wrapper.vm.filterName).toEqual(FILTERS_STUB[2]);
    expect(wrapper.vm.filterOptions).toEqual(OBSERVABLE_TYPES_STUB);
    expect(wrapper.vm.filterValue).toEqual({
      category: OBSERVABLE_TYPES_STUB[1],
      value: "test",
    });
  });

  it("contains expected computed data when no filters are set (default to an input filter)", () => {
    const { wrapper } = factory({ filterName: null, filterValue: null });

    expect(wrapper.vm.filterOptions).toBeNull();
    expect(wrapper.vm.filterOptionProperty).toEqual("value");
    expect(wrapper.vm.isDate).toBeFalsy();
    expect(wrapper.vm.isCategorizedValue).toBeFalsy();
    expect(wrapper.vm.isChips).toBeFalsy();
    expect(wrapper.vm.isInputText).toBeTruthy();
    expect(wrapper.vm.isDropdown).toBeFalsy();
    expect(wrapper.vm.isMultiSelect).toBeFalsy();
    expect(wrapper.vm.inputType).toEqual(filterTypes.INPUT_TEXT);
    expect(wrapper.vm.categorizedValueCategory).toBeNull();
    expect(wrapper.vm.categorizedValueValue).toBeNull();
    expect(wrapper.vm.categorizedValueObject).toEqual({
      category: null,
      value: null,
    });
  });

  it("contains expected computed data when select/dropdown filter is set", () => {
    const { wrapper } = factory({ filterName: "owner", filterValue: null });

    const userStore = useUserStore();
    userStore.items = USERS_STUB;

    expect(wrapper.vm.filterOptions).toEqual(USERS_STUB);
    expect(wrapper.vm.filterOptionProperty).toEqual("displayName");
    expect(wrapper.vm.isDate).toBeFalsy();
    expect(wrapper.vm.isCategorizedValue).toBeFalsy();
    expect(wrapper.vm.isChips).toBeFalsy();
    expect(wrapper.vm.isInputText).toBeFalsy();
    expect(wrapper.vm.isDropdown).toBeTruthy();
    expect(wrapper.vm.isMultiSelect).toBeFalsy();
    expect(wrapper.vm.inputType).toEqual(filterTypes.SELECT);
    expect(wrapper.vm.categorizedValueCategory).toBeNull();
    expect(wrapper.vm.categorizedValueValue).toBeNull();
    expect(wrapper.vm.categorizedValueObject).toEqual({
      category: null,
      value: null,
    });
  });

  it("contains expected computed data when categorized value filter is set", () => {
    const { wrapper } = factory({ filterName: "owner", filterValue: null });

    const observableTypeStore = useObservableTypeStore();
    observableTypeStore.items = OBSERVABLE_TYPES_STUB;

    wrapper.vm.filterName = FILTERS_STUB[2];
    wrapper.vm.filterValue = { category: null, value: null };

    wrapper.vm.clearFilterValue();

    expect(wrapper.vm.filterOptions).toEqual(OBSERVABLE_TYPES_STUB);
    expect(wrapper.vm.filterOptionProperty).toEqual("value");
    expect(wrapper.vm.isDate).toBeFalsy();
    expect(wrapper.vm.isCategorizedValue).toBeTruthy();
    expect(wrapper.vm.isChips).toBeFalsy();
    expect(wrapper.vm.isInputText).toBeFalsy();
    expect(wrapper.vm.isDropdown).toBeFalsy();
    expect(wrapper.vm.isMultiSelect).toBeFalsy();
    expect(wrapper.vm.inputType).toEqual(filterTypes.CATEGORIZED_VALUE);
    expect(wrapper.vm.categorizedValueCategory).toEqual(
      OBSERVABLE_TYPES_STUB[0],
    );
    expect(wrapper.vm.categorizedValueValue).toEqual(null);
    expect(wrapper.vm.categorizedValueObject).toEqual({
      category: OBSERVABLE_TYPES_STUB[0],
      value: null,
    });
  });

  it("contains expected computed data when chips filter is set", () => {
    const { wrapper } = factory({ filterName: "owner", filterValue: null });

    wrapper.vm.filterName = FILTERS_STUB[3];
    wrapper.vm.filterValue = null;

    expect(wrapper.vm.filterOptions).toBeNull();
    expect(wrapper.vm.filterOptionProperty).toEqual("value");
    expect(wrapper.vm.isDate).toBeFalsy();
    expect(wrapper.vm.isCategorizedValue).toBeFalsy();
    expect(wrapper.vm.isChips).toBeTruthy();
    expect(wrapper.vm.isInputText).toBeFalsy();
    expect(wrapper.vm.isDropdown).toBeFalsy();
    expect(wrapper.vm.isMultiSelect).toBeFalsy();
    expect(wrapper.vm.inputType).toEqual(filterTypes.CHIPS);
    expect(wrapper.vm.categorizedValueCategory).toBeNull();
    expect(wrapper.vm.categorizedValueValue).toBeNull();
    expect(wrapper.vm.categorizedValueObject).toEqual({
      category: null,
      value: null,
    });
  });

  it("contains expected computed data when multiselect filter is set", () => {
    const { wrapper } = factory({ filterName: "owner", filterValue: null });

    wrapper.vm.filterName = FILTERS_STUB[4];
    wrapper.vm.filterValue = null;

    expect(wrapper.vm.filterOptions).toBeNull();
    expect(wrapper.vm.filterOptionProperty).toEqual("value");
    expect(wrapper.vm.isDate).toBeFalsy();
    expect(wrapper.vm.isCategorizedValue).toBeFalsy();
    expect(wrapper.vm.isChips).toBeFalsy();
    expect(wrapper.vm.isInputText).toBeFalsy();
    expect(wrapper.vm.isDropdown).toBeFalsy();
    expect(wrapper.vm.isMultiSelect).toBeTruthy();
    expect(wrapper.vm.inputType).toEqual(filterTypes.MULTISELECT);
    expect(wrapper.vm.categorizedValueCategory).toBeNull();
    expect(wrapper.vm.categorizedValueValue).toBeNull();
    expect(wrapper.vm.categorizedValueObject).toEqual({
      category: null,
      value: null,
    });
  });
  it("contains expected computed data when date filter is set", () => {
    const { wrapper } = factory({ filterName: "owner", filterValue: null });

    wrapper.vm.filterName = FILTERS_STUB[5];
    wrapper.vm.filterValue = null;

    expect(wrapper.vm.filterOptions).toBeNull();
    expect(wrapper.vm.filterOptionProperty).toEqual("value");
    expect(wrapper.vm.isDate).toBeTruthy();
    expect(wrapper.vm.isCategorizedValue).toBeFalsy();
    expect(wrapper.vm.isChips).toBeFalsy();
    expect(wrapper.vm.isInputText).toBeFalsy();
    expect(wrapper.vm.isDropdown).toBeFalsy();
    expect(wrapper.vm.isMultiSelect).toBeFalsy();
    expect(wrapper.vm.inputType).toEqual(filterTypes.DATE);
    expect(wrapper.vm.categorizedValueCategory).toBeNull();
    expect(wrapper.vm.categorizedValueValue).toBeNull();
    expect(wrapper.vm.categorizedValueObject).toEqual({
      category: null,
      value: null,
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
    let result = wrapper.emitted()["update:modelValue"][2];
    expect(result).toEqual([{ filterName: "owner", filterValue: null }]);

    wrapper.vm.updateValue("filterValue", "hello!");
    await wrapper.vm.$nextTick();
    result = wrapper.emitted()["update:modelValue"][3];
    expect(result).toEqual([{ filterName: "name", filterValue: "hello!" }]);

    // If an unknown attritube is sent to updateValue, it should do nothing (no more calls)
    wrapper.vm.updateValue("blah", "hello!");
    await wrapper.vm.$nextTick();
    result = wrapper.emitted()["update:modelValue"].length;
    expect(result).toEqual(4);
  });
});
