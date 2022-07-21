import EmailAnalysisVue from "@/components/Analysis/EmailAnalysis.vue";
import UserAnalysisVue from "@/components/Analysis/UserAnalysis.vue";
import SandboxAnalysisVue from "@/components/Analysis/SandboxAnalysis.vue";

export const analysisModuleComponents: Record<string, unknown> = {
  "User Analysis": UserAnalysisVue,
  "Email Analysis": EmailAnalysisVue,
  "Sandbox Analysis": SandboxAnalysisVue,
};
