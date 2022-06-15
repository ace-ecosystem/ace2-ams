export interface urlDomainSummaryIndividual {
  domain: string;
  count: number;
}

export interface urlDomainSummary {
  domains: urlDomainSummaryIndividual[];
  total: number;
}
