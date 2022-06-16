import { metadataDisplayTypeRead } from "./metadataDisplayType";
import { metadataDisplayValueRead } from "./metadataDisplayValue";
import { metadataTagRead } from "./metadataTag";

export interface analysisMetadataRead {
  displayType: metadataDisplayTypeRead | null;
  displayValue: metadataDisplayValueRead | null;
  tags: metadataTagRead[];
}
