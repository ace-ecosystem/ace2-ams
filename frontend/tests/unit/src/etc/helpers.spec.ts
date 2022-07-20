import { describe, it, expect, vi } from "vitest";
import { alertFilters } from "@/etc/configuration/alerts";
import {
  formatObjectFiltersForAPI,
  parseFilters,
  getAlertLink,
  getAllAlertTags,
  groupItemsByQueue,
  findClosestMatchingString,
  parseAlertSummary,
  prettyPrintDateTime,
  dateParser,
  camelToSnakeCase,
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
import { alertReadFactory, alertSummaryFactory } from "@mocks/alert";
import { userReadFactory } from "@mocks/user";

createTestingPinia({ createSpy: vi.fn, stubActions: false });

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
  it("will skip any unknown filter types", async () => {
    const unknownFilter = {
      name: "unknown",
      label: "Unknown",
      type: "unknown",
    };

    const results = parseFilters({ unknown: "test" }, [
      ...alertFilters.external,
      unknownFilter,
    ]);

    expect(results).toEqual({});
  });

  it("will skip any empty multiselect filters", async () => {
    const observableTypeStore = useObservableTypeStore();
    observableTypeStore.items = [
      { value: "ipv4", description: null, uuid: "1" },
      { value: "file", description: null, uuid: "2" },
      { value: "url", description: null, uuid: "3" },
      { value: "fqdn", description: null, uuid: "4" },
    ];

    const results = parseFilters(
      { observableTypes: " , " },
      alertFilters.external,
    );

    expect(results).toEqual({});
  });

  it("will correctly parse and add any multiselect filters", async () => {
    const observableTypeStore = useObservableTypeStore();
    observableTypeStore.items = [
      { value: "ipv4", description: null, uuid: "1" },
      { value: "file", description: null, uuid: "2" },
      { value: "url", description: null, uuid: "3" },
      { value: "fqdn", description: null, uuid: "4" },
    ];

    const results = parseFilters(
      {
        observableTypes: "ipv4,file,fake",
        notObservableTypes: "url,fqdn,fake",
      },
      alertFilters.external,
    );

    expect(results).toEqual({
      observableTypes: {
        included: [
          [
            { value: "ipv4", description: null, uuid: "1" },
            { value: "file", description: null, uuid: "2" },
          ],
        ],
        notIncluded: [
          [
            { value: "url", description: null, uuid: "3" },
            { value: "fqdn", description: null, uuid: "4" },
          ],
        ],
      },
    });
  });

  it("will correctly parse and add any chips filters", async () => {
    const results = parseFilters(
      { tags: "tagA,tagB", notTags: "tagC,tagD" },
      alertFilters.external,
    );

    expect(results).toEqual({
      tags: { included: [["tagA", "tagB"]], notIncluded: [["tagC", "tagD"]] },
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

    const results = parseFilters(
      { owner: "analystB", notOwner: "analystA" },
      alertFilters.external,
    );

    expect(results).toEqual({
      owner: { included: [mockUserB], notIncluded: [mockUserA] },
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

    const results = parseFilters(
      { owner: "none", notOwner: "none" },
      alertFilters.external,
    );

    expect(results).toEqual({
      owner: {
        included: [{ displayName: "None", username: "none" }],
        notIncluded: [{ displayName: "None", username: "none" }],
      },
    });
  });

  it("will correctly parse and add any nullable select filters (simple)", async () => {
    const dispositionStore = useAlertDispositionStore();
    dispositionStore.items = [];

    const results = parseFilters(
      { disposition: "None", notDisposition: "None" },
      alertFilters.external,
    );

    expect(results).toEqual({
      disposition: {
        included: [{ value: "None" }],
        notIncluded: [{ value: "None" }],
      },
    });
  });

  it("will correctly parse and add any date filters", async () => {
    const results = parseFilters(
      {
        eventTimeBefore:
          "Sat Jan 08 2022 11:31:51 GMT-0500 (Eastern Standard Time)",
        notEventTimeBefore:
          "Sun Jan 09 2022 11:31:51 GMT-0500 (Eastern Standard Time)",
      },
      alertFilters.external,
    );

    expect(results).toEqual({
      eventTimeBefore: {
        included: [new Date("2022-01-08T16:31:51.000Z")],
        notIncluded: [new Date("2022-01-09T16:31:51.000Z")],
      },
    });
  });

  it("will skip any date filters that fail to parse", async () => {
    const results = parseFilters(
      { eventTimeBefore: ["Bad Date"], notEventTimeBefore: ["Other Bad Date"] },
      alertFilters.external,
    );

    expect(results).toEqual({});
  });

  it("will correctly parse and add any input text filters", async () => {
    const results = parseFilters(
      { name: "test name", notName: "test name 2" },
      alertFilters.external,
    );

    expect(results).toEqual({
      name: { included: ["test name"], notIncluded: ["test name 2"] },
    });
  });
  it("will correctly parse and add any catetgorized value filters", async () => {
    const observableTypeStore = useObservableTypeStore();
    observableTypeStore.items = [
      { value: "ipv4", description: null, uuid: "1" },
      { value: "file", description: null, uuid: "2" },
    ];

    const results = parseFilters(
      { observable: "ipv4|1.2.3.4", notObservable: "file|blah.jpg" },
      alertFilters.external,
    );

    expect(results).toEqual({
      observable: {
        included: [
          {
            category: { value: "ipv4", description: null, uuid: "1" },
            value: "1.2.3.4",
          },
        ],
        notIncluded: [
          {
            category: { value: "file", description: null, uuid: "2" },
            value: "blah.jpg",
          },
        ],
      },
    });
  });
  it("will correctly parse and add any combined filters", async () => {
    const observableTypeStore = useObservableTypeStore();
    observableTypeStore.items = [
      { value: "ipv4", description: null, uuid: "1" },
      { value: "file", description: null, uuid: "2" },
      { value: "url", description: null, uuid: "3" },
      { value: "fqdn", description: null, uuid: "4" },
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
        notObservable: "file|blah.jpg",
        notEventTimeBefore:
          "Sun Jan 09 2022 11:31:51 GMT-0500 (Eastern Standard Time)",
        notName: "test name 2",
        notObservableTypes: "url,fqdn,fake",
        notFake: "blah",
        notOwner: "analystA",
        notTags: "tagC,tagD",
      },
      alertFilters.external,
    );

    expect(results).toEqual({
      tags: { included: [["tagA", "tagB"]], notIncluded: [["tagC", "tagD"]] },
      owner: { included: [mockUserB], notIncluded: [mockUserA] },
      observableTypes: {
        included: [
          [
            { value: "ipv4", description: null, uuid: "1" },
            { value: "file", description: null, uuid: "2" },
          ],
        ],
        notIncluded: [
          [
            { value: "url", description: null, uuid: "3" },
            { value: "fqdn", description: null, uuid: "4" },
          ],
        ],
      },
      eventTimeBefore: {
        included: [new Date("2022-01-08T16:31:51.000Z")],
        notIncluded: [new Date("2022-01-09T16:31:51.000Z")],
      },
      name: { included: ["test name"], notIncluded: ["test name 2"] },
      observable: {
        included: [
          {
            category: { value: "ipv4", description: null, uuid: "1" },
            value: "1.2.3.4",
          },
        ],
        notIncluded: [
          {
            category: { value: "file", description: null, uuid: "2" },
            value: "blah.jpg",
          },
        ],
      },
    });
  });
  it("will correctly parse and add any combined filters with multiple filter values", async () => {
    const observableTypeStore = useObservableTypeStore();
    observableTypeStore.items = [
      { value: "ipv4", description: null, uuid: "1" },
      { value: "file", description: null, uuid: "2" },
      { value: "url", description: null, uuid: "3" },
      { value: "fqdn", description: null, uuid: "4" },
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

    const mockUserC: userRead = {
      defaultAlertQueue: { description: null, uuid: "1", value: "default" },
      defaultEventQueue: { description: null, uuid: "1", value: "default" },
      displayName: "Test Analyst",
      email: "analyst@test.com",
      enabled: true,
      roles: [],
      timezone: "UTC",
      training: false,
      username: "analystC",
      uuid: "1",
    };

    const mockUserD: userRead = {
      defaultAlertQueue: { description: null, uuid: "1", value: "default" },
      defaultEventQueue: { description: null, uuid: "1", value: "default" },
      displayName: "Test Analyst",
      email: "analyst@test.com",
      enabled: true,
      roles: [],
      timezone: "UTC",
      training: false,
      username: "analystD",
      uuid: "1",
    };

    const userStore = useUserStore();
    userStore.items = [mockUserA, mockUserB, mockUserC, mockUserD];

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
        notObservable: ["file|blah.jpg", "file|blah.png"],
        notEventTimeBefore: [
          "Sat Jan 09 2022 11:31:51 GMT-0500 (Eastern Standard Time)",
          "Sat Jan 11 2022 11:31:51 GMT-0500 (Eastern Standard Time)",
        ],
        notName: ["test name 3", "test name 4"],
        notObservableTypes: ["url,fqdn,fake", "url"],
        notFake: ["blah"],
        notOwner: ["analystC", "analystD"],
        notTags: ["tagE,tagF", "tagG,tagH"],
      },
      alertFilters.external,
    );

    expect(results).toEqual({
      tags: {
        included: [
          ["tagA", "tagB"],
          ["tagC", "tagD"],
        ],
        notIncluded: [
          ["tagE", "tagF"],
          ["tagG", "tagH"],
        ],
      },
      owner: {
        included: [mockUserB, mockUserA],
        notIncluded: [mockUserC, mockUserD],
      },
      observableTypes: {
        included: [
          [
            { value: "ipv4", description: null, uuid: "1" },
            { value: "file", description: null, uuid: "2" },
          ],
          [{ value: "ipv4", description: null, uuid: "1" }],
        ],
        notIncluded: [
          [
            { value: "url", description: null, uuid: "3" },
            { value: "fqdn", description: null, uuid: "4" },
          ],
          [{ value: "url", description: null, uuid: "3" }],
        ],
      },
      eventTimeBefore: {
        included: [
          new Date("2022-01-08T16:31:51.000Z"),
          new Date("2022-01-10T16:31:51.000Z"),
        ],
        notIncluded: [
          new Date("2022-01-09T16:31:51.000Z"),
          new Date("2022-01-11T16:31:51.000Z"),
        ],
      },
      name: {
        included: ["test name", "test name 2"],
        notIncluded: ["test name 3", "test name 4"],
      },
      observable: {
        included: [
          {
            category: { value: "ipv4", description: null, uuid: "1" },
            value: "1.2.3.4",
          },
          {
            category: { value: "ipv4", description: null, uuid: "1" },
            value: "5.6.7.8",
          },
        ],
        notIncluded: [
          {
            category: { value: "file", description: null, uuid: "2" },
            value: "blah.jpg",
          },
          {
            category: { value: "file", description: null, uuid: "2" },
            value: "blah.png",
          },
        ],
      },
    });
  });
});

describe("formatObjectFiltersForAPI", () => {
  const MOCK_PARAMS: alertFilterParams = {
    limit: 10,
    offset: 10,
    name: {
      included: ["Test Name", "Test Name 2"],
      notIncluded: ["Test Name 3", "Test Name 4"],
    },
    disposition: {
      included: [
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
      notIncluded: [
        {
          rank: 3,
          description: null,
          uuid: "3",
          value: "DELIVERY",
        },
        {
          rank: 4,
          description: null,
          uuid: "4",
          value: "WEAPONIZATION",
        },
      ],
    },
    observableTypes: {
      included: [
        [
          { value: "testA", description: null, uuid: "1" },
          { value: "testB", description: null, uuid: "2" },
        ],
        [{ value: "testC", description: null, uuid: "3" }],
      ],
      notIncluded: [
        [
          { value: "testC", description: null, uuid: "3" },
          { value: "testE", description: null, uuid: "4" },
        ],
        [{ value: "testF", description: null, uuid: "5" }],
      ],
    },
    tags: {
      included: [["tagA", "tagB"], ["tagC"]],
      notIncluded: [["tagD", "tagE"], ["tagF"]],
    },
    threats: {
      included: [
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
      notIncluded: [
        [
          {
            value: "threatD",
            description: null,
            types: [],
            uuid: "4",
            queues: [],
          },
          {
            value: "threatE",
            description: null,
            types: [],
            uuid: "5",
            queues: [],
          },
        ],
        [
          {
            value: "threatF",
            description: null,
            types: [],
            uuid: "6",
            queues: [],
          },
        ],
      ],
    },
    observable: {
      included: [
        {
          category: { value: "test", description: null, uuid: "1" },
          value: "example",
        },
        {
          category: { value: "test2", description: null, uuid: "2" },
          value: "example2",
        },
      ],
      notIncluded: [
        {
          category: { value: "test", description: null, uuid: "3" },
          value: "example3",
        },
        {
          category: { value: "test2", description: null, uuid: "4" },
          value: "example4",
        },
      ],
    },
    insertTimeBefore: {
      included: [
        new Date("2020-01-01T00:00:00.000Z"),
        new Date("2020-01-02T00:00:00.000Z"),
      ],
      notIncluded: [
        new Date("2020-02-01T00:00:00.000Z"),
        new Date("2020-02-02T00:00:00.000Z"),
      ],
    },
  };
  it("will correctly format filters for each given input type (select, text, multiselect, chips, categorizedValue, date)", async () => {
    const formattedFilters = formatObjectFiltersForAPI(
      alertFilters.external,
      MOCK_PARAMS,
    );
    expect(formattedFilters).toEqual({
      limit: 10,
      offset: 10,
      disposition: ["FALSE_POSITIVE", "IGNORE"],
      notDisposition: ["DELIVERY", "WEAPONIZATION"],
      name: ["Test Name", "Test Name 2"],
      notName: ["Test Name 3", "Test Name 4"],
      threats: ["threatA,threatB", "threatC"],
      notThreats: ["threatD,threatE", "threatF"],
      observableTypes: ["testA,testB", "testC"],
      notObservableTypes: ["testC,testE", "testF"],
      tags: ["tagA,tagB", "tagC"],
      notTags: ["tagD,tagE", "tagF"],
      observable: ["test|example", "test2|example2"],
      notObservable: ["test|example3", "test2|example4"],
      insertTimeBefore: ["2020-01-01T00:00:00", "2020-01-02T00:00:00"],
      notInsertTimeBefore: ["2020-02-01T00:00:00", "2020-02-02T00:00:00"],
    });
  });
});

describe("getAlertLink", () => {
  it("getAlertLink correctly generates an alert link given an alert object", () => {
    const result = getAlertLink(mockAlertTreeRead);
    expect(result).toEqual("/alert/testAlertUuid");
  });
});

describe("getAllAlertTags", () => {
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

describe("parseAlertSummary", () => {
  it("correctly generates an alert summary given an alertRead object", () => {
    const alertA = alertReadFactory({
      tool: null,
      toolInstance: null,
    });
    const alertB = alertReadFactory({
      description: "Test Description",
      disposition: {
        rank: 0,
        ...genericObjectReadFactory({ value: "FALSE_POSITIVE" }),
      },
      dispositionTime: "2020-01-01T00:00:00.000Z",
      dispositionUser: userReadFactory(),
      eventTime: "2020-01-01T00:00:00.000Z",
      eventUuid: "testEventUuid",
      insertTime: "2020-01-01T00:00:00.000Z",
      owner: userReadFactory(),
      ownershipTime: "2020-01-01T00:00:00.000Z",
      tool: genericObjectReadFactory({ value: "Test Tool" }),
      toolInstance: genericObjectReadFactory({ value: "Test Tool Instance" }),
    });

    const expectedA = alertSummaryFactory({
      tool: "None",
      toolInstance: "None",
    });
    const expectedB = alertSummaryFactory({
      description: "Test Description",
      disposition: "FALSE_POSITIVE",
      dispositionTime: "1/1/2020, 12:00:00 AM UTC",
      dispositionWithUserAndTime:
        "FALSE_POSITIVE by Test Analyst @ 1/1/2020, 12:00:00 AM UTC",
      dispositionUser: "Test Analyst",
      eventTime: "1/1/2020, 12:00:00 AM UTC",
      eventUuid: "testEventUuid",
      insertTime: "1/1/2020, 12:00:00 AM UTC",
      owner: "Test Analyst",
      ownerWithTime: "Test Analyst @ 1/1/2020, 12:00:00 AM UTC",
      ownershipTime: "1/1/2020, 12:00:00 AM UTC",
      tool: "Test Tool",
      toolInstance: "Test Tool Instance",
    });

    const resultA = parseAlertSummary(alertA);
    const resultB = parseAlertSummary(alertB);

    expect(resultA).toEqual(expectedA);
    expect(resultB).toEqual(expectedB);
  });
});

describe("findClosestMatchingString", () => {
  const stringArr = ["a - b", "a - b - c", "a", "b - c", "b", "c"];

  it.each([
    [stringArr, "a - b - c", "a - b - c"],
    [stringArr, "a - b - d", "a - b"],
    [stringArr, "a - d", "a"],
    [stringArr, "d", null],
  ])(
    "correctly returns closest matching string",
    (strings, searchString, result) => {
      const res = findClosestMatchingString(strings, searchString);
      expect(res).toEqual(result);
    },
  );
});

describe("prettyPrintDateTime", () => {
  it.each([
    [null, undefined, "None"],
    [
      new Date("2020-01-02T00:00:00.000Z"),
      undefined,
      "1/2/2020, 12:00:00 AM UTC",
    ],
    ["2020-01-02T00:00:00.000Z", undefined, "1/2/2020, 12:00:00 AM UTC"],
    ["invalid", undefined, "invalid"],
  ])(
    "correctly returns closest matching string",
    (datetime, timezone, result) => {
      const res = prettyPrintDateTime(datetime, timezone);
      expect(res).toEqual(result);
    },
  );
});

describe("dateParser", () => {
  it.each([
    ["key", "2020-01-02T00:00:00.000Z", new Date("1/2/2020, 12:00:00 AM UTC")],
    ["key", "invalid", "invalid"],
  ])("correctly returns closest matching string", (key, value, result) => {
    const res = dateParser(key, value);
    expect(res).toEqual(result);
  });
});

describe("camelToSnakeCase", () => {
  it.each([
    ["single", "single"],
    ["doubleWord", "double_word"],
  ])("correctly returns closest matching string", (string, result) => {
    const res = camelToSnakeCase(string);
    expect(res).toEqual(result);
  });
});
