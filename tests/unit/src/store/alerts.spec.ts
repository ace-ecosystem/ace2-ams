/**
 * @jest-environment node
 */

import Vuex from "vuex";
import alerts from "@/store/alerts";
import myNock from "@unit/services/api/nock";
import { AlertRead } from "@/models/alert";
import snakecaseKeys from "snakecase-keys";
const actions = alerts.actions;
const mutations = alerts.mutations;

const mockAlertCreate = {
  queue: "default",
  type: "MockType",
  uuid: "uuid1",
  version: "VersionId1",
  eventTime: new Date(0),
  name: "MockAlert",
};

const mockAlertRead = {
  analysis: {},
  insertTime: new Date(0).toDateString(),
  queue: "default",
  type: "MockType",
  uuid: "uuid1",
  comments: [],
  directives: [],
  threats: [],
  tags: [],
  version: "VersionId1",
  eventTime: new Date(0).toDateString(),
  instructions: "MockInstructions",
  name: "MockAlert",
};

describe("alerts Mutations", () => {
  it("will set the openAlert state value to a given alert object", () => {
    const queriedAlerts: AlertRead[] = [];
    const state = {
      openAlert: null,
      lastQueriedAlertsTime: null,
      queriedAlerts: queriedAlerts,
    };
    const store = new Vuex.Store({ state, mutations });

    store.commit("SET_OPEN_ALERT", mockAlertRead);
    expect(state.openAlert).toEqual(mockAlertRead);
  });
  it("will add a list of queried alerts to the queriedAlerts list", () => {
    const queriedAlerts: AlertRead[] = [];
    const state = {
      openAlert: null,
      lastQueriedAlertsTime: null,
      queriedAlerts: queriedAlerts,
    };
    const store = new Vuex.Store({ state, mutations });

    store.commit("SET_QUERIED_ALERTS", [mockAlertRead, mockAlertRead]);
    expect(state.queriedAlerts.length).toBe(2);
  });
  it("will set the lastGetAll timestamp to the current time", () => {
    const queriedAlerts: AlertRead[] = [];
    const state = {
      openAlert: null,
      lastQueriedAlertsTime: null,
      queriedAlerts: queriedAlerts,
    };
    const store = new Vuex.Store({ state, mutations });

    const before_time = new Date().getTime();
    store.commit("SET_QUERY_TIMESTAMP");
    const after_time = new Date().getTime();
    expect(state.lastQueriedAlertsTime).toBeGreaterThanOrEqual(before_time);
    expect(state.lastQueriedAlertsTime).toBeLessThanOrEqual(after_time);
  });
});

describe("alerts Actions", () => {
  it("will request to create an alert with a given AlertCreate object, and set the openAlert to result on success", async () => {
    const queriedAlerts: AlertRead[] = [];
    const state = {
      openAlert: null,
      lastQueriedAlertsTime: null,
      queriedAlerts: queriedAlerts,
    };
    const store = new Vuex.Store({ state, mutations, actions });
    const mockRequest = myNock
      .post("/alert/", JSON.stringify(snakecaseKeys(mockAlertCreate)))
      .reply(200, mockAlertRead);

    await store.dispatch("createAlert", mockAlertCreate);

    expect(mockRequest.isDone()).toEqual(true);
    expect(state.openAlert).toEqual(mockAlertRead);
  });

  it("will make fetch alert data given an alert ID", async () => {
    const queriedAlerts: AlertRead[] = [];
    const state = {
      openAlert: null,
      lastQueriedAlertsTime: null,
      queriedAlerts: queriedAlerts,
    };
    const store = new Vuex.Store({ state, mutations, actions });
    const mockRequest = myNock.get("/alert/uuid1").reply(200, mockAlertRead);
    await store.dispatch("openAlert", "uuid1");

    expect(mockRequest.isDone()).toEqual(true);

    expect(state.openAlert).toEqual(mockAlertRead);
  });
  it("will make a request to update an alert given the UUID and update data upon the updateAlert action", async () => {
    const queriedAlerts: AlertRead[] = [];
    const state = {
      openAlert: null,
      lastQueriedAlertsTime: null,
      queriedAlerts: queriedAlerts,
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
    expect(state.queriedAlerts).toEqual(queriedAlerts);
    expect(state.lastQueriedAlertsTime).toBeNull();
  });

  it("will make multiple reqs to update multiple alerts given a list of UUIDS and update data upon the updateAlerts action", async () => {
    const queriedAlerts: AlertRead[] = [];
    const state = {
      openAlert: null,
      lastQueriedAlertsTime: null,
      queriedAlerts: queriedAlerts,
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
    expect(state.queriedAlerts).toEqual(queriedAlerts);
    expect(state.lastQueriedAlertsTime).toBeNull();
  });

  it("will throw an error when a request fails in any action", async () => {
    const queriedAlerts: AlertRead[] = [];
    const state = {
      openAlert: null,
      lastQueriedAlertsTime: null,
      queriedAlerts: queriedAlerts,
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
    await expect(store.dispatch("openAlert")).rejects.toEqual(
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
