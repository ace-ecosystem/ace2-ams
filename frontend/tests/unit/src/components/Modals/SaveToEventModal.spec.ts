import SaveToEventModal from "@/components/Modals/SaveToEventModal.vue";
import { createTestingPinia, TestingOptions } from "@pinia/testing";
import { flushPromises, mount } from "@vue/test-utils";
import PrimeVue from "primevue/config";
import nock from "nock";

import myNock from "@unit/services/api/nock";
import { useAlertStore } from "@/stores/alert";
import { useAuthStore } from "@/stores/auth";
import { useModalStore } from "@/stores/modal";
import { useSelectedAlertStore } from "@/stores/selectedAlert";
import { useEventStatusStore } from "@/stores/eventStatus";
import { genericObjectReadFactory } from "../../../../mocks/genericObject";
import { eventReadFactory } from "../../../../mocks/events";
import { parseEventSummary } from "@/stores/eventTable";
import { userReadFactory } from "../../../../mocks/user";

const OPEN_EVENT_STATUS = genericObjectReadFactory({
  value: "OPEN",
  uuid: "1",
});
const CLOSED_EVENT_STATUS = genericObjectReadFactory({
  value: "CLOSED",
  uuid: "2",
});
const NEW_EVENT = eventReadFactory({
  // eslint-disable-next-line prettier/prettier
  name: "New Event",
  status: OPEN_EVENT_STATUS,
});
const OPEN_EVENT = eventReadFactory({
  // eslint-disable-next-line prettier/prettier
  name: "Open Event",
  status: OPEN_EVENT_STATUS,
});
const CLOSED_EVENT = eventReadFactory({
  name: "Closed Event",
  status: CLOSED_EVENT_STATUS,
});

function factory(options?: TestingOptions) {
  const wrapper = mount(SaveToEventModal, {
    attachTo: document.body,
    global: {
      plugins: [createTestingPinia(options), PrimeVue],
    },
    props: { name: "SaveToEventModal" },
  });

  const eventStatusStore = useEventStatusStore();
  const alertStore = useAlertStore();
  const authStore = useAuthStore();
  const modalStore = useModalStore();
  const selectedAlertStore = useSelectedAlertStore();
  eventStatusStore.items = [CLOSED_EVENT_STATUS, OPEN_EVENT_STATUS];

  return {
    eventStatusStore,
    alertStore,
    authStore,
    modalStore,
    selectedAlertStore,
    wrapper,
  };
}

