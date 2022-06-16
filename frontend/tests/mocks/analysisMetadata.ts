import { analysisMetadataRead } from "@/models/analysisMetadata";

export const analysisMetadataReadFactory = ({
  displayType = null,
  displayValue = null,
  tags = [],
}: Partial<analysisMetadataRead> = {}): analysisMetadataRead => ({
  displayType: displayType,
  displayValue: displayValue,
  tags: tags,
});
