import { UUID } from "./base";
import { observableRead } from "./observable";

export interface emailSummary {
  alertUuid: UUID;
  attachments: string[];
  ccAddresses: string[];
  fromAddress: string;
  messageId: string;
  replyToAddress: string | null;
  subject: string | null;
  time: Date;
  toAddress: string;
}

export interface observableSummary extends observableRead {
  faqueueHits: number;
  faqueueLink: string;
}

interface urlDomainSummaryIndividual {
  domain: string;
  count: number;
}

export interface urlDomainSummary {
  domains: urlDomainSummaryIndividual[];
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
