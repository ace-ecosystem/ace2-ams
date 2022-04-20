import CSS from "csstype";
import {
  genericObjectCreate,
  genericObjectRead,
  genericObjectReadPage,
  genericObjectUpdate,
} from "./base";
import { observableActionSection } from "./observable";

export type observableTypeCreate = genericObjectCreate;

export type observableTypeRead = genericObjectRead;

export interface observableTypeReadPage extends genericObjectReadPage {
  items: observableTypeRead[];
}

export type observableTypeUpdate = genericObjectUpdate;

export type observableTypeMetaData = {
  actions?: observableActionSection[];
  style?: CSS.Properties;
};
