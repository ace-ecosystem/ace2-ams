import { observableRead } from "./observable";

export interface observableSummary extends observableRead {
  faqueueHits: number;
  faqueueLink: string | null;
}
