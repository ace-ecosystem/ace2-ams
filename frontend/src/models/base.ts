import { StoreDefinition } from "pinia";

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

export interface genericQueueableObjectRead
  extends genericObjectRead,
    queueableObjectRead {}

export interface genericObjectReadPage extends page {
  items: genericObjectRead[];
}

export interface genericObjectUpdate {
  description?: string;
  value?: string;
  [key: string]: unknown;
}

export interface historyUsername {
  historyUsername: string;
}

export interface queueableObjectCreate {
  queues: string[];
}

export interface queueableObjectRead {
  queues: genericObjectRead[];
}

export interface queueableObjectUpdate {
  queues?: string[];
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
export interface propertyOption {
  readonly name: string;
  readonly label: string;
  readonly type: string;
  readonly optionProperty?: string;
  readonly valueProperty?: string;
  readonly store?: StoreDefinition;
  readonly nullOptions?: {
    nullOption: Record<string, unknown>;
    nullableFilter: boolean;
    nullableEdit: boolean;
  };
  readonly queueDependent?: boolean;
  readonly stringRepr?: (filter: any) => string;
  readonly displayRepr?: (filter: any) => string;
  readonly parseStringRepr?: (
    filter: string,
  ) => string[] | Date | { category: string; value: string };
}

export interface columnOption {
  field: string;
  header: string;
  sortable: boolean;
  default?: boolean;
  required?: boolean;
}
