import { StoreDefinition } from "pinia";
import { queueRead } from "./queue";

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
  queues?: queueRead[]
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
export interface propertyOption {
  readonly name: string;
  readonly label: string;
  readonly type: string;
  readonly optionProperty?: string;
  readonly valueProperty?: string;
  readonly store?: StoreDefinition;
  readonly queueDependent?: boolean;
  readonly stringRepr?: (filter: any) => string;
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
