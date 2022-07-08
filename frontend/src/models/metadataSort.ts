import { page, UUID } from "./base";

export interface metadataSortCreate {
  description?: string;
  uuid?: UUID;
  value: number;
  [key: string]: unknown;
}

export interface metadataSortRead {
  description: string | null;
  metadataType: string;
  uuid: UUID;
  value: number;
}

export interface metadataSortReadPage extends page {
  items: metadataSortRead[];
}

export interface metadataSortUpdate {
  description?: string;
  value?: number;
  [key: string]: unknown;
}
