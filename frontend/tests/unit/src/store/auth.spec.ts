import { createTestingPinia } from "@pinia/testing";
import { useAuthStore } from "@/stores/auth";
import { userRead } from "@/models/user";
import myNock from "@unit/services/api/nock";

createTestingPinia();

const store = useAuthStore();

const mockUser: userRead = {
  defaultAlertQueue: { description: null, uuid: "1", value: "default" },
  displayName: "Test Analyst",
  email: "analyst@test.com",
  enabled: true,
  roles: [],
  timezone: "UTC",
  username: "test analyst",
  uuid: "1",
};

describe("auth Getters", () => {
  beforeEach(() => {
    store.$reset();
  });

  it("will return isAuthenticated state when not logged in", () => {
    expect(store.isAuthenticated).toStrictEqual(false);
  });

  it("will return isAuthenticated state when logged in", () => {
    store.authenticated = true;

    expect(store.isAuthenticated).toStrictEqual(true);
  });

  it("will return displayName when not logged in", () => {
    expect(store.displayName).toStrictEqual("Unauthenticated User");
  });

  it("will return displayName when logged in", () => {
    store.authenticated = true;
    store.user = mockUser;

    expect(store.displayName).toStrictEqual("Test Analyst");
  });
});

describe("auth Actions", () => {
  beforeEach(() => {
    store.$reset();
  });

  it("will set authenticated state when the refreshTokens call fails", async () => {
    myNock.get("/auth/refresh").reply(403);

    await store.refreshTokens();
    expect(store.authenticated).toStrictEqual(false);
  });

  it("will set authenticated state when the refreshTokens call succeeds", async () => {
    myNock.get("/auth/refresh").reply(200);

    await store.refreshTokens();
    expect(store.authenticated).toStrictEqual(true);
  });

  it("will set authenticated state when setAuthenticated is called with false", () => {
    store.setAuthenticated(false);
    expect(store.authenticated).toStrictEqual(false);
  });

  it("will set authenticated state when setAuthenticated is called with true", () => {
    store.setAuthenticated(true);
    expect(store.authenticated).toStrictEqual(true);
  });
});
