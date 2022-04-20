import { describe, it, expect } from "vitest";
import { Analysis } from "@/services/api/analysis";
import myNock from "@unit/services/api/nock";
import { analysisReadFactory } from "@mocks/analysis";

describe("Analysis API calls", () => {
  it("will make a get request to /alert/queue/{uuid} when getSingle is called", async () => {
    const mockAnalysis = analysisReadFactory();
    myNock.get("/analysis/uuid2").reply(200, mockAnalysis);

    const res = await Analysis.read("uuid2");

    expect(res).toEqual(JSON.parse(JSON.stringify(mockAnalysis)));
  });

  it("will throw an error if a request fails", async () => {
    myNock.get("/analysis/uuid2").reply(404, "Couldn't find analysis");
    try {
      await Analysis.read("uuid2");
    } catch (e) {
      const error = e as Error;
      expect(error.message).toStrictEqual(
        "Request failed with status code 404",
      );
    }
  });
});
