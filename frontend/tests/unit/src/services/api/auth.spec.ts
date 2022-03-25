import auth from "@/services/api/auth";
import myNock from "@unit/services/api/nock";
import { createCustomPinia } from "@unit/helpers";

createCustomPinia();

const mockLoginData = {
  username: "user",
  password: "pass",
};

describe("/auth API calls", () => {
  it("will make a post request to /auth when authenticate is called", async () => {
    myNock.post("/auth").reply(200);
    const res = await auth.authenticate(mockLoginData);
    expect(res).to.equal(undefined);
  });

  it("will make a get request to /auth/refresh when refresh is called", async () => {
    myNock.get("/auth/refresh").reply(200);
    const res = await auth.refresh();
    expect(res).to.equal(undefined);
  });

  it("will make a get request to /auth/validate when validate is called", async () => {
    myNock.get("/auth/validate").reply(200);
    const res = await auth.validate();
    expect(res).to.equal(undefined);
  });

  it("will make a get request to /auth/logout when logout is called", async () => {
    myNock.get("/auth/logout").reply(200);
    const res = await auth.logout();
    expect(res).to.equal(undefined);
  });

  it("will throw an error if refreshing without being authenticated", async () => {
    myNock.get("/auth/refresh").reply(401, "Not authenticated");
    try {
      await auth.refresh();
    } catch (e) {
      const error = e as Error;
      expect(error.message).to.equal("Request failed with status code 401");
    }
  });

  it("will throw an error if authenticate request fails", async () => {
    myNock.post("/auth").reply(401, "Invalid username or password");
    try {
      await auth.authenticate(mockLoginData);
    } catch (e) {
      const error = e as Error;
      expect(error.message).to.equal("Request failed with status code 401");
    }
  });

  it("will throw an error if validate request fails", async () => {
    myNock.get("/auth/validate").reply(401, "Invalid token");
    try {
      await auth.validate();
    } catch (e) {
      const error = e as Error;
      expect(error.message).to.equal("Request failed with status code 401");
    }
  });

  it("will throw an error if logout request fails", async () => {
    myNock.get("/auth/logout").reply(405, "Method not allowed");
    try {
      await auth.logout();
    } catch (e) {
      const error = e as Error;
      expect(error.message).to.equal("Request failed with status code 405");
    }
  });
});
