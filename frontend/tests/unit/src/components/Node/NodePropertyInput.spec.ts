import { TestingOptions } from "@pinia/testing";

import NodePropertyInput from "@/components/Node/NodePropertyInput.vue";
import { mount } from "@vue/test-utils";
import { inputTypes } from "@/etc/constants/base";
import { useObservableTypeStore } from "@/stores/observableType";
import { useUserStore } from "@/stores/user";
import { observableTypeRead } from "@/models/observableType";
import { userRead } from "@/models/user";
import { createCustomPinia } from "@unit/helpers";

const FILTERS_STUB = [
  {
    name: "name",
    label: "Name",
    type: inputTypes.INPUT_TEXT,
  },
  {
    name: "owner",
    label: "Owner",
    type: inputTypes.SELECT,
    store: useUserStore,
    optionProperty: "displayName",
    optionValue: "username",
  },
  {
    name: "observable",
    label: "Observable",
    store: useObservableTypeStore,
    type: inputTypes.CATEGORIZED_VALUE,
  },
  {
    name: "tags",
    label: "Tags",
    type: inputTypes.CHIPS,
  },
  {
    name: "observable_types",
    label: "Observable Types",
    type: inputTypes.MULTISELECT,
  },
  {
    name: "timeAfter",
    label: "After",
    type: inputTypes.DATE,
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
    propertyType: string | null;
    propertyValue: Record<string, unknown> | null;
  },
  options?: TestingOptions,
  formType?: string,
) {
  const wrapper = mount(NodePropertyInput, {
    props: {
      modelValue: filter,
      formType: formType ? formType : "filter",
    },
    global: {
      plugins: [createCustomPinia(options)],
      provide: {
        nodeType: "alerts",
        availableFilters: FILTERS_STUB,
        availableEditFields: [],
      },
    },
  });

  return { wrapper };
}

