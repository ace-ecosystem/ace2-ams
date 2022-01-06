import { useAlertDispositionStore } from "@/stores/alertDisposition";
import { useAlertQueueStore } from "@/stores/alertQueue";
import { useAlertTypeStore } from "@/stores/alertType";
import { useNodeDirectiveStore } from "@/stores/nodeDirective";
import { useObservableTypeStore } from "@/stores/observableType";
import { useUserStore } from "@/stores/user";

export const camelToSnakeCase = (str: string): string =>
  str.replace(/[A-Z]/g, (letter) => `_${letter.toLowerCase()}`);

export async function populateCommonStores(): Promise<void> {
  const alertDispositionStore = useAlertDispositionStore();
  const alertQueueStore = useAlertQueueStore();
  const alertTypeStore = useAlertTypeStore();
  const nodeDirectiveStore = useNodeDirectiveStore();
  const observableTypeStore = useObservableTypeStore();
  const userStore = useUserStore();

  await Promise.all([
    alertDispositionStore.readAll(),
    alertQueueStore.readAll(),
    alertTypeStore.readAll(),
    nodeDirectiveStore.readAll(),
    observableTypeStore.readAll(),
    userStore.readAll(),
  ]).catch((error) => {
    throw error;
  });
}

export function copyToClipboard(text: string) {
  // if (window.clipboardData && window.clipboardData.setData) {
  //     // Internet Explorer-specific code path to prevent textarea being shown while dialog is visible.
  //     return window.clipboardData.setData("Text", text);

  // }
  if (
    document.queryCommandSupported &&
    document.queryCommandSupported("copy")
  ) {
    const textarea = document.createElement("textarea");
    textarea.textContent = text;
    textarea.style.position = "fixed"; // Prevent scrolling to bottom of page in Microsoft Edge.
    document.body.appendChild(textarea);
    textarea.select();
    try {
      return document.execCommand("copy"); // Security exception may be thrown by some browsers.
    } catch (ex) {
      console.warn("Copy to clipboard failed.", ex);
      return prompt("Copy to clipboard: Ctrl+C, Enter", text);
    } finally {
      document.body.removeChild(textarea);
    }
  }
}
