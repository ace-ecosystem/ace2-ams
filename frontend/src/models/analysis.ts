import { UUID } from "./base";
import { nodeCreate, nodeRead, nodeTreeCreate, nodeUpdate } from "./node";
import {
  analysisModuleTypeNodeTreeRead,
  analysisModuleTypeRead,
} from "./analysisModuleType";
import { observableTreeRead } from "./observable";

export interface analysisCreate extends nodeCreate {
  analysisModuleType?: UUID;
  details?: Record<string, unknown>;
  errorMessage?: string;
  nodeTree: nodeTreeCreate;
  stackTrace?: string;
  summary?: string;
  [key: string]: unknown;
}

export interface analysisRead extends nodeRead {
  analysisModuleType: analysisModuleTypeRead;
  details: Record<string, unknown> | null;
  errorMessage: string | null;
  stackTrace: string | null;
  summary: string | null;
}

export interface analysisTreeRead extends nodeRead {
  analysisModuleType: analysisModuleTypeNodeTreeRead;
  children: observableTreeRead[];
  firstAppearance?: boolean;
  parentTreeUuid: UUID | null;
  treeUuid: UUID;
}

export interface analysisUpdate extends nodeUpdate {
  analysisModuleType?: UUID;
  details?: Record<string, unknown> | null;
  errorMessage?: string | null;
  stackTrace?: string | null;
  summary?: string | null;
  [key: string]: unknown;
}
