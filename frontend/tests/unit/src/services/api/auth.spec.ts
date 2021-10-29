import auth from "@/services/api/auth";
import myNock from "@unit/services/api/nock";

const mockLoginData = {
  username: "user",
  password: "pass",
};

describe("/auth API calls", () => {
  it("will make a post request to /auth when authenticate is called", async () => {
    myNock.post("/auth").reply(200);
    await expect(auth.authenticate(mockLoginData)).resolves.toBe(undefined);
  });

  it("will make a get request to /auth/refresh when refresh is called", async () => {
    myNock.get("/auth/refresh").reply(200);
    await expect(auth.refresh()).resolves.toBe(undefined);
  });

  it("will make a get request to /auth/validate when validate is called", async () => {
    myNock.get("/auth/validate").reply(200);
    await expect(auth.validate()).resolves.toBe(undefined);
  });

  it("will make a get request to /auth/logout when logout is called", async () => {
    myNock.get("/auth/logout").reply(200);
    await expect(auth.logout()).resolves.toBe(undefined);
  });

  it("will throw an error if refreshing without being authenticated", async () => {
    myNock.get("/auth/refresh").reply(401, "Not authenticated");
    await expect(auth.refresh()).rejects.toEqual(
      new Error("Request failed with status code 401"),
    );
  });

  it("will throw an error if authenticate request fails", async () => {
    myNock.post("/auth").reply(401, "Invalid username or password");
    await expect(auth.authenticate(mockLoginData)).rejects.toEqual(
      new Error("Request failed with status code 401"),
    );
  });

  it("will throw an error if validate request fails", async () => {
    myNock.get("/auth/validate").reply(401, "Invalid token");
    await expect(auth.validate()).rejects.toEqual(
      new Error("Request failed with status code 401"),
    );
  });

  it("will throw an error if logout request fails", async () => {
    myNock.get("/auth/logout").reply(405, "Method not allowed");
    await expect(auth.logout()).rejects.toEqual(
      new Error("Request failed with status code 405"),
    );
  });
});
