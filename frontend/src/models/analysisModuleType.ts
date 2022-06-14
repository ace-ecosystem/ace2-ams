import { genericObjectRead, UUID } from "./base";

import { nodeDirectiveRead } from "./nodeDirective";
import { tagRead } from "./tag";
import { observableTypeRead } from "./observableType";

export interface analysisModuleTypeRead extends genericObjectRead {
  cacheSeconds: number;
  extendedVersion: Record<string, unknown> | null;
  manual: boolean;
  observableTypes: observableTypeRead[];
  requiredDirectives: nodeDirectiveRead[];
  requiredTags: tagRead[];
  version: string;
}

export interface analysisModuleTypeNodeTreeRead {
  uuid: UUID;
  value: string;
}
