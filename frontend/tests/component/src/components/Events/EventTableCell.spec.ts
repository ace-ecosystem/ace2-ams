import { mount } from "@cypress/vue";
import { createPinia } from "pinia";
import PrimeVue from "primevue/config";

import EventTableCell from "@/components/Events/EventTableCell.vue";

import router from "@/router/index";
import { eventSummary } from "@/models/event";
import { eventCommentReadFactory } from "@mocks/comment";
import { eventSummaryFactory } from "@mocks/events";
import { metadataTagReadFactory } from "@mocks/metadata";

interface EventTableCellProps {
  data: eventSummary;
  field: keyof eventSummary | "edit";
  showTags?: boolean;
}

const mockEvent: eventSummary = eventSummaryFactory({
  name: "Test",
  createdTime: new Date(Date.UTC(2022, 2, 24)),
  comments: [eventCommentReadFactory({ value: "Test comment" })],
  tags: [metadataTagReadFactory({ value: "testTag" })],
  threats: ["threat A", "threat B"],
  queue: "testEventQueue",
});

const defaultProps: EventTableCellProps = {
  data: mockEvent,
  field: "name",
};

function factory(
  args = {
    props: defaultProps,
  },
) {
  return mount(EventTableCell, {
    global: {
      plugins: [createPinia(), PrimeVue, router],
      provide: { objectType: "events" },
    },
    propsData: args.props,
  });
}

describe("EventTableCell", () => {
  it("correctly renders an event name cell with any tags and comments", () => {
    const props: EventTableCellProps = {
      data: mockEvent,
      field: "name",
    };
    factory({ props: props });
    // Event name & link
    cy.contains("Test")
      .invoke("attr", "href")
      .should("contain", "/event/testEvent1");
    // Tags
    cy.contains("testTag");
    // Comments
    cy.contains("(Test Analyst) Test comment");
  });
  it("correctly renders an event name cell with comments and WITHOUT tags ", () => {
    const props: EventTableCellProps = {
      data: mockEvent,
      field: "name",
      showTags: false,
    };
    factory({ props: props });
    // Event name & link
    cy.contains("Test")
      .invoke("attr", "href")
      .should("contain", "/event/testEvent1");
    // Tags
    cy.contains("testTag").should("not.exist");
    // Comments
    cy.contains("(Test Analyst) Test comment");
  });
  it("correctly renders an event time-type cell", () => {
    const props: EventTableCellProps = {
      data: mockEvent,
      field: "createdTime",
    };
    factory({ props: props });
    cy.contains("3/24/2022, 12:00:00 AM");
  });
  it("correctly renders an event array-type cell", () => {
    const props: EventTableCellProps = {
      data: mockEvent,
      field: "threats",
    };
    factory({ props: props });
    cy.contains("threat A, threat B");
  });
  it("correctly renders an edit event cell", () => {
    const props: EventTableCellProps = {
      data: mockEvent,
      field: "edit",
    };
    factory({ props: props });
    cy.get('[data-cy="edit-event-button"]').should("be.visible").click();
    cy.contains("Edit Event").should("be.visible"); // Check that clicking opened the modal
  });
  it("correctly renders a generic event cell (queue)", () => {
    const props: EventTableCellProps = {
      data: mockEvent,
      field: "queue",
    };
    factory({ props: props });
    cy.contains("testEventQueue");
  });
});
