import {
  genericObjectCreate,
  genericObjectRead,
  genericObjectReadPage,
  genericObjectUpdate,
} from "./base";

export type eventRiskLevelCreate = genericObjectCreate;

export type eventRiskLevelRead = genericObjectRead;

export interface eventRiskLevelReadPage extends genericObjectReadPage {
  items: eventRiskLevelRead[];
}

export type eventRiskLevelUpdate = genericObjectUpdate;
