import { defineConfig } from "allure";

export default defineConfig({
  name: "Mobile ATQC — API & Android Allure 3 Report",
  output: "./allure-report",
  historyPath: "./allure-history/history.jsonl",
  plugins: {
    awesome: {
      options: {
        singleFile: false,
        reportLanguage: "en",
        reportName: "API & Android Automation Report",
        groupBy: ["parentSuite", "suite", "subSuite"],
      },
    },
  },
  environments: {
    api: {
      name: "API Tests",
      matcher: ({ labels }) =>
        labels?.some((l) => l.name === "tag" && l.value === "api") ?? false,
    },
    android: {
      name: "Android Mobile Tests",
      matcher: ({ labels }) =>
        labels?.some(
          (l) => l.name === "tag" && (l.value === "mobile" || l.value === "smoke")
        ) ?? false,
    },
  },
});
