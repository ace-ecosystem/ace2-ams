import { commentReadFactory } from "./../../../../mocks/comment";
import { useEventStore } from "@/stores/event";
import { eventReadFactory, mockEventUUID } from "./../../../../mocks/events";
import { propertyOption } from "@/models/base";
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
import { genericObjectReadFactory } from "../../../../mocks/genericObject";
import { Event } from "../../../../../src/services/api/event";
import { vi, expect } from "vitest";

const testNameField: propertyOption = {
  name: "name",
  label: "Name",
  type: "inputText",
};
const testOwnerField: propertyOption = {
  name: "owner",
  label: "Owner",
  type: "select",
  valueProperty: "username",
  optionProperty: "displayName",
};
const testCommentsField: propertyOption = {
  name: "comments",
  label: "Comments",
  type: "inputText",
};
const testQueue = genericObjectReadFactory({ value: "external" });
const availableEditFields: Record<string, readonly propertyOption[]> = {
  external: [testNameField],
};
const mockEvent = eventReadFactory({ queue: testQueue });

async function factory(options?: TestingOptions) {
  vi.spyOn(Event, "read").mockResolvedValueOnce(mockEvent);

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

  await flushPromises();

  const modalStore = useModalStore();
  const userStore = useUserStore();
  const eventStore = useEventStore();

  return { wrapper, modalStore, userStore, eventStore };
}

describe("EditEventModal.vue", () => {
  afterEach(() => {
    nock.cleanAll();
  });

  it("renders", async () => {
    const { wrapper } = await factory();
    expect(wrapper.exists()).toBe(true);
  });

  it("loads data as expected after onMounted hook", async () => {
    const { wrapper } = await factory();
    expect(wrapper.vm.error).toBeNull();
    expect(wrapper.vm.event).toEqual(mockEvent);
    expect(wrapper.vm.fieldOptionObjects).toEqual({ name: testNameField });
    expect(wrapper.vm.formFields).toEqual({
      name: { propertyType: "name", propertyValue: null },
    });
    expect(wrapper.vm.isLoading).toEqual(false);
  });

  it("loads given event and populates event stores on initializeData", async () => {
    const eventSpy = vi.spyOn(Event, "read").mockResolvedValueOnce(undefined);
    const storeSpy = vi
      .spyOn(helpers, "populateEventStores")
      .mockResolvedValueOnce(undefined);

    const { wrapper } = await factory();

    await wrapper.vm.initializeData();

    // Check at least one of the stores in populateEventStores
    expect(eventSpy).toHaveBeenCalled();
    expect(storeSpy).toHaveBeenCalled();
    expect(wrapper.vm.isLoading).toBeFalsy();
  });
  it("will catch and set error if any are thrown in initializeData", async () => {
    const eventSpy = vi.spyOn(Event, "read").mockResolvedValueOnce(undefined);
    const storeSpy = vi
      .spyOn(helpers, "populateEventStores")
      .mockRejectedValueOnce(new Error("Request failed with status code 403"));
    const { wrapper } = await factory();
    await wrapper.vm.initializeData();

    // Check at least one of the stores in populateEventStores
    expect(eventSpy).toHaveBeenCalled();
    expect(storeSpy).toHaveBeenCalled();

    expect(wrapper.vm.error).toEqual("Request failed with status code 403");
    expect(wrapper.vm.isLoading).toBeFalsy();
  });
  it("correctly computes updateData", async () => {
    const { wrapper } = await factory();
    wrapper.vm.formFields = {
      name: { propertyType: "name", propertyValue: "test name" },
    };
    expect(wrapper.vm.updateData).toEqual([
      { uuid: mockEventUUID, name: "test name" },
    ]);
  });
  it("will fetch event data and execute fillFormFields on resetForm", async () => {
    const { wrapper } = await factory();
    await wrapper.vm.resetForm();

    expect(wrapper.vm.formFields).toEqual({
      name: { propertyType: "name", propertyValue: "Test Event" },
    });
  });
  it("will fill form field propertyValues using data from event object", async () => {
    const { wrapper } = await factory();
    wrapper.vm.event = mockEvent;
    wrapper.vm.fillFormFields();
    expect(wrapper.vm.formFields).toEqual({
      name: { propertyType: "name", propertyValue: "Test Event" },
    });
  });
  it("will use updateData to make a call to update an event on saveEvent, closing the modal and requestingReload on completion", async () => {
    const { wrapper, modalStore, eventStore } = await factory();

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

    const { wrapper, modalStore } = await factory();

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

    const { wrapper } = await factory();

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
    const { wrapper, modalStore, eventStore } = await factory();

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
    async (fieldOptionObjects, field, value, expected) => {
      const { wrapper } = await factory();
      wrapper.vm.fieldOptionObjects = fieldOptionObjects;
      const result = wrapper.vm.formatValue(field, value);
      expect(result).toEqual(expected);
    },
  );
  it("will clear the error value and execute close on handleError", async () => {
    const { wrapper, modalStore } = await factory();
    wrapper.vm.error = "test error";
    wrapper.vm.handleError();
    expect(wrapper.vm.error).toBeNull();
    expect(modalStore.close).toHaveBeenCalledWith("EditEventModal");
  });
  it("will close the modal in modalStore on close", async () => {
    const { wrapper, modalStore } = await factory();
    wrapper.vm.close();
    expect(modalStore.close).toHaveBeenCalledWith("EditEventModal");
  });
});
