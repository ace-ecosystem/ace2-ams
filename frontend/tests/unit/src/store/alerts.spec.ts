/**
 * @jest-environment node
 */

import Vuex from "vuex";
import alerts from "@/store/alerts";
import { parseAlertSummary } from "@/store/alerts";
import myNock from "@unit/services/api/nock";
import snakecaseKeys from "snakecase-keys";
import { userRead } from "@/models/user";
import { nodeCommentRead } from "@/models/nodeComment";
import { alertSummaryRead } from "@/models/alert";

const actions = alerts.actions;
const mutations = alerts.mutations;

const mockAlertCreate = {
  queue: "default",
  type: "MockType",
  uuid: "uuid1",
  version: "VersionId1",
  eventTime: new Date(0),
  name: "mockAlert",
};

const mockAlert = {
  comments: [],
  description: "A test alert",
  disposition: "",
  dispositionTime: Date(),
  dispositionUser: "",
  eventTime: Date(),
  insertTime: Date(),
  name: "Test Alert",
  owner: "Analyst",
  queue: "Default",
  tags: [],
  tool: "GUI",
  type: "Manual",
  uuid: "uuid1",
};

const mockUser: userRead = {
  defaultAlertQueue: {
    value: "Default",
    description: "queue",
    uuid: "uuid1",
  },
  displayName: "Imma Analyst",
  email: "analyst@company.com",
  enabled: true,
  roles: [{ value: "test_role", description: null, uuid: "uuid1" }],
  timezone: "UTC",
  username: "analyst",
  uuid: "uuid1",
};

const mockComment: nodeCommentRead = {
  insertTime: new Date(0),
  nodeUuid: "uuid1",
  user: mockUser,
  uuid: "uuid1",
  value: "A comment",
};

const mockAPIAlert: alertSummaryRead = {
  comments: [],
  description: "",
  directives: [],
  disposition: null,
  dispositionTime: null,
  dispositionUser: null,
  eventTime: new Date(0),
  eventUuid: null,
  insertTime: new Date(0),
  instructions: null,
  name: "Test Alert",
  owner: null,
  queue: { value: "Default", description: "queue", uuid: "uuid1" },
  tags: [],
  threatActor: null,
  threats: [],
  tool: null,
  toolInstance: null,
  type: { value: "Manual", description: "type", uuid: "uuid1" },
  uuid: "uuid1",
  version: "uuid2",
};

const mockAPIAlertOptionalProperties: alertSummaryRead = {
  comments: [mockComment],
  description: "A test alert",
  directives: [],
  disposition: {
    value: "False Positive",
    description: "fp",
    rank: 1,
    uuid: "uuid1",
  },
  dispositionTime: new Date(0),
  dispositionUser: mockUser,
  eventTime: new Date(0),
  eventUuid: null,
  insertTime: new Date(0),
  instructions: null,
  name: "Test Alert",
  owner: mockUser,
  queue: { value: "Default", description: "queue", uuid: "uuid1" },
  tags: [{ value: "a tag", description: "tag", uuid: "uuid1" }],
  threatActor: null,
  threats: [],
  tool: { value: "GUI", description: null, uuid: "uuid1" },
  toolInstance: null,
  type: { value: "Manual", description: "type", uuid: "uuid1" },
  uuid: "uuid1",
  version: "uuid2",
};

describe("alerts utilities", () => {
  it("will use default values when parsing an API alert object that has missing properties", () => {
    expect(parseAlertSummary(mockAPIAlert)).toStrictEqual({
      comments: [],
      description: "",
      disposition: "OPEN",
      dispositionTime: null,
      dispositionUser: "None",
      eventTime: new Date(0),
      insertTime: new Date(0),
      name: "Test Alert",
      owner: "None",
      queue: "Default",
      tags: [],
      tool: "None",
      type: "Manual",
      uuid: "uuid1",
    });
  });
  it("will use the available values when parsing an API alert object with all optional properties", () => {
    expect(parseAlertSummary(mockAPIAlertOptionalProperties)).toStrictEqual({
      comments: [mockComment],
      description: "A test alert",
      disposition: "False Positive",
      dispositionTime: new Date(0),
      dispositionUser: "Imma Analyst",
      eventTime: new Date(0),
      insertTime: new Date(0),
      name: "Test Alert",
      owner: "Imma Analyst",
      queue: "Default",
      tags: [{ value: "a tag", description: "tag", uuid: "uuid1" }],
      tool: "GUI",
      type: "Manual",
      uuid: "uuid1",
    });
  });
});

describe("alerts Mutations", () => {
  it("will set the openAlert state value to a given alert object", () => {
    const state = {
      openAlert: null,
      visibleQueriedAlerts: [],
      totalAlerts: 0,
    };
    const store = new Vuex.Store({ state, mutations });

    store.commit("SET_OPEN_ALERT", mockAlert);
    expect(state.openAlert).toEqual(mockAlert);
  });
  it("will add a list of queried alerts to the visibleQueriedAlerts list", () => {
    const state = {
      openAlert: null,
      visibleQueriedAlerts: [],
      totalAlerts: 0,
    };
    const store = new Vuex.Store({ state, mutations });

    store.commit("SET_VISIBLE_QUERIED_ALERTS", [mockAlert, mockAlert]);
    expect(state.visibleQueriedAlerts.length).toBe(2);
  });
  it("will set the total alerts to a given number", () => {
    const state = {
      openAlert: null,
      visibleQueriedAlerts: [],
      totalAlerts: 0,
    };
    const store = new Vuex.Store({ state, mutations });

    store.commit("SET_TOTAL_ALERTS", 2);
    expect(state.totalAlerts).toEqual(2);
  });
});

