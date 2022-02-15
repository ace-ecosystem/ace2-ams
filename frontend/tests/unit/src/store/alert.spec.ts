/**
 * @jest-environment node
 */

import myNock from "@unit/services/api/nock";
import snakecaseKeys from "snakecase-keys";
import { alertCreate } from "@/models/alert";
import { useAlertStore } from "@/stores/alert";
import { createCustomPinia } from "@unit/helpers";
import { mockAlertReadA, mockAlertReadASummary } from "../../../mocks/alert";

createCustomPinia();

const store = useAlertStore();

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
describe("alert Actions", () => {
  beforeEach(() => {
    store.$reset();
  });

  it("will have openAlertSummary return the current openAlert summary if there is one, otherwise it will return null", () => {
    expect(store.openAlertSummary).toBeNull();
    store.openAlert = mockAlertReadA;
    expect(store.openAlertSummary).toEqual(mockAlertReadASummary);
  });

  it("will request to create an alert with a given AlertCreate object, and set the openAlert to result on success", async () => {
    const mockRequest = myNock
      .post("/alert/", JSON.stringify(snakecaseKeys(mockAlertCreate)))
      .reply(200, mockAlert);

    await store.create(mockAlertCreate);

    expect(mockRequest.isDone()).toEqual(true);
    expect(store.openAlert).toEqual(mockAlert);
  });

  it("will fetch alert data given an alert ID", async () => {
    const mockRequest = myNock.get("/alert/uuid1").reply(200, mockAlert);
    await store.read("uuid1");

    expect(mockRequest.isDone()).toEqual(true);

    expect(store.openAlert).toEqual(mockAlert);
  });

  it("will make a request to update an alert given the UUID and update data upon the updateAlert action", async () => {
    const mockRequest = myNock.patch("/alert/").reply(200);
    await store.update([{ uuid: "uuid1", disposition: "test" }]);

    expect(mockRequest.isDone()).toEqual(true);
    // None of these should be changed
    expect(store.openAlert).toBeNull();
  });

  it("will throw an error when a request fails in any action", async () => {
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
      store.update([{ uuid: "uuid1", disposition: "test" }]),
    ).rejects.toEqual(new Error("Request failed with status code 403"));

    mockRequest.persist(false); // cleanup persisted nock request
  });
});
