// Misinfo Guardian MV3 background service worker
// Minimal logging-only script per Step 7.

console.log('Misinfo Guardian background script loaded');

chrome.runtime.onInstalled.addListener(() => {
  console.log('Misinfo Guardian installed');
});
