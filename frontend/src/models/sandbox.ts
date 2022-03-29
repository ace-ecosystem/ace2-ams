export interface sandboxContactedHost {
  ip: string;
  port: number | null;
  protocol: string | null;
  location: string | null;
  associatedDomains: string[];
}

export interface sandboxDnsRequest {
  request: string;
  type: string | null;
  answer: string | null;
  answerType: string | null;
}

export interface sandboxDroppedFile {
  filename: string;
  path: string | null;
  size: number | null;
  type: string | null;
  md5: string | null;
  sha1: string | null;
  sha256: string | null;
  sha512: string | null;
  ssdeep: string | null;
}

export interface sandboxHttpRequest {
  host: string;
  port: number | null;
  path: string | null;
  method: string | null;
  userAgent: string | null;
}

export interface sandboxProcess {
  command: string;
  pid: number;
  parentPid: number;
}
