import { alertFilters } from "../../../../src/etc/configuration/alerts";
import {
  formatNodeFiltersForAPI,
  parseFilters,
  getAlertLink,
  getAllAlertTags,
  groupItemsByQueue,
} from "../../../../src/etc/helpers";
import { alertTreeReadFactory } from "../../../mocks/alert";
import { alertFilterParams } from "../../../../src/models/alert";
import { userRead } from "../../../../src/models/user";
import { useObservableTypeStore } from "../../../../src/stores/observableType";
import { useUserStore } from "../../../../src/stores/user";
import { createTestingPinia } from "@pinia/testing";
import { expect } from "vitest";
import { vi, describe, it } from "vitest";
import { genericObjectReadFactory } from "../../../mocks/genericObject";

createTestingPinia({ createSpy: vi.fn });

const mockAlertTreeRead = alertTreeReadFactory({
  tags: [
    genericObjectReadFactory({
      value: "from_address",
      uuid: "uuid3",
      description: null,
    }),
    genericObjectReadFactory({
      value: "contacted_host",
      uuid: "uuid2",
      description: null,
    }),
    genericObjectReadFactory({
      value: "contacted_host",
      uuid: "uuid2",
      description: null,
    }),
    genericObjectReadFactory({
      value: "contacted_host",
      uuid: "uuid2",
      description: null,
    }),
    genericObjectReadFactory({ value: "c2", uuid: "uuid1", description: null }),
    genericObjectReadFactory({
      value: "recipient",
      uuid: "uuid4",
      description: null,
    }),
  ],
});

describe("parseFilters", () => {
  it("will correctly parse and add any multiselect filters", async () => {
    const observableTypeStore = useObservableTypeStore();
    observableTypeStore.items = [
      { value: "ipv4", description: null, uuid: "1" },
      { value: "file", description: null, uuid: "2" },
    ];

    const results = parseFilters(
      { observableTypes: "ipv4,file,fake" },
      alertFilters.external,
    );

    expect(results).toEqual({
      observableTypes: [
        { value: "ipv4", description: null, uuid: "1" },
        { value: "file", description: null, uuid: "2" },
      ],
    });
  });

  it("will correctly parse and add any chips filters", async () => {
    const results = parseFilters({ tags: "tagA,tagB" }, alertFilters.external);

    expect(results).toEqual({
      tags: ["tagA", "tagB"],
    });
  });

  it("will correctly parse and add any select filters", async () => {
    const mockUserA: userRead = {
      defaultAlertQueue: { description: null, uuid: "1", value: "default" },
      defaultEventQueue: { description: null, uuid: "1", value: "default" },
      displayName: "Test Analyst",
      email: "analyst@test.com",
      enabled: true,
      roles: [],
      timezone: "UTC",
      training: false,
      username: "analystA",
      uuid: "1",
    };

    const mockUserB: userRead = {
      defaultAlertQueue: { description: null, uuid: "1", value: "default" },
      defaultEventQueue: { description: null, uuid: "1", value: "default" },
      displayName: "Test Analyst",
      email: "analyst@test.com",
      enabled: true,
      roles: [],
      timezone: "UTC",
      training: false,
      username: "analystB",
      uuid: "1",
    };

    const userStore = useUserStore();
    userStore.items = [mockUserA, mockUserB];

    const results = parseFilters({ owner: "analystB" }, alertFilters.external);

    expect(results).toEqual({
      owner: mockUserB,
    });
  });

  it("will correctly parse and add any date filters", async () => {
    const results = parseFilters(
      {
        eventTimeBefore:
          "Sat Jan 08 2022 11:31:51 GMT-0500 (Eastern Standard Time)",
      },
      alertFilters.external,
    );

    expect(results).toEqual({
      eventTimeBefore: new Date("2022-01-08T16:31:51.000Z"),
    });
  });

  it("will skip any date filters that fail to parse", async () => {
    const results = parseFilters(
      { eventTimeBefore: "Bad Date" },
      alertFilters.external,
    );

    expect(results).toEqual({});
  });

  it("will correctly parse and add any input text filters", async () => {
    const results = parseFilters({ name: "test name" }, alertFilters.external);

    expect(results).toEqual({
      name: "test name",
    });
  });
  it("will correctly parse and add any catetgorized value filters", async () => {
    const observableTypeStore = useObservableTypeStore();
    observableTypeStore.items = [
      { value: "ipv4", description: null, uuid: "1" },
      { value: "file", description: null, uuid: "2" },
    ];

    const results = parseFilters(
      { observable: "ipv4|1.2.3.4" },
      alertFilters.external,
    );

    expect(results).toEqual({
      observable: {
        category: { value: "ipv4", description: null, uuid: "1" },
        value: "1.2.3.4",
      },
    });
  });
  it("will correctly parse and add any combined filters", async () => {
    const observableTypeStore = useObservableTypeStore();
    observableTypeStore.items = [
      { value: "ipv4", description: null, uuid: "1" },
      { value: "file", description: null, uuid: "2" },
    ];

    const mockUserA: userRead = {
      defaultAlertQueue: { description: null, uuid: "1", value: "default" },
      defaultEventQueue: { description: null, uuid: "1", value: "default" },
      displayName: "Test Analyst",
      email: "analyst@test.com",
      enabled: true,
      roles: [],
      timezone: "UTC",
      training: false,
      username: "analystA",
      uuid: "1",
    };

    const mockUserB: userRead = {
      defaultAlertQueue: { description: null, uuid: "1", value: "default" },
      defaultEventQueue: { description: null, uuid: "1", value: "default" },
      displayName: "Test Analyst",
      email: "analyst@test.com",
      enabled: true,
      roles: [],
      timezone: "UTC",
      training: false,
      username: "analystB",
      uuid: "1",
    };

    const userStore = useUserStore();
    userStore.items = [mockUserA, mockUserB];

    const results = parseFilters(
      {
        observable: "ipv4|1.2.3.4",
        eventTimeBefore:
          "Sat Jan 08 2022 11:31:51 GMT-0500 (Eastern Standard Time)",
        name: "test name",
        observableTypes: "ipv4,file,fake",
        fake: "blah",
        owner: "analystB",
        tags: "tagA,tagB",
      },
      alertFilters.external,
    );

    expect(results).toEqual({
      tags: ["tagA", "tagB"],
      owner: mockUserB,
      observableTypes: [
        { value: "ipv4", description: null, uuid: "1" },
        { value: "file", description: null, uuid: "2" },
      ],
      eventTimeBefore: new Date("2022-01-08T16:31:51.000Z"),
      name: "test name",
      observable: {
        category: { value: "ipv4", description: null, uuid: "1" },
        value: "1.2.3.4",
      },
    });
  });
});

