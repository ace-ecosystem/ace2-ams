import { useAlertQueueStore } from "@/stores/alertQueue";
import { useAlertTypeStore } from "@/stores/alertType";
import { useNodeDirectiveStore } from "@/stores/nodeDirective";
import { useObservableTypeStore } from "@/stores/observableType";
import { useUserStore } from "@/stores/user";

export const camelToSnakeCase = (str: string): string =>
  str.replace(/[A-Z]/g, (letter) => `_${letter.toLowerCase()}`);

export async function populateCommonStores(): Promise<void> {
  const alertQueueStore = useAlertQueueStore();
  const alertTypeStore = useAlertTypeStore();
  const nodeDirectiveStore = useNodeDirectiveStore();
  const observableTypeStore = useObservableTypeStore();
  const userStore = useUserStore();

  await Promise.all([
    alertQueueStore.readAll(),
    alertTypeStore.readAll(),
    nodeDirectiveStore.readAll(),
    observableTypeStore.readAll(),
    userStore.readAll(),
  ]).catch((error) => {
    throw error;
  });
}
