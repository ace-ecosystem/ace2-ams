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
        "content-location": "/newItem",
      })
      .get("/newItem")
      .reply(200, "Read successful");
    const res = await api.create("/create", {}, true);
    expect(res).to.eql("Read successful");
  });

  it("will make only a post request when getAfterCreate is true and there is NOT a 'content-location' header", async () => {
    myNock.post("/create").reply(200, "Create successful");
    const res = await api.create("/create", {}, true);
    expect(res).to.eql("Create successful");
  });

  it("will make only a post request when getAfterCreate is false and there is a 'content-location' header", async () => {
    myNock.post("/create").reply(200, "Create successful", {
      "content-location": "/newItem",
    });
    const res = await api.create("/create", {}, false);
    expect(res).to.eql("Create successful");
  });

  it("will make only a post request when getAfterCreate is false and there is NOT a 'content-location' header", async () => {
    myNock.post("/create").reply(200, "Create successful");
    const res = await api.create("/create", {}, false);
    expect(res).to.eql("Create successful");
  });

  it("make a get request when readRequest called", async () => {
    myNock.get("/read").reply(200, "Read successful");
    const res = await api.read("/read");
    expect(res).to.eql("Read successful");
  });

  it("make a patch request when updateRequest called", async () => {
    myNock.patch("/update").reply(200, "Update successful");
    const res = await api.update("/update");
    expect(res).to.eql("Update successful");
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
    expect(res).to.eql("Create successful");
  });

  it("will not change format of outgoing data if its an array of strings", async () => {
    myNock.post("/create", ["A", "B"]).reply(200, "Create successful");
    const res = await api.baseRequest(
      "/create",
      "POST",
      { data: ["A", "B"] },
      false,
    );
    expect(res).to.eql("Create successful");
  });

  it("will format incoming data into camelCase keys", async () => {
    myNock.post("/create").reply(200, { first_key: "A", second_key: 2 });
    const res = await api.create("/create", {}, false);
    expect(res).to.eql({
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
    expect(res).to.eql([
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
    expect(res).to.eql("Read successful");
  });

  it("will throw an error if a request completes, but without a successful response code", async () => {
    myNock.patch("/update").reply(404, "Not found :(");
    try {
      await api.update("/update");
    } catch (e) {
      const error = e as Error;
      expect(error.message).to.equal("Request failed with status code 404");
    }
  });
});
