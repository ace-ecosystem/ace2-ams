import { Analysis } from "@/services/api/analysis";
import myNock from "@unit/services/api/nock";
import { mockAnalysisRead } from "../../../../mockData/alert";

describe("Analysis API calls", () => {
  it("will make a get request to /alert/queue/{uuid} when getSingle is called", async () => {
    myNock.get("/analysis/uuid2").reply(200, mockAnalysisRead);

    const res = await Analysis.read("uuid2");
    expect(res).toEqual(mockAnalysisRead);
  });

  it("will throw an error if a request fails", async () => {
    myNock.get("/analysis/uuid2").reply(404, "Couldn't find analysis");

    await expect(Analysis.read("uuid2")).rejects.toEqual(
      new Error("Request failed with status code 404"),
    );
  });
});
