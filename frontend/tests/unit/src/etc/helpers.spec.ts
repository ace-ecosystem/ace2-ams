import { alertFilters } from "../../../../src/etc/configuration/alerts";
import {
  formatNodeFiltersForAPI,
  parseFilters,
  getAlertLink,
  getAllAlertTags,
} from "../../../../src/etc/helpers";
import { mockAlertTreeReadA } from "../../../mocks/alert";
import { alertFilterParams } from "../../../../src/models/alert";
import { userRead } from "../../../../src/models/user";
import { useObservableTypeStore } from "../../../../src/stores/observableType";
import { useUserStore } from "../../../../src/stores/user";
import { createTestingPinia } from "@pinia/testing";
import { expect } from "vitest";
import { vi } from "vitest";
import { setUserDefaults } from "../../../../src/etc/helpers";
import { useAuthStore } from "../../../../src/stores/auth";
import { useCurrentUserSettingsStore } from "../../../../src/stores/currentUserSettings";
import { useFilterStore } from "../../../../src/stores/filter";
import { userReadFactory } from "../../../mocks/user";
import { genericObjectReadFactory } from "../../../mocks/genericObject";

describe("parseFilters", () => {
  createTestingPinia({ createSpy: vi.fn });
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

  it("getAlertLink correctly generates an alert link given an alert object", () => {
    const result = getAlertLink(mockAlertTreeReadA);
    expect(result).toEqual("/alert/uuid1");
  });

  it("getAllAlertTags formats a given alert's tags into a sorted and dedup'd list of tags", () => {
    const result = getAllAlertTags(mockAlertTreeReadA);
    expect(result).toEqual([
      {
        description: null,
        value: "c2",
        uuid: "a0b2d514-c544-4a8f-a059-b6151b9f1dd6",
      },
      {
        description: null,
        value: "contacted_host",
        uuid: "3c1ca637-48d1-4d47-aeee-0962bc32d96d",
      },
      {
        description: null,
        value: "from_address",
        uuid: "f9081b70-c2bf-4a7d-ba90-a675e8a929d2",
      },
      {
        description: null,
        value: "recipient",
        uuid: "c5d3321d-883c-4772-b511-489273e13fde",
      },
    ]);
  });
});

describe("setUserDefaults", () => {
  const authStore = useAuthStore();
  const filterStore = useFilterStore();
  const currentUserSettingsStore = useCurrentUserSettingsStore();

  const alertQueue = genericObjectReadFactory({ value: "alertQueue" });
  const eventQueue = genericObjectReadFactory({ value: "eventQueue" });

  beforeEach(() => {
    authStore.user = userReadFactory({
      defaultAlertQueue: alertQueue,
      defaultEventQueue: eventQueue,
    });
    filterStore.$reset();
    currentUserSettingsStore.$reset();
  });

  it("will do nothing when there is no authStore user set", () => {
    authStore.user = null;
    setUserDefaults();
    expect(currentUserSettingsStore.preferredEventQueue).toBeNull();
    expect(currentUserSettingsStore.preferredAlertQueue).toBeNull();

    expect(filterStore.events).toEqual({});
    expect(filterStore.alerts).toEqual({});
  });

  it("will correctly set all user defaults when nodeType == 'all'", () => {
    setUserDefaults();
    expect(currentUserSettingsStore.preferredEventQueue).toEqual(eventQueue);
    expect(currentUserSettingsStore.preferredAlertQueue).toEqual(alertQueue);
    expect(filterStore.events).toEqual({
      queue: eventQueue,
    });
    expect(filterStore.alerts).toEqual({
      queue: alertQueue,
    });
  });
  it("will correctly set event user defaults when nodeType == 'events'", () => {
    setUserDefaults("events");
    expect(currentUserSettingsStore.preferredEventQueue).toEqual(eventQueue);
    expect(currentUserSettingsStore.preferredAlertQueue).toBeNull();
    expect(filterStore.events).toEqual({
      queue: eventQueue,
    });
    expect(filterStore.alerts).toEqual({});
  });
  it("will correctly set alert user defaults when nodeType == 'alerts'", () => {
    setUserDefaults("alerts");
    expect(currentUserSettingsStore.preferredEventQueue).toBeNull();
    expect(currentUserSettingsStore.preferredAlertQueue).toEqual(alertQueue);
    expect(filterStore.events).toEqual({});
    expect(filterStore.alerts).toEqual({
      queue: alertQueue,
    });
  });

  it("will not set any user defaults when nodeType is unknown", () => {
    authStore.user = null;
    setUserDefaults("unknown");
    expect(currentUserSettingsStore.preferredEventQueue).toBeNull();
    expect(currentUserSettingsStore.preferredAlertQueue).toBeNull();

    expect(filterStore.events).toEqual({});
    expect(filterStore.alerts).toEqual({});
  });
});
