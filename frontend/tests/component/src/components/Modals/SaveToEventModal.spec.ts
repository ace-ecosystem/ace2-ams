import { mount } from "@cypress/vue";
import PrimeVue from "primevue/config";

import SaveToEventModal from "@/components/Modals/SaveToEventModal.vue";
import { createCustomCypressPinia } from "@tests/cypressHelpers";
import { queueableObjectReadFactory } from "@mocks/genericObject";
import { Event } from "@/services/api/event";
import { eventReadFactory } from "@mocks/events";
import { eventRead } from "@/models/event";
import { Alert } from "@/services/api/alert";
import { Comment } from "@/services/api/comment";
import { userReadFactory } from "@mocks/user";

const openStatus = queueableObjectReadFactory({ value: "OPEN" });
const closedStatus = queueableObjectReadFactory({ value: "CLOSED" });

const defaultReadAllPagesOpen = {
  status: [openStatus],
  sort: "created_time|asc",
};
const defaultReadAllPagesClosed = {
  status: [closedStatus],
  sort: "created_time|asc",
};

function factory(
  args: {
    selected: string[];
    openEvents?: eventRead[];
    closedEvents?: eventRead[];
  } = {
    selected: [],
    openEvents: [],
    closedEvents: [],
  },
) {
  const readAllPages = cy.stub(Event, "readAllPages");

  readAllPages
    .withArgs(defaultReadAllPagesOpen)
    .as("getEventsOpen")
    .returns(args.openEvents);
  readAllPages
    .withArgs(defaultReadAllPagesClosed)
    .as("getEventsClosed")
    .returns(args.closedEvents);

  return mount(SaveToEventModal, {
    global: {
      plugins: [
        PrimeVue,
        createCustomCypressPinia({
          stubActions: false,
          initialState: {
            authStore: { user: userReadFactory() },
            selectedAlertStore: {
              selected: args.selected,
            },
            eventStatusStore: {
              items: [openStatus, closedStatus],
            },
            recentCommentsStore: {
              recentComments: ["test"],
            },
          },
        }),
      ],
      provide: {
        objectType: "alerts",
      },
    },
    propsData: {
      name: "SaveToEventModal",
    },
  }).then((wrapper) => {
    wrapper.vm.modalStore.open("SaveToEventModal");
    cy.get("[data-cy='save-to-event-modal']").should("be.visible");
    cy.contains("Save to Event").should("be.visible");
    cy.contains("Back").should("be.visible");
    cy.contains("Save").should("be.visible");
    cy.contains("NEW").should("be.visible");
    cy.contains("OPEN").should("be.visible");
    cy.contains("CLOSED").should("be.visible");
  });
}

