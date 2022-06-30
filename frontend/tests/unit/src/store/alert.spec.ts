import { describe, it, beforeEach, expect } from "vitest";
import myNock from "@unit/services/api/nock";
import snakecaseKeys from "snakecase-keys";
import { useAlertStore } from "@/stores/alert";
import { createCustomPinia } from "@tests/unitHelpers";
import { observableReadFactory } from "@mocks/observable";

import {
  alertCreateFactory,
  alertTreeReadFactory,
  alertReadFactory,
  alertSummaryFactory,
} from "@mocks/alert";

createCustomPinia();

const mockAlertTree = alertTreeReadFactory();
const mockAlert = alertReadFactory();
const mockAlertCreate = alertCreateFactory();
const mockAlertSummary = alertSummaryFactory();
const mockObservable = observableReadFactory();

const store = useAlertStore();

describe("alert Actions", () => {
  beforeEach(() => {
    store.$reset();
  });

  it("will have openAlertSummary return the current opensummary if there is one, otherwise it will return null", () => {
    expect(store.openAlertSummary).toStrictEqual(null);
    store.open = mockAlertTree;
    expect(store.openAlertSummary).toEqual(mockAlertSummary);
  });

  it("will request to create an alert with a given AlertCreate object, and set the opento result on success", async () => {
    const mockRequest = myNock
      .post("/alert/", JSON.stringify(snakecaseKeys(mockAlertCreate)))
      .reply(200, mockAlert);

    await store.create(mockAlertCreate);

    expect(mockRequest.isDone()).toEqual(true);
    expect(store.open).toEqual(JSON.parse(JSON.stringify(mockAlert)));
  });

  it("will fetch alert and observable data given an alert ID", async () => {
    const mockRequest = myNock.get("/alert/uuid1").reply(200, mockAlert);
    const mockRequest2 = myNock
      .post("/alert/observables", ["uuid1"])
      .reply(200, [mockObservable]);
    await store.read("uuid1");

    expect(mockRequest.isDone()).toEqual(true);
    expect(mockRequest2.isDone()).toEqual(true);

    expect(store.open).toEqual(JSON.parse(JSON.stringify(mockAlert)));
    expect(store.openObservables).toEqual(
      JSON.parse(JSON.stringify([mockObservable])),
    );
  });

  it("will make a request to update an alert given the UUID and update data upon the updateAlert action", async () => {
    const mockRequest = myNock.patch("/alert/").reply(200);
    await store.update([
      { uuid: "uuid1", disposition: "test", historyUsername: "analyst" },
    ]);

    expect(mockRequest.isDone()).toEqual(true);
    // None of these should be changed
    expect(store.open).toStrictEqual(null);
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

    try {
      await store.create(mockAlertCreate);
    } catch (e) {
      const error = e as Error;
      expect(error.message).toStrictEqual(
        "Request failed with status code 403",
      );
    }

    try {
      await store.read("uuid1");
    } catch (e) {
      const error = e as Error;
      expect(error.message).toStrictEqual(
        "Request failed with status code 403",
      );
    }

    try {
      await store.update([
        { uuid: "uuid1", disposition: "test", historyUsername: "analyst" },
      ]);
    } catch (e) {
      const error = e as Error;
      expect(error.message).toStrictEqual(
        "Request failed with status code 403",
      );
    }

    mockRequest.persist(false); // cleanup persisted nock request
  });
});
