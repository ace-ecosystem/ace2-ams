import { observableRead } from "./observable";

export interface observableSummary extends observableRead {
  faqueueHits: number;
  faqueueLink: string;
}

export interface urlDomainSummary {
  domain: string;
  count: number;
  total: number;
}

export interface userSummary {
  company: string | null;
  department: string | null;
  division: string | null;
  email: string;
  managerEmail: string | null;
  title: string | null;
  userId: string;
}
