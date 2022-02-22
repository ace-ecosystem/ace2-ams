import { commentReadFactory } from "./../../../../mocks/comment";
import { useEventStore } from "@/stores/event";
import { eventReadFactory, mockEventUUID } from "./../../../../mocks/events";
import { filterOption } from "@/models/base";
import EditEventModal from "@/components/Modals/EditEventModal.vue";
import { TestingOptions } from "@pinia/testing";
import { createCustomPinia } from "@unit/helpers";
import { flushPromises, mount } from "@vue/test-utils";
import PrimeVue from "primevue/config";
import nock from "nock";
import * as helpers from "@/etc/helpers";

import myNock from "@unit/services/api/nock";
import { useModalStore } from "@/stores/modal";
import { useUserStore } from "@/stores/user";

const testNameField: filterOption = {
  name: "name",
  label: "Name",
  type: "inputText",
};
const testOwnerField: filterOption = {
  name: "owner",
  label: "Owner",
  type: "select",
  valueProperty: "username",
  optionProperty: "displayName",
};
const testCommentsField: filterOption = {
  name: "comments",
  label: "Comments",
  type: "inputText",
};
const availableEditFields: readonly filterOption[] = [testNameField];
const mockEvent = eventReadFactory();

function factory(options?: TestingOptions) {
  const wrapper = mount(EditEventModal, {
    attachTo: document.body,
    global: {
      plugins: [createCustomPinia(options), PrimeVue],
      provide: { availableEditFields: availableEditFields },
      stubs: {
        NodePropertyInput: true,
      },
    },
    props: { name: "EditEventModal", eventUuid: mockEventUUID },
  });

  const modalStore = useModalStore();
  const userStore = useUserStore();
  const eventStore = useEventStore();

  return { wrapper, modalStore, userStore, eventStore };
}

