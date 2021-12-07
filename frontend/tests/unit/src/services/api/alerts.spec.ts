/**
 * @jest-environment node
 */

import { alertCreate, alertFilterParams, alertUpdate } from "@/models/alert";
import { Alert } from "@/services/api/alerts";
import myNock from "@unit/services/api/nock";

const MOCK_ALERT_CREATE: alertCreate = {
  name: "Test",
  queue: "Default",
  type: "test",
  observableInstances: [],
};
const MOCK_ALERT_UPDATE: alertUpdate = { version: "test" };
const MOCK_PARAMS: alertFilterParams = {
  limit: 10,
  offset: 10,
  name: "Test Name",
  observableTypes: ["testA", "testB"],
  tags: ["tagA", "tagB"],
  threats: ["threatA", "threatB"],
  observable: { category: "test", value: "example" },
};

describe("Alert calls", () => {
  const api = Alert;

  it("will make a post to the /alert endpoint with alertCreate data when 'create' is called", async () => {
    myNock
      .post("/alert/")
      .reply(200, "Create successful", {
        "content-location": "http://test_app.com:1234/newItem",
      })
      .get("/newItem")
      .reply(200, "Read successful");
    const res = await api.create(MOCK_ALERT_CREATE);
    expect(res).toEqual("Read successful");
  });

  it("will not get the created object when 'create' is called with getAfterCreate set to false", async () => {
    myNock.post("/alert/").reply(200, "Create successful", {
      "content-location": "http://test_app.com:1234/newItem",
    });
    const res = await api.create(MOCK_ALERT_CREATE, false);
    expect(res).toEqual("Create successful");
  });

  it("will make a get request to the /alert/{uuid} endpoint when 'read' is called with a given UUID", async () => {
    myNock.get("/alert/uuid").reply(200, "Read successful");
    const res = await api.read("uuid");
    expect(res).toEqual("Read successful");
  });

  it("will make a get request to the /alert/ endpoint when 'readPage' is called properly formatted params", async () => {
    myNock
      .get(
        "/alert/?limit=10&offset=10&name=Test+Name&observable_types=testA,testB&tags=tagA,tagB&threats=threatA,threatB&observable=test%7Cexample",
      )
      .reply(200, "Read successful");
    const res = await api.readPage(MOCK_PARAMS);
    expect(res).toEqual("Read successful");
  });

  it("will make a patch request to the /alert/{uuid} endpoint when 'update' is called with a given UUID and update data", async () => {
    myNock.patch("/alert/uuid").reply(200, "Update successful");
    const res = await api.update("uuid", MOCK_ALERT_UPDATE);
    expect(res).toEqual("Update successful");
  });
});
