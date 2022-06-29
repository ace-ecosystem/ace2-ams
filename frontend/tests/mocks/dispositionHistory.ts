import { observableDispositionHistoryIndividual } from "@/models/observable";

export const dispositionHistoryReadFactory = ({
  disposition = "disposition1",
  count = 1,
  percent = 100,
}: Partial<observableDispositionHistoryIndividual> = {}): observableDispositionHistoryIndividual => ({
  disposition: disposition,
  count: count,
  percent: percent,
});
