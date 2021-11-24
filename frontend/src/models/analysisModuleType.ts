import {
  genericObjectCreate,
  genericObjectRead,
  genericObjectReadPage,
  genericObjectUpdate,
} from "./base";

import { nodeDirectiveRead } from "./nodeDirective";
import { nodeTagRead } from "./nodeTag";
import { observableTypeRead } from "./observableType";

export interface analysisModuleTypeCreate extends genericObjectCreate {
  extendedVersion?: Record<string, unknown>;
  manual?: boolean;
  observableTypes?: string[];
  requiredDirectives?: string[];
  requiredTags?: string[];
  version: string;
}

export interface analysisModuleTypeRead extends genericObjectRead {
  extendedVersion: Record<string, unknown> | null;
  manual: boolean;
  observableTypes: observableTypeRead[];
  requiredDirectives: nodeDirectiveRead[];
  requiredTags: nodeTagRead[];
  version: string;
}

export interface analysisModuleTypeReadPage extends genericObjectReadPage {
  items: analysisModuleTypeRead[];
}

export interface analysisModuleTypeUpdate extends genericObjectUpdate {
  extendedVersion?: Record<string, unknown> | null;
  manual?: boolean;
  observableTypes?: string[];
  requiredDirectives?: string[];
  requiredTags?: string[];
  version?: string;
}
