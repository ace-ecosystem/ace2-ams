import {
  genericObjectCreate,
  genericObjectRead,
  genericObjectReadPage,
  genericObjectUpdate,
} from "./base";

export type analysisStatusCreate = genericObjectCreate;

export type analysisStatusRead = genericObjectRead;

export interface analysisStatusReadPage extends genericObjectReadPage {
  items: analysisStatusRead[];
}

export type analysisStatusUpdate = genericObjectUpdate;
