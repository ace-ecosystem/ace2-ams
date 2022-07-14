/**
 * @jest-environment node
 */

import { describe, it, expect } from "vitest";
import snakecaseKeys from "snakecase-keys";
import { Threat } from "@/services/api/threat";
import myNock from "@unit/services/api/nock";
import { threatCreate, threatRead } from "@/models/threat";

describe("threat API calls", () => {
  const successMessage = "Request successful";
  const secondSuccessMessage = "Request 2 successful";
  const failureMessage = "Request failed";
  const mockObjectCreate: threatCreate = {
    description: "This is an alert threat",
    value: "Test",
  };
  const mockObjectRead: threatRead = {
    uuid: "1",
    description: "This is an alert threat",
    value: "Test",
  };

  it("will make only a post request when create is called and return create results if getAfterCreate is false and there is NOT a content-location header", async () => {
    myNock
      .post("/threat/", JSON.stringify(snakecaseKeys(mockObjectCreate)))
      .reply(200, successMessage);

    const res = await Threat.create(mockObjectCreate, false);
    expect(res).toEqual(successMessage);
  });

  it("will make only a post request when create is called and return create results if getAfterCreate is false and there is a content-location header", async () => {
    myNock
      .post("/threat/", JSON.stringify(snakecaseKeys(mockObjectCreate)))
      .reply(200, successMessage, {
        "content-location": "/newItem",
      });

    const res = await Threat.create(mockObjectCreate, false);
    expect(res).toEqual(successMessage);
  });

  it("will make only a post request when create is called and return create results if getAfterCreate is true and there is NOT a content-location header", async () => {
    myNock
      .post("/threat/", JSON.stringify(snakecaseKeys(mockObjectCreate)))
      .reply(200, successMessage);

    const res = await Threat.create(mockObjectCreate);
    expect(res).toEqual(successMessage);
  });

  it("will make a post and get request when create is called and return GET results if getAfterCreate is true and there is a content-location header", async () => {
    myNock
      .post("/threat/", JSON.stringify(snakecaseKeys(mockObjectCreate)))
      .reply(200, successMessage, {
        "content-location": "/newItem",
      })
      .get("/newItem")
      .reply(200, secondSuccessMessage);

    const res = await Threat.create(mockObjectCreate, true);
    expect(res).toEqual(secondSuccessMessage);
  });

  it("will make a get request to /threat/{uuid} when read is called", async () => {
    myNock.get("/threat/1").reply(200, successMessage);

    const res = await Threat.read("1");
    expect(res).toEqual(successMessage);
  });

  it("will make a get request to /threat/ when readAll is called", async () => {
    myNock
      .get("/threat/?offset=0")
      .reply(200, JSON.stringify({ items: [mockObjectRead, mockObjectRead] }));

    const res = await Threat.readAll();
    expect(res).toEqual([mockObjectRead, mockObjectRead]);
  });

  it("will make a patch request to /threat/{uuid} when update is called", async () => {
    myNock
      .patch("/threat/1", JSON.stringify({ value: "New Name" }))
      .reply(200, successMessage);

    const res = await Threat.update("1", { value: "New Name" });
    expect(res).toEqual(successMessage);
  });

  it("will throw an error if a request fails", async () => {
    myNock.get("/threat/1").reply(404, failureMessage);

    try {
      await Threat.read("1");
    } catch (e) {
      const error = e as Error;
      expect(error.message).toStrictEqual(
        "Request failed with status code 404",
      );
    }
  });
});
