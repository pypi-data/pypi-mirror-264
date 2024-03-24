import { join } from "node:path";
import { mkdtemp, rm, writeFile } from "node:fs/promises";
import { spawnSync } from "node:child_process";
import { tmpdir } from "node:os";

import { describe, expect, test } from "vitest";

import Dialect from "./Dialect";
import { fromSerialized } from "./parseReportData";

function tag(image: string) {
  // Should match what's used in our `noxfile`, certainly until we handle image
  // building here from the frontend test suite.
  return `bowtie-ui-tests/${image}`;
}

function bowtie(args: string[] = [], input?: string, status = 0) {
  const result = spawnSync("bowtie", args, { input });

  try {
    expect(result.status).toStrictEqual(status);
  } catch (error: unknown) {
    if (!(error instanceof Error)) {
      throw error;
    }
    error.message =
      error.message +
      `
      stdout contained:

        ${result.stdout?.toString()}

      stderr contained:

        ${result.stderr?.toString()}
    `;
    throw error;
  }
  return result.stdout.toString();
}

describe("parseReportData", () => {
  test("parses reports", async () => {
    let lines: string;

    const tempdir = await mkdtemp(join(tmpdir(), "bowtie-ui-tests-"));

    try {
      const schema = join(tempdir, "schema.json");
      await writeFile(schema, "{}");

      const instance = join(tempdir, "instance.json");
      await writeFile(instance, "37");

      lines = bowtie(["validate", "-i", tag("envsonschema"), schema, instance]);
    } finally {
      await rm(tempdir, { recursive: true });
    }

    const report = fromSerialized(lines);

    const metadata = report.runInfo.implementations[tag("envsonschema")];
    const testCase = report.cases.get(1);

    expect(report).toStrictEqual({
      runInfo: {
        started: report.runInfo.started,
        bowtie_version: report.runInfo.bowtie_version,
        dialect: Dialect.withName("draft2020-12").uri,
        implementations: {
          [tag("envsonschema")]: {
            name: "envsonschema",
            language: "python",
            dialects: metadata?.dialects,
            homepage: metadata?.homepage,
            issues: metadata?.issues,
            source: metadata?.source,
            links: metadata?.links,
          },
        },
        metadata: {},
      },
      implementationsResults: new Map([
        [
          tag("envsonschema"),
          {
            erroredCases: 0,
            erroredTests: 0,
            skippedTests: 0,
            failedTests: 1,

            id: tag("envsonschema"),
            cases: new Map([[1, [{ state: "failed", valid: false }]]]),
          },
        ],
      ]),
      cases: new Map([
        [
          1,
          {
            description: testCase?.description,
            schema: {},
            tests: [
              {
                description: testCase?.tests[0].description,
                instance: 37,
                valid: null,
              },
            ],
          },
        ],
      ]),
      didFailFast: false,
    });
  });

  test("parses reports with multiple test cases", () => {
    const case1 = {
      description: "case1",
      schema: {
        additionalProperties: { type: "boolean" },
        properties: { bar: {}, foo: {} },
      },
      tests: [
        {
          description: "one",
          instance: { foo: 1 },
          valid: true,
        },
        {
          description: "two",
          instance: { foo: 1, bar: 2, quux: true },
          valid: true,
        },
        {
          description: "three",
          instance: { foo: 1, bar: 2, quux: 12 },
          valid: false,
        },
      ],
    };
    const case2 = {
      description: "case2",
      schema: {
        additionalProperties: { type: "boolean" },
      },
      tests: [
        {
          description: "one",
          instance: { foo: true },
          valid: true,
        },
        {
          description: "two",
          instance: { foo: 1 },
          valid: false,
        },
      ],
    };
    const case3 = {
      description: "case3",
      schema: {
        allOf: [
          { $ref: "https://example.com/schema-with-anchor#foo" },
          { then: { $id: "http://example.com/ref/then", type: "integer" } },
        ],
      },
      tests: [
        {
          description: "one",
          instance: "foo",
          valid: false,
        },
        {
          description: "two",
          instance: 12,
          valid: true,
        },
      ],
    };
    const cases = [case1, case2, case3].map((each) => JSON.stringify(each));

    const lines = bowtie(
      ["run", "-i", tag("envsonschema"), "-D", "7"],
      cases.join("\n") + "\n",
    );

    const report = fromSerialized(lines);

    const metadata = report.runInfo.implementations[tag("envsonschema")];

    expect(report).toStrictEqual({
      runInfo: {
        started: report.runInfo.started,
        bowtie_version: report.runInfo.bowtie_version,
        dialect: Dialect.withName("draft7").uri,
        implementations: {
          [tag("envsonschema")]: {
            name: "envsonschema",
            language: "python",
            dialects: metadata?.dialects,
            homepage: metadata?.homepage,
            issues: metadata?.issues,
            source: metadata?.source,
            links: metadata?.links,
          },
        },
        metadata: {},
      },
      implementationsResults: new Map([
        [
          tag("envsonschema"),
          {
            erroredCases: 0,
            erroredTests: 0,
            skippedTests: 0,
            failedTests: 4,

            id: tag("envsonschema"),
            cases: new Map([
              [
                1,
                [
                  { state: "failed", valid: false },
                  { state: "failed", valid: false },
                  { state: "successful", valid: false },
                ],
              ],
              [
                2,
                [
                  { state: "failed", valid: false },
                  { state: "successful", valid: false },
                ],
              ],
              [
                3,
                [
                  { state: "successful", valid: false },
                  { state: "failed", valid: false },
                ],
              ],
            ]),
          },
        ],
      ]),
      cases: new Map([
        [
          1,
          {
            description: case1.description,
            schema: case1.schema,
            tests: case1.tests,
          },
        ],
        [
          2,
          {
            description: case2.description,
            schema: case2.schema,
            tests: case2.tests,
          },
        ],
        [
          3,
          {
            description: case3.description,
            schema: case3.schema,
            tests: case3.tests,
          },
        ],
      ]),
      didFailFast: false,
    });
  });
});
