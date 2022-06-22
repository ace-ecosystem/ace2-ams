import { metadataDetectionPointRead } from "./metadataDetectionPoint";
import { metadataDirectiveRead } from "./metadataDirective";
import { metadataDisplayTypeRead } from "./metadataDisplayType";
import { metadataDisplayValueRead } from "./metadataDisplayValue";
import { metadataTagRead } from "./metadataTag";
import { metadataTimeRead } from "./metadataTime";

export interface analysisMetadataCreate {
  type:
    | "detection_point"
    | "directive"
    | "display_type"
    | "display_value"
    | "tag"
    | "time";
  value: string;
}

export interface analysisMetadataRead {
  detectionPoints: metadataDetectionPointRead[];
  directives: metadataDirectiveRead[];
  displayType: metadataDisplayTypeRead | null;
  displayValue: metadataDisplayValueRead | null;
  tags: metadataTagRead[];
  time: metadataTimeRead | null;
}