describe("alerts Actions", () => {
  it("will request to create an alert with a given AlertCreate object, and set the openAlert to result on success", async () => {
    const state = {
      openAlert: null,
      visibleQueriedAlerts: [],
      totalAlerts: 0,
    };
    const store = new Vuex.Store({ state, mutations, actions });
    const mockRequest = myNock
      .post("/alert/", JSON.stringify(snakecaseKeys(mockAlertCreate)))
      .reply(200, mockAlert);

    await store.dispatch("createAlert", mockAlertCreate);

    expect(mockRequest.isDone()).toEqual(true);
    expect(state.openAlert).toEqual(mockAlert);
  });

  it("will fetch alert data given an alert ID", async () => {
    const state = {
      openAlert: null,
      visibleQueriedAlerts: [],
      totalAlerts: 0,
    };
    const store = new Vuex.Store({ state, mutations, actions });
    const mockRequest = myNock.get("/alert/uuid1").reply(200, mockAlert);
    await store.dispatch("getSingle", "uuid1");

    expect(mockRequest.isDone()).toEqual(true);

    expect(state.openAlert).toEqual(mockAlert);
  });

  it("will fetch all alerts when getPage is called and no filter options are set", async () => {
    const state = {
      openAlert: null,
      visibleQueriedAlerts: [],
      totalAlerts: 0,
    };
    const store = new Vuex.Store({ state, mutations, actions });
    const mockRequest = myNock
      .get("/alert/")
      .reply(200, { items: [mockAPIAlert, mockAPIAlert], total: 2 });
    await store.dispatch("getPage");

    expect(mockRequest.isDone()).toEqual(true);

    expect(state.openAlert).toBeNull();
    expect(state.totalAlerts).toEqual(2);
    expect(state.visibleQueriedAlerts).toHaveLength(2);
  });

  it("will pass params along when getPage is and pagination options are set", async () => {
    const state = {
      openAlert: null,
      visibleQueriedAlerts: [],
      totalAlerts: 0,
    };
    const store = new Vuex.Store({ state, mutations, actions });
    const mockRequest = myNock
      .get("/alert/?limit=2&offset=0")
      .reply(200, { items: [mockAPIAlert, mockAPIAlert], total: 2 });
    await store.dispatch("getPage", { limit: 2, offset: 0 });

    expect(mockRequest.isDone()).toEqual(true);

    expect(state.openAlert).toBeNull();
    expect(state.totalAlerts).toEqual(2);
    expect(state.visibleQueriedAlerts).toHaveLength(2);
  });

  it("will make a request to update an alert given the UUID and update data upon the updateAlert action", async () => {
    const state = {
      openAlert: null,
      visibleQueriedAlerts: [],
      totalAlerts: 0,
    };
    const store = new Vuex.Store({ state, mutations, actions });
    const mockRequest = myNock.patch("/alert/uuid1").reply(200);
    await store.dispatch("updateAlert", {
      oldAlertUUID: "uuid1",
      updateData: { disposition: "test" },
    });

    expect(mockRequest.isDone()).toEqual(true);
    // None of these should be changed
    expect(state.openAlert).toBeNull();
    expect(state.visibleQueriedAlerts).toEqual([]);
  });

  it("will make multiple reqs to update multiple alerts given a list of UUIDS and update data upon the updateAlerts action", async () => {
    const state = {
      openAlert: null,
      visibleQueriedAlerts: [],
      totalAlerts: 0,
    };
    const store = new Vuex.Store({ state, mutations, actions });
    const mockRequest = myNock
      .patch(/\/alert\/uuid\d/)
      .twice()
      .reply(200);
    await store.dispatch("updateAlerts", {
      oldAlertUUIDs: ["uuid1", "uuid2"],
      updateData: { disposition: "test" },
    });

    expect(mockRequest.isDone()).toEqual(true);
    // None of these should be changed
    expect(state.openAlert).toBeNull();
    expect(state.visibleQueriedAlerts).toEqual([]);
  });

  it("will throw an error when a request fails in any action", async () => {
    const state = {
      openAlert: null,
      visibleQueriedAlerts: [],
      totalAlerts: 0,
    };
    const store = new Vuex.Store({ state, mutations, actions });
    const mockRequest = myNock
      .persist()
      .post(/\/alert\/*/)
      .reply(403, "Bad request :(")
      .get(/\/alert\/*/)
      .reply(403, "Bad request :(")
      .patch(/\/alert\/*/)
      .reply(403, "Bad request :(");

    await expect(store.dispatch("createAlert")).rejects.toEqual(
      new Error("Request failed with status code 403"),
    );
    await expect(store.dispatch("getSingle")).rejects.toEqual(
      new Error("Request failed with status code 403"),
    );
    await expect(
      store.dispatch("updateAlert", {
        oldAlertUUID: "uuid1",
        updateData: { disposition: "test" },
      }),
    ).rejects.toEqual(new Error("Request failed with status code 403"));
    await expect(
      store.dispatch("updateAlerts", {
        oldAlertUUIDs: ["uuid1"],
        updateData: { disposition: "test" },
      }),
    ).rejects.toEqual(new Error("Request failed with status code 403"));

    mockRequest.persist(false); // cleanup persisted nock request
  });
});
