import { dispositionHistoryIndividual } from "@/models/observable";

export const dispositionHistoryReadFactory = ({
  disposition = "disposition1",
  count = 1,
  percent = 100,
}: Partial<dispositionHistoryIndividual> = {}): dispositionHistoryIndividual => ({
  disposition: disposition,
  count: count,
  percent: percent,
});
