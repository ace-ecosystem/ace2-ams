import { UUID } from "./base";
import { nodeMetadata, nodeRead } from "./node";
import {
  analysisModuleTypeNodeTreeRead,
  analysisModuleTypeRead,
} from "./analysisModuleType";
import { observableTreeRead } from "./observable";

export interface analysisRead extends nodeRead {
  analysisModuleType: analysisModuleTypeRead;
  cachedUntil: Date;
  details: Record<string, unknown> | null;
  errorMessage: string | null;
  stackTrace: string | null;
  summary: string | null;
}

export interface analysisTreeRead extends nodeRead {
  analysisModuleType: analysisModuleTypeNodeTreeRead;
  children: observableTreeRead[];
  firstAppearance?: boolean;
  nodeMetadata?: nodeMetadata;
  parentTreeUuid: UUID | null;
  treeUuid: UUID;
}
