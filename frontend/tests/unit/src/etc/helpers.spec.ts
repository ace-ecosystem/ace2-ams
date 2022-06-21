import { describe, it, expect, vi } from "vitest";
import { alertFilters } from "@/etc/configuration/alerts";
import {
  formatNodeFiltersForAPI,
  parseFilters,
  getAlertLink,
  getAllAlertTags,
  groupItemsByQueue,
} from "@/etc/helpers";
import { alertTreeReadFactory } from "@mocks/alert";
import { alertFilterParams } from "@/models/alert";
import { userRead } from "@/models/user";
import { useObservableTypeStore } from "@/stores/observableType";
import { useUserStore } from "@/stores/user";
import { createTestingPinia } from "@pinia/testing";
import { genericObjectReadFactory } from "@mocks/genericObject";
import { metadataTagReadFactory } from "@mocks/metadata";
import { genericQueueableObjectRead } from "@/models/base";
import { useAlertDispositionStore } from "@/stores/alertDisposition";

createTestingPinia({ createSpy: vi.fn });

const mockAlertTreeRead = alertTreeReadFactory({
  tags: [
    metadataTagReadFactory({
      value: "from_address",
      uuid: "uuid3",
    }),
    metadataTagReadFactory({
      value: "contacted_host",
      uuid: "uuid2",
    }),
    metadataTagReadFactory({
      value: "c2",
      uuid: "uuid1",
    }),
    metadataTagReadFactory({
      value: "recipient",
      uuid: "uuid4",
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
        [
          { value: "ipv4", description: null, uuid: "1" },
          { value: "file", description: null, uuid: "2" },
        ],
      ],
    });
  });

  it("will correctly parse and add any chips filters", async () => {
    const results = parseFilters({ tags: "tagA,tagB" }, alertFilters.external);

    expect(results).toEqual({
      tags: [["tagA", "tagB"]],
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
      owner: [mockUserB],
    });
  });

  it("will correctly parse and add any nullable select filters (complex)", async () => {
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

    const results = parseFilters({ owner: "none" }, alertFilters.external);

    expect(results).toEqual({
      owner: [{ displayName: "None", username: "none" }],
    });
  });

  it("will correctly parse and add any nullable select filters (simple)", async () => {
    const dispositionStore = useAlertDispositionStore();
    dispositionStore.items = [];

    const results = parseFilters(
      { disposition: "None" },
      alertFilters.external,
    );

    expect(results).toEqual({
      disposition: [{ value: "None" }],
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
      eventTimeBefore: [new Date("2022-01-08T16:31:51.000Z")],
    });
  });

  it("will skip any date filters that fail to parse", async () => {
    const results = parseFilters(
      { eventTimeBefore: ["Bad Date"] },
      alertFilters.external,
    );

    expect(results).toEqual({});
  });

  it("will correctly parse and add any input text filters", async () => {
    const results = parseFilters({ name: "test name" }, alertFilters.external);

    expect(results).toEqual({
      name: ["test name"],
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
      observable: [
        {
          category: { value: "ipv4", description: null, uuid: "1" },
          value: "1.2.3.4",
        },
      ],
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
      tags: [["tagA", "tagB"]],
      owner: [mockUserB],
      observableTypes: [
        [
          { value: "ipv4", description: null, uuid: "1" },
          { value: "file", description: null, uuid: "2" },
        ],
      ],
      eventTimeBefore: [new Date("2022-01-08T16:31:51.000Z")],
      name: ["test name"],
      observable: [
        {
          category: { value: "ipv4", description: null, uuid: "1" },
          value: "1.2.3.4",
        },
      ],
    });
  });
  it("will correctly parse and add any combined filters with multiple filter values", async () => {
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
        observable: ["ipv4|1.2.3.4", "ipv4|5.6.7.8"],
        eventTimeBefore: [
          "Sat Jan 08 2022 11:31:51 GMT-0500 (Eastern Standard Time)",
          "Sat Jan 10 2022 11:31:51 GMT-0500 (Eastern Standard Time)",
        ],
        name: ["test name", "test name 2"],
        observableTypes: ["ipv4,file,fake", "ipv4"],
        fake: ["blah"],
        owner: ["analystB", "analystA"],
        tags: ["tagA,tagB", "tagC,tagD"],
      },
      alertFilters.external,
    );

    expect(results).toEqual({
      tags: [
        ["tagA", "tagB"],
        ["tagC", "tagD"],
      ],
      owner: [mockUserB, mockUserA],
      observableTypes: [
        [
          { value: "ipv4", description: null, uuid: "1" },
          { value: "file", description: null, uuid: "2" },
        ],
        [{ value: "ipv4", description: null, uuid: "1" }],
      ],
      eventTimeBefore: [
        new Date("2022-01-08T16:31:51.000Z"),
        new Date("2022-01-10T16:31:51.000Z"),
      ],
      name: ["test name", "test name 2"],
      observable: [
        {
          category: { value: "ipv4", description: null, uuid: "1" },
          value: "1.2.3.4",
        },
        {
          category: { value: "ipv4", description: null, uuid: "1" },
          value: "5.6.7.8",
        },
      ],
    });
  });
});

