import { genericObjectRead, UUID } from "./base";

import { nodeDirectiveRead } from "./nodeDirective";
import { nodeTagRead } from "./nodeTag";
import { observableTypeRead } from "./observableType";

export interface analysisModuleTypeRead extends genericObjectRead {
  cacheSeconds: number;
  extendedVersion: Record<string, unknown> | null;
  manual: boolean;
  observableTypes: observableTypeRead[];
  requiredDirectives: nodeDirectiveRead[];
  requiredTags: nodeTagRead[];
  version: string;
}

export interface analysisModuleTypeNodeTreeRead {
  uuid: UUID;
  value: string;
}
