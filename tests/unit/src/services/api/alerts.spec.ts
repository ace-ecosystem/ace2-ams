/**
 * @jest-environment node
 */

import alert from "@/services/api/alerts";

describe("/alert API calls", () => {
  it("will fail when attempting to getAll (not implmented)", async () => {
    await expect(alert.getAll()).rejects.toEqual(new Error("Not implemented."));
  });
});