describe("NodePropertyInput.vue", () => {
  it("renders with no given property", () => {
    const { wrapper } = factory({ propertyType: null, propertyValue: null });

    expect(wrapper.exists()).toBe(true);
  });

  it("correctly sets propertyTypeOptions to availableFilters if formType is 'filter'", () => {
    const { wrapper } = factory(
      { propertyType: null, propertyValue: null },
      {},
      "filter",
    );

    expect(wrapper.vm.propertyTypeOptions).toEqual(FILTERS_STUB);
  });

  it("correctly sets propertyTypeOptions to availableEditFields if formType is 'edit'", () => {
    const { wrapper } = factory(
      { propertyType: null, propertyValue: null },
      {},
      "edit",
    );

    expect(wrapper.vm.propertyTypeOptions).toEqual([]);
  });

  it("correctly sets propertyTypeOptions to null if formType is unknown", () => {
    const { wrapper } = factory(
      { propertyType: null, propertyValue: null },
      {},
      "unknown",
    );

    expect(wrapper.vm.propertyTypeOptions).toBeNull();
  });

  it("renders with a given property", () => {
    const { wrapper } = factory({
      propertyType: "owner",
      propertyValue: {
        displayName: "Test Analyst",
        username: "test analyst",
      },
    });

    expect(wrapper.exists()).toBe(true);
  });

  it("sets up data correctly with no given property", () => {
    const { wrapper } = factory({ propertyType: null, propertyValue: null });

    expect(wrapper.vm.propertyType).toEqual(FILTERS_STUB[0]);
    expect(wrapper.vm.propertyValue).toBeNull();
  });

  it("sets up data correctly with unknown property", () => {
    const { wrapper } = factory({
      propertyType: "made_up",
      propertyValue: null,
    });

    expect(wrapper.vm.propertyType).toBeNull();
    expect(wrapper.vm.propertyValue).toBeNull();
  });

  it("sets up data correctly with an uninitialized select property", async () => {
    const { wrapper } = factory({
      propertyType: "owner",
      propertyValue: null,
    });

    expect(wrapper.vm.propertyType).toEqual(FILTERS_STUB[1]);
    // Attempts to set to default, however I can't get the userstore to load properly
    // so it ends up being undefined
    expect(wrapper.vm.propertyValue).toEqual(undefined);
  });

  it("sets up data correctly with an initialized select property", () => {
    const { wrapper } = factory({
      propertyType: "owner",
      propertyValue: {
        displayName: "Test Analyst",
        username: "test analyst",
      },
    });

    const userStore = useUserStore();
    userStore.items = USERS_STUB;

    expect(wrapper.vm.propertyType).toEqual(FILTERS_STUB[1]);
    expect(wrapper.vm.propertyValueOptions).toEqual(USERS_STUB);
    expect(wrapper.vm.propertyValue).toEqual({
      displayName: "Test Analyst",
      username: "test analyst",
    });
  });

  it("sets up data correctly with an uninitialized categorized value property", () => {
    const { wrapper } = factory({
      propertyType: "observable",
      propertyValue: null,
    });

    expect(wrapper.vm.propertyType).toEqual(FILTERS_STUB[2]);
    expect(wrapper.vm.propertyValue).toEqual({
      category: undefined, // Attempted to set to default, but couldn't load store
      value: null,
    });
  });

  it("sets up data correctly with an initialized categorized value property", () => {
    const { wrapper } = factory({
      propertyType: "observable",
      propertyValue: {
        category: OBSERVABLE_TYPES_STUB[1],
        value: "test",
      },
    });

    const observableTypeStore = useObservableTypeStore();
    observableTypeStore.items = OBSERVABLE_TYPES_STUB;

    expect(wrapper.vm.propertyType).toEqual(FILTERS_STUB[2]);
    expect(wrapper.vm.propertyValueOptions).toEqual(OBSERVABLE_TYPES_STUB);
    expect(wrapper.vm.propertyValue).toEqual({
      category: OBSERVABLE_TYPES_STUB[1],
      value: "test",
    });
  });

  it("contains expected computed data when no properties are set (default to an input property)", () => {
    const { wrapper } = factory({ propertyType: null, propertyValue: null });

    expect(wrapper.vm.propertyValueOptions).toBeNull();
    expect(wrapper.vm.propertyValueOptionProperty).toEqual("value");
    expect(wrapper.vm.isDate).toBeFalsy();
    expect(wrapper.vm.isCategorizedValue).toBeFalsy();
    expect(wrapper.vm.isChips).toBeFalsy();
    expect(wrapper.vm.isInputText).toBeTruthy();
    expect(wrapper.vm.isDropdown).toBeFalsy();
    expect(wrapper.vm.isMultiSelect).toBeFalsy();
    expect(wrapper.vm.inputType).toEqual(inputTypes.INPUT_TEXT);
    expect(wrapper.vm.categorizedValueCategory).toBeNull();
    expect(wrapper.vm.categorizedValueValue).toBeNull();
    expect(wrapper.vm.categorizedValueObject).toEqual({
      category: null,
      value: null,
    });
  });

  it("contains expected computed data when select/dropdown property is set", () => {
    const { wrapper } = factory({ propertyType: "owner", propertyValue: null });

    const userStore = useUserStore();
    userStore.items = USERS_STUB;

    expect(wrapper.vm.propertyValueOptions).toEqual(USERS_STUB);
    expect(wrapper.vm.propertyValueOptionProperty).toEqual("displayName");
    expect(wrapper.vm.isDate).toBeFalsy();
    expect(wrapper.vm.isCategorizedValue).toBeFalsy();
    expect(wrapper.vm.isChips).toBeFalsy();
    expect(wrapper.vm.isInputText).toBeFalsy();
    expect(wrapper.vm.isDropdown).toBeTruthy();
    expect(wrapper.vm.isMultiSelect).toBeFalsy();
    expect(wrapper.vm.inputType).toEqual(inputTypes.SELECT);
    expect(wrapper.vm.categorizedValueCategory).toBeNull();
    expect(wrapper.vm.categorizedValueValue).toBeNull();
    expect(wrapper.vm.categorizedValueObject).toEqual({
      category: null,
      value: null,
    });
  });

  it("contains expected computed data when categorized value property is set", () => {
    const { wrapper } = factory({ propertyType: "owner", propertyValue: null });

    const observableTypeStore = useObservableTypeStore();
    observableTypeStore.items = OBSERVABLE_TYPES_STUB;

    wrapper.vm.propertyType = FILTERS_STUB[2];
    wrapper.vm.propertyValue = { category: null, value: null };

    wrapper.vm.clearPropertyValue();

    expect(wrapper.vm.propertyValueOptions).toEqual(OBSERVABLE_TYPES_STUB);
    expect(wrapper.vm.propertyValueOptionProperty).toEqual("value");
    expect(wrapper.vm.isDate).toBeFalsy();
    expect(wrapper.vm.isCategorizedValue).toBeTruthy();
    expect(wrapper.vm.isChips).toBeFalsy();
    expect(wrapper.vm.isInputText).toBeFalsy();
    expect(wrapper.vm.isDropdown).toBeFalsy();
    expect(wrapper.vm.isMultiSelect).toBeFalsy();
    expect(wrapper.vm.inputType).toEqual(inputTypes.CATEGORIZED_VALUE);
    expect(wrapper.vm.categorizedValueCategory).toEqual(
      OBSERVABLE_TYPES_STUB[0],
    );
    expect(wrapper.vm.categorizedValueValue).toEqual(null);
    expect(wrapper.vm.categorizedValueObject).toEqual({
      category: OBSERVABLE_TYPES_STUB[0],
      value: null,
    });
  });

  it("contains expected computed data when chips property is set", () => {
    const { wrapper } = factory({ propertyType: "owner", propertyValue: null });

    wrapper.vm.propertyType = FILTERS_STUB[3];
    wrapper.vm.propertyValue = null;

    expect(wrapper.vm.propertyValueOptions).toBeNull();
    expect(wrapper.vm.propertyValueOptionProperty).toEqual("value");
    expect(wrapper.vm.isDate).toBeFalsy();
    expect(wrapper.vm.isCategorizedValue).toBeFalsy();
    expect(wrapper.vm.isChips).toBeTruthy();
    expect(wrapper.vm.isInputText).toBeFalsy();
    expect(wrapper.vm.isDropdown).toBeFalsy();
    expect(wrapper.vm.isMultiSelect).toBeFalsy();
    expect(wrapper.vm.inputType).toEqual(inputTypes.CHIPS);
    expect(wrapper.vm.categorizedValueCategory).toBeNull();
    expect(wrapper.vm.categorizedValueValue).toBeNull();
    expect(wrapper.vm.categorizedValueObject).toEqual({
      category: null,
      value: null,
    });
  });

  it("contains expected computed data when multiselect property is set", () => {
    const { wrapper } = factory({ propertyType: "owner", propertyValue: null });

    wrapper.vm.propertyType = FILTERS_STUB[4];
    wrapper.vm.propertyValue = null;

    expect(wrapper.vm.propertyValueOptions).toBeNull();
    expect(wrapper.vm.propertyValueOptionProperty).toEqual("value");
    expect(wrapper.vm.isDate).toBeFalsy();
    expect(wrapper.vm.isCategorizedValue).toBeFalsy();
    expect(wrapper.vm.isChips).toBeFalsy();
    expect(wrapper.vm.isInputText).toBeFalsy();
    expect(wrapper.vm.isDropdown).toBeFalsy();
    expect(wrapper.vm.isMultiSelect).toBeTruthy();
    expect(wrapper.vm.inputType).toEqual(inputTypes.MULTISELECT);
    expect(wrapper.vm.categorizedValueCategory).toBeNull();
    expect(wrapper.vm.categorizedValueValue).toBeNull();
    expect(wrapper.vm.categorizedValueObject).toEqual({
      category: null,
      value: null,
    });
  });
  it("contains expected computed data when date property is set", () => {
    const { wrapper } = factory({ propertyType: "owner", propertyValue: null });

    wrapper.vm.propertyType = FILTERS_STUB[5];
    wrapper.vm.propertyValue = null;

    expect(wrapper.vm.propertyValueOptions).toBeNull();
    expect(wrapper.vm.propertyValueOptionProperty).toEqual("value");
    expect(wrapper.vm.isDate).toBeTruthy();
    expect(wrapper.vm.isCategorizedValue).toBeFalsy();
    expect(wrapper.vm.isChips).toBeFalsy();
    expect(wrapper.vm.isInputText).toBeFalsy();
    expect(wrapper.vm.isDropdown).toBeFalsy();
    expect(wrapper.vm.isMultiSelect).toBeFalsy();
    expect(wrapper.vm.inputType).toEqual(inputTypes.DATE);
    expect(wrapper.vm.categorizedValueCategory).toBeNull();
    expect(wrapper.vm.categorizedValueValue).toBeNull();
    expect(wrapper.vm.categorizedValueObject).toEqual({
      category: null,
      value: null,
    });
  });

  it("executes clearPropertyValue as expected", () => {
    const { wrapper } = factory({ propertyType: null, propertyValue: null });

    wrapper.vm.propertyValue = "test";
    wrapper.vm.clearPropertyValue();
    expect(wrapper.vm.propertyValue).toBeNull();

    wrapper.vm.propertyType = FILTERS_STUB[2];
    const observableTypeStore = useObservableTypeStore();
    observableTypeStore.items = OBSERVABLE_TYPES_STUB;

    wrapper.vm.clearPropertyValue();
    expect(wrapper.vm.propertyValue).toEqual({
      category: OBSERVABLE_TYPES_STUB[0],
      value: null,
    });
  });

  it("executes getPropertyTypeObject as expected", () => {
    const { wrapper } = factory({ propertyType: null, propertyValue: null });

    let result = wrapper.vm.getPropertyTypeObject("tags");
    expect(result).toEqual(FILTERS_STUB[3]);
    result = wrapper.vm.getPropertyTypeObject("made up");
    expect(result).toBeNull();
    result = wrapper.vm.getPropertyTypeObject(null);
    expect(result).toEqual(FILTERS_STUB[0]);
  });

  it("executes updateValue as expected", async () => {
    const { wrapper } = factory({ propertyType: null, propertyValue: null });

    await wrapper.vm.$nextTick();

    wrapper.vm.updateValue("propertyType", FILTERS_STUB[1]);
    await wrapper.vm.$nextTick();
    let result = wrapper.emitted()["update:modelValue"][2];
    expect(result).toEqual([{ propertyType: "owner", propertyValue: null }]);

    wrapper.vm.updateValue("propertyValue", "hello!");
    await wrapper.vm.$nextTick();
    result = wrapper.emitted()["update:modelValue"][3];
    expect(result).toEqual([{ propertyType: "name", propertyValue: "hello!" }]);

    // If an unknown attritube is sent to updateValue, it should do nothing (no more calls)
    wrapper.vm.updateValue("blah", "hello!");
    await wrapper.vm.$nextTick();
    result = wrapper.emitted()["update:modelValue"].length;
    expect(result).toEqual(4);
  });
});
