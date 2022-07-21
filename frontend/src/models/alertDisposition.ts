import {
  genericObjectCreate,
  genericObjectRead,
  genericObjectReadPage,
  genericObjectUpdate,
} from "./base";

export interface alertDispositionCreate extends genericObjectCreate {
  rank: number;
}

export interface alertDispositionRead extends genericObjectRead {
  rank: number;
}

export interface alertDispositionReadPage extends genericObjectReadPage {
  items: alertDispositionRead[];
}

export interface alertDispositionUpdate extends genericObjectUpdate {
  rank?: number;
}
