import { alertFilters } from "@/etc/constants";
import { formatNodeFiltersForAPI, parseFilters } from "@/etc/helpers";
import { alertFilterParams } from "@/models/alert";
import { userRead } from "@/models/user";
import { useObservableTypeStore } from "@/stores/observableType";
import { useUserStore } from "@/stores/user";
import { createTestingPinia } from "@pinia/testing";

describe("parseFilters", () => {
  createTestingPinia();
  it("will correctly parse and add any multiselect filters", async () => {
    const observableTypeStore = useObservableTypeStore();
    observableTypeStore.items = [
      { value: "ipv4", description: null, uuid: "1" },
      { value: "file", description: null, uuid: "2" },
    ];

    const results = parseFilters(
      { observableTypes: "ipv4,file,fake" },
      alertFilters,
    );

    expect(results).toEqual({
      observableTypes: [
        { value: "ipv4", description: null, uuid: "1" },
        { value: "file", description: null, uuid: "2" },
      ],
    });
  });

  it("will correctly parse and add any chips filters", async () => {
    const results = parseFilters({ tags: "tagA,tagB" }, alertFilters);

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

    const results = parseFilters({ owner: "analystB" }, alertFilters);

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
      alertFilters,
    );

    expect(results).toEqual({
      eventTimeBefore: new Date("2022-01-08T16:31:51.000Z"),
    });
  });

  it("will skip any date filters that fail to parse", async () => {
    const results = parseFilters({ eventTimeBefore: "Bad Date" }, alertFilters);

    expect(results).toEqual({});
  });

  it("will correctly parse and add any input text filters", async () => {
    const results = parseFilters({ name: "test name" }, alertFilters);

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

    const results = parseFilters({ observable: "ipv4|1.2.3.4" }, alertFilters);

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
      alertFilters,
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
    const formattedFilters = formatNodeFiltersForAPI(alertFilters, MOCK_PARAMS);
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
});
