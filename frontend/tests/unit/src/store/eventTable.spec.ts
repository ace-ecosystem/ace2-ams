// TODO: Move to eventTable store tests
import myNock from "@unit/services/api/nock";
import { eventFilterParams } from "@/models/event";
import { parseEventSummary, useEventTableStore } from "@/stores/eventTable";
import { createTestingPinia } from "@pinia/testing";
import { eventReadFactory, eventSummaryFactory } from "../../../mocks/events";
import { genericObjectReadFactory } from "../../../mocks/genericObject";
import { nodeThreatReadFactory } from "../../../mocks/nodeThreat";
import { userReadFactory } from "../../../mocks/user";

createTestingPinia();
const store = useEventTableStore();

const mockEventReadA = eventReadFactory({ uuid: "uuid1" });
const mockEventReadASummary = eventSummaryFactory({ uuid: "uuid1" });
const mockEventReadB = eventReadFactory({ uuid: "uuid2" });
const mockEventReadBSummary = eventSummaryFactory({ uuid: "uuid2" });

const mockOwner = userReadFactory();
const mockPreventionTool = genericObjectReadFactory({
  value: "preventionTool",
});
const mockRiskLevel = genericObjectReadFactory({ value: "riskLevel" });
const mockStatus = genericObjectReadFactory({ value: "status" });
const mockThreat = nodeThreatReadFactory();
const mockThreatActor = genericObjectReadFactory({ value: "threatActor" });
const mockType = genericObjectReadFactory({ value: "type" });
const mockVector = genericObjectReadFactory({ value: "vector" });
const mockEventReadC = eventReadFactory({
  uuid: "uuid3",
  owner: mockOwner,
  preventionTools: [mockPreventionTool],
  riskLevel: mockRiskLevel,
  status: mockStatus,
  threatActors: [mockThreatActor],
  threats: [mockThreat],
  type: mockType,
  vectors: [mockVector],
});
const mockEventReadCSummary = eventSummaryFactory({
  uuid: "uuid3",
  owner: "Test Analyst",
  preventionTools: ["preventionTool"],
  riskLevel: "riskLevel",
  status: "status",
  threatActors: ["threatActor"],
  threats: ["nodeThreat"],
  type: "type",
  vectors: ["vector"],
});

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
    expect(store.sortFilter).toEqual("created_time|desc");

    store.sortField = null;
    store.sortOrder = null;
    expect(store.sortFilter).toBeNull();
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
      JSON.parse(JSON.stringify(mockEventReadA)),
      JSON.parse(JSON.stringify(mockEventReadB)),
      JSON.parse(JSON.stringify(mockEventReadC)),
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

    expect(store.sortField).toEqual("createdTime");
    expect(store.sortOrder).toEqual("desc");
  });
});