describe("SaveToEventModal", () => {
  it("renders correctly when there are no existing events to choose from", () => {
    factory();
    cy.contains("No available options").should("be.visible");
  });
  it("renders correctly when there are events to choose from", () => {
    factory({
      selected: [],
      openEvents: [
        eventReadFactory({ name: "Test Open Event", status: openStatus }),
      ],
      closedEvents: [
        eventReadFactory({ name: "Test Closed Event", status: closedStatus }),
      ],
    });
    cy.contains("Test Open Event").should("be.visible");
    cy.contains("CLOSED").click();
    cy.contains("Test Closed Event").should("be.visible");
  });
  it("loads the new event tab content correctly when selected", () => {
    factory();
    cy.contains("NEW").click();
    cy.findByLabelText("Event Name").should("be.visible");
    cy.findByLabelText("Event Comment").should("be.visible");
  });
  it("closes the modal without doing anything when back button is clicked", () => {
    cy.stub(Alert, "update").as("updateAlert");
    cy.stub(Event, "create").as("createEvent");
    cy.stub(Comment, "create").as("createComment");
    factory();
    cy.contains("Back").click();
    cy.get("[data-cy='save-to-event-modal']").should("not.exist");
    cy.get("@updateAlert").should("not.have.been.called");
    cy.get("@createEvent").should("not.have.been.called");
    cy.get("@createComment").should("not.have.been.called");
  });
  it("has 'Save' button enabled when alert is selected and new event is selected and given a name", () => {
    factory({
      selected: ["uuid"],
      openEvents: [
        eventReadFactory({ name: "Test Open Event", status: openStatus }),
      ],
      closedEvents: [
        eventReadFactory({ name: "Test Closed Event", status: closedStatus }),
      ],
    });
    cy.contains("NEW").click();
    cy.findByLabelText("Event Name").click().type("Test Name");
    cy.contains("Save").should("not.be.disabled");
  });
  it("has 'Save' button disabled when alert is selected and new event is selected and is not given a name", () => {
    factory({
      selected: ["uuid"],
      openEvents: [
        eventReadFactory({ name: "Test Open Event", status: openStatus }),
      ],
      closedEvents: [
        eventReadFactory({ name: "Test Closed Event", status: closedStatus }),
      ],
    });
    cy.contains("NEW").click();
    cy.findByText("Save").parent().should("be.disabled");
  });
  it("has 'Save' button enabled when alert is selected and existing event is selected", () => {
    factory({
      selected: ["uuid"],
      openEvents: [
        eventReadFactory({ name: "Test Open Event", status: openStatus }),
      ],
      closedEvents: [
        eventReadFactory({ name: "Test Closed Event", status: closedStatus }),
      ],
    });
    cy.contains("Test Open Event").click();
    cy.findByText("Save").parent().should("not.be.disabled");
  });
  it("has 'Save' button disabled when alert is selected and no event is selected", () => {
    factory({
      selected: ["uuid"],
      openEvents: [
        eventReadFactory({ name: "Test Open Event", status: openStatus }),
      ],
      closedEvents: [
        eventReadFactory({ name: "Test Closed Event", status: closedStatus }),
      ],
    });
    cy.findByText("Save").parent().should("be.disabled");
  });
  it("has 'Save' button disabled when alert is not selected and new event is selected and not given a name", () => {
    factory({
      selected: [],
      openEvents: [
        eventReadFactory({ name: "Test Open Event", status: openStatus }),
      ],
      closedEvents: [
        eventReadFactory({ name: "Test Closed Event", status: closedStatus }),
      ],
    });
    cy.contains("NEW").click();
    cy.findByText("Save").parent().should("be.disabled");
  });
  it("has 'Save' button disabled when alert is not selected and new event is selected and is given a name", () => {
    factory({
      selected: [],
      openEvents: [
        eventReadFactory({ name: "Test Open Event", status: openStatus }),
      ],
      closedEvents: [
        eventReadFactory({ name: "Test Closed Event", status: closedStatus }),
      ],
    });
    cy.contains("NEW").click();
    cy.findByLabelText("Event Name").click().type("Test Name");
    cy.findByText("Save").parent().should("be.disabled");
  });
  it("has 'Save' button disabled when alert is not selected and existing event is selected", () => {
    factory({
      selected: [],
      openEvents: [
        eventReadFactory({ name: "Test Open Event", status: openStatus }),
      ],
      closedEvents: [
        eventReadFactory({ name: "Test Closed Event", status: closedStatus }),
      ],
    });
    cy.contains("Test Open Event").click();
    cy.findByText("Save").parent().should("be.disabled");
  });
  it("attempts to save to existing event when an event is selected and the 'Save' button is clicked", () => {
    cy.stub(Alert, "update")
      .withArgs([
        {
          uuid: "uuid",
          eventUuid: "testEvent1",
          historyUsername: "analyst",
        },
      ])
      .as("updateAlert")
      .resolves();
    factory({
      selected: ["uuid"],
      openEvents: [
        eventReadFactory({ name: "Test Open Event", status: openStatus }),
      ],
      closedEvents: [
        eventReadFactory({ name: "Test Closed Event", status: closedStatus }),
      ],
    });
    cy.contains("Test Open Event").click();
    cy.findByText("Save").click();
    cy.get("@updateAlert").should("have.been.calledOnce");
    cy.get("[data-cy='save-to-event-modal']").should("not.exist");
  });
  it("attempts to create and save to new event when new event is selected and the 'Save' button is clicked", () => {
    cy.stub(Event, "create")
      .withArgs(
        {
          name: "Test Name",
          queue: "testObject",
          owner: "analyst",
          status: "OPEN",
          historyUsername: "analyst",
        },
        true,
      )
      .as("createEvent")
      .returns(eventReadFactory());
    cy.stub(Alert, "update")
      .withArgs([
        {
          uuid: "uuid",
          eventUuid: "testEvent1",
          historyUsername: "analyst",
        },
      ])
      .as("updateAlert")
      .resolves();
    factory({
      selected: ["uuid"],
      openEvents: [
        eventReadFactory({ name: "Test Open Event", status: openStatus }),
      ],
      closedEvents: [
        eventReadFactory({ name: "Test Closed Event", status: closedStatus }),
      ],
    });
    cy.contains("NEW").click();
    cy.findByLabelText("Event Name").click().type("Test Name");
    cy.findByText("Save").click();
    cy.get("@createEvent").should("have.been.calledOnce");
    cy.get("@updateAlert").should("have.been.calledOnce");
    cy.get("[data-cy='save-to-event-modal']").should("not.exist");
  });
  it("attempts to create and save to new event when new event, and disposition comment when is selected, comment is given, and the 'Save' button is clicked", () => {
    cy.stub(Event, "create")
      .withArgs(
        {
          name: "Test Name",
          queue: "testObject",
          owner: "analyst",
          status: "OPEN",
          historyUsername: "analyst",
        },
        true,
      )
      .as("createEvent")
      .returns(eventReadFactory());
    cy.stub(Comment, "create")
      .withArgs([
        {
          username: "analyst",
          nodeUuid: "testEvent1",
          user: "analyst",
          value: "Test Comment",
        },
      ])
      .as("createComment")
      .resolves();
    cy.stub(Alert, "update")
      .withArgs([
        {
          uuid: "uuid",
          eventUuid: "testEvent1",
          historyUsername: "analyst",
        },
      ])
      .as("updateAlert")
      .resolves();
    factory({
      selected: ["uuid"],
      openEvents: [
        eventReadFactory({ name: "Test Open Event", status: openStatus }),
      ],
      closedEvents: [
        eventReadFactory({ name: "Test Closed Event", status: closedStatus }),
      ],
    });
    cy.contains("NEW").click();
    cy.findByLabelText("Event Name").click().type("Test Name");
    cy.findByLabelText("Event Comment").click().type("Test Comment");
    cy.findByText("Save").click();
    cy.get("@createEvent").should("have.been.calledOnce");
    cy.get("@createComment").should("have.been.calledOnce");
    cy.get("@updateAlert").should("have.been.calledOnce");
    cy.get("[data-cy='save-to-event-modal']").should("not.exist");
  });
  it("attempts to create and save to new event when new event, and disposition comment when is selected, comment is given using CommentAutocomplete, and the 'Save' button is clicked", () => {
    cy.stub(Event, "create")
      .withArgs(
        {
          name: "Test Name",
          queue: "testObject",
          owner: "analyst",
          status: "OPEN",
          historyUsername: "analyst",
        },
        true,
      )
      .as("createEvent")
      .returns(eventReadFactory());
    cy.stub(Comment, "create")
      .withArgs([
        {
          username: "analyst",
          nodeUuid: "testEvent1",
          user: "analyst",
          value: "test extra content",
        },
      ])
      .as("createComment")
      .resolves();
    cy.stub(Alert, "update")
      .withArgs([
        {
          uuid: "uuid",
          eventUuid: "testEvent1",
          historyUsername: "analyst",
        },
      ])
      .as("updateAlert")
      .resolves();
    factory({
      selected: ["uuid"],
      openEvents: [
        eventReadFactory({ name: "Test Open Event", status: openStatus }),
      ],
      closedEvents: [
        eventReadFactory({ name: "Test Closed Event", status: closedStatus }),
      ],
    });
    cy.contains("NEW").click();
    cy.findByLabelText("Event Name").click().type("Test Name");
    cy.get(".p-autocomplete > .p-button").click();
    cy.contains("test").click();
    cy.findByDisplayValue("test").click().type(" extra content");
    cy.findByText("Save").click();
    cy.get("@createEvent").should("have.been.calledOnce");
    cy.get("@createComment").should("have.been.calledOnce");
    cy.get("@updateAlert").should("have.been.calledOnce");
    cy.get("[data-cy='save-to-event-modal']").should("not.exist");
  });
  it("shows error when attempt to save to existing event fails", () => {
    cy.stub(Alert, "update")
      .withArgs([
        {
          uuid: "uuid",
          eventUuid: "testEvent1",
          historyUsername: "analyst",
        },
      ])
      .as("updateAlert")
      .rejects(new Error("404 request failed"));
    factory({
      selected: ["uuid"],
      openEvents: [
        eventReadFactory({ name: "Test Open Event", status: openStatus }),
      ],
      closedEvents: [
        eventReadFactory({ name: "Test Closed Event", status: closedStatus }),
      ],
    });
    cy.contains("Test Open Event").click();
    cy.findByText("Save").click();
    cy.get("@updateAlert").should("have.been.calledOnce");
    cy.contains("404 request failed").should("be.visible");
  });
  it("shows error when attempt to create new event fails", () => {
    cy.stub(Event, "create")
      .withArgs(
        {
          name: "Test Name",
          queue: "testObject",
          owner: "analyst",
          status: "OPEN",
          historyUsername: "analyst",
        },
        true,
      )
      .as("createEvent")
      .rejects(new Error("404 request failed"));
    cy.stub(Alert, "update").as("updateAlert").resolves();
    factory({
      selected: ["uuid"],
      openEvents: [
        eventReadFactory({ name: "Test Open Event", status: openStatus }),
      ],
      closedEvents: [
        eventReadFactory({ name: "Test Closed Event", status: closedStatus }),
      ],
    });
    cy.contains("NEW").click();
    cy.findByLabelText("Event Name").click().type("Test Name");
    cy.findByText("Save").click();
    cy.get("@createEvent").should("have.been.calledOnce");
    cy.get("@updateAlert").should("not.have.been.calledOnce");
    cy.contains("404 request failed").should("be.visible");
  });
  it("shows error when attempt create comment fails with error code other than 409", () => {
    cy.stub(Event, "create")
      .withArgs(
        {
          name: "Test Name",
          queue: "testObject",
          owner: "analyst",
          status: "OPEN",
          historyUsername: "analyst",
        },
        true,
      )
      .as("createEvent")
      .returns(eventReadFactory());
    cy.stub(Comment, "create")
      .withArgs([
        {
          username: "analyst",
          nodeUuid: "testEvent1",
          user: "analyst",
          value: "Test Comment",
        },
      ])
      .as("createComment")
      .rejects(new Error("404 request failed"));
    cy.stub(Alert, "update")
      .withArgs([
        {
          uuid: "uuid",
          eventUuid: "testEvent1",
          historyUsername: "analyst",
        },
      ])
      .as("updateAlert")
      .resolves();
    factory({
      selected: ["uuid"],
      openEvents: [
        eventReadFactory({ name: "Test Open Event", status: openStatus }),
      ],
      closedEvents: [
        eventReadFactory({ name: "Test Closed Event", status: closedStatus }),
      ],
    });
    cy.contains("NEW").click();
    cy.findByLabelText("Event Name").click().type("Test Name");
    cy.findByLabelText("Event Comment").click().type("Test Comment");
    cy.findByText("Save").click();
    cy.get("@createEvent").should("have.been.calledOnce");
    cy.get("@createComment").should("have.been.calledOnce");
    cy.contains("404 request failed").should("be.visible");
  });
  it("does not show error when attempt create comment fails with error code 409", () => {
    cy.stub(Event, "create")
      .withArgs(
        {
          name: "Test Name",
          queue: "testObject",
          owner: "analyst",
          status: "OPEN",
          historyUsername: "analyst",
        },
        true,
      )
      .as("createEvent")
      .returns(eventReadFactory());
    cy.stub(Comment, "create")
      .withArgs([
        {
          username: "analyst",
          nodeUuid: "testEvent1",
          user: "analyst",
          value: "Test Comment",
        },
      ])
      .as("createComment")
      .rejects(new Error("409 already exists"));
    cy.stub(Alert, "update")
      .withArgs([
        {
          uuid: "uuid",
          eventUuid: "testEvent1",
          historyUsername: "analyst",
        },
      ])
      .as("updateAlert")
      .resolves();
    factory({
      selected: ["uuid"],
      openEvents: [
        eventReadFactory({ name: "Test Open Event", status: openStatus }),
      ],
      closedEvents: [
        eventReadFactory({ name: "Test Closed Event", status: closedStatus }),
      ],
    });
    cy.contains("NEW").click();
    cy.findByLabelText("Event Name").click().type("Test Name");
    cy.findByLabelText("Event Comment").click().type("Test Comment");
    cy.findByText("Save").click();
    cy.get("@createEvent").should("have.been.calledOnce");
    cy.get("@createComment").should("have.been.calledOnce");
    cy.get("@updateAlert").should("have.been.calledOnce");
    cy.get("[data-cy='save-to-event-modal']").should("not.exist");
  });
});
