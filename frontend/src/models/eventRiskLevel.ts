import {
  genericObjectCreate,
  genericObjectRead,
  genericObjectReadPage,
  genericObjectUpdate,
  queueableObjectCreate,
  queueableObjectRead,
  queueableObjectUpdate,
} from "./base";

export interface eventRiskLevelCreate
  extends genericObjectCreate,
    queueableObjectCreate {}

export interface eventRiskLevelRead
  extends genericObjectRead,
    queueableObjectRead {}

export interface eventRiskLevelReadPage extends genericObjectReadPage {
  items: eventRiskLevelRead[];
}

export interface eventRiskLevelUpdate
  extends genericObjectUpdate,
    queueableObjectUpdate {}
