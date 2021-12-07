export type UUID = string;

export interface genericObjectCreate {
  description?: string;
  uuid?: UUID;
  value: string;
  [key: string]: unknown;
}

export interface genericObjectRead {
  description: string | null;
  uuid: UUID;
  value: string;
}

export interface genericObjectReadPage extends page {
  items: genericObjectRead[];
}

export interface genericObjectUpdate {
  description?: string;
  value?: string;
  [key: string]: unknown;
}

export interface page {
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  items: any[];
  limit: number;
  offset: number;
  total: number;
}

export interface pageOptionParams {
  limit?: number;
  offset?: number;
  [key: string]: unknown;
}
export interface filterOption {
  readonly name: string;
  readonly label: string;
  readonly type: string;
  readonly options?: string;
  readonly optionLabel?: string;
  readonly formatForAPI?: (filter: any) => string;
}