describe("EditEventModal.vue", () => {
  afterEach(() => {
    nock.cleanAll();
  });

  it("renders", () => {
    const { wrapper } = factory();
    expect(wrapper.exists()).toBe(true);
  });

  it("loads data as expected after onMounted hook", () => {
    const { wrapper } = factory();
    expect(wrapper.vm.error).toBeNull();
    expect(wrapper.vm.event).toBeNull();
    expect(wrapper.vm.fieldOptionObjects).toEqual({ name: testNameField });
    expect(wrapper.vm.formFields).toEqual({
      name: { propertyType: "name", propertyValue: null },
    });
    expect(wrapper.vm.isLoading).toEqual(false);
  });

  it("loads given event and populates event stores on initializeData", async () => {
    const spy = vi
      .spyOn(helpers, "populateEventStores")
      .mockResolvedValueOnce(undefined);
    const { wrapper } = factory();

    const getEvent = myNock
      .get(`/event/${mockEventUUID}`)
      .reply(200, mockEvent);

    await wrapper.vm.initializeData();

    // Check at least one of the stores in populateEventStores
    expect(spy).toHaveBeenCalled();
    expect(getEvent.isDone()).toBe(true);
    expect(wrapper.vm.isLoading).toBeFalsy();
  });
  it("will catch and set error if any are thrown in initializeData", async () => {
    const spy = vi
      .spyOn(helpers, "populateEventStores")
      .mockResolvedValueOnce(undefined);
    const { wrapper } = factory();

    const getEvent = myNock
      .get(`/event/${mockEventUUID}`)
      .reply(403, mockEvent);

    await wrapper.vm.initializeData();

    // Check at least one of the stores in populateEventStores
    expect(spy).toHaveBeenCalled();
    expect(getEvent.isDone()).toBe(true);

    expect(wrapper.vm.error).toEqual("Request failed with status code 403");
    expect(wrapper.vm.isLoading).toBeFalsy();
  });
  it("correctly computes updateData", () => {
    const { wrapper } = factory();
    wrapper.vm.formFields = {
      name: { propertyType: "name", propertyValue: "test name" },
    };
    expect(wrapper.vm.updateData).toEqual([
      { uuid: mockEventUUID, name: "test name" },
    ]);
  });
  it("will fetch event data and execute fillFormFields on resetForm", async () => {
    const getEvent = myNock
      .get(`/event/${mockEventUUID}`)
      .reply(200, mockEvent);
    const { wrapper } = factory();
    await wrapper.vm.resetForm();
    expect(getEvent.isDone()).toBe(true);

    expect(wrapper.vm.formFields).toEqual({
      name: { propertyType: "name", propertyValue: "Test Event" },
    });
  });
  it("will fill form field propertyValues using data from event object", () => {
    const { wrapper } = factory();
    wrapper.vm.event = mockEvent;
    wrapper.vm.fillFormFields();
    expect(wrapper.vm.formFields).toEqual({
      name: { propertyType: "name", propertyValue: "Test Event" },
    });
  });
  it("will use updateData to make a call to update an event on saveEvent, closing the modal and requestingReload on completion", async () => {
    const { wrapper, modalStore, eventStore } = factory();

    wrapper.vm.formFields = {
      name: { propertyType: "name", propertyValue: "New Name" },
    };

    await wrapper.vm.saveEvent();

    expect(eventStore.update).toHaveBeenCalledWith([
      { name: "New Name", uuid: "testEvent1" },
    ]);
    expect(wrapper.emitted("requestReload")).toBeTruthy();
    expect(wrapper.vm.error).toBeNull();
    expect(modalStore.close).toHaveBeenCalled();
  });
  it("will attempt to save any comments if 'comments' is in the formFields on saveEvent", async () => {
    const updateComment = myNock.patch("/node/comment/commentUuid1").reply(200);

    const { wrapper, modalStore } = factory();

    wrapper.vm.fieldOptionObjects = { comments: testCommentsField };
    wrapper.vm.formFields = {
      comments: {
        propertyType: "comments",
        propertyValue: [commentReadFactory()],
      },
    };

    await wrapper.vm.saveEvent();

    expect(updateComment.isDone()).toBe(true);
    expect(wrapper.vm.error).toBeNull();
    expect(wrapper.emitted("requestReload")).toBeTruthy();
    expect(modalStore.close).toHaveBeenCalled();
  });
  it("will attempt to update all comments in the formFields on saveEventComments", async () => {
    const updateComment = myNock.patch("/node/comment/commentUuid1").reply(200);

    const { wrapper } = factory();

    wrapper.vm.fieldOptionObjects = { comments: testCommentsField };
    wrapper.vm.formFields = {
      comments: {
        propertyType: "comments",
        propertyValue: [commentReadFactory()],
      },
    };

    await wrapper.vm.saveEventComments();

    expect(updateComment.isDone()).toBe(true);
  });
  it("will use updateData to make a call to update an event on saveEvent, but won't close or emit anything if there is an error", async () => {
    const { wrapper, modalStore, eventStore } = factory();

    wrapper.vm.formFields = {
      name: { propertyType: "name", propertyValue: "New Name" },
    };

    eventStore.update = vi.fn().mockImplementationOnce(() => {
      throw new Error("Request failed");
    });

    await wrapper.vm.saveEvent();

    expect(eventStore.update).toHaveBeenCalledWith([
      { name: "New Name", uuid: "testEvent1" },
    ]);
    expect(wrapper.emitted("requestReload")).toBeFalsy();
    expect(wrapper.vm.error).toEqual("Request failed");
    expect(modalStore.close).not.toHaveBeenCalled();
  });

  it.each([
    [{ name: testNameField }, "name", "test", "test"],
    [{ name: testNameField }, "name", ["test"], ["test"]],
    [{ owner: testOwnerField }, "owner", { username: "test" }, "test"],
    [{ owner: testOwnerField }, "owner", "test", "test"],
    [{ owner: testOwnerField }, "owner", ["test"], ["test"]],
    [{ owner: testOwnerField }, "owner", [{ username: "test" }], ["test"]],
    [
      { owner: testOwnerField },
      "owner",
      [{ value: "test" }],
      [{ value: "test" }],
    ],
  ])(
    "will correctly format a value on formatValue",
    (fieldOptionObjects, field, value, expected) => {
      const { wrapper } = factory();
      wrapper.vm.fieldOptionObjects = fieldOptionObjects;
      const result = wrapper.vm.formatValue(field, value);
      expect(result).toEqual(expected);
    },
  );
  it("will clear the error value and execute close on handleError", () => {
    const { wrapper, modalStore } = factory();
    wrapper.vm.error = "test error";
    wrapper.vm.handleError();
    expect(wrapper.vm.error).toBeNull();
    expect(modalStore.close).toHaveBeenCalledWith("EditEventModal");
  });
  it("will close the modal in modalStore on close", () => {
    const { wrapper, modalStore } = factory();
    wrapper.vm.close();
    expect(modalStore.close).toHaveBeenCalledWith("EditEventModal");
  });
});