describe("formatNodeFiltersForAPI", () => {
  const MOCK_PARAMS: alertFilterParams = {
    limit: 10,
    offset: 10,
    name: ["Test Name", "Test Name 2"],
    disposition: [
      {
        rank: 0,
        description: null,
        uuid: "1",
        value: "FALSE_POSITIVE",
      },
      {
        rank: 1,
        description: null,
        uuid: "2",
        value: "IGNORE",
      },
    ],
    observableTypes: [
      [
        { value: "testA", description: null, uuid: "1" },
        { value: "testB", description: null, uuid: "2" },
      ],
      [{ value: "testC", description: null, uuid: "3" }],
    ],
    tags: [["tagA", "tagB"], ["tagC"]],
    threats: [
      [
        {
          value: "threatA",
          description: null,
          types: [],
          uuid: "1",
          queues: [],
        },
        {
          value: "threatB",
          description: null,
          types: [],
          uuid: "2",
          queues: [],
        },
      ],
      [
        {
          value: "threatC",
          description: null,
          types: [],
          uuid: "3",
          queues: [],
        },
      ],
    ],
    observable: [
      {
        category: { value: "test", description: null, uuid: "1" },
        value: "example",
      },
      {
        category: { value: "test2", description: null, uuid: "2" },
        value: "example2",
      },
    ],
  };
  it("will correctly parse and add any multiselect filters", async () => {
    const formattedFilters = formatNodeFiltersForAPI(
      alertFilters.external,
      MOCK_PARAMS,
    );
    expect(formattedFilters).toEqual({
      limit: 10,
      offset: 10,
      disposition: ["FALSE_POSITIVE", "IGNORE"],
      name: ["Test Name", "Test Name 2"],
      threats: ["threatA,threatB", "threatC"],
      observableTypes: ["testA,testB", "testC"],
      tags: ["tagA,tagB", "tagC"],
      observable: ["test|example", "test2|example2"],
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
        description: "A tag object",
        value: "c2",
        uuid: "uuid1",
        metadataType: "tag",
      },
      {
        description: "A tag object",
        value: "contacted_host",
        uuid: "uuid2",
        metadataType: "tag",
      },
      {
        description: "A tag object",
        value: "from_address",
        uuid: "uuid3",
        metadataType: "tag",
      },
      {
        description: "A tag object",
        value: "recipient",
        uuid: "uuid4",
        metadataType: "tag",
      },
    ]);
  });
});

describe("groupItemsByQueue", () => {
  it("correctly returns an object of items grouped by their 'queues' property", () => {
    const queueA = genericObjectReadFactory({ value: "A" });
    const queueB = genericObjectReadFactory({ value: "B" });
    const queueC = genericObjectReadFactory({ value: "C" });
    const testData: genericQueueableObjectRead[] = [
      { value: "1", queues: [queueA, queueB], uuid: "1", description: null },
      { value: "2", queues: [queueB], uuid: "1", description: null },
      { value: "3", queues: [queueA, queueC], uuid: "1", description: null },
      { value: "5", queues: [queueA], uuid: "1", description: null },
      { value: "6", queues: [queueB], uuid: "1", description: null },
      { value: "7", queues: [queueB, queueC], uuid: "1", description: null },
    ];

    const expected = {
      A: [
        { value: "1", queues: [queueA, queueB], uuid: "1", description: null },
        { value: "3", queues: [queueA, queueC], uuid: "1", description: null },
        { value: "5", queues: [queueA], uuid: "1", description: null },
      ],
      B: [
        { value: "1", queues: [queueA, queueB], uuid: "1", description: null },
        { value: "2", queues: [queueB], uuid: "1", description: null },
        { value: "6", queues: [queueB], uuid: "1", description: null },
        { value: "7", queues: [queueB, queueC], uuid: "1", description: null },
      ],
      C: [
        { value: "3", queues: [queueA, queueC], uuid: "1", description: null },
        { value: "7", queues: [queueB, queueC], uuid: "1", description: null },
      ],
    };

    const result = groupItemsByQueue(testData);
    expect(result).toEqual(expected);
  });
});
