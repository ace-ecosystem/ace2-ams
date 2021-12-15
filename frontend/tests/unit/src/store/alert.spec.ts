/**
 * @jest-environment node
 */

import myNock from "@unit/services/api/nock";
import snakecaseKeys from "snakecase-keys";
import { userRead } from "@/models/user";
import { nodeCommentRead } from "@/models/nodeComment";
import { alertCreate, alertRead } from "@/models/alert";
import { useAlertStore } from "@/stores/alert";
import { createTestingPinia } from "@pinia/testing";

createTestingPinia();

const mockAlertCreate: alertCreate = {
  queue: "default",
  type: "MockType",
  uuid: "uuid1",
  version: "VersionId1",
  eventTime: new Date(0),
  name: "mockAlert",
  observables: [{ type: "ipv4", value: "127.0.0.1" }],
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

const mockAPIAlert: alertRead = {
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

const mockAPIAlertOptionalProperties: alertRead = {
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

// TODO: Move to alertTable store tests
// describe("alerts utilities", () => {
//   it("will use default values when parsing an API alert object that has missing properties", () => {
//     expect(parseAlertSummary(mockAPIAlert)).toStrictEqual({
//       comments: [],
//       description: "",
//       disposition: "OPEN",
//       dispositionTime: null,
//       dispositionUser: "None",
//       eventTime: new Date(0),
//       insertTime: new Date(0),
//       name: "Test Alert",
//       owner: "None",
//       queue: "Default",
//       tags: [],
//       tool: "None",
//       type: "Manual",
//       uuid: "uuid1",
//     });
//   });

//   it("will use the available values when parsing an API alert object with all optional properties", () => {
//     expect(parseAlertSummary(mockAPIAlertOptionalProperties)).toStrictEqual({
//       comments: [mockComment],
//       description: "A test alert",
//       disposition: "False Positive",
//       dispositionTime: new Date(0),
//       dispositionUser: "Imma Analyst",
//       eventTime: new Date(0),
//       insertTime: new Date(0),
//       name: "Test Alert",
//       owner: "Imma Analyst",
//       queue: "Default",
//       tags: [{ value: "a tag", description: "tag", uuid: "uuid1" }],
//       tool: "GUI",
//       type: "Manual",
//       uuid: "uuid1",
//     });
//   });
// });

describe("alert Actions", () => {
  it("will request to create an alert with a given AlertCreate object, and set the openAlert to result on success", async () => {
    const store = useAlertStore();
    const mockRequest = myNock
      .post("/alert/", JSON.stringify(snakecaseKeys(mockAlertCreate)))
      .reply(200, mockAlert);

    await store.create(mockAlertCreate);

    expect(mockRequest.isDone()).toEqual(true);
    expect(store.openAlert).toEqual(mockAlert);
  });

  it("will fetch alert data given an alert ID", async () => {
    const store = useAlertStore();
    const mockRequest = myNock.get("/alert/uuid1").reply(200, mockAlert);
    await store.read("uuid1");

    expect(mockRequest.isDone()).toEqual(true);

    expect(store.openAlert).toEqual(mockAlert);
  });

  // TODO: Move to alertTable store tests
  // it("will fetch all alerts when getPage is called and no filter options are set", async () => {
  //   const store = useAlertStore();
  //   const mockRequest = myNock
  //     .get("/alert/")
  //     .reply(200, { items: [mockAPIAlert, mockAPIAlert], total: 2 });
  //   await store.dispatch("getPage");

  //   expect(mockRequest.isDone()).toEqual(true);

  //   expect(state.openAlert).toBeNull();
  //   expect(state.totalAlerts).toEqual(2);
  //   expect(state.visibleQueriedAlerts).toHaveLength(2);
  // });

  // TODO: Move to alertTable store tests
  // it("will pass params along when getPage is called and pagination options are set", async () => {
  //   const state = {
  //     openAlert: null,
  //     visibleQueriedAlerts: [],
  //     totalAlerts: 0,
  //   };
  //   const store = new Vuex.Store({ state, mutations, actions });
  //   const mockRequest = myNock
  //     .get("/alert/?limit=2&offset=0")
  //     .reply(200, { items: [mockAPIAlert, mockAPIAlert], total: 2 });
  //   await store.dispatch("getPage", { limit: 2, offset: 0 });

  //   expect(mockRequest.isDone()).toEqual(true);

  //   expect(state.openAlert).toBeNull();
  //   expect(state.totalAlerts).toEqual(2);
  //   expect(state.visibleQueriedAlerts).toHaveLength(2);
  // });

  // TODO: Move to alertTable store tests
  // it("will pass params along when getPage is called and sort options are set", async () => {
  //   const state = {
  //     openAlert: null,
  //     visibleQueriedAlerts: [],
  //     totalAlerts: 0,
  //   };
  //   const store = new Vuex.Store({ state, mutations, actions });
  //   const mockRequest = myNock
  //     .get("/alert/?sort=event_time%7Casc")
  //     .reply(200, { items: [mockAPIAlert, mockAPIAlert], total: 2 });
  //   await store.dispatch("getPage", { sort: "event_time|asc" });

  //   expect(mockRequest.isDone()).toEqual(true);

  //   expect(state.openAlert).toBeNull();
  //   expect(state.totalAlerts).toEqual(2);
  //   expect(state.visibleQueriedAlerts).toHaveLength(2);
  // });

  it("will make a request to update an alert given the UUID and update data upon the updateAlert action", async () => {
    const state = {
      openAlert: null,
      visibleQueriedAlerts: [],
      totalAlerts: 0,
    };
    const store = useAlertStore();
    const mockRequest = myNock.patch("/alert/uuid1").reply(200);
    await store.update("uuid1", { disposition: "test", version: "1" });

    expect(mockRequest.isDone()).toEqual(true);
    // None of these should be changed
    expect(state.openAlert).toBeNull();
    expect(state.visibleQueriedAlerts).toEqual([]);
  });

  it("will make multiple reqs to update multiple alerts given a list of UUIDS and update data upon the updateAlerts action", async () => {
    const store = useAlertStore();
    const mockRequest = myNock
      .patch(/\/alert\/uuid\d/)
      .twice()
      .reply(200);
    await store.updateMultiple(["uuid1", "uuid2"], {
      disposition: "test",
      version: "1",
    });

    expect(mockRequest.isDone()).toEqual(true);
    // None of these should be changed
    expect(store.openAlert).toBeNull();
  });

  it("will throw an error when a request fails in any action", async () => {
    const store = useAlertStore();
    const mockRequest = myNock
      .persist()
      .post(/\/alert\/*/)
      .reply(403, "Bad request :(")
      .get(/\/alert\/*/)
      .reply(403, "Bad request :(")
      .patch(/\/alert\/*/)
      .reply(403, "Bad request :(");

    await expect(store.create(mockAlertCreate)).rejects.toEqual(
      new Error("Request failed with status code 403"),
    );

    await expect(store.read("uuid1")).rejects.toEqual(
      new Error("Request failed with status code 403"),
    );

    await expect(
      store.update("uuid1", { disposition: "test", version: "1" }),
    ).rejects.toEqual(new Error("Request failed with status code 403"));

    await expect(
      store.updateMultiple(["uuid1", "uuid2"], {
        disposition: "test",
        version: "1",
      }),
    ).rejects.toEqual(new Error("Request failed with status code 403"));

    mockRequest.persist(false); // cleanup persisted nock request
  });
});
