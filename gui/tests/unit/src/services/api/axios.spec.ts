import auth from "@/services/api/auth";
import users from "@/services/api/users";
import myNock from "@unit/services/api/nock";

describe("Axios interceptor functionality", () => {
  it("will reject the request if it the response was not a 401", async () => {
    myNock.get("/user/").reply(405);
    await expect(users.getAll()).rejects.toEqual(
      new Error("Request failed with status code 405"),
    );
  });

  it("will reject the request if the 401 came from an /auth url", async () => {
    myNock.get("/auth/logout").reply(405, "Method not allowed");
    await expect(auth.logout()).rejects.toEqual(
      new Error("Request failed with status code 405"),
    );
  });

  it("will refresh the tokens if a request receives a 401 and replay the original request", async () => {
    const mockUsers = [{ username: "analyst" }];
    myNock.get("/user/").reply(401);
    myNock.get("/auth/refresh").reply(200);
    myNock.get("/user/").reply(200, mockUsers);

    await expect(users.getAll()).resolves.toEqual(mockUsers);
  });

  it("will reject a bad request after successfully refreshing tokens", async () => {
    myNock.get("/user/").reply(401);
    myNock.get("/auth/refresh").reply(200);
    myNock.get("/user/").reply(405);

    await expect(users.getAll()).rejects.toEqual(
      new Error("Request failed with status code 405"),
    );
  });

  it("will reject the request if unable to refresh the tokens", async () => {
    myNock.get("/user/").reply(401);
    myNock.get("/auth/refresh").reply(401);

    await expect(users.getAll()).rejects.toEqual(
      new Error("Request failed with status code 401"),
    );
  });
});