describe("SaveToEventModal.vue", () => {
  afterEach(() => {
    nock.cleanAll();
  });

  it("renders", () => {
    const { wrapper } = factory();

    expect(wrapper.exists()).toBe(true);
  });

  it("correctly sets and sorts availableEventStatusOptions with all event status objects from the eventStore into that are configured in eventStatusOptions on getavailableEventStatusOptions", () => {
    const { wrapper } = factory();

    wrapper.vm.eventStatusOptions = ["OPEN", "CLOSED", "UNKNOWN"];

    wrapper.vm.getAvailableEventStatusOptions();

    expect(wrapper.vm.availableEventStatusOptions).toEqual([
      OPEN_EVENT_STATUS,
      CLOSED_EVENT_STATUS,
    ]);
  });

  it("correctly loads events for each status in availableEventStatusOptions and sets them in events on loadEvents", async () => {
    myNock
      .get("/event/?status=OPEN&sort=created_time%7Casc&offset=0")
      .reply(200, {
        items: [OPEN_EVENT],
        total: 1,
      });
    myNock
      .get("/event/?status=CLOSED&sort=created_time%7Casc&offset=0")
      .reply(200, {
        items: [CLOSED_EVENT],
        total: 1,
      });

    const { wrapper } = factory();
    wrapper.vm.availableEventStatusOptions = [
      OPEN_EVENT_STATUS,
      CLOSED_EVENT_STATUS,
    ];

    await wrapper.vm.loadEvents();

    expect(wrapper.vm.events).toEqual({
      CLOSED: [parseEventSummary(CLOSED_EVENT)],
      OPEN: [parseEventSummary(OPEN_EVENT)],
    });
  });

  it("correctly sets error and returns early if fetch events call fails", async () => {
    myNock
      .get("/event/?status=OPEN&sort=created_time%7Casc&offset=0")
      .reply(500);

    const { wrapper } = factory();

    await wrapper.vm.loadEvents();
    expect(wrapper.vm.events).toEqual({});
    expect(wrapper.vm.error).toEqual("Request failed with status code 500");
  });

  it("correctly fetches all events for a given status object on getEventsWithStatus and returns the list parsed into eventSummary objects", async () => {
    myNock
      .get("/event/?status=OPEN&sort=created_time%7Casc&offset=0")
      .reply(200, {
        items: [OPEN_EVENT],
        total: 1,
      });
    const { wrapper } = factory();
    const res = await wrapper.vm.getEventsWithStatus(OPEN_EVENT_STATUS);
    expect(res).toEqual([parseEventSummary(OPEN_EVENT)]);
  });

  it("correctly executes loadEvents when the modal is made active in the modalStore", async () => {
    myNock
      .get("/event/?status=CLOSED&sort=created_time%7Casc&offset=0")
      .reply(200, {
        items: [CLOSED_EVENT],
        total: 1,
      });
    myNock
      .get("/event/?status=OPEN&sort=created_time%7Casc&offset=0")
      .reply(200, {
        items: [OPEN_EVENT],
        total: 1,
      });

    const { wrapper, modalStore } = factory();
    expect(wrapper.vm.events).toEqual({});
    modalStore.openModals = ["SaveToEventModal"];

    // this is defs unintuitive, but since there's nothing to actually await in this test (changing the modalStore is not async)
    // we just have to set a timeout to make sure that code completes and the req is made :/
    // (flushPromises and wrapper.vm.$nextTick() did not seem to work)
    jest.setTimeout(30000);
    await new Promise((r) => setTimeout(r, 2000));

    expect(wrapper.vm.events).toEqual({
      OPEN: [parseEventSummary(OPEN_EVENT)],
      CLOSED: [parseEventSummary(CLOSED_EVENT)],
    });
  });
  it("correctly executes saveToEvent when a newEvent is selected and no comment is given and all reqs complete successfully", async () => {
    const createEventSuccess = myNock
      .post(
        "/event/",
        (body) => body.name == "New Event" && body.status == "OPEN",
      )
      .reply(201, NEW_EVENT);

    myNock.options("/alert/").reply(200, "Success");
    const updateAlertsSuccess = myNock
      .patch(
        "/alert/",
        '[{"uuid":"1","event_uuid":"testEvent1"},{"uuid":"2","event_uuid":"testEvent1"}]',
      )
      .reply(200, "Success");

    const { wrapper, selectedAlertStore, modalStore, authStore } = factory({
      stubActions: false,
    });
    wrapper.vm.newEventName = "New Event";
    wrapper.vm.selectedEventStatusOption = 0;
    authStore.user = userReadFactory();
    selectedAlertStore.selected = ["1", "2"];

    await wrapper.vm.saveToEvent();
    expect(createEventSuccess.isDone()).toBe(true);
    expect(updateAlertsSuccess.isDone()).toBe(true);
    expect(wrapper.emitted("saveToEvent")).toBeTruthy();
    expect(wrapper.vm.selectedExistingEvent).toBeNull();
    expect(wrapper.vm.newEventName).toEqual("");
    expect(wrapper.vm.newEventComment).toBeNull();
    expect(modalStore.close).toHaveBeenCalled();
  });
  it("correctly executes saveToEvent when an existing is selected and all reqs complete successfully", async () => {
    myNock.options("/alert/").reply(200, "Success");
    const updateAlertsSuccess = myNock
      .patch(
        "/alert/",
        '[{"uuid":"1","event_uuid":"testEvent1"},{"uuid":"2","event_uuid":"testEvent1"}]',
      )
      .reply(200, "Success");

    const { wrapper, selectedAlertStore, modalStore, authStore } = factory({
      stubActions: false,
    });
    wrapper.vm.selectedExistingEvent = OPEN_EVENT;
    wrapper.vm.selectedEventStatusOption = 1;
    authStore.user = userReadFactory();
    selectedAlertStore.selected = ["1", "2"];

    await wrapper.vm.saveToEvent();
    expect(updateAlertsSuccess.isDone()).toBe(true);
    expect(wrapper.emitted("saveToEvent")).toBeTruthy();
    expect(wrapper.vm.selectedExistingEvent).toBeNull();
    expect(wrapper.vm.newEventName).toEqual("");
    expect(wrapper.vm.newEventComment).toBeNull();
    expect(modalStore.close).toHaveBeenCalled();
  });
  it("correctly executes saveToEvent when a newEvent is selected and a comment is given and all reqs complete successfully", async () => {
    const createEventSuccess = myNock
      .post(
        "/event/",
        (body) => body.name == "New Event" && body.status == "OPEN",
      )
      .reply(201, NEW_EVENT);

    const createCommentSuccess = myNock
      .post(
        "/node/comment/",
        '[{"node_uuid":"1","user":"analyst","value":"Test comment"},{"node_uuid":"2","user":"analyst","value":"Test comment"}]',
      )
      .reply(201);

    myNock.options("/alert/").reply(200, "Success");
    const updateAlertsSuccess = myNock
      .patch(
        "/alert/",
        '[{"uuid":"1","event_uuid":"testEvent1"},{"uuid":"2","event_uuid":"testEvent1"}]',
      )
      .reply(200, "Success");

    const { wrapper, selectedAlertStore, modalStore, authStore } = factory({
      stubActions: false,
    });
    wrapper.vm.newEventName = "New Event";
    wrapper.vm.newEventComment = "Test comment";
    wrapper.vm.selectedEventStatusOption = 0;
    authStore.user = userReadFactory();
    selectedAlertStore.selected = ["1", "2"];

    await wrapper.vm.saveToEvent();
    expect(createEventSuccess.isDone()).toBe(true);
    expect(createCommentSuccess.isDone()).toBe(true);
    expect(updateAlertsSuccess.isDone()).toBe(true);
    expect(wrapper.emitted("saveToEvent")).toBeTruthy();
    expect(wrapper.vm.selectedExistingEvent).toBeNull();
    expect(wrapper.vm.newEventName).toEqual("");
    expect(wrapper.vm.newEventComment).toBeNull();
    expect(modalStore.close).toHaveBeenCalled();
  });

  it("correctly executes saveToEvent when a newEvent is selected and no comment is given and event creation fails", async () => {
    const createEventFailure = myNock
      .post(
        "/event/",
        (body) => body.name == "New Event" && body.status == "OPEN",
      )
      .reply(500);

    const { wrapper, selectedAlertStore, modalStore, authStore } = factory({
      stubActions: false,
    });
    wrapper.vm.newEventName = "New Event";
    wrapper.vm.selectedEventStatusOption = 0;
    authStore.user = userReadFactory();
    selectedAlertStore.selected = ["1", "2"];

    await wrapper.vm.saveToEvent();
    expect(createEventFailure.isDone()).toBe(true);
    expect(wrapper.emitted("saveToEvent")).toBeFalsy();
    expect(wrapper.vm.selectedExistingEvent).toBeNull();
    expect(wrapper.vm.newEventName).toEqual("New Event");
    expect(wrapper.vm.newEventComment).toBeNull();
    expect(modalStore.close).not.toHaveBeenCalled();

    expect(wrapper.vm.error).toEqual("Request failed with status code 500");
  });
  it("correctly executes saveToEvent when a newEvent is selected and no comment is given and alert eventUuid update fails", async () => {
    const createEventSuccess = myNock
      .post(
        "/event/",
        (body) => body.name == "New Event" && body.status == "OPEN",
      )
      .reply(201, NEW_EVENT);

    myNock.options("/alert/").reply(200, "Success");
    const updateAlertsFailure = myNock
      .patch(
        "/alert/",
        '[{"uuid":"1","event_uuid":"testEvent1"},{"uuid":"2","event_uuid":"testEvent1"}]',
      )
      .reply(500);

    const { wrapper, selectedAlertStore, modalStore, authStore } = factory({
      stubActions: false,
    });
    wrapper.vm.newEventName = "New Event";
    wrapper.vm.selectedEventStatusOption = 0;
    authStore.user = userReadFactory();
    selectedAlertStore.selected = ["1", "2"];

    await wrapper.vm.saveToEvent();
    expect(createEventSuccess.isDone()).toBe(true);
    expect(updateAlertsFailure.isDone()).toBe(true);
    expect(wrapper.emitted("saveToEvent")).toBeFalsy();
    expect(wrapper.vm.selectedExistingEvent).toBeNull();
    expect(wrapper.vm.newEventName).toEqual("New Event");
    expect(wrapper.vm.newEventComment).toBeNull();
    expect(modalStore.close).not.toHaveBeenCalled();
    expect(wrapper.vm.error).toEqual("Request failed with status code 500");
  });
  it("correctly executes saveToEvent when an existing is selected and and alert eventUuid update fails", async () => {
    myNock.options("/alert/").reply(200, "Success");
    const updateAlertsFailure = myNock
      .patch(
        "/alert/",
        '[{"uuid":"1","event_uuid":"testEvent1"},{"uuid":"2","event_uuid":"testEvent1"}]',
      )
      .reply(500);

    const { wrapper, selectedAlertStore, modalStore, authStore } = factory({
      stubActions: false,
    });
    wrapper.vm.selectedExistingEvent = OPEN_EVENT;
    wrapper.vm.selectedEventStatusOption = 1;
    authStore.user = userReadFactory();
    selectedAlertStore.selected = ["1", "2"];

    await wrapper.vm.saveToEvent();
    expect(updateAlertsFailure.isDone()).toBe(true);
    expect(wrapper.emitted("saveToEvent")).toBeFalsy();
    expect(wrapper.vm.selectedExistingEvent).toEqual(OPEN_EVENT);
    expect(wrapper.vm.newEventName).toEqual("");
    expect(wrapper.vm.newEventComment).toBeFalsy();
    expect(modalStore.close).not.toHaveBeenCalled();
    expect(wrapper.vm.error).toEqual("Request failed with status code 500");
  });
  it("correctly executes saveToEvent when a newEvent is selected and a comment is given and comment creation fails (duplicate)", async () => {
    const createEventSuccess = myNock
      .post(
        "/event/",
        (body) => body.name == "New Event" && body.status == "OPEN",
      )
      .reply(201, NEW_EVENT);

    const createCommentFailure = myNock
      .post(
        "/node/comment/",
        '[{"node_uuid":"1","user":"analyst","value":"Test comment"},{"node_uuid":"2","user":"analyst","value":"Test comment"}]',
      )
      .reply(409);

    myNock.options("/alert/").reply(200, "Success");
    const updateAlertsSuccess = myNock
      .patch(
        "/alert/",
        '[{"uuid":"1","event_uuid":"testEvent1"},{"uuid":"2","event_uuid":"testEvent1"}]',
      )
      .reply(200, "Success");

    const { wrapper, selectedAlertStore, modalStore, authStore } = factory({
      stubActions: false,
    });
    wrapper.vm.newEventName = "New Event";
    wrapper.vm.newEventComment = "Test comment";
    wrapper.vm.selectedEventStatusOption = 0;
    authStore.user = userReadFactory();
    selectedAlertStore.selected = ["1", "2"];

    await wrapper.vm.saveToEvent();
    expect(createEventSuccess.isDone()).toBe(true);
    expect(createCommentFailure.isDone()).toBe(true);
    expect(updateAlertsSuccess.isDone()).toBe(true);
    expect(wrapper.emitted("saveToEvent")).toBeTruthy();
    expect(wrapper.vm.selectedExistingEvent).toBeNull();
    expect(wrapper.vm.newEventName).toEqual("");
    expect(wrapper.vm.newEventComment).toBeNull();
    expect(modalStore.close).toHaveBeenCalled();
  });
  it("correctly executes saveToEvent when a newEvent is selected and a comment is given and comment creation fails (general error)", async () => {
    const createEventSuccess = myNock
      .post(
        "/event/",
        (body) => body.name == "New Event" && body.status == "OPEN",
      )
      .reply(201, NEW_EVENT);

    const { wrapper, selectedAlertStore, modalStore, authStore } = factory({
      stubActions: false,
    });
    wrapper.vm.newEventName = "New Event";
    wrapper.vm.newEventComment = "Test comment";
    wrapper.vm.selectedEventStatusOption = 0;
    authStore.user = userReadFactory();
    selectedAlertStore.selected = ["1", "2"];

    const createCommentFailure = myNock
      .post(
        "/node/comment/",
        '[{"node_uuid":"1","user":"analyst","value":"Test comment"},{"node_uuid":"2","user":"analyst","value":"Test comment"}]',
      )
      .reply(500);

    await wrapper.vm.saveToEvent();
    expect(createEventSuccess.isDone()).toBe(true);
    expect(createCommentFailure.isDone()).toBe(true);
    expect(wrapper.emitted("saveToEvent")).toBeFalsy();
    expect(wrapper.vm.selectedExistingEvent).toBeNull();
    expect(wrapper.vm.newEventName).toEqual("New Event");
    expect(wrapper.vm.newEventComment).toEqual("Test comment");
    expect(modalStore.close).not.toHaveBeenCalled();
    expect(wrapper.vm.error).toEqual("Request failed with status code 500");
  });

  it.each([
    [[], null, 0, "", false],
    [[], null, 0, "New Event", false],
    [[], null, 1, "", false],
    [[], null, 1, "New Event", false],

    [[], OPEN_EVENT, 0, "", false],
    [[], OPEN_EVENT, 0, "New Event", false],
    [[], OPEN_EVENT, 1, "", false],
    [[], OPEN_EVENT, 1, "New Event", false],

    [["1"], null, 0, "", false],
    [["1"], null, 0, "New Event", true],
    [["1"], null, 1, "", false],
    [["1"], null, 1, "New Event", false],

    [["1"], OPEN_EVENT, 0, "", false],
    [["1"], OPEN_EVENT, 0, "New Event", true],
    [["1"], OPEN_EVENT, 1, "", true],
    [["1"], OPEN_EVENT, 1, "New Event", true],
  ])(
    "correctly computes allowEventSelectionSubmit",
    (
      alertsSelected,
      selectedExistingEvent,
      selectedEventStatusOption,
      newEventName,
      result,
    ) => {
      const { wrapper, selectedAlertStore } = factory();
      selectedAlertStore.selected = alertsSelected;
      wrapper.vm.selectedExistingEvent = selectedExistingEvent;
      wrapper.vm.selectedEventStatusOption = selectedEventStatusOption;
      wrapper.vm.newEventName = newEventName;
      expect(wrapper.vm.allowEventSelectionSubmit).toEqual(result);
    },
  );

  it("correctly computes commentData", () => {
    const { wrapper, authStore } = factory();

    expect(wrapper.vm.commentData).toBeNull();

    // Set the selected user
    authStore.user = userReadFactory();

    // Set the new comment value
    wrapper.vm.newEventComment = "test comment";

    expect(wrapper.vm.commentData).toEqual({
      user: "analyst",
      value: "test comment",
    });
  });

  it("correctly computes newEventSelected", () => {
    const { wrapper } = factory();

    wrapper.vm.selectedEventStatusOption = 0;
    expect(wrapper.vm.newEventSelected).toBeTruthy();
    wrapper.vm.selectedEventStatusOption = 1;
    expect(wrapper.vm.newEventSelected).toBeFalsy();
  });

  it("correctly handleError", () => {
    const { wrapper } = factory();
    wrapper.vm.error = "There was an error!";
    wrapper.vm.handleError();

    expect(wrapper.vm.error).toBeNull();
  });

  it("correctly executes close", () => {
    const { wrapper, modalStore } = factory();
    wrapper.vm.selectedExistingEvent = OPEN_EVENT;
    wrapper.vm.selectedEventStatusOption = 0;
    wrapper.vm.newEventComment = "test comment";
    wrapper.vm.newEventName = "new event";
    wrapper.vm.error = "There was an error!";
    wrapper.vm.close();

    expect(wrapper.vm.selectedEventStatusOption).toEqual(1);
    expect(wrapper.vm.selectedExistingEvent).toBeNull();
    expect(wrapper.vm.error).toBeNull();
    expect(wrapper.vm.newEventComment).toBeNull();
    expect(wrapper.vm.newEventName).toEqual("");
    expect(modalStore.close).toHaveBeenCalled();
  });
});
