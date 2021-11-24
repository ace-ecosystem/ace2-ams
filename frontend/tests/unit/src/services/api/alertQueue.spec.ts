/**
 * @jest-environment node
 */

import snakecaseKeys from "snakecase-keys";
import { AlertQueue } from "@/services/api/alertQueue";
import myNock from "@unit/services/api/nock";
import { alertQueueCreate, alertQueueRead } from "@/models/alertQueue";

describe("AlertQueue API calls", () => {
  const successMessage = "Request successful";
  const secondSuccessMessage = "Request 2 successful";
  const failureMessage = "Request failed";
  const mockObjectCreate: alertQueueCreate = {
    description: "This is an alert queue",
    value: "Test",
  };
  const mockObjectRead: alertQueueRead = {
    uuid: "1",
    description: "This is an alert queue",
    value: "Test",
  };

  it("will make only a post request when create is called and return create results if getAfterCreate is false and there is NOT a content-location header", async () => {
    myNock
      .post("/alert/queue/", JSON.stringify(snakecaseKeys(mockObjectCreate)))
      .reply(200, successMessage);

    const res = await AlertQueue.create(mockObjectCreate, false);
    expect(res).toEqual(successMessage);
  });

  it("will make only a post request when create is called and return create results if getAfterCreate is false and there is a content-location header", async () => {
    myNock
      .post("/alert/queue/", JSON.stringify(snakecaseKeys(mockObjectCreate)))
      .reply(200, successMessage, {
        "content-location": "http://test_app.com:1234/newItem",
      });

    const res = await AlertQueue.create(mockObjectCreate, false);
    expect(res).toEqual(successMessage);
  });

  it("will make only a post request when create is called and return create results if getAfterCreate is true and there is NOT a content-location header", async () => {
    myNock
      .post("/alert/queue/", JSON.stringify(snakecaseKeys(mockObjectCreate)))
      .reply(200, successMessage);

    const res = await AlertQueue.create(mockObjectCreate);
    expect(res).toEqual(successMessage);
  });

  it("will make a post and get request when create is called and return GET results if getAfterCreate is true and there is a content-location header", async () => {
    myNock
      .post("/alert/queue/", JSON.stringify(snakecaseKeys(mockObjectCreate)))
      .reply(200, successMessage, {
        "content-location": "http://test_app.com:1234/newItem",
      })
      .get("/newItem")
      .reply(200, secondSuccessMessage);

    const res = await AlertQueue.create(mockObjectCreate, true);
    expect(res).toEqual(secondSuccessMessage);
  });

  it("will make a get request to /alert/queue/{uuid} when getSingle is called", async () => {
    myNock.get("/alert/queue/1").reply(200, successMessage);

    const res = await AlertQueue.read("1");
    expect(res).toEqual(successMessage);
  });

  it("will make a get request to /alert/queue/ when readAll is called", async () => {
    myNock
      .get("/alert/queue/?offset=0")
      .reply(200, JSON.stringify({ items: [mockObjectRead, mockObjectRead] }));

    const res = await AlertQueue.readAll();
    expect(res).toEqual([mockObjectRead, mockObjectRead]);
  });

  it("will make a patch request to /alert/queue/{uuid} when updateSingle is called", async () => {
    myNock
      .patch("/alert/queue/1", JSON.stringify({ value: "New Name" }))
      .reply(200, successMessage);

    const res = await AlertQueue.update("1", { value: "New Name" });
    expect(res).toEqual(successMessage);
  });

  it("will throw an error if a request fails", async () => {
    myNock.get("/alert/queue/1").reply(404, failureMessage);

    await expect(AlertQueue.read("1")).rejects.toEqual(
      new Error("Request failed with status code 404"),
    );
  });
});
