// TODO: Move to eventTable store tests
import myNock from "@unit/services/api/nock";
import { eventFilterParams, eventRead, eventSummary } from "@/models/event";
import { parseEventSummary, useEventTableStore } from "@/stores/eventTable";
import { createTestingPinia } from "@pinia/testing";
import { eventQueueRead } from "@/models/eventQueue";

createTestingPinia();
const store = useEventTableStore();

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

const mockEventReadA = Object.assign({}, mockEvent, { uuid: "uuid1" });
const mockEventReadB = Object.assign({}, mockEvent, { uuid: "uuid2" });
const mockEventReadC: eventRead = {
  dispositionTime: new Date("2021-12-18T00:59:43.570343+00:00"),
  eventTime: new Date("2021-12-18T00:59:43.570343+00:00"),
  name: "Test event",
  owner: null,
  queue: { value: "testQueue", description: null, uuid: "1" },
  type: { value: "testType", description: null, uuid: "1" },
  comments: [],
  nodeType: "",
  tags: [],
  threats: [],
  uuid: "uuid3",
  version: "",
  threatActors: [],
  alertTime: null,
  alertUuids: [],
  containTime: null,
  creationTime: new Date("2020-01-01"),
  ownershipTime: null,
  preventionTools: [],
  remediations: [],
  remediationTime: null,
  riskLevel: null,
  source: null,
  status: null,
  vectors: [],
};

const mockEventReadASummary: eventSummary = {
  comments: [],
  name: "Small Event",
  owner: "Analyst",
  tags: [],
  type: "test_type",
  uuid: "uuid1",
  createdTime: new Date(),
  preventionTools: [],
  riskLevel: "",
  status: "",
  vectors: [],
};

const mockEventReadBSummary: eventSummary = {
  comments: [],
  name: "Small Event",
  owner: "Analyst",
  tags: [],
  type: "test_type",
  uuid: "uuid1",
  createdTime: new Date(),
  preventionTools: [],
  riskLevel: "",
  status: "",
  vectors: [],
};

const mockEventReadCSummary: eventSummary = {
  comments: [],
  name: "Small Event",
  owner: "Analyst",
  tags: [],
  type: "test_type",
  uuid: "uuid1",
  createdTime: new Date(),
  preventionTools: [],
  riskLevel: "",
  status: "",
  vectors: [],
};

const mockParams: eventFilterParams = { limit: 5, offset: 0 };

describe("eventTable helpers", () => {
  it("will correctly parse an event received from the backend using parseEventSummary", () => {
    const resA = parseEventSummary(mockEventReadA);
    const resB = parseEventSummary(mockEventReadC);
    expect(resA).toEqual(mockEventReadASummary);
    expect(resB).toEqual(mockEventReadCSummary);
  });
});

describe("eventTable getters", () => {
  beforeEach(() => {
    store.$reset();
  });

  it("will correctly return  visibleQueriedItemSummaries", () => {
    store.visibleQueriedItems = [
      mockEventReadA,
      mockEventReadB,
      mockEventReadC,
    ];
    expect(store.visibleQueriedItemSummaries).toEqual([
      mockEventReadASummary,
      mockEventReadBSummary,
      mockEventReadCSummary,
    ]);
  });

  it("will correctly return  visibleQueriedItemsUuids", () => {
    store.visibleQueriedItems = [
      mockEventReadA,
      mockEventReadB,
      mockEventReadC,
    ];
    expect(store.visibleQueriedItemsUuids).toEqual(["uuid1", "uuid2", "uuid3"]);
  });

  it("will correctly return  visibleQueriedItemById", () => {
    store.visibleQueriedItems = [
      mockEventReadA,
      mockEventReadB,
      mockEventReadC,
    ];
    expect(store.visibleQueriedItemById("uuid1")).toEqual(mockEventReadA);
  });

  it("will correctly return sortFilter", () => {
    expect(store.sortFilter).toEqual("event_time|desc");
  });
});

describe("eventTable actions", () => {
  beforeEach(() => {
    store.$reset();
  });

  it("will request to read page of events with given params on readPage", async () => {
    const mockRequest = myNock.get("/event/?limit=5&offset=0").reply(200, {
      total: 3,
      items: [mockEventReadA, mockEventReadB, mockEventReadC],
    });

    await store.readPage(mockParams);

    expect(mockRequest.isDone()).toEqual(true);
    expect(store.visibleQueriedItems).toEqual([
      Object.assign({}, JSON.parse(JSON.stringify(mockEventReadA)), {
        eventTime: "2021-12-18T00:59:43.570Z",
        insertTime: "2021-12-18T00:59:43.570Z",
        uuid: "uuid1",
      }),
      Object.assign({}, JSON.parse(JSON.stringify(mockEventReadB)), {
        eventTime: "2021-12-18T00:59:43.570Z",
        insertTime: "2021-12-18T00:59:43.570Z",
        uuid: "uuid2",
      }),
      Object.assign({}, JSON.parse(JSON.stringify(mockEventReadC)), {
        eventTime: "2021-12-18T00:59:43.570Z",
        insertTime: "2021-12-18T00:59:43.570Z",
        dispositionTime: "2021-12-18T00:59:43.570Z",
        uuid: "uuid3",
      }),
    ]);
    expect(store.totalItems).toEqual(3);
    expect(store.requestReload).toEqual(false);
  });

  it("will throw an error if request fails on readPage", async () => {
    myNock.get("/event/?limit=5&offset=0").reply(403);

    await expect(store.readPage(mockParams)).rejects.toEqual(
      new Error("Request failed with status code 403"),
    );

    expect(store.visibleQueriedItems).toEqual([]);
    expect(store.totalItems).toEqual(0);
    expect(store.requestReload).toEqual(false);
  });
  it("will reset the sort order and sort field to written defaults on resetSort", () => {
    store.sortField = "exampleSort";
    store.sortOrder = "asc";

    store.resetSort();

    expect(store.sortField).toEqual("eventTime");
    expect(store.sortOrder).toEqual("desc");
  });
});
