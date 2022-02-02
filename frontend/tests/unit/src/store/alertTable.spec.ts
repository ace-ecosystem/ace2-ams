// TODO: Move to alertTable store tests
import myNock from "@unit/services/api/nock";
import { alertFilterParams, alertRead, alertSummary } from "@/models/alert";
import { useAlertTableStore } from "@/stores/alertTable";
import { parseAlertSummary } from "@/etc/helpers";
import { createTestingPinia } from "@pinia/testing";
import {
  mockAlert,
  mockAlertReadA,
  mockAlertReadASummary,
} from "../../../mocks/alert";

createTestingPinia();
const store = useAlertTableStore();

const mockAlertReadB = Object.assign({}, mockAlert, { uuid: "uuid2" });
const mockAlertReadC: alertRead = {
  childTags: [],
  childThreatActors: [],
  childThreats: [],
  description: "test description",
  disposition: {
    value: "FALSE_POSITIVE",
    rank: 0,
    uuid: "1",
    description: null,
  },
  dispositionTime: new Date("2021-12-18T00:59:43.570343+00:00"),
  dispositionUser: null,
  eventTime: new Date("2021-12-18T00:59:43.570343+00:00"),
  eventUuid: null,
  insertTime: new Date("2021-12-18T00:59:43.570343+00:00"),
  instructions: null,
  name: "Test alert",
  owner: null,
  queue: { value: "testQueue", description: null, uuid: "1" },
  tool: null,
  toolInstance: null,
  type: { value: "testType", description: null, uuid: "1" },
  comments: [],
  nodeType: "",
  tags: [],
  threats: [],
  uuid: "uuid3",
  version: "",
  threatActors: [],
};

const mockAlertReadBSummary: alertSummary = {
  childTags: [
    {
      description: null,
      value: "recipient",
      uuid: "c5d3321d-883c-4772-b511-489273e13fde",
    },
    {
      description: null,
      value: "from_address",
      uuid: "f9081b70-c2bf-4a7d-ba90-a675e8a929d2",
    },
    {
      description: null,
      value: "contacted_host",
      uuid: "3c1ca637-48d1-4d47-aeee-0962bc32d96d",
    },
    {
      description: null,
      value: "c2",
      uuid: "a0b2d514-c544-4a8f-a059-b6151b9f1dd6",
    },
  ],
  comments: [],
  description: "",
  disposition: "OPEN",
  dispositionTime: null,
  dispositionUser: "Analyst",
  eventUuid: "None",

  eventTime: new Date("2021-12-18T00:59:43.570343+00:00"),
  insertTime: new Date("2021-12-18T00:59:43.570343+00:00"),
  name: "Small Alert",
  owner: "Analyst",
  queue: "test_queue",
  tags: [],
  tool: "test_tool",
  toolInstance: "test_tool_instance",

  type: "test_type",
  uuid: "uuid2",
};
const mockAlertReadCSummary: alertSummary = {
  childTags: [],
  comments: [],
  description: "test description",
  disposition: "FALSE_POSITIVE",
  dispositionTime: new Date("2021-12-18T00:59:43.570343+00:00"),
  dispositionUser: "None",
  eventUuid: "None",
  eventTime: new Date("2021-12-18T00:59:43.570343+00:00"),
  insertTime: new Date("2021-12-18T00:59:43.570343+00:00"),
  name: "Test alert",
  owner: "None",
  queue: "testQueue",
  tags: [],
  tool: "None",
  toolInstance: "None",

  type: "testType",
  uuid: "uuid3",
};

const mockParams: alertFilterParams = { limit: 5, offset: 0 };

describe("alertTable helpers", () => {
  it("will correctly parse an alert received from the backend using parseAlertSummary", () => {
    const resA = parseAlertSummary(mockAlertReadA);
    const resB = parseAlertSummary(mockAlertReadC);
    expect(resA).toEqual(mockAlertReadASummary);
    expect(resB).toEqual(mockAlertReadCSummary);
  });
});

describe("alertTable getters", () => {
  beforeEach(() => {
    store.$reset();
  });

  it("will correctly return  visibleQueriedItemSummaries", () => {
    store.visibleQueriedItems = [
      mockAlertReadA,
      mockAlertReadB,
      mockAlertReadC,
    ];
    expect(store.visibleQueriedItemSummaries).toEqual([
      mockAlertReadASummary,
      mockAlertReadBSummary,
      mockAlertReadCSummary,
    ]);
  });

  it("will correctly return  visibleQueriedItemsUuids", () => {
    store.visibleQueriedItems = [
      mockAlertReadA,
      mockAlertReadB,
      mockAlertReadC,
    ];
    expect(store.visibleQueriedItemsUuids).toEqual(["uuid1", "uuid2", "uuid3"]);
  });

  it("will correctly return  visibleQueriedItemById", () => {
    store.visibleQueriedItems = [
      mockAlertReadA,
      mockAlertReadB,
      mockAlertReadC,
    ];
    expect(store.visibleQueriedItemById("uuid1")).toEqual(mockAlertReadA);
  });

  it("will correctly return sortFilter", () => {
    expect(store.sortFilter).toEqual("event_time|desc");
  });
});

describe("alertTable actions", () => {
  beforeEach(() => {
    store.$reset();
  });

  it("will request to read page of alerts with given params on readPage", async () => {
    const mockRequest = myNock.get("/alert/?limit=5&offset=0").reply(200, {
      total: 3,
      items: [mockAlertReadA, mockAlertReadB, mockAlertReadC],
    });

    await store.readPage(mockParams);

    expect(mockRequest.isDone()).toEqual(true);
    expect(store.visibleQueriedItems).toEqual([
      Object.assign({}, JSON.parse(JSON.stringify(mockAlertReadA)), {
        eventTime: "2021-12-18T00:59:43.570Z",
        insertTime: "2021-12-18T00:59:43.570Z",
        uuid: "uuid1",
      }),
      Object.assign({}, JSON.parse(JSON.stringify(mockAlertReadB)), {
        eventTime: "2021-12-18T00:59:43.570Z",
        insertTime: "2021-12-18T00:59:43.570Z",
        uuid: "uuid2",
      }),
      Object.assign({}, JSON.parse(JSON.stringify(mockAlertReadC)), {
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
    myNock.get("/alert/?limit=5&offset=0").reply(403);

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
