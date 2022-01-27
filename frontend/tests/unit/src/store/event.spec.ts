/**
 * @jest-environment node
 */

import myNock from "@unit/services/api/nock";
import { eventRead } from "@/models/event";
import { useEventStore } from "@/stores/event";
import { createTestingPinia } from "@pinia/testing";
import { eventQueueRead } from "@/models/eventQueue";

createTestingPinia();

const store = useEventStore();

const mockQueue: eventQueueRead = {
  description: null,
  uuid: "",
  value: "",
};

const mockEvent: eventRead = {
  comments: [],
  name: "Test Event",
  tags: [],
  uuid: "uuid1",
  alertTime: null,
  alertUuids: [],
  containTime: null,
  creationTime: new Date("2020-01-01"),
  dispositionTime: null,
  eventTime: null,
  owner: null,
  ownershipTime: null,
  preventionTools: [],
  queue: mockQueue,
  remediations: [],
  remediationTime: null,
  riskLevel: null,
  source: null,
  status: null,
  threatActors: [],
  threats: [],
  type: null,
  vectors: [],
  nodeType: "",
  version: "",
};

describe("event Actions", () => {
  beforeEach(() => {
    store.$reset();
  });

  it("will fetch event data given an event ID", async () => {
    const mockRequest = myNock.get("/event/uuid1").reply(200, mockEvent);
    await store.read("uuid1");

    expect(mockRequest.isDone()).toEqual(true);

    expect(store.openEvent).toEqual(mockEvent);
  });

  it("will make a request to update an event given the UUID and update data upon the updateEvent action", async () => {
    const mockRequest = myNock.patch("/event/").reply(200);
    await store.update([{ uuid: "uuid1", name: "test" }]);

    expect(mockRequest.isDone()).toEqual(true);
    // None of these should be changed
    expect(store.openEvent).toBeNull();
  });
});
