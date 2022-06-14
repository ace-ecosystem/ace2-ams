import { UUID } from "./base";
import { nodeDetectionPointRead } from "./nodeDetectionPoint";
import { observableInAlertRead } from "./observable";
import {
  sandboxContactedHost,
  sandboxDnsRequest,
  sandboxDroppedFile,
  sandboxHttpRequest,
  sandboxProcess,
} from "./sandbox";

export interface detectionPointSummary extends nodeDetectionPointRead {
  alertUuid: UUID;
  count: number;
}

export interface emailHeadersBody {
  alertUuid: UUID;
  bodyHtml: string | null;
  bodyText: string | null;
  headers: string;
}

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

export interface observableSummary extends observableInAlertRead {
  faqueueHits: number;
  faqueueLink: string;
}

export interface sandboxSummary {
  contactedHosts: sandboxContactedHost[];
  createdServices: string[];
  dnsRequests: sandboxDnsRequest[];
  droppedFiles: sandboxDroppedFile[];
  filename: string;
  httpRequests: sandboxHttpRequest[];
  malwareFamily: string;
  md5: string;
  memoryStrings: string[];
  memoryUrls: string[];
  mutexes: string[];
  processes: sandboxProcess[];
  processTree: string;
  registryKeys: string[];
  resolvedApis: string[];
  sandboxUrl: string;
  sha1: string;
  sha256: string;
  sha512: string;
  ssdeep: string;
  startedServices: string[];
  stringsUrls: string[];
  suricataAlerts: string[];
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
