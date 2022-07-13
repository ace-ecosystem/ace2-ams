/**
 * @jest-environment node
 */

import { describe, it, expect } from "vitest";
import snakecaseKeys from "snakecase-keys";
import { ThreatType } from "@/services/api/threatType";
import myNock from "@unit/services/api/nock";
import { threatTypeCreate, threatTypeRead } from "@/models/threatType";

describe("threatType API calls", () => {
  const successMessage = "Request successful";
  const secondSuccessMessage = "Request 2 successful";
  const failureMessage = "Request failed";
  const mockObjectCreate: threatTypeCreate = {
    description: "This is a threatType",
    value: "Test",
  };
  const mockObjectRead: threatTypeRead = {
    uuid: "1",
    description: "This is a threatType",
    value: "Test",
  };

  it("will make only a post request when create is called and return create results if getAfterCreate is false and there is NOT a content-location header", async () => {
    myNock
      .post("/threat/type/", JSON.stringify(snakecaseKeys(mockObjectCreate)))
      .reply(200, successMessage);

    const res = await ThreatType.create(mockObjectCreate, false);
    expect(res).toEqual(successMessage);
  });

  it("will make only a post request when create is called and return create results if getAfterCreate is false and there is a content-location header", async () => {
    myNock
      .post("/threat/type/", JSON.stringify(snakecaseKeys(mockObjectCreate)))
      .reply(200, successMessage, {
        "content-location": "/newItem",
      });

    const res = await ThreatType.create(mockObjectCreate, false);
    expect(res).toEqual(successMessage);
  });

  it("will make only a post request when create is called and return create results if getAfterCreate is true and there is NOT a content-location header", async () => {
    myNock
      .post("/threat/type/", JSON.stringify(snakecaseKeys(mockObjectCreate)))
      .reply(200, successMessage);

    const res = await ThreatType.create(mockObjectCreate);
    expect(res).toEqual(successMessage);
  });

  it("will make a post and get request when create is called and return GET results if getAfterCreate is true and there is a content-location header", async () => {
    myNock
      .post("/threat/type/", JSON.stringify(snakecaseKeys(mockObjectCreate)))
      .reply(200, successMessage, {
        "content-location": "/newItem",
      })
      .get("/newItem")
      .reply(200, secondSuccessMessage);

    const res = await ThreatType.create(mockObjectCreate, true);
    expect(res).toEqual(secondSuccessMessage);
  });

  it("will make a get request to /threat/type/{uuid} when getSingle is called", async () => {
    myNock.get("/threat/type/1").reply(200, successMessage);

    const res = await ThreatType.read("1");
    expect(res).toEqual(successMessage);
  });

  it("will make a get request to /threat/type/ when readAll is called", async () => {
    myNock
      .get("/threat/type/?offset=0")
      .reply(200, JSON.stringify({ items: [mockObjectRead, mockObjectRead] }));

    const res = await ThreatType.readAll();
    expect(res).toEqual([mockObjectRead, mockObjectRead]);
  });

  it("will make a patch request to /threat/type/{uuid} when updateSingle is called", async () => {
    myNock
      .patch("/threat/type/1", JSON.stringify({ value: "New Name" }))
      .reply(200, successMessage);

    const res = await ThreatType.update("1", { value: "New Name" });
    expect(res).toEqual(successMessage);
  });

  it("will throw an error if a request fails", async () => {
    myNock.get("/threat/type/1").reply(404, failureMessage);

    try {
      await ThreatType.read("1");
    } catch (e) {
      const error = e as Error;
      expect(error.message).toStrictEqual(
        "Request failed with status code 404",
      );
    }
  });
});
