import { analysisMetadataRead } from "@/models/analysisMetadata";

export const analysisMetadataReadFactory = ({
  directives = [],
  displayType = null,
  displayValue = null,
  tags = [],
  time = null,
}: Partial<analysisMetadataRead> = {}): analysisMetadataRead => ({
  directives: directives,
  displayType: displayType,
  displayValue: displayValue,
  tags: tags,
  time: time,
});
