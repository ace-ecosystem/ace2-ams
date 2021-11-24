/**
 * @jest-environment node
 */

import { BaseApi } from "@/services/api/base";
import myNock from "@unit/services/api/nock";

describe("BaseAPI calls", () => {
  const api = new BaseApi();

  it("will make a post and get request after a successful create when getAfterCreate is true and there is a 'content-location' header", async () => {
    myNock
      .post("/create")
      .reply(200, "Create successful", {
        "content-location": "http://test_app.com:1234/newItem",
      })
      .get("/newItem")
      .reply(200, "Read successful");
    const res = await api.create("/create", {}, true);
    expect(res).toEqual("Read successful");
  });

  it("will make only a post request when getAfterCreate is true and there is NOT a 'content-location' header", async () => {
    myNock.post("/create").reply(200, "Create successful");
    const res = await api.create("/create", {}, true);
    expect(res).toEqual("Create successful");
  });

  it("will make only a post request when getAfterCreate is false and there is a 'content-location' header", async () => {
    myNock.post("/create").reply(200, "Create successful", {
      "content-location": "http://test_app.com:1234/newItem",
    });
    const res = await api.create("/create", {}, false);
    expect(res).toEqual("Create successful");
  });

  it("will make only a post request when getAfterCreate is false and there is NOT a 'content-location' header", async () => {
    myNock.post("/create").reply(200, "Create successful");
    const res = await api.create("/create", {}, false);
    expect(res).toEqual("Create successful");
  });

  it("make a get request when readRequest called", async () => {
    myNock.get("/read").reply(200, "Read successful");
    const res = await api.read("/read");
    expect(res).toEqual("Read successful");
  });

  it("make a patch request when updateRequest called", async () => {
    myNock.patch("/update").reply(200, "Update successful");
    const res = await api.update("/update");
    expect(res).toEqual("Update successful");
  });

  it("will format outgoing data into snake_case keys", async () => {
    myNock
      .post("/create", { first_key: "A", second_key: 2 })
      .reply(200, "Create successful");
    const res = await api.create(
      "/create",
      {
        firstKey: "A",
        secondKey: 2,
      },
      false,
    );
    expect(res).toEqual("Create successful");
  });

  it("will format incoming data into camelCase keys", async () => {
    myNock.post("/create").reply(200, { first_key: "A", second_key: 2 });
    const res = await api.create("/create", {}, false);
    expect(res).toEqual({
      firstKey: "A",
      secondKey: 2,
    });
  });

  it("will format incoming objects in a list format into camelCase keys", async () => {
    myNock.post("/create").reply(200, [
      { first_key: "A", second_key: 2 },
      { third_key: "B", fourth_key: 3 },
    ]);
    const res = await api.create("/create", {}, false);
    expect(res).toEqual([
      {
        firstKey: "A",
        secondKey: 2,
      },
      {
        thirdKey: "B",
        fourthKey: 3,
      },
    ]);
  });

  it("will correctly format URL parameters when given", async () => {
    myNock.get("/read?limit=5&offset=0").reply(200, "Read successful");
    const res = await api.read("/read", { limit: 5, offset: 0 });
    expect(res).toEqual("Read successful");
  });

  it("will throw an error if a request completes, but without a successful response code", async () => {
    myNock.patch("/update").reply(404, "Not found :(");
    await expect(api.update("/update")).rejects.toEqual(
      new Error("Request failed with status code 404"),
    );
  });
});
