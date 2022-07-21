import { describe, beforeEach, it, expect } from "vitest";
import { useRecentCommentsStore } from "@/stores/recentComments";
import { createCustomPinia } from "@tests/unitHelpers";

createCustomPinia();

const store = useRecentCommentsStore();

describe("recentComments initialState", () => {
  beforeEach(() => {
    store.$reset();
    localStorage.removeItem("aceComments");
  });
  it("aceComments doesn't exist in localStorage", () => {
    const store = useRecentCommentsStore();
    expect(store.recentComments).toEqual([]);
  });
  it("aceComments does exist in localStorage", () => {
    const expected = ["test", "example", "another one"];
    localStorage.setItem("aceComments", JSON.stringify(expected));
    store.$reset();
    expect(store.recentComments).toEqual(expected);
  });
});

describe("recentComments Actions", () => {
  beforeEach(() => {
    store.$reset();

    localStorage.removeItem("aceComments");
  });
  it.each([
    [[], "test", ["test"]],
    [
      [
        "one",
        "two",
        "three",
        "four",
        "five",
        "six",
        "seven",
        "eight",
        "nine",
        "ten",
      ],
      "test",
      [
        "test",
        "one",
        "two",
        "three",
        "four",
        "five",
        "six",
        "seven",
        "eight",
        "nine",
      ],
    ],
    [
      [
        "one",
        "two",
        "three",
        "four",
        "five",
        "six",
        "seven",
        "eight",
        "nine",
        "ten",
      ],
      "five",
      [
        "five",
        "one",
        "two",
        "three",
        "four",
        "six",
        "seven",
        "eight",
        "nine",
        "ten",
      ],
    ],
  ])("addComment", (initialState, addition, expected) => {
    store.recentComments = initialState;
    store.addComment(addition);
    expect(store.recentComments).toEqual(expected);
    expect(localStorage.getItem("aceComments")).toEqual(
      JSON.stringify(expected),
    );
  });
  it.each([
    [[], "test", []],
    [
      [
        "one",
        "two",
        "three",
        "four",
        "five",
        "six",
        "seven",
        "eight",
        "nine",
        "ten",
      ],
      "test",
      [
        "one",
        "two",
        "three",
        "four",
        "five",
        "six",
        "seven",
        "eight",
        "nine",
        "ten",
      ],
    ],
    [
      [
        "one",
        "two",
        "three",
        "four",
        "five",
        "six",
        "seven",
        "eight",
        "nine",
        "ten",
      ],
      "five",
      ["one", "two", "three", "four", "six", "seven", "eight", "nine", "ten"],
    ],
  ])("removeComment", (initialState, addition, expected) => {
    store.recentComments = initialState;
    store.removeComment(addition);
    expect(store.recentComments).toEqual(expected);
    expect(localStorage.getItem("aceComments")).toEqual(
      JSON.stringify(expected),
    );
  });
});
