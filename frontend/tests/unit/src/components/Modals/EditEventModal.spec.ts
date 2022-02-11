import { useEventStore } from "@/stores/event";
import { eventReadFactory, mockEventUUID } from "./../../../../mocks/events";
import { filterOption } from "@/models/base";
import EditEventModal from "@/components/Modals/EditEventModal.vue";
import { createTestingPinia, TestingOptions } from "@pinia/testing";
import { mount } from "@vue/test-utils";
import PrimeVue from "primevue/config";
import nock from "nock";

import myNock from "@unit/services/api/nock";
import { useModalStore } from "@/stores/modal";
import { useUserStore } from "@/stores/user";

const testNameField: filterOption = {
  name: "name",
  label: "Name",
  type: "inputText",
};
const availableEditFields: readonly filterOption[] = [testNameField];
const mockEvent = eventReadFactory();

function factory(options?: TestingOptions) {
  const wrapper = mount(EditEventModal, {
    attachTo: document.body,
    global: {
      plugins: [createTestingPinia(options), PrimeVue],
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

  it.skip("watcher loads given event and populates event stores when modal becomes active", async () => {
    const getEvent = myNock
      .get(`/event/${mockEventUUID}`)
      .reply(200, mockEvent);

    const { wrapper, modalStore } = factory();

    modalStore.open("EditEventModal");
    jest.setTimeout(30000);

    // Check at least one of the stores in populateEventStores
    // expect(userStore.readAll).toHaveBeenCalled()
    expect(getEvent.isDone()).toBe(true);
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
  it("will use updateData to make a call to update an event on saveEvent, but won't close or emit anything if there is an error", async () => {
    const { wrapper, modalStore, eventStore } = factory();

    wrapper.vm.formFields = {
      name: { propertyType: "name", propertyValue: "New Name" },
    };

    eventStore.update = jest.fn().mockImplementationOnce(() => {throw new Error("Request failed")})

    await wrapper.vm.saveEvent();

    expect(eventStore.update).toHaveBeenCalledWith([{ name: "New Name", uuid: "testEvent1" }]);
    expect(wrapper.emitted("requestReload")).toBeFalsy();
    expect(wrapper.vm.error).toEqual("Request failed");
    expect(modalStore.close).not.toHaveBeenCalled();
  });
});