describe("formatNodeFiltersForAPI", () => {
  const MOCK_PARAMS: alertFilterParams = {
    limit: 10,
    offset: 10,
    name: "Test Name",
    disposition: {
      rank: 0,
      description: null,
      uuid: "1",
      value: "FALSE_POSITIVE",
    },
    observableTypes: [
      { value: "testA", description: null, uuid: "1" },
      { value: "testB", description: null, uuid: "2" },
    ],
    tags: ["tagA", "tagB"],
    threats: [
      { value: "threatA", description: null, types: [], uuid: "1" },
      { value: "threatB", description: null, types: [], uuid: "2" },
    ],
    observable: {
      category: { value: "test", description: null, uuid: "1" },
      value: "example",
    },
  };
  it("will correctly parse and add any multiselect filters", async () => {
    const formattedFilters = formatNodeFiltersForAPI(
      alertFilters.external,
      MOCK_PARAMS,
    );
    expect(formattedFilters).toEqual({
      limit: 10,
      offset: 10,
      disposition: "FALSE_POSITIVE",
      name: "Test Name",
      threats: "threatA,threatB",
      observableTypes: "testA,testB",
      tags: "tagA,tagB",
      observable: "test|example",
    });
  });

  it("getAlertLink correctly generates an alert link given an alert object", () => {
    const result = getAlertLink(mockAlertTreeRead);
    expect(result).toEqual("/alert/testAlertUuid");
  });

  it("getAllAlertTags formats a given alert's tags into a sorted and dedup'd list of tags", () => {
    const result = getAllAlertTags(mockAlertTreeRead);
    expect(result).toEqual([
      {
        description: null,
        value: "c2",
        uuid: "uuid1",
      },
      {
        description: null,
        value: "contacted_host",
        uuid: "uuid2",
      },
      {
        description: null,
        value: "from_address",
        uuid: "uuid3",
      },
      {
        description: null,
        value: "recipient",
        uuid: "uuid4",
      },
    ]);
  });
});

describe("groupItemsByQueue", () => {
  it("correctly returns an object of items grouped by their 'queues' property, skipping any without it", () => {
    const queueA = genericObjectReadFactory({ value: "A" });
    const queueB = genericObjectReadFactory({ value: "B" });
    const queueC = genericObjectReadFactory({ value: "C" });
    const testData = [
      { value: 1, queues: [queueA, queueB] },
      { value: 2, queues: [queueB] },
      { value: 3, queues: [queueA, queueC] },
      { value: 4 },
      { value: 5, queues: [queueA] },
      { value: 6, queues: [queueB] },
      { value: 7, queues: [queueB, queueC] },
    ];

    const expected = {
      A: [
        { value: 1, queues: [queueA, queueB] },
        { value: 3, queues: [queueA, queueC] },
        { value: 5, queues: [queueA] },
      ],
      B: [
        { value: 1, queues: [queueA, queueB] },
        { value: 2, queues: [queueB] },
        { value: 6, queues: [queueB] },
        { value: 7, queues: [queueB, queueC] },
      ],
      C: [
        { value: 3, queues: [queueA, queueC] },
        { value: 7, queues: [queueB, queueC] },
      ],
    };

    const result = groupItemsByQueue(testData);
    expect(result).toEqual(expected);
  });
});
